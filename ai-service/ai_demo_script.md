# AI Demo Script

## Demo Prompts

Describe: `{"task_title":"Add drag-and-drop Kanban cards","business_context":"Sprint board","requirements":["Update card status","Keep audit trail"]}`

Recommend: `{"tasks":["Fix login bug","Write API tests","Polish board UI"],"sprint_goal":"Demo-ready release","team_capacity":3}`

Report: `{"sprint_name":"Sprint 20","completed_tasks":18,"total_tasks":20,"key_deliverables":["AI service","Docker compose"],"blockers":["Final API key setup"]}`

## Talking Points

The service wraps Groq LLaMA-3.3-70b behind Flask endpoints. Inputs are normalized, sanitized, rate-limited, and validated before reaching the model. Failures return fallback JSON so the Sprint Board does not crash during demos.

## 60-Second Technical Explanation

This is a Flask AI microservice using blueprints for routes, a service layer for Groq, middleware for validation, Redis-backed rate limiting in Docker, and structured JSON responses for backend integration. The Groq client uses Tenacity retries with exponential backoff and timeouts.

## Security Explanation

The app blocks prompt injection phrases, SQL-like attack strings, XSS payloads, oversized bodies, and excessive request rates. Secrets come from environment variables only.
