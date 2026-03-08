# Calculus Tutor

A calculus learning assistant that handles the math and the explanation. It uses Claude 3.5 Sonnet to solve problems from text or images and breaks them down into steps that actually make sense.

## Core Features

- **Multimodal Solving**: Snap a photo, upload a PDF, or type it in.
- **Explain-First Solutions**: Moves beyond simple answers to show the "Big Idea" and step-by-step logic.
- **Follow-up Chat**: If a step is confusing, just ask. The built-in chatbot knows the context of your specific problem.
- **Interactive Quizzes**: Generate problems for Calc 1-3 and get graded feedback on your attempts.
- **Formula Library**: A clean, categorized reference for when you just need to check a rule.
- **Persistent History**: Saves your solves and quiz progress via Supabase.

## Tech

- **Backend**: Flask (Python)
- **AI**: Claude 3.5 Sonnet (Vision + Text)
- **Database**: Supabase
- **Frontend**: Vanilla JS / MathJax / Bootstrap

## Getting Started

### Prerequisites
- Python 3.9+
- Anthropic API Key
- Supabase project (optional, but needed for history/rate limiting)

### Installation

```bash
# Clone the repo
git clone https://github.com/your-username/calc-tutor.git
cd calc-tutor

# Install requirements
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

Open `.env` and add your `ANTHROPIC_API_KEY`, `FLASK_SECRET_KEY`, and Supabase credentials.

### Run it
```bash
python app.py
```
The app will be live at `http://localhost:5000`.

## Deployment

This repo is configured for Vercel out of the box. Just connect your GitHub repo to Vercel and it'll pick up `vercel.json` and the Python runtime automatically. Make sure to add your environment variables to the Vercel dashboard.

## License
MIT
