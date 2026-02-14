---
description: Check upcoming birthdays and personal events
allowed-tools: Read, Task, mcp__Claude_in_Chrome__*
argument-hint: [days-ahead]
---

Check Pete's Google Calendar for upcoming birthdays, anniversaries, and personal events.

**Scope**: Look ahead $1 days (default: 30 if not specified).

**Process**:

1. Launch the **gcal-scanner** agent: `${CLAUDE_PLUGIN_ROOT}/agents/gcal-scanner.md`
2. From the agent's results, filter for birthdays, anniversaries, and recurring personal events
3. Sort results by date (soonest first) and present with action suggestions:
   - Within 1 day: "TODAY! Don't forget to call/message"
   - Within 3 days: "Coming up soon — time to get a gift/card?"
   - Within 7 days: "This week — start planning"
   - Beyond 7 days: "On the horizon"

If no events found, suggest Pete add family birthdays to his calendar and offer to help.
