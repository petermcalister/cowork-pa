---
name: peter-morning-brief-skill
description: >
  This skill should be used when Pete asks for a "morning briefing",
  "daily summary", "what's happening today", "catch me up", "morning update",
  or wants a consolidated view of his calendar, emails, and WhatsApp channels.
version: 0.4.2
---

# Morning Brief

Compile Pete's daily morning briefing by pulling data from multiple sources,
generating a styled HTML report, and presenting a short summary to Pete.

## Briefing Structure

The report contains these sections (omit any section with zero items):

1. **Calendar** — today's events from Google Calendar
2. **Coming Up** — birthdays and personal events within the next 7 days
3. **Email Highlights** — important unread emails from Gmail and Outlook
4. **Dates to Add** — dates/deadlines extracted from recent emails
5. **Channel Digest** — article summaries from the "cowork-pa" WhatsApp channel
6. **Action Items** — consolidated list of things Pete needs to act on

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

### Step 5: Generate HTML Report

1. Read the report template: `${CLAUDE_PLUGIN_ROOT}/references/report-template.html`
2. Populate the template with collected data:
   - Replace `{{GREETING}}` with time-of-day greeting (e.g. "Good morning Pete!")
   - Replace `{{DATE}}` with short date (e.g. "2026-02-14")
   - Replace `{{DATE_FULL}}` with full date (e.g. "Friday 14 February 2026")
   - Replace `{{TIMESTAMP}}` with generation time
   - Replace each `{{*_ITEMS}}` placeholder with `<li>` elements containing the data
   - Use the CSS classes from the template: `.time`, `.sender`, `.subject`, `.summary`,
     `.priority-high/medium/low`, `.confidence-high/medium/low`, `.article-link`
   - Remove any section `<div>` entirely if it has no items
   - Replace `{{SKIPPED_SOURCES}}` with a list of failed sources, or remove if all OK
3. Write the HTML file to: `${CLAUDE_PLUGIN_ROOT}/reports/briefing-YYYY-MM-DD.html`
   (create the `reports/` directory if it doesn't exist)
4. Open the report in the browser using Bash:
   - Windows: `cmd.exe /c start "" "path\to\report.html"`
   - Mac: `open "path/to/report.html"`

### Step 6: Show Summary in Chat

After generating the HTML report, present a **short summary** (not the full briefing)
in the chat:

```
Briefing ready for [Day, Date] — opened in browser.

Quick summary:
- [N] calendar events today
- [N] emails worth reading ([N] with dates to add)
- [N] articles from cowork-pa channel
- [N] action items

Report saved: reports/briefing-YYYY-MM-DD.html
```

### Step 7: Upload Report to WhatsApp

After generating the HTML report, upload it to the "cowork-pa" WhatsApp channel.
Follow the file upload steps in `${CLAUDE_PLUGIN_ROOT}/references/browser-whatsapp-guide.md` (section 7):

1. Navigate to the cowork-pa channel (should already be open from Step 4)
2. Click the attachment/paperclip icon (📎)
3. Select "Document"
4. Upload the HTML report file: `reports/briefing-YYYY-MM-DD.html`
5. Add caption: "Morning Briefing — [Date]"
6. Send

This step is not optional — always upload the report to the channel.

## Error Handling

- If a service requires sign-in, note "[Service] skipped" in the report's skipped sources section
- If a CAPTCHA or verification appears, note "[Service] skipped — CAPTCHA required"
- If a page won't load after 15 seconds, skip it and move on
- Never get stuck on one source — compile whatever data is available
- If all sources fail, inform Pete and suggest checking browser sign-in status

## Follow-Up Actions

If Pete asks to add any of the extracted dates to his calendar, load the
calendar-intelligence skill (`${CLAUDE_PLUGIN_ROOT}/skills/calendar-intelligence/SKILL.md`)
and follow its Calendar Event Creation workflow.

## Resources

- **`${CLAUDE_PLUGIN_ROOT}/references/report-template.html`** — HTML report template
- **`${CLAUDE_PLUGIN_ROOT}/references/browser-gcal-guide.md`** — Google Calendar navigation
- **`${CLAUDE_PLUGIN_ROOT}/references/browser-gmail-guide.md`** — Gmail navigation
- **`${CLAUDE_PLUGIN_ROOT}/references/browser-outlook-guide.md`** — Outlook navigation
- **`${CLAUDE_PLUGIN_ROOT}/references/browser-whatsapp-guide.md`** — WhatsApp navigation
- **`${CLAUDE_PLUGIN_ROOT}/references/date-patterns.md`** — date extraction patterns
- **`${CLAUDE_PLUGIN_ROOT}/references/petes-interests.md`** — filtering rules and topic priorities
