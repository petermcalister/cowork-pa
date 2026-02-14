---
name: peter-morning-brief-skill
description: >
  This skill should be used when Pete asks for a "morning briefing",
  "daily summary", "what's happening today", "catch me up", "morning update",
  or wants a consolidated view of his calendar, emails, and messaging channels.
  Also triggers when Pete asks to "summarize articles" from WhatsApp or Telegram.
version: 0.1.0
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
6. **Channel Digest** — article summaries from WhatsApp and Telegram channels
7. **Action Items** — consolidated list of things Pete needs to act on

## Data Source Workflow

### Google Calendar (MCP)

Use the Google Calendar MCP tools to:
- Fetch today's events
- Fetch the next 7 days for upcoming birthdays/anniversaries
- Look for events with keywords: "birthday", "anniversary", "bday"

### Gmail (MCP)

Use the Gmail MCP tools to:
- Search for unread emails from the last 24 hours
- Prioritize emails from known contacts and flagged/starred messages
- Extract any dates, deadlines, or commitments mentioned in email bodies
- Flag emails that contain calendar-worthy dates

### Outlook (Browser-based)

Use Claude in Chrome browser tools to:
- Navigate to outlook.live.com
- Read the inbox for unread emails from the last 24 hours
- Extract key information: sender, subject, preview, any dates mentioned
- Do NOT enter credentials — Pete will already be signed in

Refer to `references/browser-outlook-guide.md` for detailed browser navigation steps.

### WhatsApp (Browser-based)

Use Claude in Chrome browser tools to:
- Navigate to web.whatsapp.com (Pete will already be signed in)
- Check specified channels/groups for shared articles and links
- Extract article URLs and titles
- Summarize each article in 2-3 sentences

Refer to `references/browser-messaging-guide.md` for detailed steps.

### Telegram (Browser-based)

Use Claude in Chrome browser tools to:
- Navigate to web.telegram.org (Pete will already be signed in)
- Check specified channels for shared articles and links
- Extract article URLs and titles
- Summarize each article in 2-3 sentences

Refer to `references/browser-messaging-guide.md` for detailed steps.

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

CHANNEL DIGEST
- [Article title] — [2-sentence summary] (from [WhatsApp/Telegram group])

ACTION ITEMS
1. Reply to [email from X]
2. Add March 15 deadline to calendar
3. Wish Sarah happy birthday on Thursday
```

## Error Handling

- If a browser source is unavailable (not signed in, page won't load), skip it and note it in the briefing
- If Gmail or Calendar MCP isn't connected, note it and suggest Pete connects them
- Never get stuck on one source — move on after 30 seconds of trying

## Additional Resources

- **`references/browser-outlook-guide.md`** — step-by-step Outlook browser navigation
- **`references/browser-messaging-guide.md`** — WhatsApp and Telegram browser navigation
