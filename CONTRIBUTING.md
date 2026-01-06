# Contributing to Guest Relations AI App

Thank you for your interest in contributing! We love your input and want to make contributing as easy and transparent as possible.

## Development Process

We use GitHub to host code, track issues and feature requests, and accept pull requests.

### Pull Request Process

1. **Fork the repo** and create your branch from `main`
2. **Install dependencies** for both backend and frontend
3. **Make your changes** with clear, descriptive commits
4. **Add tests** if you've added code that should be tested
5. **Update documentation** if you've changed APIs or added features
6. **Ensure tests pass** before submitting
7. **Open a Pull Request** with a clear description

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/guest-relations-ai-app.git
cd guest-relations-ai-app

# Backend setup
cd backend
pip install -r requirements.txt
cp env.example .env  # Configure your environment

# Frontend setup
cd ../frontend
npm install
cp env.example .env  # Configure your environment
```

## Coding Standards

### Python (Backend)
- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Use type hints for function parameters and returns
- Write docstrings for modules, classes, and functions
- Maximum line length: 88 characters (Black formatter)

### JavaScript/React (Frontend)
- Follow ESLint configuration in the project
- Use functional components with hooks
- Prefer named exports over default exports
- Use meaningful variable and function names

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Example: `feat: add email notification for follow-ups`

## Reporting Bugs

Use GitHub Issues with the bug report template. Include:
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, browser, versions)
- Screenshots if applicable

## Suggesting Features

Open a GitHub Issue with the feature request template. Describe:
- The problem you're trying to solve
- Your proposed solution
- Alternative solutions considered
- Additional context

## Code Review Process

1. Maintainers review PRs within 3-5 business days
2. Address feedback and push updates
3. Once approved, maintainers merge the PR
4. Your contribution appears in the next release

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE).

## Questions?

Open a discussion on GitHub or reach out to the maintainers.

---

**Thank you for contributing! 🎉**
