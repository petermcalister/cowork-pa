---
description: Reset and reload the database schema by running migrations and seed data
---

# Reload Schema Command

Reset the database schema and repopulate with seed/test data.

## Steps

1. **Check infrastructure is running:**
   ```bash
   docker compose ps
   docker compose exec postgres pg_isready
   ```

2. **Run migrations against target schema:**
   ```bash
   python src/migrations/migrate_database.py test
   python src/migrations/migrate_database.py develop
   ```

3. **Verify schema is correct:**
   ```bash
   docker compose exec postgres psql -U postgres -d app_db -c "\dt test.*"
   ```

4. **Run seed data if applicable:**
   ```bash
   poetry run python src/seed_data.py
   ```

5. **Run a quick smoke test to verify:**
   ```bash
   poetry run behave --tags=@storage --dry-run
   ```

## When to Use

- After pulling schema changes from git
- After a database reset or volume recreation
- When tests fail with "relation does not exist" errors
- Starting fresh development on a new feature
