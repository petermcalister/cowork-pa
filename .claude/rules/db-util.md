---
paths: "**/db*.py, **/database*.py, **/utils/**"
---

# Database Utility Patterns

**Purpose:** Database connection management, query patterns, and transaction handling.

---

## DatabaseManager Pattern

```python
class DatabaseManager:
    """Centralized database connection and query execution."""

    def __init__(self, connection_type: str = "default"):
        self.connection_type = connection_type
        self._conn = None

    def get_connection(self):
        """Get or create database connection."""
        if self._conn is None or self._conn.closed:
            self._conn = self._create_connection()
        return self._conn

    def execute(self, sql: str, params: tuple = None) -> int:
        """Execute a write query, return rows affected."""
        with self.get_connection().cursor() as cur:
            cur.execute(sql, params)
            return cur.rowcount

    def fetch_all(self, sql: str, params: tuple = None) -> list[dict]:
        """Execute a read query, return list of dicts."""
        with self.get_connection().cursor() as cur:
            cur.execute(sql, params)
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]

    def fetch_one(self, sql: str, params: tuple = None) -> dict | None:
        """Execute a read query, return single dict or None."""
        with self.get_connection().cursor() as cur:
            cur.execute(sql, params)
            row = cur.fetchone()
            if row is None:
                return None
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, row))

    def begin_transaction(self):
        """Begin a transaction context manager."""
        return TransactionContext(self.get_connection())
```

---

## Transaction Pattern

```python
class TransactionContext:
    def __init__(self, conn):
        self.conn = conn

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        return False

    def commit(self):
        self.conn.commit()
```

**Usage:**

```python
db = DatabaseManager()
try:
    with db.begin_transaction() as txn:
        db.execute("INSERT INTO ...", params)
        db.execute("UPDATE ...", params)
        txn.commit()
except Exception as e:
    logger.error(f"Transaction failed: {e}")
```

---

## Connection Configuration

```python
# Environment-based connection config
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "app_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
}
```

---

## Docker Database Commands

```bash
# Start database
docker compose up -d postgres

# Stop database
docker compose down

# Health check
docker compose exec postgres pg_isready

# Interactive shell
docker compose exec postgres psql -U postgres -d app_db

# Inspect table structure
docker compose exec postgres psql -U postgres -d app_db -c "\d schema.tablename"
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Connection not closed | Use context managers or connection pooling |
| Hardcoded credentials | Use environment variables |
| SQL injection via f-strings | Use parameterized queries (`%s` placeholders) |
| Missing transaction on multi-step writes | Wrap in `begin_transaction()` |
| Not handling connection drops | Check `conn.closed` before use |
