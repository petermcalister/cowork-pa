# Pete's Personal Assistant (pete-pa)

A Cowork plugin that acts as Pete's personal assistant — managing emails, calendar, and the "cowork-pa" WhatsApp channel with a daily morning briefing.

## What It Does

- **Morning Briefing**: Compiles a daily summary of calendar events, email highlights, birthday reminders, and article digests from the "cowork-pa" WhatsApp channel
- **Email Scanning**: Automatically extracts dates, deadlines, and commitments from Gmail and Outlook emails and offers to add them to Google Calendar
- **Birthday Tracking**: Monitors Google Calendar for upcoming birthdays and personal events with proactive reminders
- **Channel Digest**: Summarizes articles shared in the "cowork-pa" WhatsApp channel

## Commands

| Command | Description |
|---------|-------------|
| `/peter-morning-brief-cmd` | Run the full daily morning briefing |
| `/scan-emails [days]` | Scan emails for dates to add to calendar (default: 7 days) |
| `/check-birthdays [days]` | Check upcoming birthdays and events (default: 30 days) |
| `/summarize-channels` | Summarize articles from the "cowork-pa" WhatsApp channel |

## Architecture

```
pete-pa/
├── .claude-plugin/plugin.json    # Plugin manifest (v0.4.1)
├── hooks/hooks.json              # SessionStart hook — displays context on load
├── references/                   # Shared browser navigation guides
│   ├── browser-gmail-guide.md
│   ├── browser-outlook-guide.md
│   ├── browser-gcal-guide.md
│   ├── browser-whatsapp-guide.md
│   └── date-patterns.md
├── commands/                     # Thin launcher commands
│   ├── peter-morning-brief-cmd.md
│   ├── scan-emails.md
│   ├── check-birthdays.md
│   └── summarize-channels.md
└── skills/                       # Workflow skills with browser guide references
    ├── peter-morning-brief-skill/
    │   └── SKILL.md
    └── calendar-intelligence/
        └── SKILL.md
```

### How It Works

Commands are thin launchers that load a skill and set tool permissions. Skills contain the full workflow — they read shared browser guides from `references/` and navigate each web service sequentially via Chrome browser tools.

1. **Command** receives user request, sets allowed tools, loads the relevant skill
2. **Skill** reads browser guides from `references/` for each service
3. **Skill** navigates each service sequentially via Chrome browser tools
4. **Skill** compiles results and presents to Pete

## Setup

### Browser Sessions Required

All services are accessed via Chrome browser automation (Claude in Chrome). Sign into these services in Chrome before using:

1. **Gmail** — sign in at mail.google.com
2. **Google Calendar** — sign in at calendar.google.com
3. **Outlook** — sign in at outlook.live.com
4. **WhatsApp** — link at web.whatsapp.com (ensure the "cowork-pa" channel is in your contacts/groups)

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
- **5 References**: browser guides for Gmail, Outlook, Google Calendar, WhatsApp + date patterns
- **1 Hook**: SessionStart (loads assistant context)

## Tips

- Add family birthdays as recurring annual events in Google Calendar for best tracking
- The email scanner works best when emails contain explicit dates rather than vague references
- Make sure your WhatsApp browser session stays active for channel digest
- Run `/scan-emails` weekly to keep your calendar up to date with email commitments
