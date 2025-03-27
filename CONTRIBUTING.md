# Contributing to Voice-to-MIDI

Thank you for your interest in contributing to Voice-to-MIDI! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```
   git clone https://github.com/yourusername/voicemidi.git
   cd voicemidi
   ```
3. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install development dependencies:
   ```
   make dev-install
   ```
   Or manually:
   ```
   pip install -e ".[dev]"
   ```

## Development Workflow

1. Create a branch for your changes:

   ```
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and follow the coding standards:

   - Use the provided Makefile targets to ensure code quality
   - Run `make format` to automatically format your code
   - Run `make lint` to check for code style issues
   - Add tests for new features or bug fixes

3. Run the tests to ensure everything works:

   ```
   make test
   ```

4. Commit your changes with descriptive commit messages:

   ```
   git commit -m "Add feature X" -m "This feature adds X functionality to solve Y problem."
   ```

5. Push your changes to your fork:

   ```
   git push -u origin feature/your-feature-name
   ```

6. Create a pull request on GitHub

## Code Style

We follow these coding standards:

- [Black](https://black.readthedocs.io/en/stable/) for code formatting
- [isort](https://pycqa.github.io/isort/) for import sorting
- [flake8](https://flake8.pycqa.org/en/latest/) for code linting

The configuration for these tools is in `pyproject.toml` and `.flake8`.

## Testing

We use pytest for testing. All new features should include tests. Run tests with:

```
make test
```

To run with coverage:

```
make test-coverage
```

## Documentation

- Update the documentation when adding or modifying features
- Follow the existing documentation style
- Run the documentation generation and check for warnings/errors

## Pull Request Process

1. Update the README.md or documentation with details of changes if appropriate
2. Update the tests to cover your changes
3. Make sure all tests pass before submitting the PR
4. The PR should work on all supported Python versions
5. The PR description should explain the changes and the problem it solves

## License

By contributing, you agree that your contributions will be licensed under the project's license.
