.PHONY: test lint format clean docs install dev-install setup-hooks run-hooks

# Default target
all: lint test

# Install for development
dev-install:
	pip install -e ".[dev]"
	pip install pre-commit

# Install for production
install:
	pip install -e .

# Setup pre-commit hooks
setup-hooks:
	pre-commit install

# Run pre-commit hooks on all files
run-hooks:
	pre-commit run --all-files

# Run tests
test:
	pytest

# Run tests with coverage
test-coverage:
	pytest --cov=voicemidi --cov-report=html

# Lint code
lint:
	flake8 voicemidi tests
	black --check voicemidi tests
	isort --check-only --profile black voicemidi tests

# Format code
format:
	black voicemidi tests
	isort --profile black voicemidi tests

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf coverage_html_report
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run the application
run:
	python -m voicemidi

# List all audio devices
list-audio:
	python -m voicemidi --list-audio

# List all MIDI devices
list-midi:
	python -m voicemidi --list-midi 