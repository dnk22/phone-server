SHELL := /bin/sh
PNPM := corepack pnpm
export PATH := $(CURDIR)/.corepack:$(PATH)
export UV_CACHE_DIR := .uv-cache

.PHONY: help install dev dev-control-api dev-device-agent dev-backend test-control-api test-device-agent format format-check lint typecheck test build check clean

help:
	@echo "Android Linux Server development commands"
	@echo "  make install       Install JS/Python dependencies and Git hooks"
	@echo "  make dev           Run dashboard and Control API development servers"
	@echo "  make dev-control-api    Run Control API locally"
	@echo "  make dev-device-agent   Run Device Agent locally"
	@echo "  make dev-backend        Run Control API and Device Agent locally"
	@echo "  make test-control-api   Run Control API tests"
	@echo "  make test-device-agent  Run Device Agent tests"
	@echo "  make format        Format JavaScript, TypeScript, and Python"
	@echo "  make format-check  Check formatting without modifying files"
	@echo "  make lint          Run ESLint and Ruff"
	@echo "  make typecheck     Run TypeScript and Python type checking"
	@echo "  make test          Run Vitest and Pytest"
	@echo "  make build         Build TypeScript packages and validate Python imports"
	@echo "  make check         Run the complete CI quality gate"
	@echo "  make clean         Remove generated build and cache artifacts"

install:
	mkdir -p .corepack
	corepack enable --install-directory .corepack
	corepack prepare pnpm@11.9.0 --activate
	$(PNPM) install --frozen-lockfile
	uv sync --frozen --all-packages --dev
	$(PNPM) exec husky

dev:
	./tooling/scripts/dev.sh

dev-control-api:
	uv run uvicorn control_api.main:app --app-dir apps/control-api/src --reload --host 127.0.0.1 --port 8000

dev-device-agent:
	uv run --package device-agent device-agent

dev-backend:
	CONTROL_API_HOST=127.0.0.1 CONTROL_API_PORT=8000 uv run uvicorn control_api.main:app --app-dir apps/control-api/src --reload --host 127.0.0.1 --port 8000 & \
	API_PID=$$!; \
	DEVICE_AGENT_CONTROL_API_URL=http://127.0.0.1:8000 DEVICE_AGENT_ENABLE_MOCK_DEVICE=true uv run --package device-agent device-agent; \
	kill $$API_PID

format:
	$(PNPM) format
	uv run ruff check --fix .
	uv run ruff format .

format-check:
	$(PNPM) format:check
	uv run ruff format --check .

lint:
	$(PNPM) lint
	uv run ruff check .

typecheck:
	$(PNPM) typecheck
	uv run pyright

test:
	$(PNPM) test
	uv run pytest

test-control-api:
	uv run pytest apps/control-api/tests

test-device-agent:
	uv run pytest apps/device-agent/tests

build:
	$(PNPM) build
	uv run python tooling/scripts/validate_python_imports.py

check: format-check lint typecheck test build

clean:
	$(PNPM) clean
	uv run python tooling/scripts/clean.py
