.PHONY: install test lint format type-check build docker-build docker-up deploy clean

# ---------------------------------------------------------------------------
# Local Development
# ---------------------------------------------------------------------------

install:  ## Install dependencies (dev mode)
	pip install -e ".[dev]"
	pre-commit install

test:  ## Run unit tests with coverage
	pytest tests/unit/ -v --cov=src --cov-report=term-missing --cov-fail-under=80

test-all:  ## Run all tests (unit + integration)
	pytest tests/ -v --cov=src --cov-report=term-missing

test-integration:  ## Run integration tests only
	pytest -m integration -v --tb=short

lint:  ## Run linter
	ruff check .

format:  ## Auto-format code
	ruff format .
	ruff check --fix .

type-check:  ## Run mypy type checker
	mypy src/

security:  ## Run security scans
	bandit -r src/ -s B101 --exclude "*/tests/*" -ll
	pip-audit

# ---------------------------------------------------------------------------
# Build & Deploy
# ---------------------------------------------------------------------------

build:  ## Build Python package
	python -m build

docker-build:  ## Build Docker image
	docker build -t your-service:latest .

docker-up:  ## Start local dev stack
	docker compose up -d

docker-down:  ## Stop local dev stack
	docker compose down

deploy:  ## Deploy to Render (requires RENDER_API_KEY)
	@echo "Push to main branch to trigger deployment via GitHub Actions"
	@echo "Or use: render deploy --service YOUR_RENDER_SERVICE_ID"

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

clean:  ## Remove build artifacts
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
