---
name: peter-morning-brief-skill
description: >
  This skill should be used when Pete asks for a "morning briefing",
  "daily summary", "what's happening today", "catch me up", "morning update",
  or wants a consolidated view of his calendar, emails, and WhatsApp channels.
version: 0.4.1
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

## Data Collection Workflow

Scan each source sequentially using Chrome browser tools. Read the browser guide
for each service before navigating to it. If a source fails (not signed in,
CAPTCHA, page won't load), skip it after 15 seconds and move to the next.

### Step 1: Google Calendar

Read `${CLAUDE_PLUGIN_ROOT}/references/browser-gcal-guide.md`, then:
- Navigate to calendar.google.com
- Fetch today's events from the day view
- Switch to week view to check the next 7 days for birthdays/anniversaries
- Do NOT enter credentials — Pete will already be signed in

### Step 2: Gmail

Read `${CLAUDE_PLUGIN_ROOT}/references/browser-gmail-guide.md`, then:
- Navigate to mail.google.com
- Search for unread emails from the last 24 hours using `is:unread newer_than:1d`
- Prioritize emails from known contacts and starred messages
- Extract any dates, deadlines, or commitments mentioned in email bodies
- For date extraction patterns, refer to `${CLAUDE_PLUGIN_ROOT}/references/date-patterns.md`

### Step 3: Outlook

Read `${CLAUDE_PLUGIN_ROOT}/references/browser-outlook-guide.md`, then:
- Navigate to outlook.live.com
- Read the inbox for unread emails from the last 24 hours
- Extract key information: sender, subject, preview, any dates mentioned
- For date extraction patterns, refer to `${CLAUDE_PLUGIN_ROOT}/references/date-patterns.md`

### Step 4: WhatsApp "cowork-pa" Channel

Read `${CLAUDE_PLUGIN_ROOT}/references/browser-whatsapp-guide.md`, then:
- Navigate to web.whatsapp.com
- Locate and open the "cowork-pa" channel/group
- Check for shared articles and links from the last 24 hours
- Extract article URLs and titles
- Use WebFetch to read each article, then summarize in 2-3 sentences

### Step 5: Compile Results

- **Calendar + Birthdays**: Today's events and upcoming personal dates
- **Email Highlights**: Keep Gmail and Outlook under separate subheadings
- **Dates to Add**: Merge dates from both email sources, deduplicate, sort by confidence (HIGH first)
- **Channel Digest**: Article summaries from WhatsApp
- **Action Items**: Synthesize from all sources — emails needing replies, dates to add, upcoming birthdays

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

## Error Handling

- If a service requires sign-in, note "[Service] skipped — not signed in" at the end
- If a CAPTCHA or verification appears, note "[Service] skipped — CAPTCHA required"
- If a page won't load after 15 seconds, skip it and move on
- Never get stuck on one source — compile whatever data is available
- If all sources fail, inform Pete and suggest checking browser sign-in status

## Follow-Up Actions

If Pete asks to add any of the extracted dates to his calendar, load the
calendar-intelligence skill (`${CLAUDE_PLUGIN_ROOT}/skills/calendar-intelligence/SKILL.md`)
and follow its Calendar Event Creation workflow.

## Resources

- **`${CLAUDE_PLUGIN_ROOT}/references/browser-gcal-guide.md`** — Google Calendar navigation
- **`${CLAUDE_PLUGIN_ROOT}/references/browser-gmail-guide.md`** — Gmail navigation
- **`${CLAUDE_PLUGIN_ROOT}/references/browser-outlook-guide.md`** — Outlook navigation
- **`${CLAUDE_PLUGIN_ROOT}/references/browser-whatsapp-guide.md`** — WhatsApp navigation
- **`${CLAUDE_PLUGIN_ROOT}/references/date-patterns.md`** — date extraction patterns
