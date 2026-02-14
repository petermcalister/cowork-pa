---
name: calendar-intelligence
description: >
  This skill should be used when Pete asks about "birthdays", "upcoming events",
  "what's in my calendar", "add this to my calendar", "extract dates from emails",
  "find commitments in my inbox", "when is [person]'s birthday", or needs help
  managing personal calendar events and date tracking from email correspondence.
version: 0.4.0
---

# Calendar Intelligence

Manage Pete's Google Calendar with focus on birthday/event tracking and
automatic date extraction from emails.

## Routing

This skill covers 4 capabilities. Determine which one Pete needs:

| Pete says... | Capability |
|-------------|-----------|
| "check birthdays", "upcoming events", "when is X's birthday" | 1. Birthday & Event Tracking |
| "scan emails for dates", "find commitments", "extract dates" | 2. Date Extraction from Emails |
| "add this to calendar", "create an event", confirmed dates from extraction | 3. Calendar Event Creation |
| "what's in my calendar", "what's my week look like" | 4. Calendar Overview |

## Core Capabilities

### 1. Birthday & Event Tracking

Launch the **gcal-scanner** agent to find upcoming birthdays and personal events.
Use the Task tool: set the task prompt to "Read the agent definition at
`${CLAUDE_PLUGIN_ROOT}/agents/gcal-scanner.md` and execute its workflow.
Search across the next [N] days (default: 30)."

If the agent returns `GCAL_STATUS: OK`, sort results by proximity (soonest first)
and present with action suggestions:

```
UPCOMING PERSONAL EVENTS (next 7 days)
- Sister's Birthday — Saturday 15th (2 days away) — Consider: gift, card, dinner?
- Nephew Jake's Birthday — Tuesday 19th (6 days away)
```

If it returns a non-OK status, inform Pete (e.g. "Calendar not accessible — please sign in at calendar.google.com").

### 2. Date Extraction from Emails

Launch **gmail-scanner** and **outlook-scanner** agents in parallel. For each,
use the Task tool: set the task prompt to "Read the agent definition at [path]
and execute its workflow. Scan emails from the last [N] days (default: 7)."

- `${CLAUDE_PLUGIN_ROOT}/agents/gmail-scanner.md`
- `${CLAUDE_PLUGIN_ROOT}/agents/outlook-scanner.md`

Handle each agent's status code — skip any that return non-OK and note which
service was unavailable.

Merge `DATES EXTRACTED` sections from both agents into one list. Deduplicate
any dates found in both inboxes. For confidence scoring definitions, refer to
`${CLAUDE_PLUGIN_ROOT}/references/date-patterns.md`.

Present findings grouped by confidence and ask Pete which to add:

```
DATES FOUND IN RECENT EMAILS

HIGH CONFIDENCE:
1. March 15, 2026 — Project proposal deadline
   From: john@work.com — "Re: Q2 Project Proposals"
   → Add to calendar?

2. Feb 20, 2026 at 14:00 — Dentist appointment
   From: clinic@dental.com — "Appointment Confirmation"
   → Add to calendar?

MEDIUM CONFIDENCE:
3. ~End of February — Tax documents due
   From: accountant@firm.com — "Year-end tax prep"
   → Add to calendar?
```

### 3. Calendar Event Creation

When Pete confirms dates to add, read the event creation guide at
`${CLAUDE_PLUGIN_ROOT}/references/browser-gcal-guide.md` (Part 2) and follow
its step-by-step instructions to create the event via Chrome browser tools.

For each event, provide these parameters to the guide's workflow:
- **Title**: derived from the email context or Pete's request
- **Date/Time**: the confirmed date (all-day for birthdays/deadlines, timed for meetings)
- **Description**: include source reference (e.g. "Extracted from email by [Sender] — [Subject]")
- **Reminder**: 1 day before for deadlines, 1 hour before for meetings, 1 week before for birthdays
- **Recurrence**: annual for birthdays and anniversaries

### 4. Calendar Overview

Launch the **gcal-scanner** agent via the Task tool: set the task prompt to
"Read the agent definition at `${CLAUDE_PLUGIN_ROOT}/agents/gcal-scanner.md`
and execute its workflow. Read events for the next [N] days (default: 7)."

If the agent returns `GCAL_STATUS: OK`, post-process its results:
1. Group events by day
2. Highlight conflicts (overlapping events)
3. Flag any birthdays or personal events
4. Note free blocks longer than 2 hours

If it returns a non-OK status, inform Pete and suggest signing in.

## Error Handling

All error handling is based on agent status codes:

- `GCAL_STATUS: NOT_SIGNED_IN` — tell Pete to sign in at calendar.google.com
- `GMAIL_STATUS: NOT_SIGNED_IN` / `OUTLOOK_STATUS: NOT_SIGNED_IN` — tell Pete which email service needs sign-in
- `*_STATUS: CAPTCHA_BLOCKED` — inform Pete, skip that source
- `*_STATUS: TIMEOUT` — inform Pete, skip that source
- If event creation fails via the browser, present the event details as text so Pete can add manually
- For ambiguous dates, ask Pete to clarify rather than guessing

## Resources

- **`${CLAUDE_PLUGIN_ROOT}/references/browser-gcal-guide.md`** — Google Calendar browser navigation (read + create events)
- **`${CLAUDE_PLUGIN_ROOT}/references/date-patterns.md`** — date extraction patterns and confidence scoring
- **`${CLAUDE_PLUGIN_ROOT}/agents/gcal-scanner.md`** — calendar scanning agent
- **`${CLAUDE_PLUGIN_ROOT}/agents/gmail-scanner.md`** — Gmail scanning agent
- **`${CLAUDE_PLUGIN_ROOT}/agents/outlook-scanner.md`** — Outlook scanning agent
