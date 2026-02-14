---
description: Summarize articles from the cowork-pa WhatsApp channel
allowed-tools: Read, Task, WebFetch, mcp__Claude_in_Chrome__*
argument-hint:
---

Scan Pete's "cowork-pa" WhatsApp channel for shared articles and provide summaries.

**Process**:

1. Launch the **whatsapp-scanner** agent: `${CLAUDE_PLUGIN_ROOT}/agents/whatsapp-scanner.md`
2. Present the agent's article summaries in the Channel Digest format
3. Categorize articles by topic if more than 5 are found

If no articles found in the last 24 hours, report that and offer to look further back.
