#!/bin/sh
set -eu

cleanup() {
  kill "$dashboard_pid" "$api_pid" 2>/dev/null || true
}

corepack pnpm --filter @repo/dashboard dev &
dashboard_pid=$!

uv run uvicorn control_api.main:app --app-dir apps/control-api/src --reload --host 127.0.0.1 --port 8000 &
api_pid=$!

trap cleanup EXIT INT TERM
wait
