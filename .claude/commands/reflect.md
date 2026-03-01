---
description: user wants to distill and preserve learnings from the past session
---

# Session Reflection Skill

## Overview

Analyze the current conversation to identify friction points, repeated corrections, and learnings that should be codified into project instructions. Propose targeted updates to the appropriate instruction files, avoiding duplication.

## Process

### Step 1: Analyze Conversation History

Review the conversation for these signals:

| Signal Type | What to Look For |
|-------------|------------------|
| **Repeated corrections** | User corrected the same type of mistake 2+ times |
| **Explicit feedback** | User said "always do X" or "never do Y" |
| **Friction patterns** | Steps that required multiple attempts |
| **Workarounds discovered** | Solutions to recurring problems |
| **Clarifications needed** | Ambiguities that caused confusion |

### Step 2: Categorize Each Learning

For each identified learning, determine where it belongs:

```
Is this principle-based and reusable across projects?
├── YES → Is there an existing skill it fits in?
│   ├── YES → Propose UPDATE to .claude/skills/{skill}/SKILL.md
│   └── NO → Propose NEW skill (rare - only if truly reusable)
└── NO → Is this specific to THIS project?
    ├── YES → Does it relate to a specific path pattern?
    │   ├── YES → Propose .claude/rules/{topic}.md
    │   └── NO → Propose CLAUDE.md update
    └── NO → Ask user for clarification
```

### Step 3: Check for Overlaps

Before proposing changes, search existing instruction files:

1. **Read relevant files** - Load files that might already cover this topic
2. **Check for duplicates** - Don't propose what already exists
3. **Check for conflicts** - Flag if new learning contradicts existing instruction
4. **Identify merge candidates** - Sometimes learning extends existing content

### Step 4: Present Proposed Changes

Format each proposal clearly:

```markdown
## Proposed Change {N}

**Type:** [New Rule | Update Existing | New Skill Section]
**Target:** {file path}
**Reason:** {what friction/learning this addresses}

**Overlap Check:**
- Searched: {files checked}
- Existing related content: {none | brief quote}
- Recommendation: {add new | merge with existing | skip - already covered}

**Proposed Content:**
> {the actual text to add, in imperative tone}

**Approve this change?** [Waiting for user response]
```

### Step 5: Apply Approved Changes

**CRITICAL:** Do NOT edit any file until user explicitly approves.

For each approved change:
1. Read the target file
2. Make the specific edit
3. Show the user what was changed
4. Wait for confirmation before next change

## Content Guidelines

**Imperative tone:** Write instructions as commands
- "Use `get_logger(__name__)` for all logging"
- "When querying emails, always filter by `created_by` for test isolation"

**Specific over general:**
- "Use `email_metadata` not `metadata` for the column name"
- NOT "Be careful with column names"

**One rule per bullet:** Each learning = one clear instruction

## What NOT to Codify

- One-off mistakes unlikely to recur
- Personal preferences without technical basis
- Learnings already well-documented in existing files
- Temporary workarounds for bugs being fixed

## Example Output

```
Analyzed conversation: 47 messages

Found 3 learnings to codify:

---
## Proposed Change 1

**Type:** Update Existing
**Target:** .claude/rules/streamlit.md
**Reason:** User corrected form handler placement 2x

**Overlap Check:**
- Searched: streamlit.md, CLAUDE.md
- Existing: "Wrap input + button in st.form()"
- Recommendation: Extend existing section

**Proposed Content:**
> **IMPORTANT:** Place `if submitted:` handler OUTSIDE the `with st.form():` block. Handlers inside the form context may fail silently.

**Approve this change?**
---
```

## Quick Reference

| Friction Type | Likely Target |
|---------------|---------------|
| General project pattern | CLAUDE.md |
| Path-specific convention | .claude/rules/{topic}.md |
| Reusable across projects | .claude/skills/{appropriate-skill}/ |
