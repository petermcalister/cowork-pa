---
name: debug-skill
description: Use when debugging test failures, iterating over behave/pytest cycles, or when user says "run tests", "debug", "fix failing tests", or "validate"
---

# Debug Skill - Test Iteration Workflow

## Overview

Debug by iterating through test-fix cycles on isolated test swimlanes. Run tests, analyze failures, fix one bug at a time, re-test, and keep the user informed of progress.

**Core principle:** Fix bugs in isolation using tag filtering. Only run pytest/format checks after behave tests pass.

## When to Use

- User says "run tests", "debug", "validate", "fix tests"
- After making code changes that need verification
- When test failures need systematic resolution
- Debugging across multiple failing scenarios

---

## Tool Priority Hierarchy

**Always use tools in this order:**

```
┌─────────────────────────────────────────────────────────────┐
│  1. MCP TOOLS (if available)                                │
│     - Preferred for test execution and log analysis         │
│     - Provides structured output, background execution      │
│     - Check project for MCP server configuration            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  2. POETRY SHORTCUTS                                        │
│     - poetry run behave --tags=@tag                         │
│     - poetry run pytest tests/                              │
│     - Structured, repeatable commands                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  3. AD-HOC PYTHON                                           │
│     - Direct python -c "..." for quick checks               │
│     - Only when tools/poetry don't fit                      │
│     - Document what you're testing                          │
└─────────────────────────────────────────────────────────────┘
```

**Why this order:**
- MCP tools provide structured JSON output, background execution, log capture
- Poetry commands are project-configured with correct paths
- Ad-hoc is last resort - harder to repeat, no logging

---

## Test Isolation by Tag Swimlane

**Run tests in isolated swimlanes to focus debugging:**

```
┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐
│ @migration │  │ @storage   │  │ @search    │  │ @extract   │
│            │  │            │  │            │  │            │
│ Schema     │  │ Repository │  │ Vector/BM25│  │ File/API   │
│ changes    │  │ CRUD ops   │  │ queries    │  │ parsing    │
└────────────┘  └────────────┘  └────────────┘  └────────────┘
      ↓               ↓               ↓               ↓
   Fix bugs        Fix bugs        Fix bugs        Fix bugs
   in this         in this         in this         in this
   swimlane        swimlane        swimlane        swimlane
   ONLY            ONLY            ONLY            ONLY
```

**Benefits:**
- Faster feedback (don't wait for unrelated tests)
- Clear scope (know which code is under test)
- Prevents cross-contamination of fixes

---

## The Debug Iteration Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                    DEBUG ITERATION CYCLE                    │
└─────────────────────────────────────────────────────────────┘

     ┌──────────────────────────────────────────────────┐
     │  1. RUN TESTS (on isolated tag swimlane)         │
     │     - Use MCP tool or poetry command             │
     │     - Filter by relevant tag                     │
     └──────────────────────────────────────────────────┘
                              ↓
     ┌──────────────────────────────────────────────────┐
     │  2. ANALYZE FAILURES                             │
     │     - Use log analyzer to find errors            │
     │     - Identify FIRST failure (fix one at a time) │
     │     - Note the scenario/test name                │
     └──────────────────────────────────────────────────┘
                              ↓
     ┌──────────────────────────────────────────────────┐
     │  3. INFORM USER                                  │
     │     "Working on: [scenario name]"                │
     │     "Error: [brief description]"                 │
     │     "Fix: [what you're changing]"                │
     └──────────────────────────────────────────────────┘
                              ↓
     ┌──────────────────────────────────────────────────┐
     │  4. FIX THE BUG                                  │
     │     - Make minimal change                        │
     │     - One fix at a time                          │
     └──────────────────────────────────────────────────┘
                              ↓
     ┌──────────────────────────────────────────────────┐
     │  5. RE-TEST (same tag swimlane)                  │
     │     - Verify fix worked                          │
     │     - Check for new failures                     │
     └──────────────────────────────────────────────────┘
                              ↓
              ┌─────────────────────────┐
              │  More failures?         │
              └─────────────────────────┘
                    │           │
                   YES          NO
                    │           │
                    ↓           ↓
              Loop back    Move to next
              to step 2    swimlane or
                           finish
```

---

## User Communication Pattern

**Keep user informed at each stage:**

```python
# Starting a swimlane
"Running @storage tests to verify repository changes..."

# Found failures
"Found 3 failing scenarios. Starting with first failure."

# Working on specific bug
"Working on: 'Insert record via Repository'
 Error: column 'metadata' does not exist
 Fix: Updating column name to 'item_metadata'"

# After fix
"Fix applied. Re-running @storage tests..."

# Swimlane complete
"@storage tests passing (5/5). Moving to @search swimlane..."

# All done
"All behave tests passing. Running pytest and format checks..."
```

**Why this matters:**
- User knows what's happening without asking
- Can interrupt if fix approach is wrong
- Tracks progress through complex debugging

---

## Test Execution Order

**Behave first, pytest/format last:**

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: BEHAVE (BDD Integration Tests)                    │
│                                                             │
│  Run each tag swimlane until all pass:                      │
│  @migration → @storage → @search → @extract → @integration │
└─────────────────────────────────────────────────────────────┘
                              ↓
                     All behave passing?
                              ↓
                             YES
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: PYTEST (Unit Tests)                               │
│                                                             │
│  Run after behave passes to catch unit-level issues         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 3: FORMAT/LINT                                       │
│                                                             │
│  Run formatting checks last (ruff, black, etc.)             │
└─────────────────────────────────────────────────────────────┘
```

**Why this order:**
- Behave tests exercise real integration paths
- Fix integration issues before worrying about unit tests
- Format/lint last - don't waste time formatting broken code

---

## Common Log Patterns

**Patterns to search for when analyzing failures:**

| Pattern | Meaning | Likely Fix |
|---------|---------|------------|
| `column "X" does not exist` | Schema/query mismatch | Check actual column name in DB |
| `undefined step` | Step pattern doesn't match | Check for missing colon with tables |
| `AssertionError: Expected X, got Y` | Logic error | Trace the data flow |
| `ImportError: No module named` | Path/import issue | Check sys.path, module location |
| `ValidationError` | Pydantic type mismatch | Match DTO types to DB returns |
| `UNIQUE constraint` | Duplicate key | Check test data cleanup |
| `connection refused` | DB not running | Start infrastructure |
| `relation "X.Y" does not exist` | Missing table in schema | Run migrations for that schema |

---

## Quick Reference

| Situation | Action |
|-----------|--------|
| User says "run tests" | Run behave on relevant tag swimlane |
| Multiple failures | Fix FIRST failure, re-test, repeat |
| Behave passing | Run pytest, then format checks |
| Unknown error | Search logs for pattern, add context |
| Stuck on bug | Inform user, ask for guidance |

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Run ALL tests at once | Use tag isolation |
| Fix multiple bugs before re-testing | One fix, one test cycle |
| Skip user updates | Inform at each stage |
| Run pytest before behave passes | Behave first, pytest after |
| Use ad-hoc python first | MCP tools → Poetry → Ad-hoc |
| Stay silent during debugging | Regular progress updates |
