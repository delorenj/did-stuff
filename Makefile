# Makefile for DeLoOps Did Stuff hook

# Variables
PYTHON = python3
PYTEST = pytest
PIP = pip3
INSTALL_SCRIPT = ./install-cli.sh
CONFIG_FILE = .git-commit-message-generator-config.json

# Installs the DidStuff CLI tool
.PHONY: all
all: install

# Install the cli tool
.PHONY: install
install:
	@echo "Installing DeLoOps Did Stuff hook..."
	@bash $(INSTALL_SCRIPT)

# Install the hook to your local git repo
.PHONY: install-hook
install-hook:
	@echo "Installing DeLoOps Did Stuff hook..."
	@bash $(INSTALL_SCRIPT) hook

.PHONY: test
test:
	@echo "Running tests..."
	@$(PYTEST) tests

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

# Show help
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  install  - Install the cli tool"
	@echo "  install-hook - Install the hook to your local git repo"
	@echo "  test     - Run the test suite"
	@echo "  lint     - Lint the Python code"
	@echo "  format   - Format the Python code"
	@echo "  clean    - Clean up temporary files and caches"
	@echo "  help     - Show this help message"
