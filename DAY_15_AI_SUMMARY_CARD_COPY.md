# Tool-109 AI Summary Card

## Demo Day One-Page Overview

### AI Service Key Endpoints
1. **GET /status**
   - Purpose: Quick unauthenticated service availability check
   - Expected response: `{"status": "operational"}`
2. **GET /health**
   - Purpose: Authenticated health check for AI service readiness
   - Required header: `X-API-Key`
   - Expected response: `{"status": "AI service running"}`
3. **GET /test**
   - Purpose: Verify Flask blueprint routing and AI service registration
   - Expected response: `{"message": "Report route working"}`

---

## Technology Stack
- **Backend:** Python Flask AI service
- **Middleware:** Flask-CORS, Flask-Limiter, custom security middleware
- **Security:** API key authentication, input sanitization, security headers, rate limiting
- **Additional Service:** Java backend integration (AI service client)
- **Frontend:** React application
- **Containerization:** Docker + docker-compose
- **Repository:** GitHub source control

---

## Why this matters
- Demonstrates the AI service is live, secure, and ready for production
- Shows both authenticated and unauthenticated endpoints for two demo scenarios
- Highlights a modern tech stack with secure API practices and container deployment

---

## GitHub Link
https://github.com/srujancshetty/grc-sprint-board-kanban

---

## Demo Day Notes
- This card is designed as a single-slide summary for stakeholders.
- Two identical copies are prepared for Demo Day distribution.
- Keep the API key secure when demonstrating authenticated calls.
