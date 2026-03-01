---
name: behave-test-writer
description: Use when writing BDD tests with Python Behave framework - step definitions, feature files, Gherkin syntax, handling tables, and debugging test failures
---

# Behave Test Writer

## Overview

Write BDD tests that exercise real code paths, not test framework mechanics. Tests should verify business logic through actual repository and service classes, with test data visible in Gherkin tables.

**Core principle:** If your test passes without calling production code, it's testing the wrong thing.

## When to Use

- Writing new feature files or step definitions
- Debugging "undefined step" errors
- Tests pass but don't verify actual persistence
- Converting unit tests to integration/BDD tests
- Test data is hidden in step definitions

## When NOT to Use Behave

**Move these to pytest instead:**

| Test Type | Example | Why Pytest |
|-----------|---------|------------|
| Entity CRUD | "Insert and retrieve record" | No workflow, just ORM verification |
| API smoke tests | "API returns 200" | Connectivity check, not business logic |
| Method return types | "Returns DTO" | Unit/integration test concern |
| Parameterized edge cases | "Score boundaries" | `@pytest.mark.parametrize` is cleaner |

**Rule of thumb:** If your Then step just verifies what the When step set, it's a pytest candidate.

```gherkin
# BAD for Behave - This tests nothing meaningful
Scenario: Task entity creates task record
  Given I have a valid task payload
  When I create a Task record
  Then a Task record exists with status "pending"
  # ^^ Just echoes what the When step did
```

```python
# GOOD for pytest - Concise, parameterized
@pytest.mark.integration
@pytest.mark.parametrize("status", ["pending", "running", "completed", "failed"])
def test_update_status(db, schema, sample_id, status):
    success = Task.update_status(db=db, task_id=sample_id, status=status)
    assert success
    task = Task.get_by_id(db=db, task_id=sample_id)
    assert task['status'] == status
```

---

## Real LLM Testing Pattern

**Prefer real LLM calls over mocks for end-to-end validation:**

**Setup in environment.py:**

```python
def before_all(context):
    # LLM rate limiting: 1 real LLM call per test run
    context.llm_calls_remaining = 1
    context.llm_calls_made = 0
```

**Step definition:**

```python
@given('the LLM rate limit has not been exceeded')
def step_check_llm_rate_limit(context):
    remaining = getattr(context, 'llm_calls_remaining', 0)
    if remaining <= 0:
        context.scenario.skip("LLM rate limit exceeded for this test run")
        return
    print(f"LLM rate limit OK: {remaining} call(s) remaining")

@when('I run the analysis pipeline')
def step_run_analysis(context):
    # Decrement rate limit on real LLM call
    context.llm_calls_remaining -= 1
    context.llm_calls_made += 1

    analyzer = Analyzer(schema=context.schema)
    result = analyzer.run(data_id=context.selected_data_id)
    context.analysis_result = result
```

**Feature file:**

```gherkin
@analysis @llm
Scenario: Analyzer processes data end-to-end with real LLM
  Given I have at least 3 records in the database
  And the LLM rate limit has not been exceeded
  When I run the analysis pipeline
  Then the analysis result status is "completed"
  And the analysis created output records
```

**Benefits:**

- Tests actual prompt/response contract
- No fixture staleness
- Catches API changes early

**Cost control:**

- 1 call per test run (~$0.02-0.05 for Claude Opus)
- Consolidate scenarios that need LLM into single comprehensive test
- Use `@skip` tag for expensive scenarios during development

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Raw SQL in steps | Bypasses business logic | Use Repository classes |
| Context variable checking | No real verification | Query via Repository in Then steps |
| Hidden test data | Hard to understand tests | Use Gherkin tables |
| Skipping layers | Incomplete coverage | Test Extract, Core, Entity layers |
| Manual assertions | Tests framework, not code | Use actual business classes |

---

## Gherkin Table Syntax (Critical)

**Step patterns must include colon when tables follow:**

```python
# WRONG - step won't match
@given('the following emails via EmailRepository')
def step_emails(context):
    for row in context.table:
        ...

# CORRECT - colon required for table steps
@given('the following emails via EmailRepository:')
def step_emails(context):
    for row in context.table:
        ...
```

**Why this matters:** Behave includes the colon in pattern matching when a step has a table. Without the colon, the step is "undefined" even though it looks correct.

**Debugging undefined steps:**

```bash
# Dry run shows which steps are undefined
behave --dry-run

# Look for steps with tables that are missing colons
```

---

## Test Data Isolation

**Use a marker column for test data isolation:**

```python
# Step definition inserts with marker
repo.insert_record(
    name=row['name'],
    value=row['value'],
    created_by='bdd_test'  # Marker for isolation
)

# Verification queries filter by marker
results = repo.find_by_name(name, created_by='bdd_test')
assert len(results) == expected_count
```

**Why this matters:**

- Production data uses values derived from enums
- Test data uses `created_by='bdd_test'`
- Queries in Then steps filter by marker
- No accidental pollution between test and production

---

## DTO Field Types Must Match Database

**Common error:** Pydantic validation fails because DTO field type doesn't match what the database returns.

```python
# Database returns: ['user1@example.com', 'user2@example.com']
# If DTO has:
recipients: Optional[str] = None  # WRONG - expects string

# Validation error: expects str, got list
# Fix:
recipients: Optional[List[str]] = None  # Matches database array type
```

**Debugging pattern:**

```python
# When you see validation errors like:
# "value is not a valid str" or "expected str, got list"

# Check the database column type
# PostgreSQL TEXT[] returns Python List[str]
# DTO must use List[str] not str
```

---

## Repository Method Verification

**Then steps must verify via business logic, not context variables:**

```python
# WRONG - just checks variable set by When step
@then('{count:d} records should be inserted')
def step_verify(context, count):
    assert context.inserted_count == count  # Proves nothing

# CORRECT - actually queries through repository
@then('{count:d} records should be retrievable')
def step_verify(context, count):
    repo = Repository(schema=context.schema)
    found = repo.find_by_created_by('bdd_test')
    assert len(found) == count, f"Expected {count}, found {len(found)}"
```

---

## Column Name Accuracy

**Query column names must match actual schema:**

```sql
-- Schema defines:
CREATE TABLE items (
    item_metadata JSONB,  -- NOT "metadata"
    ...
);
```

```python
# WRONG - column name mismatch
query = "SELECT id, metadata FROM items"  # Error: column does not exist

# CORRECT - matches schema exactly
query = "SELECT id, item_metadata FROM items"
```

**Debugging:** When you see `column "X" does not exist`:

```bash
# Inspect actual table structure
docker exec postgres psql -U postgres -d dbname -c "\d schema.tablename"
```

---

## Gherkin Table Best Practices

**Data visible in feature file:**

```gherkin
Scenario: Record retrieval by owner
    Given the following records via Repository:
        | name            | category             | created_date |
        | Task Alpha      | planning             | 2025-01-10   |
        | Task Beta       | execution            | 2025-02-05   |
    When I retrieve records for category "planning"
    Then I should find 1 record
```

**Step handles table iteration:**

```python
@given('the following records via Repository:')
def step_insert_records(context):
    repo = Repository(schema=context.schema)
    for row in context.table:
        repo.insert_record(
            id=f"test-{uuid.uuid4()}",
            name=row['name'],
            category=row['category'],
            created_date=parse_date(row['created_date']),
            created_by='bdd_test'
        )
```

---

## Data Cleanup Strategy (CRITICAL)

**Choose the right cleanup pattern based on scenario dependencies.**

### ⚠️ WARNING: Background Runs Before EVERY Scenario

**NEVER put cleanup in Background if your scenarios build cumulative state.**

Background runs before **every single scenario** in the feature file. If Scenario 2 depends on data from Scenario 1, putting cleanup in Background will wipe that data before Scenario 2 runs.

### Pattern 1: Cumulative State (Scenarios Depend on Each Other)

**Use cleanup in FIRST SCENARIO ONLY when subsequent scenarios query previous data.**

```gherkin
# ✅ CORRECT - Cleanup only in first scenario
@dataImport
Feature: Data Import Integration
  # IMPORTANT: Scenarios run in order and build cumulative state.
  # DO NOT add "clean test data" to Background - it would run before EVERY scenario.

  @setup
  Scenario: Clean and import records from source file
    Given clean test data            # Only runs once, at the start
    And the database is accessible
    And I extract records from "data/test_sample.json"
    When I import the data into the database
    Then at least 100 records should be in the database

  @parsing
  Scenario: Verify parsing created expected records
    Given the database is accessible  # No cleanup - uses data from Scenario 1
    When I query records that were parsed from source
    Then at least 50 records should have is_parsed set to True

  @deduplication
  Scenario: Verify content hash uniqueness
    Given the database is accessible  # Still using data from Scenario 1
    When I query records grouped by content_hash
    Then no content_hash should appear more than once
```

```
┌─────────────────────────────────────────────────────────────────────┐
│  Cumulative State Flow                                              │
│                                                                     │
│  Scenario 1: Setup        Scenario 2: Verify      Scenario 3: More  │
│  ┌─────────────────┐      ┌─────────────────┐     ┌───────────────┐ │
│  │ Clean + Import  │  →   │ Query imported  │  →  │ Query again   │ │
│  │ 100+ emails     │      │ data            │     │ same data     │ │
│  └─────────────────┘      └─────────────────┘     └───────────────┘ │
│                                                                     │
│  Data persists across scenarios, cleaned up at NEXT test run start  │
└─────────────────────────────────────────────────────────────────────┘
```

### Pattern 2: Independent Scenarios (Each Scenario Standalone)

**Use Background with cleanup when scenarios are completely independent.**

```gherkin
# ✅ OK - Background for independent scenarios
Feature: Email Validation Rules

Background:
  Given clean test data
  And the database is accessible

Scenario: Reject email without sender
  When I try to insert an email without sender
  Then validation should fail with "sender required"

Scenario: Reject email without message_id
  When I try to insert an email without message_id
  Then validation should fail with "message_id required"
```

### Step Implementation

```python
@given('clean test data')
def step_cleanup_before_test(context):
    """
    Delete test data using entity methods filtered by created_by.
    CASCADE handles child records.
    """
    db = DatabaseManager(connection_type='admin')
    test_schema = context.schema

    # Test creator identifiers used by BDD tests
    test_creators = ['bdd_test', 'behave-test', 'behave_test']

    for creator in test_creators:
        Entity.delete_by_created_by(db=db, created_by=creator, schema=test_schema)
```

### Decision Matrix

| Scenario Type | Cleanup Location | Why |
|---------------|------------------|-----|
| Cumulative state | First scenario only | Subsequent scenarios depend on prior data |
| Independent tests | Background | Each scenario needs fresh state |
| Mixed feature | Split into separate features | Don't mix patterns in one file |

### Anti-Pattern: Background with Cumulative State

```gherkin
# ❌ WRONG - This WILL fail
Background:
  Given clean test data    # Runs before Scenario 2, 3, 4... wiping data!

Scenario: Import emails
  When I import 100 emails
  Then 100 emails exist

Scenario: Query imported emails    # FAILS - cleanup ran, no data!
  When I query by sender
  Then I find results              # AssertionError: 0 results
```

### Benefits of This Approach

- **Debug failed tests** - Data persists after test run for DBeaver/pgAdmin inspection
- **Cumulative verification** - Scenarios can verify data from earlier scenarios
- **Clear data flow** - Comment in feature file explains the pattern
- **Isolation via created_by** - Uses marker column, not TRUNCATE

---

## Test Isolation via Tags

**Organize tests by functional area for targeted execution:**

| Tag Category | Purpose | Example Scenarios |
|--------------|---------|-------------------|
| `@migration` | Schema changes, version tracking | Create tables, add columns, run migrations |
| `@data_storage` | CRUD operations, persistence | Insert email, find by sender, update record |
| `@search` | Query operations, vector search | Semantic search, BM25 search, hybrid ranking |
| `@extraction` | Data parsing, file reading | File parsing, data import |
| `@integration` | End-to-end workflows | Full pipeline from file to searchable data |

**Feature file tagging:**

```gherkin
@database @migration
Feature: Database Schema Management

    @destructive
    Scenario: Full schema reset
        # WARNING: Drops all tables

    @safe
    Scenario: Add new column
        # Non-destructive migration

@database @data_storage
Feature: Email Repository Operations

    Scenario: Insert and retrieve email
    Scenario: Find emails by sender

@search @vectorData
Feature: Semantic Search

    Scenario: Find similar emails by embedding
```

**Running by tag:**

```bash
# Run only storage tests (fast feedback)
behave --tags=@data_storage

# Run everything except destructive migrations
behave --tags="not @destructive"

# Run search OR extraction tests
behave --tags="@search or @extraction"

# Run integration tests that use search
behave --tags="@integration and @search"
```

**Tag hierarchy benefits:**

- Fast iteration: run `@data_storage` while developing repository code
- Safe CI: exclude `@destructive` from automated runs
- Focused debugging: run only `@search` when investigating search bugs
- Infrastructure isolation: `@migration` tests can run separately

---

## Quick Reference

| Situation | Solution |
|-----------|----------|
| Step undefined despite matching text | Add colon for table steps: `@given('step:')` |
| Data not found in Then step | Add `created_by='bdd_test'` marker to insert and query |
| Pydantic validation error | Match DTO field type to database return type |
| Column does not exist | Check actual column name in schema |
| Test passes but nothing verified | Query via Repository, not context variable |

---

## Common Mistakes

1. **Forgetting colon in table steps** - Behave treats `Given X` and `Given X:` as different patterns

2. **Testing context instead of database** - Then steps that only check `context.result` don't verify persistence

3. **Hardcoded schema** - Use environment config for schema name, not a hardcoded string

4. **Insert without marker** - Data inserted without `created_by` marker can't be isolated

5. **DTO type mismatch** - Database arrays return as `List[str]`, not `str`
