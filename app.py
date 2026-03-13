import os
# Restarting to pick up .env changes
import base64
import logging
import requests as http_requests
from datetime import date
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import anthropic
from prompts import PRACTICE_SYSTEM, RAPID_SYSTEM, QUIZ_GENERATE_SYSTEM, QUIZ_GRADE_SYSTEM, CHAT_SYSTEM
from formulas import FORMULAS
try:
    import app_config
except ImportError:
    app_config = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/Users/nolanselby/Desktop/coding-projects/calc-tutor/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv("/Users/nolanselby/Desktop/coding-projects/calc-tutor/.env")

def get_secret(key, default=None):
    val = os.getenv(key)
    if val: return val
    if app_config and hasattr(app_config, key):
        return getattr(app_config, key)
    return default

app = Flask(__name__)
app.secret_key = get_secret("FLASK_SECRET_KEY", "dev-secret-change-in-production")
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB

# ── Clients ──────────────────────────────────────────────────────────────────
claude = anthropic.Anthropic(api_key=get_secret("ANTHROPIC_API_KEY"))

SUPABASE_URL      = get_secret("SUPABASE_URL", "")
SUPABASE_ANON_KEY = get_secret("SUPABASE_ANON_KEY", "")

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
ALLOWED_MEDIA_TYPES = {
    "image/jpeg": "image/jpeg",
    "image/png":  "image/png",
    "image/gif":  "image/gif",
    "image/webp": "image/webp",
}


# ── Supabase REST helpers (simplified, no auth) ──────────────────────────────

def _sb_headers() -> dict:
    return {
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "apikey": SUPABASE_ANON_KEY,
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }

def sb_post(table: str, data: dict):
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        return None
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    r = http_requests.post(url, json=data, headers=_sb_headers(), timeout=5)
    return r


# ── Persistence helpers ───────────────────────────────────────────────────────

def save_problem(mode, input_type, input_text, solution, filename=None):
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
        sb_post("problems", data)
    except Exception:
        pass  # non-critical

def save_quiz_attempt(level, topic, problem, student_answer, feedback, result):
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
        sb_post("quiz_attempts", data)
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
    # Return empty user since auth is removed
    return jsonify({"user": None})


# ── Solve ─────────────────────────────────────────────────────────────────────

@app.route("/solve", methods=["POST"])
def solve():
    mode         = request.form.get("mode", "practice")
    text_problem = request.form.get("text_problem", "").strip()
    is_file      = "file" in request.files and request.files["file"].filename != ""

    system_prompt = PRACTICE_SYSTEM if mode == "practice" else RAPID_SYSTEM

    # ── Text-only path ────────────────────────────────────────────────────────
    if text_problem and not is_file:
        try:
            resp = claude.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=3072,
                system=system_prompt,
                messages=[{"role": "user", "content": text_problem}],
            )
            solution = resp.content[0].text
            save_problem(mode, "text", text_problem, solution)
            return jsonify({"solution": solution, "mode": mode})
        except anthropic.APIError as e:
            logger.error(f"Anthropic API error: {e}")
            return jsonify({"error": f"API error: {str(e)}"}), 500
        except Exception as e:
            logger.exception("Unexpected error in solve (text)")
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500

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
            model="claude-3-haiku-20240307",
            max_tokens=3072,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}],
        )
        solution = resp.content[0].text

        save_problem(mode, "file", text_problem, solution, filename=file.filename)

        return jsonify({"solution": solution, "mode": mode})
    except anthropic.APIError as e:
        logger.error(f"Anthropic API error: {e}")
        return jsonify({"error": f"API error: {str(e)}"}), 500
    except Exception as e:
        logger.exception("Unexpected error in solve (file)")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# ── Quiz ──────────────────────────────────────────────────────────────────────

@app.route("/quiz/generate", methods=["POST"])
def quiz_generate():
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
            model="claude-3-haiku-20240307",
            max_tokens=512,
            system=QUIZ_GENERATE_SYSTEM,
            messages=[{"role": "user", "content": user_msg}],
        )
        problem = resp.content[0].text.strip()
        return jsonify({"problem": problem})
    except anthropic.APIError as e:
        return jsonify({"error": f"API error: {str(e)}"}), 500


@app.route("/quiz/grade", methods=["POST"])
def quiz_grade():
    data          = request.get_json() or {}
    problem       = data.get("problem", "").strip()
    answer        = data.get("answer",  "").strip()
    level         = data.get("level",   "calc1")
    topic         = data.get("topic",   "")

    if not problem or not answer:
        return jsonify({"error": "Both problem and answer are required."}), 400

    try:
        resp     = claude.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            system=QUIZ_GRADE_SYSTEM,
            messages=[{"role": "user",
                       "content": f"Problem: {problem}\n\nStudent's Answer: {answer}"}],
        )
        feedback = resp.content[0].text

        result = "incorrect"
        if "**Result:** Correct"           in feedback: result = "correct"
        elif "**Result:** Partially Correct" in feedback: result = "partial"

        save_quiz_attempt(level, topic, problem, answer, feedback, result)
        return jsonify({"feedback": feedback})
    except anthropic.APIError as e:
        return jsonify({"error": f"API error: {str(e)}"}), 500


# ── Chat follow-up ────────────────────────────────────────────────────────────

@app.route("/chat", methods=["POST"])
def chat():
    data    = request.get_json() or {}
    message = data.get("message", "").strip()
    history = data.get("history", [])

    if not message:
        return jsonify({"error": "No message provided."}), 400

    # Build conversation: keep the last 20 messages + the new one
    messages = []
    for msg in history[-20:]:
        role = msg.get("role")
        content = msg.get("content", "")
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": message})

    try:
        resp = claude.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            system=CHAT_SYSTEM,
            messages=messages,
        )
        return jsonify({"reply": resp.content[0].text})
    except anthropic.APIError as e:
        return jsonify({"error": f"API error: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, port=port)
