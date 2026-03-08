# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dev server (http://localhost:5000)
python app.py

# Verify all routes and imports are healthy
python3 -c "import app, formulas, prompts; print('Routes:', [r.rule for r in app.app.url_map.iter_rules()])"
```

Requires `ANTHROPIC_API_KEY` in `.env` (see `.env.example`).

## Architecture

Flask app with three pages and five API routes. All Claude calls are in `app.py`; prompts are in `prompts.py`; formula reference data is hardcoded in `formulas.py`.

**Routes:**
- `GET /` → `solve.html` — drag-and-drop or typed problem input, practice/rapid mode toggle
- `GET /teach` → `teach.html` — static formula reference library (no API calls, data from `formulas.py`)
- `GET /quiz` → `quiz.html` — AI-generated problems with graded student answers
- `POST /solve` — accepts `multipart/form-data` with optional `file` (image/PDF) and/or `text_problem`; returns `{solution, mode}`
- `POST /quiz/generate` — accepts `{level, topic}` JSON; returns `{problem}`
- `POST /quiz/grade` — accepts `{problem, answer}` JSON; returns `{feedback}`
- `POST /chat` — accepts `{message, history}` JSON; returns `{reply}` — follow-up chatbot for practice mode solutions

**Claude model:** `claude-sonnet-4-6` for all API endpoints. PDFs are converted to PNG via PyMuPDF before sending to Claude vision.

**Frontend JS split:**
- `static/js/app.js` — solve page only (mode toggle, file/text input, result rendering, localStorage history, follow-up chatbot)
- `static/js/quiz.js` — quiz page only (level selection, problem generation, answer grading)
- Both files duplicate `mathSafeEscape()`, `protectedMarked()`, and `escapeHtml()` helpers — intentional since they're separate pages with no shared JS bundle.

## Result Rendering

Claude's structured markdown output is parsed client-side, not server-side.

**Practice mode** (`renderPractice()` in `app.js`): Parses `**Problem Type:**`, `**Formulas Used:**`, `**Step-by-Step Solution:**` (split on `Step N:`), and `**Final Answer:**` into styled HTML sections. Falls back to `protectedMarked()` if structure is missing.

**Quiz grading** (`renderFeedback()` in `quiz.js`): Strips the `**Result:**` line (shown in the colored header), then extracts remaining `**Label:** content` sections.

**Math safety:** `mathSafeEscape()` extracts `\[...\]`, `\(...\)`, and `$...$` LaTeX blocks into a placeholder array before HTML-escaping, then restores them. This prevents backslashes from being corrupted. MathJax 3 typeset is triggered manually after any dynamic DOM injection via `MathJax.typesetPromise([el])`.

## Prompt Structure

Prompts in `prompts.py` enforce strict output formats that the JS parsers depend on. If you change a section header in a prompt (e.g. `**Final Answer:**`), update the corresponding regex in `app.js`/`quiz.js` or the parser will fall back to raw markdown rendering.

- `PRACTICE_SYSTEM` → parsed by `renderPractice()`
- `QUIZ_GRADE_SYSTEM` → parsed by `renderFeedback()` / `showGradeResult()`
- `QUIZ_GENERATE_SYSTEM` / `RAPID_SYSTEM` → output rendered as-is (no structured parsing)
- `CHAT_SYSTEM` → follow-up chatbot for practice mode; responses rendered with `protectedMarked()` in chat bubbles
