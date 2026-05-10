# Final Demo Outputs

Health endpoint screenshot reference: open `http://localhost:5000/health`; expected JSON includes `success: true` and `status: healthy`.

Example AI output: `/describe` returns a task summary, acceptance criteria, risks, and test notes.

Example report output: `/generate-report` returns executive summary, progress, risks, and next steps.

Fallback output: if `GROQ_API_KEY` is not configured, AI endpoints return HTTP 503 with `AI service temporarily unavailable`.
