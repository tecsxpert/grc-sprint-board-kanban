#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

docker compose up --build -d
echo "Waiting for service to start..."
sleep 15

if curl -f http://localhost:5000/health >/dev/null 2>&1; then
  echo "Health check passed. Docker E2E container test succeeded."
  docker compose down
else
  echo "Health check failed."
  docker compose logs --no-color
  docker compose down
  exit 1
fi
