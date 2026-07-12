# Architecture

InterviewForge AI is a compact FastAPI application. HTML pages and the JSON API share the same SQLAlchemy models and services.

- `routers/` handles HTTP.
- `services/` contains interview, evaluation, statistics, reports, PDF, and AI-provider logic.
- `models/` contains SQLAlchemy 2.0 models.
- `data/questions/` stores local interview questions so the app works without AI keys.

