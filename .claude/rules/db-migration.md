---
paths: "**/migrations/**/*.sql, **/migrations/**/*.py"
---

# Database Migration Patterns

**Purpose:** Conventions for creating, versioning, and applying database schema migrations.

---

## Migration File Structure

```
src/migrations/
├── migrate_database.py       # Migration runner script
└── sql/
    ├── initial_schema_v0.0.1.sql
    ├── add_search_v0.0.2.sql
    └── add_metadata_v0.0.3.sql
```

### Naming Convention

```
{object_or_feature}_v{major}.{minor}.{patch}.sql
```

Examples:
- `initial_schema_v0.0.1.sql`
- `add_vector_search_v0.0.2.sql`
- `add_user_profiles_v0.1.0.sql`

---

## Migration File Template

```sql
-- Migration: {description}
-- Version: v{X.Y.Z}
-- Date: YYYY-MM-DD

-- Up
CREATE TABLE IF NOT EXISTS {schema}.new_table (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_new_table_name
    ON {schema}.new_table(name);

-- Track migration
INSERT INTO {schema}.schema_migrations (version, description, applied_at)
VALUES ('v{X.Y.Z}', '{description}', CURRENT_TIMESTAMP)
ON CONFLICT (version) DO NOTHING;
```

---

## Migration Runner

```python
# migrate_database.py
import os
import sys
from pathlib import Path

def run_migrations(schema: str, db):
    """Apply pending migrations in order."""
    migration_dir = Path(__file__).parent / "sql"
    applied = get_applied_migrations(db, schema)

    for sql_file in sorted(migration_dir.glob("*.sql")):
        version = extract_version(sql_file.name)
        if version not in applied:
            print(f"Applying: {sql_file.name}")
            sql = sql_file.read_text().replace("{schema}", schema)
            db.execute(sql)
            print(f"  ✓ Applied {version}")

if __name__ == "__main__":
    schema = sys.argv[1] if len(sys.argv) > 1 else "develop"
    run_migrations(schema, DatabaseManager())
```

---

## Applying Migrations

```bash
# Apply to specific schema
python src/migrations/migrate_database.py develop
python src/migrations/migrate_database.py test

# Verify table structure after migration
docker compose exec postgres psql -U postgres -d app_db -c "\d schema.tablename"
```

---

## Migration Checklist

For each migration:
- [ ] SQL file created with version number
- [ ] Applied to test schema
- [ ] Applied to development schema
- [ ] Verified with `\d` table inspection
- [ ] Handles IF NOT EXISTS / IF EXISTS for idempotency
- [ ] Uses `{schema}` placeholder, not hardcoded schema name

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Non-idempotent migration | Use `IF NOT EXISTS` / `IF EXISTS` |
| Hardcoded schema in SQL | Use `{schema}` placeholder |
| Missing index on FK | Add index for every foreign key column |
| Forgetting to apply to all schemas | Run against test AND develop |
| No migration tracking table | Create `schema_migrations` table |
