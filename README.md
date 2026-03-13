# Calculus Tutor

ChatGPT kept fumbling my calc questions — wrong steps, skipped logic, no real explanation. So I built this instead. It uses Claude 3.5 Sonnet to actually walk through problems the way a good tutor would: big picture first, then step by step, in plain English before the math.

You can type a problem, upload a photo of your homework, or drop in a PDF. It covers Calc 1, 2, and 3.

## What it does

- Type a problem, snap a photo, or upload an image/PDF
- Shows the "Big Idea" before diving into steps so you actually understand what you're solving
- Follow-up chat if something doesn't click — it knows the context of your specific problem
- Practice quizzes with graded feedback for Calc 1–3
- Formula reference page for quick lookups

## Stack

Flask backend, Claude 3.5 Sonnet for the AI (vision + text), vanilla JS / MathJax / Bootstrap on the frontend.

## Getting Started

You'll need Python 3.9+ and an Anthropic API key.

```bash
git clone https://github.com/nolanselby/calculus-teacher.git
cd calculus-teacher
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and add your `ANTHROPIC_API_KEY` and `FLASK_SECRET_KEY`, then run it:

```bash
python app.py
```

App runs at `http://localhost:5000`.

## License

MIT
