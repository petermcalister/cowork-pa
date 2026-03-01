---
description: Scan emails for dates and calendar commitments
allowed-tools: Read, WebFetch, mcp__Claude_in_Chrome__*
argument-hint: [days-back]
---

Scan Pete's recent emails for dates, deadlines, and commitments that should be added to his Google Calendar.

Load the calendar-intelligence skill: read `${CLAUDE_PLUGIN_ROOT}/skills/calendar-intelligence/SKILL.md`.
Follow its **Date Extraction from Emails** capability (section 2).

**Scope**: Scan emails from the last $1 days (default: 7 if not specified).

For confirmed dates, follow the skill's **Calendar Event Creation** capability (section 3)
to create events via Chrome browser.
