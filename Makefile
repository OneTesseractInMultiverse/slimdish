.DEFAULT_GOAL := help

.PHONY: help install test lint format typecheck quality frontend-install frontend-dev frontend-build dev build run update clean

help: ## Show available targets
	@awk 'BEGIN {FS = ":.*## "; printf "Usage: make <target>\n\n"} /^[a-zA-Z_-]+:.*## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install locked Python dependencies
	uv sync --all-groups --frozen

test: ## Run self-contained tests
	uv run pytest

lint: frontend-install ## Check Python and frontend source
	uv run ruff check .
	cd frontend && npm run lint

format: ## Format Python source
	uv run ruff format .

typecheck: ## Run strict Python type checks
	uv run mypy

quality: test lint typecheck frontend-build ## Run all quality gates

frontend-install: ## Install frontend dependencies
	cd frontend && npm ci

frontend-dev: ## Start the Vite development server
	cd frontend && npm run dev

frontend-build: frontend-install ## Build the frontend bundle
	cd frontend && npm run build

dev: ## Start the API with reload (run frontend-dev separately)
	APP_ENV=development uv run --env-file .env uvicorn slimdash.bootstrap.app:create_app --factory --reload

build: ## Build the production container
	docker build --tag slimdash:local .

run: ## Run the container with persistent SQLite storage
	docker compose up --build

update: ## Update Python and frontend dependency lock files
	uv lock --upgrade
	cd frontend && npm update && npm install --package-lock-only

clean: ## Remove generated local build artifacts
	uv run python -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ('.pytest_cache','.ruff_cache','.mypy_cache','htmlcov','frontend/dist')]"
