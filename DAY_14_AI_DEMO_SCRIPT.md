# Day 14 AI Demo Script

## Demo Purpose
This script demonstrates the current AI service interaction flow, exact request inputs, expected JSON outputs, and a short 60-second technical explanation for a non-technical panel.

---

## Environment
- Service address: `http://localhost:5000`
- Authenticated endpoint: `/health`
- Unauthenticated endpoint: `/status`
- Service test endpoint: `/test`
- Required header for `/health`: `X-API-Key`

### Required example API key
- `X-API-Key: test-api-key-123`

---

## Demo Step 1: Verify operational status (no auth required)

### Request
```bash
curl -X GET "http://localhost:5000/status"
```

### Expected output
```json
{
  "status": "operational"
}
```

### Notes
- This endpoint proves the service is running.
- It is intentionally unauthenticated to allow basic health checks.

---

## Demo Step 2: Verify authenticated health check

### Request
```bash
curl -X GET "http://localhost:5000/health" \
  -H "X-API-Key: test-api-key-123"
```

### Expected output
```json
{
  "status": "AI service running"
}
```

### Notes
- This endpoint requires the API key header.
- It demonstrates that secure endpoints reject unauthorized access.

---

## Demo Step 3: Verify AI service route

### Request
```bash
curl -X GET "http://localhost:5000/test"
```

### Expected output
```json
{
  "message": "Report route working"
}
```

### Notes
- This route confirms the AI service blueprint is registered correctly.
- It is useful for a live demo to prove that the Flask app is serving expected responses.

---

## Demo Step 4: Show security behavior for invalid input

### Request
```bash
curl -X POST "http://localhost:5000/health" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key-123" \
  -d '{"input": "<script>alert(1)</script>"}'
```

### Expected output
```json
{
  "error": "Request processing failed"
}
```

### Notes
- The service sanitizes dangerous input and avoids leaking sensitive internal details.
- This demonstrates security controls even when the endpoint is not intended for POST payloads.

---

## 60-Second Tech Explanation for a Non-Technical Panel

"Our AI service is a lightweight, secure backend that exposes a few key endpoints. For the demo, we show a simple status check that anyone can call, and a protected health check that only works when the request includes a valid secret key. That means the system is both observable and locked down, which is essential for business use.

Under the hood, the service also adds industry-standard security headers, blocks suspicious payloads, and sanitizes any potentially dangerous text before it gets processed. The main benefit is that the application is no longer an open target — only authorized systems can use it, and malformed or malicious inputs are rejected safely.

In practical terms, this delivers reliability and trust: executives can say the AI service is live, monitored, and protected, while engineers can continue building the next AI features without risking a security breach."