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

## Configuration

The application uses a central configuration system based on Pydantic settings. Configuration can be set through:

1. Environment variables
2. `.env` file in the project root
3. Default values in the code

Key configuration options:

- `ENVIRONMENT`: Set to "development" or "production" (defaults to "development")
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `LOG_LEVEL`: Logging level (automatically set based on environment)

Example `.env` file:

```env
ENVIRONMENT=development
DATABASE_URL=sqlite:///./meow_bank.db
```

## Development Setup

After installation, set up pre-commit hooks to automatically format and lint your code:

```bash
pre-commit install
```

Now, every time you make a commit, the following checks will run automatically:

- Code formatting with Black
- Import sorting with isort
- Linting with Ruff

## Database Setup

The project uses SQLite as the database. To initialize the database and create all necessary tables:

```bash
python -m meow_bank.db.init_db
```

This will create the following tables:

- `customers` - Stores customer information
- `accounts` - Stores bank account information
- `transfers` - Records money transfers between accounts
- `balance_cache` - Caches account balances for quick lookups

## Logging

The application uses Loguru for logging with the following features:

- Console output with colored formatting for better readability
- JSON-formatted logs stored in the `logs` directory
- Daily log rotation with 30-day retention
- Log compression to save disk space
- Environment-based logging levels:
  - Development: Shows DEBUG and above in console
  - Production: Shows INFO and above in console
  - All environments: DEBUG and above are always logged to file

Log files are stored in the `logs` directory with the format `meow_bank_YYYYMMDD.log`.

## Running the Application

To start the FastAPI application:

```bash
uvicorn meow_bank.main:app --reload
```

The API will be available at `http://localhost:8000`.
Swagger API Documentation: `http://localhost:8000/docs`
