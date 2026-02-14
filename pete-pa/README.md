# Pete's Personal Assistant (pete-pa)

A Cowork plugin that acts as Pete's personal assistant — managing emails, calendar, and messaging channels with a daily morning briefing.

## What It Does

- **Morning Briefing**: Compiles a daily summary of calendar events, email highlights, birthday reminders, and article digests from messaging channels
- **Email Scanning**: Automatically extracts dates, deadlines, and commitments from Gmail and Outlook emails and offers to add them to Google Calendar
- **Birthday Tracking**: Monitors Google Calendar for upcoming birthdays and personal events with proactive reminders
- **Channel Digest**: Summarizes articles shared in WhatsApp and Telegram channels

## Commands

| Command | Description |
|---------|-------------|
| `/peter-morning-brief-cmd` | Run the full daily morning briefing |
| `/scan-emails [days]` | Scan emails for dates to add to calendar (default: 7 days) |
| `/check-birthdays [days]` | Check upcoming birthdays and events (default: 30 days) |
| `/summarize-channels [name]` | Summarize articles from messaging channels |

## Setup

### Browser Sessions Required

All services are accessed via Chrome browser automation (Claude in Chrome). Sign into these services in Chrome before using:

1. **Gmail** — sign in at mail.google.com
2. **Google Calendar** — sign in at calendar.google.com
3. **Outlook** — sign in at outlook.live.com
4. **WhatsApp** — link at web.whatsapp.com
5. **Telegram** — sign in at web.telegram.org

### Claude in Chrome Extension

The Claude in Chrome extension must be installed and active for browser automation to work.

### Scheduled Morning Brief

To set up the daily 7am briefing, create a scheduled shortcut in Cowork:
- Command: `/peter-morning-brief-cmd`
- Schedule: Daily at 07:00
- Requires: PC to be running and Cowork active

## Components

- **2 Skills**: peter-morning-brief-skill, calendar-intelligence
- **4 Commands**: peter-morning-brief-cmd, scan-emails, check-birthdays, summarize-channels
- **1 Hook**: SessionStart (loads assistant context)

## Tips

- Add family birthdays as recurring annual events in Google Calendar for best tracking
- The email scanner works best when emails contain explicit dates rather than vague references
- For WhatsApp/Telegram, make sure your browser sessions stay active
- Run `/scan-emails` weekly to keep your calendar up to date with email commitments
