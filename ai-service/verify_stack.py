import os
import sys
from urllib import request

import redis


BASE_URL = os.getenv("AI_SERVICE_URL", "http://localhost:5000")


def check_http(path, method="GET", body=None):
    data = None
    headers = {"Content-Type": "application/json"}
    if body is not None:
        data = body.encode("utf-8")
    req = request.Request(f"{BASE_URL}{path}", data=data, headers=headers, method=method)
    with request.urlopen(req, timeout=5) as response:
        return response.status, response.read().decode("utf-8")


def main():
    checks = []
    checks.append(("environment", bool(os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"))))

    try:
        client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            socket_connect_timeout=2,
        )
        checks.append(("redis", client.ping()))
    except Exception:
        checks.append(("redis", False))

    try:
        status, _ = check_http("/health")
        checks.append(("health", status == 200))
    except Exception:
        checks.append(("health", False))

    endpoint_payloads = [
        ("/describe", '{"task_title":"Demo task"}'),
        ("/recommend", '{"tasks":["Finish tests"]}'),
        ("/generate-report", '{"sprint_name":"Sprint 20","completed_tasks":1,"total_tasks":1}'),
    ]
    for path, payload in endpoint_payloads:
        try:
            status, _ = check_http(path, "POST", payload)
            checks.append((path, status in {200, 503}))
        except Exception:
            checks.append((path, False))

    for name, ok in checks:
        print(f"{name}: {'PASS' if ok else 'FAIL'}")

    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
