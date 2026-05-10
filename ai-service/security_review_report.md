# OWASP Style Security Review

Headers: secure headers are applied after each request.
Rate limiting: 30 requests per minute per IP through Flask-Limiter.
Sanitization: `bleach` removes HTML and dangerous patterns are rejected.
Error responses: all exceptions return structured JSON without stack traces.
Secrets: loaded from `.env`; no API keys committed.
Availability: Groq failures return fallback JSON.

Result: approved for capstone demo with backend authentication assumption documented in `SECURITY.md`.
