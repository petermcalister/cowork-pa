---
description: Summarize articles from WhatsApp and Telegram channels
allowed-tools: Read, WebFetch
argument-hint: [channel-name]
---

Scan Pete's WhatsApp and Telegram channels for shared articles and provide summaries.

Load the browser messaging guide: read `${CLAUDE_PLUGIN_ROOT}/skills/peter-morning-brief-skill/references/browser-messaging-guide.md`.

**Process**:

1. If a specific channel name is provided ($1), focus on that channel only.
   Otherwise, scan all recently active channels in both WhatsApp and Telegram.

2. **WhatsApp Web**:
   - Navigate to web.whatsapp.com via Chrome
   - Find the specified channel or scan recent channels
   - Identify shared article links (URLs with preview cards)
   - Note the article title, URL, and source channel

3. **Telegram Web**:
   - Navigate to web.telegram.org/k/ via Chrome
   - Find the specified channel or scan recent channels
   - Identify shared article links and posts
   - Note the article title, URL, and source channel

4. **Summarize**:
   - For each article URL, use WebFetch to retrieve the content
   - Generate a 2-3 sentence summary of each article
   - Categorize articles by topic if more than 5 are found

5. **Present as**:
```
CHANNEL DIGEST — [Date]

FROM WHATSAPP:
[Channel Name]
1. "[Article Title]" — [2-3 sentence summary]
   Link: [URL]

2. "[Article Title]" — [2-3 sentence summary]
   Link: [URL]

FROM TELEGRAM:
[Channel Name]
1. "[Article Title]" — [2-3 sentence summary]
   Link: [URL]
```

If no articles found in the last 24 hours, report that and offer to look further back.
