---
description: Scan emails for dates and calendar commitments
allowed-tools: Read, WebFetch, mcp__Gmail__*, mcp__Google_Calendar__*
argument-hint: [days-back]
---

Scan Pete's recent emails for dates, deadlines, and commitments that should be added to his Google Calendar.

Load the calendar-intelligence skill: read `${CLAUDE_PLUGIN_ROOT}/skills/calendar-intelligence/SKILL.md`
and the date patterns reference: `${CLAUDE_PLUGIN_ROOT}/skills/calendar-intelligence/references/date-patterns.md`.

**Scope**: Scan emails from the last $1 days (default: 7 if not specified).

**Process**:

1. Use Gmail MCP to search for emails from the specified period.
2. Open Outlook via Chrome browser to scan the inbox for the same period.
   Follow `${CLAUDE_PLUGIN_ROOT}/skills/peter-morning-brief-skill/references/browser-outlook-guide.md`.
3. For each email, apply the date extraction patterns to identify:
   - Explicit dates and deadlines
   - Meeting proposals and appointment confirmations
   - Event invitations
   - Recurring commitments
4. Score each finding by confidence (HIGH, MEDIUM, LOW).
5. Present all findings grouped by confidence level.
6. Ask Pete which dates he wants added to Google Calendar.
7. For confirmed dates, use Google Calendar MCP to create events with:
   - Appropriate title derived from the email context
   - Source email reference in the description
   - Reminders: 1 day before for deadlines, 1 hour before for meetings
