# AI Talking Points

Groq: provides low-latency LLaMA-3.3-70b chat completions through an OpenAI-compatible endpoint.
Prompt engineering: templates constrain output to sprint-board sections and forbid unsupported facts.
Security: middleware validates JSON, sanitizes HTML, blocks injection patterns, and applies size limits.
Redis cache/rate limit: Redis stores Flask-Limiter counters in Docker for consistent per-IP throttling.
Flask architecture: `app.py` creates the app, `routes/` exposes endpoints, `services/` owns Groq calls, and `middleware/` handles input defense.
