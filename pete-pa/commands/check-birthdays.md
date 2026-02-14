---
description: Check upcoming birthdays and personal events
allowed-tools: Read, mcp__Claude_in_Chrome__*
argument-hint: [days-ahead]
---

Check Pete's Google Calendar for upcoming birthdays, anniversaries, and personal events.

Load the calendar-intelligence skill: read `${CLAUDE_PLUGIN_ROOT}/skills/calendar-intelligence/SKILL.md`.

**Scope**: Look ahead $1 days (default: 30 if not specified).

**Process**:

1. Open Chrome and navigate to calendar.google.com.
   Follow `${CLAUDE_PLUGIN_ROOT}/skills/calendar-intelligence/references/browser-gcal-guide.md`.
2. Search the calendar for events in the specified period containing:
   - "birthday", "bday", "b-day"
   - "anniversary"
   - Known family names Pete has mentioned
3. Also check for any recurring annual events.
4. Sort results by date (soonest first).
5. For each event, calculate days until and suggest actions:
   - Within 1 day: "TODAY! Don't forget to call/message"
   - Within 3 days: "Coming up soon — time to get a gift/card?"
   - Within 7 days: "This week — start planning"
   - Beyond 7 days: "On the horizon"

**Present as**:
```
BIRTHDAY & EVENT TRACKER (next [N] days)

THIS WEEK:
- [Name]'s Birthday — [Day, Date] ([N] days away)
  Suggestion: [gift/call/card/dinner]

COMING UP:
- [Name]'s Anniversary — [Day, Date] ([N] days away)

FURTHER OUT:
- [Name]'s Birthday — [Day, Date] ([N] days away)
```

If no events found, suggest Pete add family birthdays to his calendar and offer to help.
