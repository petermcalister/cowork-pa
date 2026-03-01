# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Superpowers is a software development workflow system for AI coding agents (Claude Code, Codex, OpenCode). It provides composable "skills" — structured workflow documents that agents load and follow automatically. Skills enforce practices like TDD, systematic debugging, and code review throughout the development process.

**Author:** Jesse Vincent | **License:** MIT | **Repo:** https://github.com/obra/superpowers

## Architecture

### Skill System

The core unit is a **skill** — a `SKILL.md` file with YAML frontmatter (`name` and `description` fields only) containing workflow instructions, flowcharts (DOT/GraphViz), and decision trees that agents follow as mandatory processes.

**Skill loading flow:**
1. `hooks/hooks.json` defines a SessionStart hook that runs `hooks/session-start.sh`
2. The hook injects the `using-superpowers` skill content at session start
3. `using-superpowers` teaches the agent to check for applicable skills before any action
4. `lib/skills-core.js` handles discovery — finds `SKILL.md` files, extracts frontmatter, resolves paths with shadowing (personal skills override superpowers skills of the same name)

**Skill resolution order:** Personal (`~/.claude/skills/`) → Superpowers (`skills/`). Prefix `superpowers:` to force the superpowers version.

### Directory Layout

- `skills/` — 14 skills organized by concern (testing, debugging, planning, execution, collaboration, meta)
- `lib/skills-core.js` — Node.js ESM module for skill discovery, frontmatter parsing, path resolution, update checking
- `hooks/` — SessionStart hook system (hooks.json + session-start.sh + run-hook.cmd for Windows)
- `commands/` — Slash command definitions (`/brainstorm`, `/write-plan`, `/execute-plan`)
- `agents/` — Agent templates (e.g., code-reviewer)
- `docs/` — Developer documentation, plan examples, platform-specific guides
- `tests/` — Integration tests, skill triggering tests, end-to-end workflow tests
- `.claude-plugin/` — Claude Code plugin metadata
- `.codex/`, `.opencode/` — Platform-specific integration files

### The Core Workflow

Skills chain together: **brainstorming** → **using-git-worktrees** → **writing-plans** → **subagent-driven-development** (or **executing-plans**) → **test-driven-development** (throughout) → **requesting-code-review** (between tasks) → **finishing-a-development-branch**

The **subagent-driven-development** skill uses a two-stage review pattern: spec compliance review first, then code quality review, with review loops if issues are found.

## Testing

Tests run real Claude Code sessions in headless mode and verify behavior by parsing JSONL session transcripts.

### Running Tests

```bash
# Integration test for subagent-driven-development (10-30 min, real Claude execution)
cd tests/claude-code
./test-subagent-driven-development-integration.sh

# Skill triggering validation (verifies skills trigger from naive prompts)
cd tests/skill-triggering
./run-all.sh

# Token usage analysis from any session transcript
python3 tests/claude-code/analyze-token-usage.py ~/.claude/projects/<project-dir>/<session-id>.jsonl
```

### Test Requirements

- Must run from the superpowers plugin directory
- Claude Code CLI available as `claude`
- `"superpowers@superpowers-dev": true` in `~/.claude/settings.json` for local dev
- Test helpers in `tests/claude-code/test-helpers.sh` provide assertions: `contains`, `not_contains`, `count`, `order`, `equals`

### End-to-End Test Projects

- `tests/subagent-driven-dev/go-fractals/` — CLI tool with 10 tasks
- `tests/subagent-driven-dev/svelte-todo/` — CRUD app with 12 tasks

## Key Conventions

### Skill Authoring (CSO — Claude Search Optimization)

- Frontmatter `description` MUST start with "Use when..." and describe only triggering conditions
- NEVER summarize the skill's workflow in the description (Claude will follow the summary instead of reading the full skill)
- Skill names: lowercase with hyphens, verb-first gerunds preferred (`writing-plans` not `plan-writer`)
- Flowcharts in DOT format only for non-obvious decision points, never for linear instructions
- Token budgets: getting-started skills <150 words, frequently-loaded <200 words, others <500 words
- Cross-reference skills by name with `REQUIRED` markers, never use `@` file links (burns context)

### Skill Creation Process

Skills follow TDD: RED (run pressure scenario without skill, document baseline failures) → GREEN (write minimal skill addressing those failures) → REFACTOR (close rationalization loopholes, re-test). See `skills/writing-skills/SKILL.md`.

### Plan File Naming

Plans go in `docs/plans/YYYY-MM-DD-<feature-name>-design.md` or `-plan.md` with exact file paths, not abstract references.
