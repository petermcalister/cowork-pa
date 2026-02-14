---
description: Run Pete's daily morning briefing
allowed-tools: Read, Grep, Glob, Bash, WebFetch, mcp__Gmail__*, mcp__Google_Calendar__*
model: sonnet
---

Compile Pete's full morning briefing using the peter-morning-brief-skill.

Load the skill by reading `${CLAUDE_PLUGIN_ROOT}/skills/peter-morning-brief-skill/SKILL.md`.

Execute the briefing in this order:

1. **Calendar**: Use Google Calendar MCP to fetch today's events and the next 7 days.
   Flag any birthdays or personal events coming up.

2. **Gmail**: Use Gmail MCP to search for unread emails from the last 24 hours.
   Extract any dates, deadlines, or commitments found in email bodies.

3. **Outlook**: Open Chrome and navigate to outlook.live.com to read unread emails.
   Follow the browser guide in `${CLAUDE_PLUGIN_ROOT}/skills/peter-morning-brief-skill/references/browser-outlook-guide.md`.

4. **WhatsApp & Telegram**: Open Chrome tabs for web.whatsapp.com and web.telegram.org.
   Scan channels for shared articles. Summarize each article in 2-3 sentences.
   Follow the guide in `${CLAUDE_PLUGIN_ROOT}/skills/peter-morning-brief-skill/references/browser-messaging-guide.md`.

5. **Compile**: Present everything in the briefing format defined in the peter-morning-brief-skill.

If any source fails (not signed in, MCP not connected), skip it and note it at the end.
Present the briefing directly to Pete — keep it concise and actionable.
