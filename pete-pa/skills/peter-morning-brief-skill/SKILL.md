---
name: peter-morning-brief-skill
description: >
  This skill should be used when Pete asks for a "morning briefing",
  "daily summary", "what's happening today", "catch me up", "morning update",
  or wants a consolidated view of his calendar, emails, and WhatsApp channels.
  Also triggers when Pete asks to "summarize articles" from WhatsApp.
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

## Agent Orchestration

Launch all 4 scanner agents in parallel using the Task tool to gather data concurrently:

1. **gcal-scanner** — `${CLAUDE_PLUGIN_ROOT}/agents/gcal-scanner.md`
   Fetches today's events and upcoming birthdays/anniversaries
2. **gmail-scanner** — `${CLAUDE_PLUGIN_ROOT}/agents/gmail-scanner.md`
   Scans Gmail for unread emails and extracts dates
3. **outlook-scanner** — `${CLAUDE_PLUGIN_ROOT}/agents/outlook-scanner.md`
   Scans Outlook for unread emails and extracts dates
4. **whatsapp-scanner** — `${CLAUDE_PLUGIN_ROOT}/agents/whatsapp-scanner.md`
   Scans cowork-pa channel for shared articles

Wait for all agents to return, then compile their results into the briefing format below.

### Handling Agent Status Codes

Each agent returns a status header. Handle failures gracefully:

- `*_STATUS: OK` — include the agent's data in the briefing
- `*_STATUS: NOT_SIGNED_IN` — note "[Service] skipped — not signed in" in the briefing
- `*_STATUS: CAPTCHA_BLOCKED` — note "[Service] skipped — CAPTCHA required" in the briefing
- `*_STATUS: TIMEOUT` — note "[Service] skipped — page didn't load" in the briefing
- `WHATSAPP_STATUS: QR_CODE_NEEDED` — note "WhatsApp skipped — QR code scan needed"

Never get stuck on a failed source — compile whatever data is available.

## Presentation Format

Use a clean, scannable format:

```
Good morning Pete! Here's your briefing for [Day, Date].

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
- "Project deadline March 15" (from email by [Sender])

CHANNEL DIGEST (cowork-pa)
- [Article title] — [2-sentence summary]
- [Article title] — [2-sentence summary]

ACTION ITEMS
1. Reply to [email from X]
2. Add March 15 deadline to calendar
3. Wish Sarah happy birthday on Thursday
```

## Error Handling

- If a scanner agent fails or times out, skip that source and note it in the briefing
- Never get stuck on one source — move on and compile whatever is available
- If all agents fail, inform Pete and suggest checking browser sign-in status

## Resources

- **`${CLAUDE_PLUGIN_ROOT}/references/`** — shared browser navigation guides
- **`${CLAUDE_PLUGIN_ROOT}/agents/`** — parallel scanner agents
- **`${CLAUDE_PLUGIN_ROOT}/references/date-patterns.md`** — date extraction patterns
