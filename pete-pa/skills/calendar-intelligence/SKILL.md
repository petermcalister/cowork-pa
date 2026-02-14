---
name: calendar-intelligence
description: >
  This skill should be used when Pete asks about "birthdays", "upcoming events",
  "what's in my calendar", "add this to my calendar", "extract dates from emails",
  "find commitments in my inbox", "when is [person]'s birthday", or needs help
  managing personal calendar events and date tracking from email correspondence.
version: 0.1.0
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

Use the Google Calendar MCP tools to search for events containing keywords:
- "birthday", "bday", "b-day"
- "anniversary"
- Names of family members Pete has mentioned

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

1. Use Gmail MCP to search recent emails (last 7 days unless specified)
2. Use Outlook browser automation to scan inbox
3. For each email, identify date-bearing content:
   - Explicit dates: "March 15", "15/03", "next Friday"
   - Relative dates: "in two weeks", "end of month", "next quarter"
   - Deadline language: "due by", "deadline", "submit before", "RSVP by"
   - Meeting proposals: "let's schedule", "how about Tuesday at 3pm"
   - Event invitations: "you're invited", "save the date", "join us on"

4. For each extracted date, capture:
   - The date/time (resolve relative dates to absolute)
   - Source email: sender and subject
   - Context: what the date is about (1 sentence)
   - Confidence: HIGH (explicit date), MEDIUM (relative date), LOW (inferred)

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
1. Use Google Calendar MCP to create the event
2. Set appropriate reminders (1 day before for deadlines, 1 week for birthdays)
3. Include the source email reference in the event description
4. For all-day events (birthdays, deadlines), create as all-day events
5. For timed events, set the specific time

### 4. Calendar Overview

When Pete asks "what's in my calendar" or "what's my week look like":
1. Fetch events for the requested period (default: next 7 days)
2. Group by day
3. Highlight conflicts (overlapping events)
4. Flag any birthdays or personal events
5. Note free blocks longer than 2 hours

## Error Handling

- If Google Calendar MCP is not connected, inform Pete and suggest connecting it
- If event creation fails, provide the event details so Pete can add it manually
- For ambiguous dates, ask Pete to clarify rather than guessing

## Additional Resources

- **`references/date-patterns.md`** — comprehensive date extraction patterns and regex
