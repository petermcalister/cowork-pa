---
description: Scan emails for dates and calendar commitments
allowed-tools: Read, Task, WebFetch, mcp__Claude_in_Chrome__*
argument-hint: [days-back]
---

Scan Pete's recent emails for dates, deadlines, and commitments that should be added to his Google Calendar.

**Scope**: Scan emails from the last $1 days (default: 7 if not specified).

**Process**:

1. Load the date patterns reference: `${CLAUDE_PLUGIN_ROOT}/references/date-patterns.md`
2. Launch **gmail-scanner** and **outlook-scanner** agents in parallel:
   - `${CLAUDE_PLUGIN_ROOT}/agents/gmail-scanner.md`
   - `${CLAUDE_PLUGIN_ROOT}/agents/outlook-scanner.md`
3. Compile extracted dates from both agents, scored by confidence (HIGH, MEDIUM, LOW)
4. Present all findings grouped by confidence level
5. Ask Pete which dates he wants added to Google Calendar
6. For confirmed dates, read `${CLAUDE_PLUGIN_ROOT}/references/browser-gcal-guide.md` Part 2 and create events via Chrome browser with:
   - Appropriate title derived from the email context
   - Source email reference in the description
   - Reminders: 1 day before for deadlines, 1 hour before for meetings
