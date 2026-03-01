---
description: Create a comprehensive implementation plan with structured artifacts for multi-session work
---

# Super Plan Command

Create a plan in `.claude/plans/{plan-name}.md` with structured artifacts for multi-session work.

---

## Phase 1: Get Your Bearings (REQUIRED)

Before doing anything, orient yourself:

```bash
# 1. Where am I?
pwd

# 2. What happened recently?
git log --oneline -10

# 3. Read progress file (if exists)
cat .claude/plans/claude-progress.txt

# 4. Check for existing plans
ls .claude/plans/*.md
```

**If previous session left bugs:** Fix them BEFORE planning new work.

---

## Phase 2: Clarify Until 90% Confident (REQUIRED)

**Ask clarifying questions until you reach 90% confidence** on:

| Area | Questions to Consider |
|------|----------------------|
| **Requirements** | What exactly should this feature do? What are the acceptance criteria? |
| **Scope** | What's in scope vs out of scope? Are there related features to avoid touching? |
| **Technical Approach** | Which existing patterns should we follow? Any architectural constraints? |
| **Edge Cases** | What happens with empty data? Nulls? Large datasets? Concurrent access? |
| **Dependencies** | What must exist before this can work? What depends on this? |
| **Testing** | How will we verify this works? What test scenarios cover it? |

**Process:**
1. Explore the codebase to understand current state
2. Identify ambiguities or gaps in understanding
3. Use `AskUserQuestion` tool to clarify before writing the plan
4. Only proceed to write the plan when confidence >= 90%

**Do NOT write the plan if:**
- Requirements could be interpreted multiple ways
- You're unsure which existing code to modify
- The scope feels unclear or unbounded
- You're guessing at the user's intent

---

## Phase 3: Create Structured Artifacts

### 3.1 Feature List (JSON) - CRITICAL

Create `.claude/plans/{plan-name}-features.json` with pass/fail tracking:

```json
{
  "plan_name": "{plan-name}",
  "created": "YYYY-MM-DD",
  "features": [
    {
      "id": "F001",
      "description": "Short description of feature",
      "acceptance": "How to verify this is done",
      "passes": false
    }
  ]
}
```

**CRITICAL RULES:**
- Use JSON, not Markdown (harder to accidentally corrupt)
- Only change `passes` field - NEVER remove or edit feature descriptions
- Each feature must be independently testable
- Features should be small enough to complete in one session

### 3.2 Plan File (Markdown)

Create `.claude/plans/{plan-name}.md` using template below.

### 3.3 Progress File

Create/update `.claude/plans/claude-progress.txt`:

```text
=== Session: YYYY-MM-DD HH:MM ===
Plan: {plan-name}
Worked on: F001, F002
Completed: F001
Blocked: None
Next session should: Start with F002, then F003
Environment state: Clean, all tests pass
```

---

## Phase 4: Work Incrementally

### ONE Feature Per Session

**Do NOT attempt multiple features at once.** The harness pattern is:

1. Pick the highest-priority feature with `passes: false`
2. Implement it completely
3. Test it thoroughly
4. Mark `passes: true` only after verification
5. Commit with descriptive message
6. Update progress file
7. If time remains, pick next feature

### Clean State Rule

End every session with:
- [ ] All changes committed to git
- [ ] Tests passing (or documented why not)
- [ ] Progress file updated
- [ ] No half-implemented features

---

## Phase 5: End-of-Session Protocol

Before ending work:

1. Run relevant tests
2. Check `git status`
3. Commit with descriptive message referencing the feature ID
4. Update progress file with session summary
5. Update feature list — change `passes: false` to `passes: true` for completed features

---

## Plan Template

```markdown
# {Feature Name} Plan

## Overview
{Brief description - 1-2 sentences}

## Feature List
See: `.claude/plans/{plan-name}-features.json`

Total features: {N}
Passing: {0}

## Files to Modify
| File | Change |
|------|--------|
| `path/to/file` | Description of change |

## Test Strategy
- **Scenarios:** {list}
- **Verification:** {how to confirm}

## Incremental Order
Work on features in this order:
1. F001 - {description} (blocking)
2. F002 - {description} (depends on F001)
3. F003 - {description} (independent)

## Acceptance Criteria
All features in `{plan-name}-features.json` have `passes: true`
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| Implement entire plan in one session | Runs out of context mid-feature | One feature at a time |
| Skip testing before marking done | Bugs accumulate | Always verify with tests |
| Edit feature descriptions in JSON | Loses requirements | Only change `passes` field |
| Leave uncommitted changes | Next session starts broken | Commit before ending |
| Skip progress file | Next session has no context | Always update progress |

---

## Quick Checklist

### Before Planning
- [ ] Ran `git log` and read progress file
- [ ] Verified project runs
- [ ] Asked clarifying questions (90% confidence)

### Plan Created
- [ ] Feature list JSON created
- [ ] Plan markdown created
- [ ] Features are small, independently testable

### After Each Feature
- [ ] Feature tested and verified
- [ ] `passes: true` in feature JSON
- [ ] Changes committed with descriptive message
- [ ] Progress file updated

### End of Session
- [ ] No uncommitted changes
- [ ] Tests passing
- [ ] Progress file has "Next session should:" guidance
