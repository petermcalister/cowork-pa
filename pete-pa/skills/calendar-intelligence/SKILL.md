---
name: calendar-intelligence
description: >
  This skill should be used when Pete asks about "birthdays", "upcoming events",
  "what's in my calendar", "add this to my calendar", "extract dates from emails",
  "find commitments in my inbox", "when is [person]'s birthday", or needs help
  managing personal calendar events and date tracking from email correspondence.
version: 0.4.1
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

Read `${CLAUDE_PLUGIN_ROOT}/references/browser-gcal-guide.md`, then use Chrome browser tools to:
- Navigate to calendar.google.com
- Search for events in the next [N] days (default: 30) containing "birthday", "bday", "anniversary"
- Check that the "Birthdays" calendar (from Google Contacts) is visible in the sidebar

Sort results by proximity (soonest first) and present with action suggestions:

```
UPCOMING PERSONAL EVENTS (next 7 days)
- Sister's Birthday — Saturday 15th (2 days away) — Consider: gift, card, dinner?
- Nephew Jake's Birthday — Tuesday 19th (6 days away)
```

### 2. Date Extraction from Emails

Scan Gmail and Outlook sequentially for dates that should be added to Pete's calendar.

1. Read `${CLAUDE_PLUGIN_ROOT}/references/date-patterns.md` for extraction patterns
2. Read `${CLAUDE_PLUGIN_ROOT}/references/browser-gmail-guide.md`, then navigate to
   mail.google.com and scan emails from the last [N] days (default: 7). Extract dates.
3. Read `${CLAUDE_PLUGIN_ROOT}/references/browser-outlook-guide.md`, then navigate to
   outlook.live.com and scan the inbox for the same period. Extract dates.
4. Merge dates from both sources, deduplicate, and score by confidence:
   - **HIGH**: Explicit date + deadline/meeting indicator + specific time
   - **MEDIUM**: Explicit date without time, or relative date with clear context
   - **LOW**: Vague relative dates, inferred deadlines
5. Present findings grouped by confidence and ask Pete which to add:

```
DATES FOUND IN RECENT EMAILS

HIGH CONFIDENCE:
1. March 15, 2026 — Project proposal deadline
   From: john@work.com — "Re: Q2 Project Proposals"
   → Add to calendar?

MEDIUM CONFIDENCE:
2. ~End of February — Tax documents due
   From: accountant@firm.com — "Year-end tax prep"
   → Add to calendar?
```

### 3. Calendar Event Creation

When Pete confirms dates to add, read `${CLAUDE_PLUGIN_ROOT}/references/browser-gcal-guide.md`
(Part 2) and follow its step-by-step instructions to create the event via Chrome browser tools.

For each event, provide these parameters:
- **Title**: derived from the email context or Pete's request
- **Date/Time**: the confirmed date (all-day for birthdays/deadlines, timed for meetings)
- **Description**: include source reference (e.g. "Extracted from email by [Sender] — [Subject]")
- **Reminder**: 1 day before for deadlines, 1 hour before for meetings, 1 week before for birthdays
- **Recurrence**: annual for birthdays and anniversaries

### 4. Calendar Overview

Read `${CLAUDE_PLUGIN_ROOT}/references/browser-gcal-guide.md`, then use Chrome browser tools to:
- Navigate to calendar.google.com
- Read events for the requested period (default: next 7 days)

Post-process the results:
1. Group events by day
2. Highlight conflicts (overlapping events)
3. Flag any birthdays or personal events
4. Note free blocks longer than 2 hours

## Error Handling

- If a service requires sign-in, inform Pete and skip that source
- If a CAPTCHA or verification appears, inform Pete and skip that source
- If a page won't load after 15 seconds, skip and move on
- If event creation fails via the browser, present the event details as text so Pete can add manually
- For ambiguous dates, ask Pete to clarify rather than guessing

## Resources

- **`${CLAUDE_PLUGIN_ROOT}/references/browser-gcal-guide.md`** — Google Calendar navigation (read + create)
- **`${CLAUDE_PLUGIN_ROOT}/references/browser-gmail-guide.md`** — Gmail navigation
- **`${CLAUDE_PLUGIN_ROOT}/references/browser-outlook-guide.md`** — Outlook navigation
- **`${CLAUDE_PLUGIN_ROOT}/references/date-patterns.md`** — date extraction patterns and confidence scoring
