# URL Alias Service

A service for creating and managing URL aliases with FastAPI and clean architecture.

## Getting Started

You need: python3, make, uv(for local development), docker(for startup in docker)

1. Bootstrap the project:
```bash
uv sync --extra dev
source .venv/bin/activate

make bootstrap
```

This will:
- Copy environment files from `.env.dist`
- Generate JWT keys
- Install dependencies using uv
- Set up pre-commit hooks

2. Choose your deployment method:

### Local Development
```bash
# Start infrastructure (database)
make infra

# Run the application
python -m url_alias
```

### Docker Deployment
```bash
# Start all services in containers
make up
```

## Available Make Commands

### Development
- `make bootstrap` - Initial project setup
- `make lint` - Run code linting (ruff, codespell)
- `make static` - Run static analysis (bandit)
- `make alembic m="message"` - Generate new database migration

### Infrastructure
- `make infra` - Start database container
- `make up` - Start all services in containers
- `make stop` - Stop all containers
- `make down` - Stop and remove all containers

### Container Management
- `make api-shell` - Access application container shell
- `make api-logs` - View application logs
- `make db-shell` - Access database container shell
- `make db-logs` - View database logs
