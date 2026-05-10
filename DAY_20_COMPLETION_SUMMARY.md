# Day 20 Completion Summary — Demo Tech Stack and Security

**Date:** May 7, 2026
**Status:** ✅ COMPLETE — Day 20 demo documentation finalized

## Primary Deliverables
- Tech stack overview for the demo
- Security demonstration: `401 Unauthorized` behavior
- Prompt injection rejection behavior
- Reference to `ai-service/SECURITY.md`

---

## 1. Tech Stack Overview

### Frontend
- React-based UI for the Kanban board application
- Uses standard frontend tooling and a development host at `http://localhost:3000`
- Communicates with backend APIs over secure HTTP

### Backend
- Java backend service using Maven/Spring Boot conventions
- Exposes REST APIs for task/workflow management and future persistence

### AI Service
- Python Flask service in `ai-service/`
- Uses:
  - `Flask` for HTTP routing
  - `Flask-CORS` for origin-restricted cross-origin requests
  - `Flask-Limiter` for request rate limiting
  - `Werkzeug` for HTTP exception handling
  - `Groq` client integration for LLM-powered recommendations, reports, and descriptions
- Security middleware in `ai-service/middleware/security.py` centralizes:
  - API key validation
  - JSON input validation
  - Prompt injection detection
  - Input sanitization
  - Error handling

### Containerization
- Docker-based deployment for reproducible local and cloud-ready environments
- Health checks and secure runtime defaults are part of the service design

---

## 2. Security Demo — 401 Unauthorized

### What is implemented
- All non-`/status` requests now require a valid `X-API-Key` header
- The expected key is loaded from environment variable `AI_SERVICE_API_KEY`
- Missing or invalid API keys return a `401 Unauthorized` response

### Code areas
- `ai-service/middleware/security.py`
- `ai-service/app.py`

### Demo flow
1. Call a protected endpoint such as `/recommend` or `/generate-report`
2. Omit the `X-API-Key` header
3. Confirm the response is `401 Unauthorized`

---

## 3. Security Demo — Injection Rejection

### What is implemented
- The security middleware rejects prompt injection attempts
- It detects suspicious patterns like:
  - `ignore previous instructions`
  - `system prompt`
  - `bypass`
  - `jailbreak`
  - `override`
  - `forget the`
- Rejected injection attempts return `400 Invalid input`

### Code areas
- `ai-service/middleware/security.py`
- `ai-service/test_endpoints.py`

### Demo flow
1. Call a protected AI endpoint with malicious prompt text
2. Confirm the middleware rejects the request
3. Confirm the response is `400 Invalid input`

---

## 4. `SECURITY.md` Reference

This task is documented in `ai-service/SECURITY.md`, including:
- Critical vulnerability resolution evidence for `CRT-002: Service Authentication`
- Confirmation that `401` is returned when `X-API-Key` is missing or invalid
- Injection prevention audit showing prompt injection attempts are rejected with `400`
- OWASP mapping for `A03 Injection` and `A07 Authentication Failures`

---

## 5. Status
- ✅ Day 20 deliverable complete
- ✅ Tech stack explained
- ✅ `401 Unauthorized` security demo implemented
- ✅ Prompt injection rejection implemented
- ✅ Security reference added to `ai-service/SECURITY.md`

**Prepared by:** Developer
**Task:** Day 20 demo complete
