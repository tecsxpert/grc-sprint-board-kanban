# Tool-109 - Sprint Board (Kanban)

Capstone Sprint Board project with a Flask AI microservice for task descriptions, sprint recommendations, and sprint reports.

## Project Structure

```text
backend/
ai-service/
frontend/
docker-compose.yml
README.md
```

## Run AI Service

```bash
cp ai-service/.env.example .env
docker compose up --build
```

Health check:

```bash
curl http://localhost:5000/health
```

## Test

```bash
cd ai-service
pytest
```
