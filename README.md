# Production CI/CD Template for Python AI Services

Battle-tested GitHub Actions workflows extracted from production AI services handling real traffic. Fork, replace placeholders, ship.

## What's Included

| # | Workflow | File | Trigger | What It Does |
|---|---------|------|---------|-------------|
| 1 | **CI** | `ci.yml` | Push/PR | Ruff lint + format + mypy type check + pytest with 80% coverage gate |
| 2 | **Security** | `security.yml` | Push/PR/Weekly | Secrets detection, Bandit SAST, pip-audit CVE scan, SQL injection check, Docker config audit |
| 3 | **Cost Gate** | `cost-gate.yml` | Every 6h | LLM token budget monitoring -- alerts at 75%, blocks at 90% |
| 4 | **Docker Build** | `docker-build.yml` | Push to main | Multi-platform build + push to Docker Hub with GHA cache |
| 5 | **Deploy (Render)** | `deploy-render.yml` | Push to main | Build image, trigger Render deploy, poll until live (15 min timeout) |
| 6 | **Health Monitor** | `health-monitor.yml` | Every 30 min | Uptime checks + auto-issue on failure + auto-close on recovery |
| 7 | **Integration Tests** | `integration-tests.yml` | Push/PR | Slower tests with service containers (Postgres, Redis) |
| 8 | **Release** | `release.yml` | Version bump | Auto-tag from pyproject.toml + GitHub Release with changelog |
| 9 | **API Docs** | `api-docs.yml` | Push to main | Extract OpenAPI spec from FastAPI + publish Redoc to GitHub Pages |

## Workflow Architecture

```
                         Push/PR to main
                              |
                    +---------+---------+
                    |                   |
               +----v----+        +----v-----+
               |   CI    |        | Security |
               | lint    |        | secrets  |
               | test    |        | bandit   |
               | build   |        | pip-audit|
               +---------+        +----------+
                    |
            (on merge to main)
                    |
          +---------+---------+
          |         |         |
     +----v---+ +--v---+ +---v-----+
     | Docker | |Release| |API Docs |
     | Build  | | Tag   | | Redoc   |
     +----+---+ +------+ +---------+
          |
     +----v-------+
     | Deploy     |
     | (Render)   |
     +----+-------+
          |
     +----v-----------+
     | Health Monitor  |  (runs every 30 min)
     | (24/7 uptime)   |
     +-----------------+

     +------------------+
     | Cost Gate        |  (runs every 6 hours)
     | (token budget)   |
     +------------------+
```

## Quick Start

### 1. Fork this repo

```bash
gh repo create my-ai-service --template ChunkyTortoise/python-ai-cicd-template --public
cd my-ai-service
```

### 2. Replace placeholders

Search and replace these across all workflow files:

| Placeholder | Replace With | Example |
|-------------|-------------|---------|
| `YOUR_SERVICE_NAME` | Your service name | `my-ai-api` |
| `YOUR_DOCKERHUB_ORG` | Docker Hub org/user | `myuser` |
| `src.app:app` | Your FastAPI import path | `my_service.main:app` |

### 3. Add GitHub Secrets

Go to **Settings > Secrets and variables > Actions** and add:

| Secret | Required By | How to Get |
|--------|------------|-----------|
| `DOCKERHUB_USERNAME` | docker-build, deploy-render | Docker Hub account |
| `DOCKERHUB_TOKEN` | docker-build, deploy-render | Docker Hub > Security > New Access Token |
| `RENDER_API_KEY` | deploy-render | Render > Account Settings > API Keys |
| `ANTHROPIC_API_KEY` | integration-tests (optional) | Anthropic Console |
| `TOKEN_BUDGET_MONTHLY` | cost-gate (optional) | Set your monthly token budget (default: 5M) |

### 4. Add GitHub Variables

Go to **Settings > Secrets and variables > Actions > Variables**:

| Variable | Required By | Example |
|----------|------------|---------|
| `RENDER_SERVICE_ID` | deploy-render | `srv-abc123xyz` |
| `SERVICE_URL` | health-monitor | `https://my-app.onrender.com` |

### 5. Enable GitHub Pages

For API docs: **Settings > Pages > Source: GitHub Actions**

### 6. Push and watch

```bash
git push origin main
```

All workflows will trigger automatically based on their configured events.

## Local Development

```bash
make install       # Install deps + pre-commit hooks
make test          # Run unit tests with coverage
make lint          # Ruff linting
make format        # Auto-format
make type-check    # mypy
make security      # Bandit + pip-audit
make docker-build  # Build Docker image
make docker-up     # Start local stack (app + Redis)
```

## Project Structure

```
your-service/
├── .github/workflows/     # 9 CI/CD workflows
├── src/                   # Application code
│   ├── __init__.py
│   └── app.py            # FastAPI entry point
├── tests/
│   ├── unit/             # Fast isolated tests
│   └── integration/      # Tests hitting external services
├── pyproject.toml        # Dependencies + tool config
├── Makefile              # Local dev commands
├── Dockerfile            # Multi-stage production build
├── docker-compose.yml    # Local dev stack
├── render.yaml           # Render Blueprint
├── .ruff.toml            # Linter config
├── .pre-commit-config.yaml
├── .env.example
└── .gitignore
```

## Security Features

- **Pre-commit hooks**: Ruff lint + format, secret detection, merge conflict check
- **CI pipeline**: Bandit SAST, pip-audit CVE scanning, SQL injection patterns
- **Infrastructure**: Checkov Docker Compose audit, .env gitignore verification
- **Runtime**: Non-root Docker user, health checks, secrets via environment only

## Example Projects Using This Template

- [Jorge Real Estate Bots](https://github.com/ChunkyTortoise/jorge_real_estate_bots) -- AI-powered SMS lead qualification
- [DocExtract AI](https://github.com/ChunkyTortoise/docextract) -- Document processing pipeline
- [AI Workflow API](https://github.com/ChunkyTortoise/ai-workflow-api) -- YAML-driven workflow engine

## License

MIT
