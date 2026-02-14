---
name: peter-morning-brief-skill
description: >
  This skill should be used when Pete asks for a "morning briefing",
  "daily summary", "what's happening today", "catch me up", "morning update",
  or wants a consolidated view of his calendar, emails, and WhatsApp channels.
version: 0.4.0
---

# Morning Brief

Compile Pete's daily morning briefing by pulling data from multiple sources
and presenting a concise, actionable summary.

## Briefing Structure

Present the briefing in this exact order:

1. **Today's Date & Day** — greeting with current date
2. **Calendar Snapshot** — today's events from Google Calendar
3. **Birthday & Anniversary Alerts** — any personal events within the next 7 days
4. **Email Highlights** — important unread emails from Gmail and Outlook
5. **Date Commitments Found** — any dates/deadlines extracted from recent emails
6. **Channel Digest** — article summaries from the "cowork-pa" WhatsApp channel
7. **Action Items** — consolidated list of things Pete needs to act on

If a section has zero items, omit it entirely rather than showing an empty heading.
If all 4 agents fail, skip straight to a short status report instead of an empty briefing.

## Agent Orchestration

Launch all 4 scanner agents in parallel. For each agent, use the **Task tool** to
spawn a subagent — set the task prompt to: "Read the agent definition at [path] and
execute its workflow." The 4 tasks should be launched in a single batch so they run
concurrently:

1. **gcal-scanner** — `${CLAUDE_PLUGIN_ROOT}/agents/gcal-scanner.md`
   Fetches today's events and upcoming birthdays/anniversaries
2. **gmail-scanner** — `${CLAUDE_PLUGIN_ROOT}/agents/gmail-scanner.md`
   Scans Gmail for unread emails and extracts dates
3. **outlook-scanner** — `${CLAUDE_PLUGIN_ROOT}/agents/outlook-scanner.md`
   Scans Outlook for unread emails and extracts dates
4. **whatsapp-scanner** — `${CLAUDE_PLUGIN_ROOT}/agents/whatsapp-scanner.md`
   Scans cowork-pa channel for shared articles

Wait for all agents to return, then compile their results.

### Compiling Agent Results

- **Calendar + Birthdays**: Use gcal-scanner output directly for the CALENDAR and COMING UP sections.
- **Email Highlights**: Merge email lists from gmail-scanner and outlook-scanner, keeping them under separate Gmail/Outlook subheadings.
- **Dates to Add**: Merge the `DATES EXTRACTED` sections from both email agents into one list. Deduplicate any dates that appear in both. Sort by confidence (HIGH first).
- **Channel Digest**: Use whatsapp-scanner output directly.
- **Action Items**: Synthesize from all sources — emails needing replies, dates to add to calendar, upcoming birthdays needing attention.

### Handling Agent Status Codes

Each agent returns a status header. Handle failures gracefully:

- `*_STATUS: OK` — include the agent's data in the briefing
- `*_STATUS: NOT_SIGNED_IN` — skip that source, add a note at the end: "[Service] skipped — not signed in"
- `*_STATUS: CAPTCHA_BLOCKED` — skip, note: "[Service] skipped — CAPTCHA required"
- `*_STATUS: TIMEOUT` — skip, note: "[Service] skipped — page didn't load"
- `WHATSAPP_STATUS: QR_CODE_NEEDED` — skip, note: "WhatsApp skipped — QR code scan needed"

Never get stuck on a failed source — compile whatever data is available.
If all 4 agents fail, inform Pete and suggest checking his browser sign-in status for each service.

## Presentation Format

Adapt the greeting to time of day (morning/afternoon/evening). Use a clean, scannable format:

```
Good [morning/afternoon/evening] Pete! Here's your briefing for [Day, Date].

CALENDAR
- 09:00 — Team standup
- 14:00 — Dentist appointment

COMING UP (birthdays & events)
- Sarah's birthday — Thursday (3 days away)

EMAIL HIGHLIGHTS
Gmail:
- [Sender] — [Subject] — [1-line summary]
Outlook:
- [Sender] — [Subject] — [1-line summary]

DATES TO ADD TO CALENDAR
- "Project deadline March 15" (from email by [Sender]) — Confidence: HIGH

CHANNEL DIGEST (cowork-pa)
- [Article title] — [2-sentence summary]

ACTION ITEMS
1. Reply to [email from X]
2. Add March 15 deadline to calendar
3. Wish Sarah happy birthday on Thursday
```

## Follow-Up Actions

If Pete asks to add any of the extracted dates to his calendar, load the
calendar-intelligence skill (`${CLAUDE_PLUGIN_ROOT}/skills/calendar-intelligence/SKILL.md`)
and follow its Calendar Event Creation workflow.
