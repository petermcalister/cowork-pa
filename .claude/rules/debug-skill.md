---
paths: "**/*.py"
---

# Project-Specific Debug Companion

**Purpose:** Project-specific debugging tools, log locations, common error patterns, and diagnostic commands. Complements the generic `debug-skill` skill.

---

## Quick Diagnostic Commands

```bash
# Check infrastructure
docker compose ps
docker compose exec postgres pg_isready

# Check recent logs
tail -50 src/files/logs/app.log

# Check test status
poetry run pytest tests/ -v --tb=short
poetry run behave --dry-run
```

---

## Log Locations

| Log | Path | Contents |
|-----|------|----------|
| Application | `src/files/logs/app.log` | Runtime logs, errors |
| Test output | Terminal / CI output | Test pass/fail details |
| Docker logs | `docker compose logs postgres` | Database logs |

---

## Common Error Patterns

| Error | Likely Cause | Diagnostic | Fix |
|-------|-------------|------------|-----|
| `connection refused` | Database not running | `docker compose ps` | `docker compose up -d` |
| `relation "X" does not exist` | Missing migration | `\d schema.table` | Run migrations |
| `column "X" does not exist` | Schema mismatch | `\d schema.table` | Check actual column names |
| `UNIQUE constraint violated` | Duplicate test data | Check cleanup | Run cleanup before test |
| `ModuleNotFoundError` | Import path wrong | Check `sys.path` | Fix import statement |
| `ValidationError` (Pydantic) | Type mismatch | Check DB return types | Match DTO to DB types |

---

## Test Debugging Workflow

```bash
# 1. Run failing test in isolation
poetry run behave --tags=@failing_tag -v --no-capture

# 2. Check database state
docker compose exec postgres psql -U postgres -d app_db \
    -c "SELECT count(*) FROM test.entities WHERE created_by = 'bdd_test'"

# 3. Check for leftover test data
docker compose exec postgres psql -U postgres -d app_db \
    -c "SELECT * FROM test.entities WHERE created_by = 'bdd_test' LIMIT 5"

# 4. Manual cleanup if needed
docker compose exec postgres psql -U postgres -d app_db \
    -c "DELETE FROM test.entities WHERE created_by = 'bdd_test'"
```

---

## Infrastructure Recovery

```bash
# Full reset (last resort)
docker compose down -v          # Stop and remove volumes
docker compose up -d            # Restart fresh
python src/migrations/migrate_database.py test     # Reapply migrations
python src/migrations/migrate_database.py develop
```

---

## When to Escalate to User

- Infrastructure won't start after restart
- Test failures you can't reproduce locally
- Permission or credential errors
- Data corruption suspected
