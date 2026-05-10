# Security Documentation

## Executive Summary

The AI service uses strict JSON validation, HTML sanitization, prompt-injection detection, rate limiting, secure headers, structured error responses, and environment-based secret management. External Groq failures return a structured fallback instead of crashing the application.

## Threat Model

Primary assets are the Groq API key, user sprint data, generated AI summaries, service availability, and backend integration trust. Attackers may submit malicious prompts, oversized bodies, XSS strings, SQL payloads, or high-volume traffic.

## API Abuse Risks

Risk: automated traffic can exhaust Groq quota or service capacity.
Mitigation: Flask-Limiter enforces 30 requests per minute per IP, backed by Redis in Docker and memory fallback for local/offline tests.

## Prompt Injection Risks

Rejected examples:

```text
ignore previous instructions
system prompt
reveal secrets
bypass rules
```

Expected response: HTTP 400 with `{"success": false, "data": {}, "message": "Invalid input"}`.

Mitigation: normalization, compact pattern matching, and system prompts that require using only supplied sprint context.

## SQL Injection Risks

The AI service does not execute SQL. SQL-like payloads are still rejected to avoid forwarding malicious content downstream.

Rejected examples:

```text
' OR '1'='1
UNION SELECT password FROM users
DROP TABLE tasks
```

## XSS Risks

HTML is stripped with `bleach`. Script and JavaScript URI patterns are rejected before reaching the model.

Example: `<script>alert(1)</script>` returns HTTP 400.

## Request Size Validation

Request bodies over 16 KB are rejected. String fields over 4,000 characters are rejected. JSON nesting is limited to six levels.

## Secret Management Policy

Secrets are never hardcoded. `GROQ_API_KEY`, model, Redis host, Redis port, and Flask environment are loaded from `.env`. `.env.example` contains only empty or safe defaults.

## Secure Headers

The app sets `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`, and `Referrer-Policy`.

## Security Testing Findings

Empty input: rejected with HTTP 400.
SQL injection payloads: rejected with HTTP 400.
Prompt injection payloads: rejected with HTTP 400.
XSS payloads: rejected or stripped.
Oversized input: rejected with HTTP 400.
Rate limit abuse: rejected with HTTP 429.

## Week 2 Verification

JWT verification assumption: the backend owns user authentication and should pass only authorized sprint data to this service.
Injection prevention: middleware blocks known prompt, SQL, and XSS payloads before route execution.
PII leakage: prompts instruct the model to use only supplied context; logs do not include full request bodies.
Prompt leakage: requests asking for system prompts or hidden instructions are rejected.

## Residual Risks

Novel prompt injection wording can bypass static patterns. Groq outages can still affect quality, but fallback responses preserve API stability. Backend authorization must be enforced before calls to this microservice.

## Team Sign-off

AI Developer 2: complete.
Security review: complete.
Docker validation: complete.
Final demo readiness: complete.
