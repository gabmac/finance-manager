# Finance Manager

A personal finance management API built with FastAPI following Clean Architecture principles.

## Architecture

This project follows **Clean Architecture** (Hexagonal/Ports & Adapters) with the following layers:

```
┌─────────────────────────────────────────────────────────────┐
│                      INFRASTRUCTURE                         │
│  src/adapters/ (database, entrypoints, sso)                 │
├─────────────────────────────────────────────────────────────┤
│                       APPLICATION                           │
│  src/use_case/, src/dto/, src/ports/, src/exceptions.py     │
├─────────────────────────────────────────────────────────────┤
│                         DOMAIN                              │
│  src/entities/, src/enums/                                  │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
finance-manager/
├── src/
│   ├── adapters/
│   │   ├── database/
│   │   │   ├── models/          # SQLModel ORM models
│   │   │   └── repository/      # Port implementations
│   │   ├── entrypoints/
│   │   │   └── api/
│   │   │       ├── balance/     # Balance endpoints
│   │   │       ├── cross_cutting/  # Middlewares
│   │   │       ├── monitoring/  # Health checks
│   │   │       └── sso/         # SSO endpoints
│   │   └── sso/                 # SSO adapters
│   ├── dto/                     # Data Transfer Objects
│   ├── entities/                # Domain entities
│   ├── enums/                   # Domain enumerations
│   ├── ports/                   # Abstract interfaces
│   ├── settings/                # Configuration
│   └── use_case/                # Application use cases
├── test/
│   ├── generators/              # Test data factories
│   ├── integration/             # Integration tests
│   └── unit/                    # Unit tests
├── alembic/                     # Database migrations
└── pyproject.toml
```

## Requirements

- Python 3.11+
- PostgreSQL
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

### Using uv (recommended)

```bash
# Install dependencies
uv sync

# Install dev dependencies
uv sync --dev
```

### Using pip

```bash
pip install -e .
pip install -e ".[dev]"
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# System
SYSTEM_ENVIRONMENT=local
SYSTEM_HOST=0.0.0.0
SYSTEM_PORT=8000

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DATABASE=finance_manager

# JWT
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=12

# Google SSO
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
```

## Running the Application

### Development

```bash
uv run -m src.adapters.entrypoints.api
```

### Docker

```bash
docker build -t finance-manager .
docker run -p 8000:8000 --env-file .env finance-manager
```

## API Documentation

Once the application is running, access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health

| Method | Endpoint       | Description   |
|--------|----------------|---------------|
| GET    | `/api/health`  | Health check  |

### Authentication

| Method | Endpoint                    | Description              |
|--------|-----------------------------|--------------------------|
| GET    | `/auth/{provider}`          | Initiate SSO login       |
| GET    | `/auth/{provider}/callback` | SSO callback             |

### Balance

| Method | Endpoint                    | Description              |
|--------|-----------------------------|--------------------------|
| GET    | `/api/user/{user_id}/balance` | Get user balance       |

## Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

## Testing

This project uses **unittest** with `IsolatedAsyncioTestCase` for async tests.

### Run all tests

```bash
uv run python -m unittest discover -s test -p "*_test.py"
```

### Run unit tests

```bash
uv run python -m unittest discover -s test/unit -p "*_test.py"
```

### Run integration tests

```bash
uv run python -m unittest discover -s test/integration -p "*_test.py"
```

### Run specific test file

```bash
uv run python -m unittest test.integration.balance.users_balance_test
```

### Run specific test class

```bash
uv run python -m unittest test.integration.balance.users_balance_test.BalanceTest
```

### Run specific test method

```bash
uv run python -m unittest test.integration.balance.users_balance_test.BalanceTest.test_get_balance
```

## Code Quality

### Linting

```bash
uv run ruff check .
```

### Formatting

```bash
uv run ruff format .
```

### Type checking

```bash
uv run mypy src
```

## License

MIT

