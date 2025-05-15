# Meow Assessment

A FastAPI-based Bank API project.

## Requirements

- Python >= 3.10
- Package manager: uv

## Installation

1. Clone the repository:

```bash
git clone git@github.com:shanegrouber/meow_bank_api.git
cd meow_bank_api
```

2. Create and activate a virtual environment:

```bash
uv venv
source venv/bin/activate
```

3. Install the project with development dependencies:

```bash
uv pip install -e ".[dev]"
```

This will install both production and development dependencies. The development dependencies include:

- black (code formatting)
- isort (import sorting)
- mypy (type checking)
- pre-commit (git hooks)
- ruff (linting)

## Development Setup

After installation, set up pre-commit hooks to automatically format and lint your code:

```bash
pre-commit install
```

Now, every time you make a commit, the following checks will run automatically:

- Code formatting with Black
- Import sorting with isort
- Linting with Ruff

## Running the Application

[Add instructions for running the application here]
