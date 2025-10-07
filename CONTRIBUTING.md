# Contributing to CodeSonor

Thank you for your interest in CodeSonor! This guide covers development setup, testing, and publishing.

## 🚀 Quick Start for Development

### 1. Clone and Install

```bash
git clone https://github.com/farhanmir/CodeSonor.git
cd CodeSonor
pip install -e .[dev]
```

### 2. Set Up API Keys

Create a `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=your_github_token_here
```

Get keys:
- **Gemini API**: https://makersuite.google.com/app/apikey (Free)
- **GitHub Token**: https://github.com/settings/tokens (needs `public_repo` scope)

### 3. Test It Works

```bash
# Test CLI
python -m codesonor summary https://github.com/pallets/flask

# Run tests
pytest

# Run web app
python app.py
```

## 📦 Publishing to PyPI

### Prerequisites

1. PyPI account: https://pypi.org/account/register/
2. Install tools: `pip install build twine`

### Build and Publish

```bash
# Clean previous builds
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue

# Build package
python -m build

# Test on TestPyPI (recommended first)
twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ codesonor

# Publish to PyPI
twine upload dist/*
```

### Using API Tokens (Recommended)

Create `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
username = __token__
password = pypi-your-test-api-token-here
```

Get tokens at https://pypi.org/manage/account/token/

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/codesonor

# Run specific test
pytest tests/test_codesonor.py::TestGitHubClient -v
```

## 🔄 Version Updates

1. Update version in `pyproject.toml`:
   ```toml
   version = "0.1.1"
   ```

2. Update in `src/codesonor/__init__.py`:
   ```python
   __version__ = "0.1.1"
   ```

3. Build and publish:
   ```bash
   python -m build
   twine upload dist/*
   ```

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.2.0): New features
- **PATCH** (0.1.1): Bug fixes

## 🤝 Contributing Code

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `pytest`
5. Commit: `git commit -am "Add feature"`
6. Push: `git push origin feature-name`
7. Create Pull Request

## 📝 Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions
- Keep functions focused and small

## 🐛 Reporting Issues

Open an issue on GitHub with:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- System info (OS, Python version)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Questions?** Open an issue on GitHub or contact the maintainer.
