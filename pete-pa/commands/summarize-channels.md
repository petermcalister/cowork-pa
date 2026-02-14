---
description: Summarize articles from the cowork-pa WhatsApp channel
allowed-tools: Read, WebFetch, mcp__Claude_in_Chrome__*
argument-hint:
---

Scan Pete's "cowork-pa" WhatsApp channel for shared articles and provide summaries.

Read the browser guide: `${CLAUDE_PLUGIN_ROOT}/references/browser-whatsapp-guide.md`.

**Process**:

1. Navigate to web.whatsapp.com via Chrome browser tools
2. Locate and open the "cowork-pa" channel
3. Identify shared article links from the last 24 hours
4. Use WebFetch to read each article, then summarize in 2-3 sentences
5. Categorize articles by topic if more than 5 are found

If no articles found in the last 24 hours, report that and offer to look further back.
