---
paths: "**/*.py"
---

# No Hardcoded Schema Names

**Purpose:** Prevent hardcoded database schema names in Python code. All schema access must go through configuration.

---

## Rule

**NEVER hardcode schema names** like `'public'`, `'develop'`, `'test'` directly in SQL or Python code.

### Wrong

```python
# ❌ Hardcoded schema
query = "SELECT * FROM public.tasks WHERE status = 'active'"
query = f"INSERT INTO develop.users ..."
```

### Correct

```python
# ✅ Schema from configuration
schema = get_default_schema()
query = f"SELECT * FROM {schema}.tasks WHERE status = 'active'"
```

---

## Schema Resolution

Use a centralized configuration function:

```python
import os

def get_default_schema() -> str:
    """Get schema name from environment configuration."""
    env = os.getenv("APP_ENV", "development")
    schema_map = {
        "development": "develop",
        "test": "test",
        "production": "public",
    }
    return schema_map.get(env, "develop")
```

| Context | Schema Source |
|---------|--------------|
| Tests | Test config or `test` schema |
| Development | `APP_ENV` environment variable |
| Production | `APP_ENV` environment variable |

---

## Verification

```bash
# Find hardcoded schema references
grep -rn "FROM public\." src/
grep -rn "FROM develop\." src/
grep -rn "'public'" src/ --include="*.py"
```
