---
paths: "**/tests/**/*.py, **/test_*.py"
---

# Pytest Integration Testing Patterns

**Purpose:** Conventions for writing pytest integration tests with database fixtures, test isolation, and common patterns.

---

## Test File Organization

```
tests/
├── conftest.py              # Shared fixtures (db, schema, cleanup)
├── test_entity_name.py      # Entity-level tests
├── test_repository_name.py  # Repository integration tests
├── fixtures/                # Test data files
│   └── sample_data.json
└── integration/             # End-to-end integration tests
    └── test_pipeline.py
```

---

## Core Fixtures

```python
# conftest.py
import pytest

@pytest.fixture(scope="session")
def db():
    """Database connection for the test session."""
    manager = DatabaseManager(connection_type="test")
    yield manager
    manager.close()

@pytest.fixture(scope="session")
def schema():
    """Test schema name."""
    return "test"

@pytest.fixture(autouse=True)
def cleanup(db, schema):
    """Clean test data before each test."""
    yield
    db.execute(f"DELETE FROM {schema}.entities WHERE created_by = 'pytest'")
```

---

## Test Isolation

**Always mark test data with a creator identifier:**

```python
def test_insert_and_retrieve(db, schema):
    repo = EntityRepository(db, schema=schema)

    # Insert with test marker
    entity = EntityData(name="Test Entity", created_by="pytest")
    repo.insert(entity)

    # Query filtered by marker
    results = repo.find_by(created_by="pytest")
    assert len(results) == 1
    assert results[0].name == "Test Entity"
```

---

## Parametrized Tests

```python
@pytest.mark.parametrize("status,expected_count", [
    ("active", 2),
    ("inactive", 1),
    ("archived", 0),
])
def test_find_by_status(db, schema, status, expected_count):
    repo = EntityRepository(db, schema=schema)
    results = repo.find_by(status=status, created_by="pytest")
    assert len(results) == expected_count
```

---

## Test Markers

```python
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
markers = [
    "integration: marks tests that need database access",
    "slow: marks tests that take > 10 seconds",
    "destructive: marks tests that modify schema",
]
```

```bash
# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# Run specific test file
pytest tests/test_entity.py -v
```

---

## Common Patterns

### Assert Data Persisted

```python
def test_data_persists(db, schema):
    repo = EntityRepository(db, schema=schema)
    entity_id = repo.insert(EntityData(name="Persist Test", created_by="pytest"))

    # Re-fetch from DB to verify persistence
    result = repo.get_by_id(entity_id)
    assert result is not None
    assert result.name == "Persist Test"
```

### Assert Cascade Deletes

```python
def test_cascade_delete(db, schema):
    parent_id = parent_repo.insert(parent_data)
    child_repo.insert(ChildData(parent_id=parent_id, created_by="pytest"))

    parent_repo.delete(parent_id)

    children = child_repo.find_by(parent_id=parent_id)
    assert len(children) == 0
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Tests pollute each other | Use `created_by` marker and cleanup fixture |
| Fixture scope too narrow | Use `session` scope for DB, `function` for data |
| Missing `conftest.py` | Create at `tests/` root with shared fixtures |
| Hardcoded test schema | Use fixture, never hardcode schema name |
| Testing context not DB | Always re-fetch from database to verify |
