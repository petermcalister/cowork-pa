---
description: Run Pete's daily morning briefing
allowed-tools: Read, Grep, Glob, Bash, WebFetch, mcp__Claude_in_Chrome__*
model: sonnet
---

Compile Pete's full morning briefing using the peter-morning-brief-skill.

Load the skill by reading `${CLAUDE_PLUGIN_ROOT}/skills/peter-morning-brief-skill/SKILL.md`.

Follow the skill's Data Collection Workflow — scan each source sequentially via Chrome browser,
compile results into the briefing format, and present directly to Pete.

If any source fails (not signed in, CAPTCHA, page won't load), skip it and note it at the end.
Keep it concise and actionable.
