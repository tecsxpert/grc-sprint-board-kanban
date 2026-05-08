# 🤖 AI Service — Sprint Board (Kanban)
 
> AI-powered task descriptions, sprint recommendations, and sprint reports using Flask + Groq LLaMA 3.3.
 
---
 
## 📋 Overview
 
This AI service powers the intelligent features of the **Sprint Board (Kanban)** capstone project. It is built using **Flask** and **Groq LLaMA 3.3** to provide:
 
- AI-powered task description generation
- Sprint task prioritization recommendations
- Sprint report generation
- Redis-based response caching
- Security middleware and rate limiting
- Docker containerization
- Fallback handling for AI failures
---
 
## 🛠️ Tech Stack
 
| Technology | Version |
|---|---|
| Python | 3.12 |
| Flask | 3.x |
| Groq API | LLaMA-3.3-70b-versatile |
| Redis | 7 |
| Docker & Docker Compose | latest |
| Flask-Limiter | latest |
| Flask-CORS | latest |
 
---
 
## 📁 Project Structure
 
```txt
ai-service/
│
├── middleware/
│   └── security.py
│
├── prompts/
│   ├── describe_prompt.txt
│   ├── recommend_prompt.txt
│   └── generate_report_prompt.txt
│
├── routes/
│   └── report_routes.py
│
├── services/
│   ├── groq_client.py
│   ├── cache_service.py
│   └── chroma_service.py
│
├── app.py
├── requirements.txt
├── Dockerfile
└── README.md
```
 
---
 
## ⚙️ Environment Variables
 
Create a `.env` file in the project root:
 
```env
GROQ_API_KEY=your_groq_api_key
FLASK_ENV=development
FRONTEND_URL=http://localhost:3000
REDIS_HOST=redis
```
 
---
 
## 🚀 Installation & Setup
 
### Clone Repository
 
```bash
git clone <repository-url>
cd grc-sprint-board-kanban
```
 
---
 
## 🐳 Run Using Docker
 
### Build Containers
 
```bash
docker-compose build --no-cache
```
 
### Start Services
 
```bash
docker-compose up
```
 
### Stop Containers
 
```bash
docker-compose down
```
 
### Remove Containers & Volumes
 
```bash
docker-compose down -v
```
 
### Rebuild Containers
 
```bash
docker-compose build --no-cache
```
 
---
 
## 🌐 Service URLs
 
| Service | URL |
|---|---|
| AI Service | http://localhost:5000 |
| Health Check | http://localhost:5000/health |
| Redis | localhost:6379 |
 
---
 
## 📡 API Endpoints
 
### 1. `GET /health`
 
Returns service health information.
 
**Response:**
 
```json
{
  "status": "healthy",
  "model": "llama-3.3-70b-versatile",
  "uptime_seconds": 120,
  "avg_response_time_ms": 1200
}
```
 
---
 
### 2. `POST /describe`
 
Generates detailed AI-powered task descriptions.
 
**Request:**
 
```json
{
  "task_title": "Implement JWT authentication",
  "business_context": "Secure Kanban board access",
  "requirements": [
    "Login API",
    "Refresh token support",
    "Role-based authorization"
  ]
}
```
 
**Response:**
 
```json
{
  "description": "AI generated task description...",
  "cached": false,
  "endpoint": "/describe",
  "generated_at": "2026-05-08T20:30:00"
}
```
 
---
 
### 3. `POST /recommend`
 
Generates AI-based sprint recommendations.
 
**Request:**
 
```json
{
  "tasks": [
    "Setup Redis cache",
    "Implement JWT authentication",
    "Fix API security"
  ]
}
```
 
**Response:**
 
```json
{
  "recommendations": [
    {
      "action_type": "TASK",
      "description": "Prioritize authentication module first",
      "priority": "HIGH"
    }
  ],
  "cached": false,
  "endpoint": "/recommend"
}
```
 
---
 
### 4. `POST /generate-report`
 
Generates sprint summary reports.
 
**Request:**
 
```json
{
  "sprint_name": "Sprint 3",
  "completed_tasks": 18,
  "total_tasks": 22,
  "team_size": 5,
  "key_deliverables": [
    "JWT authentication",
    "Redis integration",
    "Docker deployment"
  ]
}
```
 
**Response:**
 
```json
{
  "report": "AI generated sprint report...",
  "cached": false,
  "endpoint": "/generate-report"
}
```
 
---
 
## 🗄️ Redis Cache
 
The service uses Redis caching to reduce repeated AI calls and improve response times.
 
**Features:**
 
- SHA256 cache keys
- 15-minute TTL
- Cached responses returned instantly
- Reduced Groq API usage
When a cached response is returned, the payload includes:
 
```json
{
  "cached": true
}
```
 
---
 
## 🔒 Security Features
 
| Protection | Description |
|---|---|
| Rate Limiting | Prevents API abuse |
| Input Sanitization | Cleans user-provided input |
| Security Headers | Adds protective HTTP headers |
| CORS Protection | Restricts cross-origin access |
| Error Handling Middleware | Graceful error responses |
| Prompt Injection Filtering | Blocks malicious prompt inputs |
 
---
 
## 🛡️ Fallback Handling
 
If the Groq API becomes unavailable, fallback responses are returned instead of crashing the service:
 
```json
{
  "is_fallback": true
}
```
 
---
 
## 🧪 Testing
 
Run endpoint tests:
 
```bash
python test_endpoints.py
```
 
Run security tests:
 
```bash
python test_security.py
```
 
---
 
## ✨ Demo Highlights
 
- ✅ AI-generated task descriptions
- ✅ AI sprint recommendations
- ✅ Sprint report generation
- ✅ Redis response caching
- ✅ Dockerized deployment
- ✅ Groq LLaMA 3.3 integration
- ✅ Security middleware protections
---
 
## 👥 Contributors
 
| Role | Name |
|---|---|
| AI Developer 1 | Sanjana M B |
| AI Developer 2 | Srujan S |
| Java Developer 1 | Abhishek Sadashiv Ganiger |
| Java Developer 2 | Manoj B N |
| Security Reviewer | Shashidharareddy M |