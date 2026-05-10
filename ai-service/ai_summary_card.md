# AI Summary Card

Endpoints: `/health`, `/describe`, `/recommend`, `/generate-report`.
Tech stack: Python 3.11, Flask, Groq LLaMA-3.3-70b, Redis, Docker Compose, pytest.
Security features: input validation, HTML sanitization, prompt injection blocking, rate limiting, secure headers, structured errors.
GitHub setup: commit `ai-service/`, `docker-compose.yml`, `.env.example`, reports, and tests. Do not commit `.env`.
Docker: run `docker compose up --build`, then call `http://localhost:5000/health`.
