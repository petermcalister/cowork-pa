---
description: Check upcoming birthdays and personal events
allowed-tools: Read, mcp__Claude_in_Chrome__*
argument-hint: [days-ahead]
---

Check Pete's Google Calendar for upcoming birthdays, anniversaries, and personal events.

Load the calendar-intelligence skill: read `${CLAUDE_PLUGIN_ROOT}/skills/calendar-intelligence/SKILL.md`.
Follow its **Birthday & Event Tracking** capability (section 1).

**Scope**: Look ahead $1 days (default: 30 if not specified).

Present results sorted by date (soonest first) with action suggestions:
- Within 1 day: "TODAY! Don't forget to call/message"
- Within 3 days: "Coming up soon — time to get a gift/card?"
- Within 7 days: "This week — start planning"
- Beyond 7 days: "On the horizon"

If no events found, suggest Pete add family birthdays to his calendar and offer to help.
