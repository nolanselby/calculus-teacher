import os
import base64
import requests as http_requests
from datetime import date
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import anthropic
from supabase import create_client
from prompts import PRACTICE_SYSTEM, RAPID_SYSTEM, QUIZ_GENERATE_SYSTEM, QUIZ_GRADE_SYSTEM
from formulas import FORMULAS

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-in-production")
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB

# ── Clients ──────────────────────────────────────────────────────────────────
claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SUPABASE_URL      = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

# ── Rate limit constants ──────────────────────────────────────────────────────
ANON_FREE_FILE_SOLVES = 2    # file uploads before requiring sign-in
AUTH_DAILY_SOLVES     = 50   # solves per day for signed-in users
AUTH_DAILY_QUIZ       = 100  # quiz generations per day

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
ALLOWED_MEDIA_TYPES = {
    "image/jpeg": "image/jpeg",
    "image/png":  "image/png",
    "image/gif":  "image/gif",
    "image/webp": "image/webp",
}


# ── Supabase REST helpers (thread-safe, no shared mutable state) ─────────────

def _sb_headers(jwt: str | None = None) -> dict:
    token = jwt if jwt else SUPABASE_ANON_KEY
    return {
        "Authorization": f"Bearer {token}",
        "apikey": SUPABASE_ANON_KEY,
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }

def sb_get(table: str, params: dict, jwt: str | None = None):
    if not SUPABASE_URL:
        return None
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    r = http_requests.get(url, params=params, headers=_sb_headers(jwt), timeout=5)
    return r.json() if r.ok else None

def sb_post(table: str, data: dict, jwt: str | None = None):
    if not SUPABASE_URL:
        return None
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    r = http_requests.post(url, json=data, headers=_sb_headers(jwt), timeout=5)
    return r

def sb_patch(table: str, params: dict, data: dict, jwt: str | None = None):
    if not SUPABASE_URL:
        return None
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    r = http_requests.patch(url, params=params, json=data, headers=_sb_headers(jwt), timeout=5)
    return r


# ── JWT validation ────────────────────────────────────────────────────────────

def validate_jwt(token: str):
    """Validate a Supabase access token and return the user object, or None."""
    if not token or not SUPABASE_URL:
        return None
    try:
        sb = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        resp = sb.auth.get_user(token)
        return resp.user
    except Exception:
        return None

def get_current_user():
    """Extract and validate the Bearer JWT from the request. Returns (user, token)."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
        user = validate_jwt(token)
        return user, token
    return None, None


# ── Rate limiting ─────────────────────────────────────────────────────────────

def _ensure_anon_session():
    if "session_id" not in session:
        import uuid
        session["session_id"]  = str(uuid.uuid4())
        session["file_solves"] = 0

def check_anon_rate_limit():
    """Returns (allowed, used, limit) for anonymous file-solve quota."""
    _ensure_anon_session()
    used = session.get("file_solves", 0)
    return used < ANON_FREE_FILE_SOLVES, used, ANON_FREE_FILE_SOLVES

def increment_anon_file_solve():
    _ensure_anon_session()
    session["file_solves"] = session.get("file_solves", 0) + 1
    session.modified = True

def _get_usage(user_id: str, jwt: str):
    rows = sb_get("usage", {"user_id": f"eq.{user_id}", "select": "*"}, jwt)
    return rows[0] if isinstance(rows, list) and rows else None

def check_auth_rate_limit(user_id: str, jwt: str, kind: str = "solve"):
    """Returns (allowed, used, limit) for an authenticated user."""
    if not SUPABASE_URL:
        return True, 0, 999
    usage = _get_usage(user_id, jwt)
    if not usage:
        sb_post("usage", {"user_id": user_id}, jwt)
        limit = AUTH_DAILY_SOLVES if kind == "solve" else AUTH_DAILY_QUIZ
        return True, 0, limit
    # Reset if it's a new day
    if usage.get("last_reset_date", "") != str(date.today()):
        sb_patch("usage", {"user_id": f"eq.{user_id}"},
                 {"solves_today": 0, "quiz_today": 0,
                  "last_reset_date": str(date.today())}, jwt)
        limit = AUTH_DAILY_SOLVES if kind == "solve" else AUTH_DAILY_QUIZ
        return True, 0, limit
    if kind == "solve":
        used, limit = usage.get("solves_today", 0), AUTH_DAILY_SOLVES
    else:
        used, limit = usage.get("quiz_today", 0), AUTH_DAILY_QUIZ
    return used < limit, used, limit

def increment_auth_usage(user_id: str, jwt: str, kind: str = "solve"):
    if not SUPABASE_URL:
        return
    usage = _get_usage(user_id, jwt)
    if not usage:
        sb_post("usage", {"user_id": user_id,
                          "solves_today": int(kind == "solve"),
                          "quiz_today":   int(kind == "quiz"),
                          "total_solves": int(kind == "solve"),
                          "total_quiz":   int(kind == "quiz")}, jwt)
        return
    if kind == "solve":
        sb_patch("usage", {"user_id": f"eq.{user_id}"},
                 {"solves_today": usage.get("solves_today", 0) + 1,
                  "total_solves": usage.get("total_solves", 0) + 1}, jwt)
    else:
        sb_patch("usage", {"user_id": f"eq.{user_id}"},
                 {"quiz_today": usage.get("quiz_today", 0) + 1,
                  "total_quiz": usage.get("total_quiz", 0) + 1}, jwt)


# ── Persistence helpers ───────────────────────────────────────────────────────

def save_problem(mode, input_type, input_text, solution,
                 filename=None, user_id=None, jwt=None):
    if not SUPABASE_URL:
        return
    try:
        data = {
            "mode":       mode,
            "input_type": input_type,
            "input_text": (input_text or "")[:500],
            "filename":   filename,
            "solution":   (solution or "")[:5000],
        }
        if user_id:
            data["user_id"] = user_id
        sb_post("problems", data, jwt)
    except Exception:
        pass  # non-critical

def save_quiz_attempt(level, topic, problem, student_answer,
                      feedback, result, user_id=None, jwt=None):
    if not SUPABASE_URL:
        return
    try:
        data = {
            "level":          level,
            "topic":          topic,
            "problem":        (problem or "")[:2000],
            "student_answer": (student_answer or "")[:2000],
            "feedback":       (feedback or "")[:3000],
            "result":         result,
        }
        if user_id:
            data["user_id"] = user_id
        sb_post("quiz_attempts", data, jwt)
    except Exception:
        pass


# ── Utility ───────────────────────────────────────────────────────────────────

def pdf_to_image_base64(pdf_bytes):
    try:
        import fitz
        doc  = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0]
        pix  = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        img_bytes = pix.tobytes("png")
        doc.close()
        return base64.standard_b64encode(img_bytes).decode("utf-8"), "image/png"
    except Exception as e:
        raise ValueError(f"Could not read PDF: {e}")


# ── Page routes ───────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("solve.html")

@app.route("/teach")
def teach():
    return render_template("teach.html", formulas=FORMULAS)

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")


# ── API routes ────────────────────────────────────────────────────────────────

@app.route("/api/me")
def api_me():
    user, jwt = get_current_user()
    if not user:
        return jsonify({"user": None})
    profile = sb_get("profiles", {"id": f"eq.{user.id}", "select": "*"}, jwt)
    usage   = sb_get("usage",    {"user_id": f"eq.{user.id}", "select": "*"}, jwt)
    return jsonify({
        "user": {
            "id":      user.id,
            "email":   user.email,
            "profile": profile[0] if isinstance(profile, list) and profile else None,
            "usage":   usage[0]   if isinstance(usage,   list) and usage   else None,
        }
    })


@app.route("/api/history")
def api_history():
    user, jwt = get_current_user()
    if not user:
        return jsonify({"error": "Authentication required"}), 401
    problems = sb_get("problems", {
        "user_id": f"eq.{user.id}",
        "select":  "id,mode,input_type,input_text,filename,created_at",
        "order":   "created_at.desc",
        "limit":   "50",
    }, jwt)
    return jsonify({"history": problems or []})


@app.route("/api/history/<problem_id>", methods=["DELETE"])
def api_delete_history(problem_id):
    user, jwt = get_current_user()
    if not user:
        return jsonify({"error": "Authentication required"}), 401
    sb_patch("problems",
             {"id": f"eq.{problem_id}", "user_id": f"eq.{user.id}"},
             {}, jwt)  # will fail to match if not owned by user — safe
    url = f"{SUPABASE_URL}/rest/v1/problems"
    http_requests.delete(url,
                         params={"id": f"eq.{problem_id}",
                                 "user_id": f"eq.{user.id}"},
                         headers=_sb_headers(jwt), timeout=5)
    return jsonify({"ok": True})


@app.route("/api/usage/anon")
def api_anon_usage():
    _ensure_anon_session()
    used = session.get("file_solves", 0)
    return jsonify({
        "file_solves":       used,
        "file_solves_limit": ANON_FREE_FILE_SOLVES,
        "remaining":         max(0, ANON_FREE_FILE_SOLVES - used),
    })


# ── Solve ─────────────────────────────────────────────────────────────────────

@app.route("/solve", methods=["POST"])
def solve():
    mode         = request.form.get("mode", "practice")
    text_problem = request.form.get("text_problem", "").strip()
    is_file      = "file" in request.files and request.files["file"].filename != ""

    user, jwt = get_current_user()

    # Gate file uploads for anonymous users
    if is_file and not user:
        allowed, used, limit = check_anon_rate_limit()
        if not allowed:
            return jsonify({
                "error":   "auth_required",
                "message": f"You've used your {limit} free file uploads. Create a free account to keep going.",
                "used":    used,
                "limit":   limit,
            }), 402

    # Daily rate limit for authenticated users
    if user:
        allowed, used, limit = check_auth_rate_limit(user.id, jwt, "solve")
        if not allowed:
            return jsonify({
                "error":   "rate_limit",
                "message": f"You've hit your daily limit of {limit} solves. Come back tomorrow!",
                "used":    used,
                "limit":   limit,
            }), 429

    system_prompt = PRACTICE_SYSTEM if mode == "practice" else RAPID_SYSTEM

    # ── Text-only path ────────────────────────────────────────────────────────
    if text_problem and not is_file:
        try:
            resp = claude.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2048,
                system=system_prompt,
                messages=[{"role": "user", "content": text_problem}],
            )
            solution = resp.content[0].text
            save_problem(mode, "text", text_problem, solution,
                         user_id=user.id if user else None, jwt=jwt)
            if user:
                increment_auth_usage(user.id, jwt, "solve")
            return jsonify({"solution": solution, "mode": mode})
        except anthropic.APIError as e:
            return jsonify({"error": f"API error: {str(e)}"}), 500

    # ── File path ─────────────────────────────────────────────────────────────
    if not is_file:
        return jsonify({"error": "No file uploaded and no problem text provided."}), 400

    file       = request.files["file"]
    file_bytes = file.read()
    ctype      = file.content_type

    if ctype == "application/pdf" or file.filename.lower().endswith(".pdf"):
        try:
            img_b64, media_type = pdf_to_image_base64(file_bytes)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    elif ctype in ALLOWED_IMAGE_TYPES:
        img_b64    = base64.standard_b64encode(file_bytes).decode("utf-8")
        media_type = ALLOWED_MEDIA_TYPES[ctype]
    else:
        return jsonify({"error": "Unsupported file type. Upload JPG, PNG, WebP, or PDF."}), 400

    user_content = [
        {"type": "image", "source": {"type": "base64",
                                     "media_type": media_type, "data": img_b64}},
        {"type": "text",  "text": "Please solve the calculus problem shown in this image."},
    ]
    if text_problem:
        user_content.append({"type": "text",
                              "text": f"Additional context: {text_problem}"})
    try:
        resp     = claude.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}],
        )
        solution = resp.content[0].text

        if not user:
            increment_anon_file_solve()
        else:
            increment_auth_usage(user.id, jwt, "solve")

        save_problem(mode, "file", text_problem, solution,
                     filename=file.filename,
                     user_id=user.id if user else None, jwt=jwt)

        out = {"solution": solution, "mode": mode}
        if not user:
            out["anon_remaining"] = max(0, ANON_FREE_FILE_SOLVES
                                        - session.get("file_solves", 0))
        return jsonify(out)
    except anthropic.APIError as e:
        return jsonify({"error": f"API error: {str(e)}"}), 500


# ── Quiz ──────────────────────────────────────────────────────────────────────

@app.route("/quiz/generate", methods=["POST"])
def quiz_generate():
    user, jwt = get_current_user()
    if user:
        allowed, used, limit = check_auth_rate_limit(user.id, jwt, "quiz")
        if not allowed:
            return jsonify({
                "error":   "rate_limit",
                "message": f"Daily quiz limit of {limit} reached. Come back tomorrow!",
            }), 429

    data        = request.get_json() or {}
    level       = data.get("level", "calc1")
    topic       = data.get("topic", "").strip()
    level_map   = {"calc1": "Calculus 1", "calc2": "Calculus 2", "calc3": "Calculus 3"}
    level_label = level_map.get(level, "Calculus 1")

    user_msg = f"Generate a {level_label} problem"
    if topic:
        user_msg += f" specifically about {topic}"
    user_msg += "."

    try:
        resp    = claude.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            system=QUIZ_GENERATE_SYSTEM,
            messages=[{"role": "user", "content": user_msg}],
        )
        problem = resp.content[0].text.strip()
        if user:
            increment_auth_usage(user.id, jwt, "quiz")
        return jsonify({"problem": problem})
    except anthropic.APIError as e:
        return jsonify({"error": f"API error: {str(e)}"}), 500


@app.route("/quiz/grade", methods=["POST"])
def quiz_grade():
    user, jwt = get_current_user()
    data          = request.get_json() or {}
    problem       = data.get("problem", "").strip()
    answer        = data.get("answer",  "").strip()
    level         = data.get("level",   "calc1")
    topic         = data.get("topic",   "")

    if not problem or not answer:
        return jsonify({"error": "Both problem and answer are required."}), 400

    try:
        resp     = claude.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=QUIZ_GRADE_SYSTEM,
            messages=[{"role": "user",
                       "content": f"Problem: {problem}\n\nStudent's Answer: {answer}"}],
        )
        feedback = resp.content[0].text

        result = "incorrect"
        if "**Result:** Correct"           in feedback: result = "correct"
        elif "**Result:** Partially Correct" in feedback: result = "partial"

        save_quiz_attempt(level, topic, problem, answer, feedback, result,
                          user_id=user.id if user else None, jwt=jwt)
        return jsonify({"feedback": feedback})
    except anthropic.APIError as e:
        return jsonify({"error": f"API error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
