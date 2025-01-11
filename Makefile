# Makefile for DeLoOps Did Stuff hook

# Variables
PYTHON = python3
PYTEST = pytest
PIP = pip3
CONFIG_FILE = .git-commit-message-generator-config.json

# Default target
.PHONY: all
all: install

# Install dependencies using UV
.PHONY: install
install: requirements.txt requirements-dev.txt
	@echo "Installing dependencies with UV..."
	@uv pip install -r requirements-dev.txt
	@echo "Installing package in development mode..."
	@uv pip install -e .

# Generate locked requirements files
requirements.txt: requirements.in
	@echo "Generating requirements.txt..."
	@uv pip compile requirements.in -o requirements.txt

requirements-dev.txt: requirements-dev.in
	@echo "Generating requirements-dev.txt..."
	@uv pip compile requirements-dev.in -o requirements-dev.txt

# Install the hook to your local git repo
.PHONY: install-hook
install-hook:
	@echo "Installing DeLoOps Did Stuff hook..."
	@bash $(INSTALL_SCRIPT) hook

# Run tests
.PHONY: test
test:
	@echo "Running tests..."
	@pytest

# Lint the Python code
.PHONY: lint
lint:
	@echo "Linting Python code..."
	@ruff check .

# Format the Python code
.PHONY: format
format:
	@echo "Formatting Python code..."
	@ruff format .

# Clean up temporary files and caches
.PHONY: clean
clean:
	@echo "Cleaning up..."
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete
	@rm -rf .pytest_cache
	@rm -f $(CONFIG_FILE)
	@rm -f requirements.txt requirements-dev.txt

.PHONY: prompt-and-tag
prompt-and-tag:
	$(eval TAG_NAME := llm-snapshot-$(shell date +%Y%m%d-%H%M%S))
	@echo "\033[1;36m🚀 Converting Codebase to Prompt and Tagging for LLM 🚀\033[0m"
	@code2prompt --path . > /tmp/${TAG_NAME}.txt
	@git tag -a -m "$(TAG_NAME)" $(TAG_NAME) > /dev/null 2>&1
	@git push origin $(TAG_NAME) > /dev/null 2>&1
	@echo "\033[1;32m✅ Created and pushed tag: \033[1;33m$(TAG_NAME)\033[0m"
	@echo
	@echo "\033[1;35mNext Steps:\033[0m"
	@echo "  1. 📋 Paste clipboard into LLM thread content"
	@echo "  2. 🏷️  (Optional) Copy the following to label content version"
	@echo
	@echo "     \033[1;34m\`Full Source: $(TAG_NAME)\`\033[0m"
	@echo

# Print a summary of recent changes
.PHONY: summary
summary:
	@echo "Generating summary of recent changes..."
	@$(PYTHON) src/print_summary.py

# Set up development environment
.PHONY: dev-setup
dev-setup: install
	@echo "Development environment setup complete."

# Show current configuration
.PHONY: show-config
show-config:
	@echo "Showing current configuration..."
	@did-stuff show-config

# Show help
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  install     - Install dependencies with UV"
	@echo "  install-hook - Install the hook to your local git repo"
	@echo "  dev-setup   - Set up development environment"
	@echo "  test        - Run the test suite"
	@echo "  lint        - Lint the Python code"
	@echo "  format      - Format the Python code"
	@echo "  clean       - Clean up temporary files and caches"
	@echo "  prompt-and-tag - Convert codebase to prompt and create a git tag"
	@echo "  summary     - Print a summary of recent changes"
	@echo "  show-config - Show current configuration based on directory context"
	@echo "  help        - Show this help message"
