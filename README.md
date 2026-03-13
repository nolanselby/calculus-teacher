# Calculus Tutor

A calculus learning assistant that handles the math and the explanation. It uses Claude 3.5 Sonnet to solve problems from text or images and breaks them down into steps that actually make sense.

## Core Features

- **Multimodal Solving**: Snap a photo, upload an image, or type it in.
- **Explain-First Solutions**: Moves beyond simple answers to show the "Big Idea" and step-by-step logic.
- **Follow-up Chat**: If a step is confusing, just ask. The built-in chatbot knows the context of your specific problem.
- **Interactive Quizzes**: Generate problems for Calc 1-3 and get graded feedback on your attempts.
- **Formula Library**: A clean, categorized reference for when you just need to check a rule.

## Tech

- **Backend**: Flask (Python)
- **AI**: Claude 3.5 Sonnet (Vision + Text)
- **Frontend**: Vanilla JS / MathJax / Bootstrap

## Getting Started

### Prerequisites
- Python 3.9+
- Anthropic API Key

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

Open `.env` and add your `ANTHROPIC_API_KEY` and `FLASK_SECRET_KEY`.

### Run it
```bash
python app.py
```
The app will be live at `http://localhost:5000`.

## License
MIT
