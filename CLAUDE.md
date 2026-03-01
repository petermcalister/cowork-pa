# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**pete-pa** is a Cowork plugin that serves as Pete's personal assistant. It automates daily productivity workflows by pulling data from Gmail, Outlook, Google Calendar, and the "cowork-pa" WhatsApp channel through browser automation (Claude in Chrome extension) — no API keys or credentials are stored.

## Build & Deploy

```bash
./deploy-plugin.sh [path-to-repo]   # Default: ~/RepoBase/cowork-pa
```

This script pulls latest from `origin/main`, zips the `pete-pa/` directory into `dist/pete-pa.plugin`, and opens it for Cowork installation. On Windows it falls back to PowerShell `Compress-Archive` if `zip` isn't available.

## Architecture

### Plugin Structure

```
pete-pa/                          # Plugin root (packaged as .plugin ZIP)
├── .claude-plugin/plugin.json    # Plugin manifest (name, version, description)
├── hooks/hooks.json              # SessionStart hook — displays context on load
├── references/                   # Shared browser navigation guides
│   ├── browser-gmail-guide.md
│   ├── browser-outlook-guide.md
│   ├── browser-gcal-guide.md
│   ├── browser-whatsapp-guide.md
│   └── date-patterns.md
├── commands/                     # Thin launcher commands (4 slash commands)
│   ├── peter-morning-brief-cmd.md
│   ├── scan-emails.md
│   ├── check-birthdays.md
│   └── summarize-channels.md
└── skills/                       # Workflow skills with browser guide references
    ├── peter-morning-brief-skill/
    │   └── SKILL.md
    └── calendar-intelligence/
        └── SKILL.md
```

### Commands → Skills → References

- **Commands** (`commands/*.md`) are thin launchers with YAML frontmatter (`description`, `allowed-tools`, `model`). They load a skill and set tool permissions for the execution context.
- **Skills** (`skills/*/SKILL.md`) contain the full workflow with YAML frontmatter (`name`, `description`, `version`). They read browser guides from `references/`, navigate each service sequentially via Chrome browser tools, and compile results.
- **References** (`references/`) are shared browser navigation guides and pattern libraries — single source of truth for browser navigation steps.

### Data Flow

```
Command → loads Skill → Skill reads References → navigates browser sequentially → compiles results → presents to Pete
```

### Key Conventions

- Commands use `allowed-tools: Read, Grep, Glob, Bash, WebFetch, mcp__Claude_in_Chrome__*` and `model: sonnet`
- Skills use YAML frontmatter with `name`, `description`, `version` fields
- Browser guides follow a consistent pattern: prerequisites, step-by-step navigation, data extraction format, error handling
- The `${CLAUDE_PLUGIN_ROOT}` variable resolves to the plugin root at runtime
- Date extraction uses confidence scoring (HIGH/MEDIUM/LOW) defined in `references/date-patterns.md`

### Known Limitation: No MCP Tools in Subagents

Plugin agents (launched via the Task tool) **cannot access MCP tools** like `mcp__Claude_in_Chrome__*`. MCP connections only exist in the parent session's execution context. All browser automation must happen directly in the skill/command execution, not in subagents. This is why the plugin uses sequential scanning in skills rather than parallel agents.

## Current State

- **Active version**: 0.4.1
- **WhatsApp**: Focused exclusively on the "cowork-pa" channel (reading articles + posting reports)
- **Telegram**: Removed in v0.3.0
- The `claude-plugins-official/` directory contains the cloned Anthropic official plugins repo (reference material for plugin-builder skill)

## Commands Reference

| Command | Skill Used | Default Args |
|---------|-----------|--------------|
| `/peter-morning-brief-cmd` | peter-morning-brief-skill | — |
| `/scan-emails [days]` | calendar-intelligence | days-back: 7 |
| `/check-birthdays [days]` | calendar-intelligence | days-ahead: 30 |
| `/summarize-channels` | peter-morning-brief-skill | cowork-pa channel |

## Project-Level Skills (`.claude/skills/`)

| Skill | Purpose |
|-------|---------|
| `plugin-builder` | Guides the coding agent through building Cowork/Claude Code plugins. References `pete-pa/` as the living example and `claude-plugins-official/` for official patterns |
| `skill-builder` | Guides the coding agent through writing effective Claude Code skills. Based on Anthropic's official skill-building guide with patterns and troubleshooting |
