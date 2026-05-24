#!/usr/bin/env bash
set -euo pipefail

FASTAPI_PID=""
DETECT_PID=""

cleanup() {
  if [[ -n "${FASTAPI_PID}" ]] && kill -0 "${FASTAPI_PID}" 2>/dev/null; then
    kill "${FASTAPI_PID}" 2>/dev/null || true
  fi
  if [[ -n "${DETECT_PID}" ]] && kill -0 "${DETECT_PID}" 2>/dev/null; then
    kill "${DETECT_PID}" 2>/dev/null || true
  fi
  wait || true
}

trap cleanup SIGINT SIGTERM EXIT

(cd /app/fastapi && python -m uvicorn api:app --host 0.0.0.0 --port 8000) &
FASTAPI_PID=$!

python /app/Webcam/object_detection.py &
DETECT_PID=$!

wait -n "${FASTAPI_PID}" "${DETECT_PID}"
