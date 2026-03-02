---
description: Summarize articles from the cowork-pa WhatsApp channel
allowed-tools: Read, WebFetch, mcp__whatsapp__*
argument-hint:
---

Scan Pete's "cowork-pa" WhatsApp channel for shared articles and provide summaries.

**Process**:

1. Call `mcp__whatsapp__list_messages` with `chat_jid: "120363333283720405@g.us"` and `limit: 50` to get recent messages from the cowork-pa group
2. Filter messages from the last 24 hours that contain URLs (article links)
3. For content filtering rules, read `${CLAUDE_PLUGIN_ROOT}/references/petes-interests.md`
4. Use WebFetch to read each article, then summarize in 2-3 sentences
5. Categorize articles by topic if more than 5 are found

If no articles found in the last 24 hours, report that and offer to look further back.
