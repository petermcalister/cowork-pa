---
name: planning-projects
description: Use when starting multi-feature implementations, complex refactoring, or any task requiring more than 3 sequential steps before the first commit
---

# Planning Projects

## Overview

Create feature-based implementation plans with interleaved testing. Each feature has a JSON definition with `passes: false` that flips to `true` when verified.

**Core principle:** Never build more than one phase without testing and committing.

## When to Use

- Starting new feature implementation
- Multi-file refactoring
- Any task where scope is unclear upfront
- When you'd naturally say "let me think about how to approach this"

**Don't use for:** Single-file fixes, typos, obvious bugs

## Plan File Location

**CRITICAL:** Always store plan files in the **workspace** `.claude/plans/` directory, NOT the user's home directory.

| Location | Path | Status |
|----------|------|--------|
| **Correct** | `{workspace}/.claude/plans/{plan-name}.md` | ✅ Use this |
| **Wrong** | `C:\Users\{user}\.claude\plans\...` | ❌ Never use |

This ensures plans are:
- Version controlled with the project
- Available to other developers
- Persisted across machines
- Discoverable in the codebase

## Context Loading

Before starting, check for relevant instruction files in `.claude/rules/` and `.claude/skills/` that match the plan's domain.

## Core Pattern

### Feature JSON Structure

```json
{
  "id": "F001",
  "category": "functional",
  "description": "User can do X",
  "acceptance_criteria": "Observable outcome Y",
  "steps": ["Setup", "Execute", "Verify", "Check side effects"],
  "test_approach": "behave|pytest|integration",
  "dependencies": ["F000"],
  "passes": false
}
```

### Phase Design

1. **Build** → 3-8 features per phase
2. **Test** → Run specified test approach
3. **Commit** → `"Phase N: {name} - Features X-Y ✅"`
4. **Update** → Flip `passes: false` → `true`

## Quick Reference

| Phase Type | Build | Test | Commit Pattern |
|------------|-------|------|----------------|
| Data models | Entity/model classes | pytest unit | `Phase 1: Models` |
| Core logic | Business logic | pytest + integration | `Phase 2: Core` |
| API/Interface | Endpoints or UI | behave/integration | `Phase 3: Interface` |
| Integration | End-to-end wiring | e2e tests | `Phase 4: Integration` |

## Progress File

Maintain `progress.json` at project root:

```json
{
  "current_phase": 3,
  "completed_features": ["F001", "F002", "F003"],
  "next_feature": "F004",
  "blockers": [],
  "last_clean_commit": "abc123"
}
```

## Session Boundaries

**Clean state criteria before ending session:**

- All current phase tests pass
- Changes committed
- `progress.json` updated
- No uncommitted work

**Starting a session:**

1. Read `progress.json`
2. Verify `last_clean_commit` matches HEAD
3. Continue from `next_feature`

## Pre-Implementation Verification Checklist

Before finalizing any plan, verify these areas are addressed:

### Test Isolation

| Question | Why It Matters |
|----------|----------------|
| How will tests filter data from previous runs? | Old data without new fields causes false failures |
| What identifier links test data to the current run? | e.g., `run_id`, `created_by`, `created_at` |
| Do step definitions query ALL records or filtered records? | Querying all records includes stale data |

**Pattern:** Filter by run identifier in verification steps:
```python
# Filter findings by current analysis run, not all historical findings
current_run_id = context.analysis_result.get('run_id')
for evidence in evidence_list:
    if str(evidence.get('analysis_run_id')) != str(current_run_id):
        continue  # Skip findings from previous runs
```

### Existing Data Impact

| Question | Action Required |
|----------|-----------------|
| What if database has records without new fields? | Plan migration + handle NULL values |
| Will new constraints break existing data? | Test migration on copy of prod data |
| Do old records need backfilling? | Add migration step or mark as N/A |

### Test Step Dependencies

Document what context/state each test step requires:

```markdown
## Step Dependencies
| Step | Requires in Context |
|------|---------------------|
| `Then each finding has explanation` | `context.analysis_result['run_id']` |
| `Then findings are persisted` | `context.thread_emails` list |
```

### UI Impact Analysis

| Check | Details |
|-------|---------|
| Components affected | List specific files/components that need changes |
| Layout constraints | Sidebar width, column counts, mobile responsiveness |
| Existing elements | What currently renders that might disappear or break? |
| Verification method | Manual check, screenshot diff, Playwright test |

### Explicit Acceptance Criteria

**Don't write:** "All tests pass"

**Do write:**
```markdown
## Acceptance Criteria
- [ ] `@explanation` scenario passes: "Output includes explanation field"
- [ ] `@confidence` scenario passes: "Low-confidence results are filtered"
- [ ] UI displays results correctly
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Batching tests at end | Test after each phase, never skip |
| Too many features per phase | Keep 3-8, smaller = faster feedback |
| Missing dependencies | Map dependencies before sequencing |
| No progress file | Create immediately, update after each commit |
| Committing broken state | Run tests before every commit |
| Testing all data instead of current run | Filter by run_id or created_by |
| Vague acceptance criteria | Name specific scenarios and UI elements |
| Ignoring existing data state | Plan for NULL handling and backfill |

## Confidence Check

Before implementing, ask:

1. Are feature boundaries clear?
2. Are dependencies mapped?
3. Is test approach specified per phase?

If confidence < 90%, ask 2-3 clarifying questions.

