---
paths: "**/.env*, **/config*.py, **/settings*.py, **/docker-compose*"
---

# Environment Setup & Configuration

**Purpose:** Project environment configuration, infrastructure setup, and runtime configuration patterns.

---

## Project Structure

```
project-root/
├── .env                 # Local environment variables (gitignored)
├── .env.example         # Template for .env (committed)
├── docker-compose.yml   # Infrastructure services
├── pyproject.toml       # Python dependencies (Poetry)
├── src/                 # Application source code
├── tests/               # Test suites
└── Makefile             # Common commands
```

---

## Environment Variables

```bash
# .env.example
APP_ENV=development          # development | test | production
DB_HOST=localhost
DB_PORT=5432
DB_NAME=app_db
DB_USER=postgres
DB_PASSWORD=postgres
LOG_LEVEL=INFO
```

**Loading pattern:**

```python
from dotenv import load_dotenv
import os

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")
DB_HOST = os.getenv("DB_HOST", "localhost")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
```

---

## Infrastructure (Docker Compose)

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: app_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

---

## Common Commands

```bash
# Infrastructure
docker compose up -d          # Start services
docker compose down           # Stop services
docker compose ps             # Check running services

# Python environment
poetry install                # Install dependencies
poetry shell                  # Activate virtualenv
poetry add <package>          # Add dependency

# Running the app
poetry run python src/main.py       # Run main entry point
poetry run streamlit run src/app.py # Run Streamlit app

# Tests
poetry run pytest tests/ -v         # Run all tests
poetry run behave                   # Run BDD tests
```

---

## Multi-Environment Configuration

```python
# config.py
import os

ENV_CONFIGS = {
    "development": {
        "debug": True,
        "schema": "develop",
        "log_level": "DEBUG",
    },
    "test": {
        "debug": False,
        "schema": "test",
        "log_level": "WARNING",
    },
    "production": {
        "debug": False,
        "schema": "public",
        "log_level": "INFO",
    },
}

def get_config() -> dict:
    env = os.getenv("APP_ENV", "development")
    return ENV_CONFIGS.get(env, ENV_CONFIGS["development"])
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `.env` committed to git | Add to `.gitignore`, use `.env.example` as template |
| Hardcoded config values | Use environment variables with defaults |
| No `.env.example` | Create one with placeholder values |
| Docker volumes not persisted | Use named volumes in compose file |
| Missing `load_dotenv()` | Call at startup before reading env vars |
