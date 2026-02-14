---
name: plugin-builder
description: >
  Guides the coding agent through building Claude Code / Cowork plugins.
  Use when Pete asks to "build a plugin", "create a plugin", "add a command",
  "add a skill", "add an agent", "add a hook", or wants to modify or extend
  any plugin structure in this repo.
---

# Plugin Builder

You are building a Claude Code plugin. Follow these instructions to produce
well-structured, working plugins that match the patterns Pete already uses.

## Before You Start

1. Read `pete-pa/` as the reference implementation — it's a working plugin with
   skills, commands, hooks, and browser guides. Match its conventions.
2. If you need to see how official Anthropic plugins solve a specific problem,
   read the relevant plugin from `claude-plugins-official/plugins/`. Key ones:
   - `example-plugin` — minimal skeleton
   - `plugin-dev` — comprehensive (7 skills, 3 agents)
   - `feature-dev` — multi-phase workflow with parallel agents
   - `code-review` — parallel agents with confidence scoring
   - `hookify` — dynamic hook creation

## Plugin Skeleton

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json       # Only this file goes here
├── commands/             # User-invoked slash commands
├── skills/               # Auto-activating knowledge/workflows
│   └── skill-name/
│       └── SKILL.md
├── references/           # Shared guides, patterns, templates
├── agents/               # Autonomous subagents (see MCP limitation below)
├── hooks/
│   └── hooks.json        # Event-driven automation
├── .mcp.json             # External tool connections
└── README.md
```

**Prefer shared `references/`** at the plugin root over per-skill `references/` subdirectories. This avoids duplication when multiple skills need the same guides.

**The one rule you must not break**: nothing goes inside `.claude-plugin/` except `plugin.json`. Commands, skills, agents, hooks — all at the plugin root.

## plugin.json

Only `name` is required. Keep it minimal:

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "One sentence: what this plugin does for the user",
  "author": { "name": "Pete" },
  "keywords": ["relevant", "terms"]
}
```

`name` becomes the namespace — skills appear as `/plugin-name:skill-name`.

## Deciding What to Build

Ask Pete what the plugin should do, then choose components:

| Pete wants... | Build a... |
|--------------|------------|
| A `/slash-command` he types manually | **Command** (`commands/name.md`) |
| Claude to automatically apply knowledge | **Skill** (`skills/name/SKILL.md`) |
| A task to run in isolated context | **Agent** (`agents/name.md`) |
| Something to happen on file save, session start, etc. | **Hook** (`hooks/hooks.json`) |
| Connection to an external API/service | **MCP server** (`.mcp.json`) |

Most plugins only need 1-2 of these. Don't add components "just in case".

## Building Commands

Single `.md` files in `commands/`. Write instructions TO Claude, not to Pete:

```markdown
---
description: Short text shown in /help
allowed-tools: Read, Grep, Glob, Bash
model: sonnet
---

Do the thing Pete asked for. Use $ARGUMENTS as the input.

1. First step
2. Second step
3. Present results to Pete
```

Follow pete-pa's pattern: commands load a skill, then execute steps that reference browser guides or other resources via `${CLAUDE_PLUGIN_ROOT}/skills/...`.

## Building Skills

See the **skill-builder** skill for detailed guidance on writing effective skills. The short version:

- `SKILL.md` must be exactly that name (case-sensitive)
- Folder name in kebab-case
- Description must say WHAT it does AND WHEN to use it, with trigger phrases
- Keep SKILL.md lean — move detail into `references/`
- Write instructions in imperative form ("Check the code", not "You should check the code")

## Building Agents

Agents run in their own context with their own model and tool restrictions:

```markdown
---
name: my-agent
description: >
  Use this agent when [specific scenario]. Proactively use for [task type].
model: haiku
tools: Read, Grep, Glob
---

You are a [role]. When invoked:
1. Do this
2. Then this
3. Return findings to the main conversation
```

Rules of thumb:
- **Read-only exploration** → haiku (fast, cheap)
- **Analysis and design** → sonnet (capable)
- **Only grant tools the agent needs** — read-only agents can't accidentally edit files
- Include "proactively" in the description if Claude should auto-delegate

### CRITICAL: MCP Tools Are Not Available in Agents

Agents run as subprocesses via the Task tool. **MCP tool connections (e.g. `mcp__Claude_in_Chrome__*`, `mcp__slack__*`) only exist in the parent session** — they are NOT passed to subagent execution contexts.

This means:
- Agents **cannot** use browser automation, external API tools, or any MCP-provided tools
- Agents **can** use built-in tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch, etc.
- If a workflow needs MCP tools, it must run directly in the skill/command context, not in an agent

**Example**: A plugin that scans Gmail via Chrome browser tools must do the scanning in the skill itself (sequential), not delegate to a "gmail-scanner" agent (the agent won't have `mcp__Claude_in_Chrome__*`).

Design accordingly: use agents for code analysis, file processing, and built-in tool work. Keep MCP-dependent workflows in skills/commands.

### CRITICAL: Chrome Browser Tools Require Cowork

Claude Code **cannot** connect to the Chrome browser extension directly. The Chrome native host (`chrome-native-host.exe`) only accepts connections from whitelisted Chrome extension origins via Chrome's native messaging API. Cowork works because it communicates through the Chrome extension; Claude Code cannot bypass Chrome's security model.

This means:
- Plugins using `mcp__Claude_in_Chrome__*` tools **must run in Cowork**, not standalone Claude Code
- There is no `.mcp.json` config that makes Chrome tools work in Claude Code on Windows
- If your plugin needs browser automation, it is a Cowork plugin — not a native Claude Code project

## Building Hooks

Event handlers in `hooks/hooks.json`:

```json
{
  "hooks": {
    "EventName": [{
      "matcher": "regex-pattern",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/my-script.sh",
        "timeout": 30
      }]
    }]
  }
}
```

Most useful events:
- **SessionStart** — inject context when plugin loads (pete-pa uses this)
- **PostToolUse** with `Write|Edit` matcher — auto-format or lint after changes
- **PreToolUse** with `Bash` matcher — block dangerous commands
- **Stop** — verify work is complete before Claude finishes

Hook types: `command` (shell script), `prompt` (single LLM call), `agent` (multi-turn with tools).

Exit codes: `0` = allow, `2` = block.

## Variables You Can Use

| Variable | Where | Purpose |
|----------|-------|---------|
| `${CLAUDE_PLUGIN_ROOT}` | Everywhere in plugin | Absolute path to plugin root |
| `$ARGUMENTS` | Skills/Commands | User input after the command name |
| `$0`, `$1`, `$2` | Skills/Commands | Individual arguments by position |

## Testing

```bash
claude --plugin-dir ./my-plugin    # Load without installing
claude --debug                      # See what's loading and why
```

## Packaging (pete-pa pattern)

Pete's deploy script zips the plugin directory into a `.plugin` file:
```bash
./deploy-plugin.sh
```

This produces `dist/plugin-name.plugin` which Cowork can install.

## Common Mistakes

1. **Putting files inside `.claude-plugin/`** — only plugin.json goes there
2. **Writing instructions for Pete instead of Claude** — commands are prompts that Claude executes
3. **Stuffing everything into SKILL.md** — use references/ for detail
4. **Vague skill descriptions** — "Helps with projects" will never trigger; include specific phrases
5. **Granting agents all tools** — restrict to what they actually need
6. **Forgetting `${CLAUDE_PLUGIN_ROOT}`** — hardcoded paths break when the plugin is installed elsewhere
7. **Delegating MCP work to agents** — agents can't access MCP tools; keep browser/API automation in skills
8. **Per-skill references/ directories** — use shared `references/` at plugin root to avoid duplication
9. **Including empty `.mcp.json`** — only add it when you have actual MCP server configs
