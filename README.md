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
- pre-commit (git hooks)
- ruff (linting)

## Configuration

The application uses a central configuration system based on Pydantic settings.
Configuration can be set through:

1. Environment variables
2. `.env` file in the project root
3. Default values in the code

Key configuration options:

- `ENVIRONMENT`: Set to "development" or "production" (defaults to "development")
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `MEOW_BANK_API_KEY`: Key to be used for API calls (defaults to "test_api_key")

## Development Setup

After installation, set up pre-commit hooks to automatically format and lint your code:

```bash
pre-commit install
```

## Database Setup

The project uses SQLite as the database.
Starting the server will initialise and create the following tables:

- `customers` - Stores customer information
- `accounts` - Stores bank account information
- `transfers` - Records money transfers between accounts

## Logging

Log files are stored in the `logs` directory with the format `meow_bank_YYYYMMDD.log`.

## Running the Application

Start the FastAPI development server:

```bash
uvicorn meow_bank.main:app --reload --port 8000
```

The API will be available at:

- Local development: `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI spec: `http://localhost:8000/openapi.json`

## Authentication

Include your API key in the `X-API-Key` header with every request:

## Testing

The project uses pytest for testing.

To run all tests:

```bash
pytest
```
