# AI Service

Flask microservice for Tool-109 Sprint Board AI features.

## Endpoints

All responses use:

```json
{"success": true, "data": {}, "message": ""}
```

### `GET /health`

Returns service status.

### `POST /describe`

Request:

```json
{"task_title": "Build sprint report API", "business_context": "Kanban board", "requirements": ["JSON output"]}
```

### `POST /recommend`

Request:

```json
{"tasks": ["Fix blocker", "Write tests"], "sprint_goal": "Stabilize release", "team_capacity": 4}
```

### `POST /generate-report`

Request:

```json
{"sprint_name": "Sprint 20", "completed_tasks": 18, "total_tasks": 20, "key_deliverables": ["AI service"]}
```

## Run

```bash
cp .env.example ../.env
docker compose up --build
```

## Test

```bash
cd ai-service
pytest
```
