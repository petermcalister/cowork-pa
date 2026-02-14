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

## Core Capabilities

### 1. Birthday & Event Tracking

Track recurring personal events in Google Calendar:
- Family birthdays (sister, nephews, nieces, parents)
- Anniversaries
- Other recurring personal dates

**How to find birthdays:**

Launch the **gcal-scanner** agent (`${CLAUDE_PLUGIN_ROOT}/agents/gcal-scanner.md`) to:
- Search for events containing keywords: "birthday", "bday", "b-day"
- Search for "anniversary"
- Search for names of family members Pete has mentioned
- Check that the "Birthdays" calendar (from Google Contacts) is visible in the sidebar

Search across the next 30 days for upcoming events.
Present results sorted by proximity (soonest first).

**Reminder format:**
```
UPCOMING PERSONAL EVENTS (next 7 days)
- Sister's Birthday — Saturday 15th (2 days away) — Consider: gift, card, dinner?
- Nephew Jake's Birthday — Tuesday 19th (6 days away)
```

### 2. Date Extraction from Emails

Scan recent Gmail and Outlook emails for dates that should be added to Pete's calendar.

**Extraction process:**

1. Launch **gmail-scanner** and **outlook-scanner** agents in parallel:
   - `${CLAUDE_PLUGIN_ROOT}/agents/gmail-scanner.md`
   - `${CLAUDE_PLUGIN_ROOT}/agents/outlook-scanner.md`
2. Both agents will scan emails for the specified period (default: last 7 days) and extract dates
3. Load the date patterns reference for confidence scoring:
   `${CLAUDE_PLUGIN_ROOT}/references/date-patterns.md`
4. Compile extracted dates from both agents, scored by confidence:
   - **HIGH**: Explicit date + deadline/meeting indicator + specific time
   - **MEDIUM**: Explicit date without time, or relative date with clear context
   - **LOW**: Vague relative dates, inferred deadlines
5. Present findings and ask Pete which ones to add to calendar

**Output format:**
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

When Pete confirms dates to add:
1. Use Chrome browser tools to navigate to calendar.google.com
2. Create the event via the browser interface (click Create, fill in details)
3. Set appropriate reminders (1 day before for deadlines, 1 hour before for meetings)
4. Include the source email reference in the event description
5. For all-day events (birthdays, deadlines), toggle the "All day" option
6. For timed events, set the specific start and end time
7. For recurring events (birthdays, anniversaries), set annual recurrence

Refer to `${CLAUDE_PLUGIN_ROOT}/references/browser-gcal-guide.md` Part 2 for event creation steps.

### 4. Calendar Overview

When Pete asks "what's in my calendar" or "what's my week look like":

Launch the **gcal-scanner** agent to read events, then:
1. Group events by day
2. Highlight conflicts (overlapping events)
3. Flag any birthdays or personal events
4. Note free blocks longer than 2 hours

Refer to `${CLAUDE_PLUGIN_ROOT}/references/browser-gcal-guide.md` for navigation steps.

## Error Handling

- If calendar.google.com requires sign-in, inform Pete and ask him to sign in manually
- If event creation fails via the browser, provide the event details so Pete can add it manually
- For ambiguous dates, ask Pete to clarify rather than guessing
- If a CAPTCHA or verification prompt appears, inform Pete and skip that source

## Resources

- **`${CLAUDE_PLUGIN_ROOT}/references/browser-gcal-guide.md`** — Google Calendar browser navigation (read + create)
- **`${CLAUDE_PLUGIN_ROOT}/references/date-patterns.md`** — comprehensive date extraction patterns
- **`${CLAUDE_PLUGIN_ROOT}/agents/gcal-scanner.md`** — calendar scanning agent
- **`${CLAUDE_PLUGIN_ROOT}/agents/gmail-scanner.md`** — Gmail scanning agent
- **`${CLAUDE_PLUGIN_ROOT}/agents/outlook-scanner.md`** — Outlook scanning agent
