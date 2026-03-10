# Python AI CI/CD Template

## Stack
Python | FastAPI | Docker | GitHub Actions | pytest

## Architecture
Reusable CI/CD template for Python AI projects. Entry: `src/main.py`.
- `src/` — FastAPI app with `/api/generate` and `/api/status/{id}` endpoints
- `.github/workflows/` — 9 workflows: ci, security, cost-gate, docker-build, deploy-render, health-monitor, integration-tests, release, api-docs
- `Dockerfile` + `render.yaml` — deploy blueprint (swap in your service name)

## Deploy
Template only — not deployed. Clone and configure for your service. Blueprint: `render.yaml`.

## Test
```pytest tests/  # 14 tests```

## Key Env
ANTHROPIC_API_KEY, RENDER_API_KEY, DOCKER_HUB_TOKEN
