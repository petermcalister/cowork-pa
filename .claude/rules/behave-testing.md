---
paths: "**/features/**/*.feature, **/features/**/*.py"
---

# Behave BDD Testing Patterns

**Purpose:** Project-specific Behave test conventions, environment setup, step patterns, and debugging.

---

## Directory Structure

```
features/
├── environment.py           # Hooks: before_all, before_scenario, after_scenario
├── steps/
│   ├── common_steps.py      # Shared Given steps (clean data, DB access)
│   ├── entity_steps.py      # Entity-specific steps
│   └── search_steps.py      # Search/query steps
├── fixtures/                # Test data files
│   └── sample_data.json
├── data_import.feature      # Feature files organized by domain
├── search.feature
└── validation.feature
```

---

## Environment Setup

```python
# features/environment.py
from database import DatabaseManager

def before_all(context):
    """One-time setup for entire test run."""
    context.db = DatabaseManager(connection_type="test")
    context.schema = "test"

def before_scenario(context, scenario):
    """Per-scenario setup."""
    context.test_marker = "bdd_test"

def after_all(context):
    """Cleanup after all tests."""
    context.db.close()
```

---

## Test Execution

```bash
# Run all features
poetry run behave

# Run by tag
poetry run behave --tags=@storage
poetry run behave --tags="@search and not @slow"

# Run specific feature file
poetry run behave features/data_import.feature

# Dry run (check step matching)
poetry run behave --dry-run

# Verbose output
poetry run behave -v --no-capture
```

---

## Tag Organization

| Tag | Purpose | Example |
|-----|---------|---------|
| `@migration` | Schema changes | Create/alter tables |
| `@storage` | CRUD operations | Insert, query, update, delete |
| `@search` | Search/query tests | Full-text, vector, hybrid |
| `@integration` | End-to-end workflows | Full pipeline tests |
| `@slow` | Long-running tests | LLM calls, large datasets |
| `@destructive` | Schema-modifying tests | DROP, TRUNCATE |

---

## Step Definition Patterns

### Table Steps (Colon Required)

```python
# CRITICAL: Include colon when step has a Gherkin table
@given('the following records:')  # ← colon required
def step_insert_records(context):
    for row in context.table:
        repo.insert(name=row['name'], value=row['value'])
```

### Parameterized Steps

```python
@then('{count:d} records should exist')
def step_verify_count(context, count):
    results = repo.find_by(created_by=context.test_marker)
    assert len(results) == count, f"Expected {count}, found {len(results)}"
```

---

## Data Cleanup Strategy

**Use `created_by` marker for test isolation, not TRUNCATE:**

```python
@given('clean test data')
def step_cleanup(context):
    db = context.db
    schema = context.schema
    markers = ['bdd_test', 'behave_test']
    for marker in markers:
        db.execute(f"DELETE FROM {schema}.entities WHERE created_by = %s", (marker,))
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Undefined step with table | Add colon to step pattern: `@given('step:')` |
| Tests pollute each other | Use `created_by` marker, clean before tests |
| `Background` with cumulative state | Only clean in first scenario if data builds up |
| Step verifies context not DB | Always re-query database in Then steps |
| Missing `--tags` filter | Use tags for focused debugging |
