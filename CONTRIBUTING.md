# Contributing

Thanks for improving InterviewForge AI.

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
python scripts/seed_questions.py
python run.py
```

## Before Opening a Pull Request

```bash
ruff check .
python scripts/check_question_files.py
pytest
```

## Good First Contributions

- Add realistic interview questions.
- Improve Russian, English, or Ukrainian wording.
- Add tests around interview flows.
- Improve accessibility and mobile layout.
- Implement richer AI-provider prompts while keeping local fallback reliable.

Keep changes focused and include a short explanation of the user-facing behavior.

