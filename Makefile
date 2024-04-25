.PHONY: style
style: ## Patch code quality style issues.
	@poetry run isort .
	@poetry run black ./source/llmtool ./tests

.PHONY: check-style
check-style: ## Run code quality style tools.
	@echo "🚀 Code style checks: Running isort"
	@poetry run isort . --check-only
	@echo "🚀 Code style checks: Running black"
	@poetry run black --check ./source/llmtool ./tests

.PHONY: check-lint
check-lint: ## Run code linting tools.
	@echo "🚀 Static code linting : Running ruff"
	@poetry run ruff check ./source

.PHONY: check-types
check-types: ## Run code quality types tools.
	@echo "🚀 Static type checking: Running mypy"
	@poetry run mypy ./source
	@echo "🚀 Static code linting : Running ruff"
	@poetry run ruff check ./source

.PHONY: check-code
check-code: check-style check-types ## Run all code quality tools.

.PHONY: patch
patch: ## Update code using quality tools.
	@echo "🚀 Patch code : Running ruff"
	@poetry run ruff check ./pulumi --fix

.PHONY: check-packages
check-packages: ## Run package quality tools.
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry lock --check"
	@poetry check --lock
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@poetry run deptry .

.PHONY: check-security
check-security: ## Run package security tools.
	@echo "🚀 Checking for security issues: Running bandit"
	@poetry run bandit -c pyproject.toml -r ./source --quiet

.PHONY: check-all
check-all: check-style check-types check-security check-packages  ## Run all quality tools.

.PHONY: install
install: ## Install the poetry environment
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@poetry install

.PHONY: test
test: ## Run package tests
	@echo "🚀 Running pytest"
	@poetry run pytest

.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@poetry run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@poetry run mkdocs serve

.PHONY: docs-deploy
docs-deploy: ## Deploy project documentation to github pages
	@poetry run mkdocs gh-deploy --force

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
