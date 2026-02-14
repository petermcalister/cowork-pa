# WhatsApp Browser Navigation Guide

Step-by-step instructions for reading the "cowork-pa" WhatsApp channel via Chrome browser tools.

## Prerequisites

- Pete must be signed into web.whatsapp.com in Chrome
- The browser session must be linked to his phone
- The "cowork-pa" channel must be in his WhatsApp contacts/groups

## Workflow

### 1. Navigate to WhatsApp Web

```
Navigate to: https://web.whatsapp.com
```

Wait for the page to fully load and sync with Pete's phone (may take 3-5 seconds).

### 2. Locate the "cowork-pa" Channel

Use the `find` tool to search for "cowork-pa":
```
find(query="cowork-pa channel", tabId=...)
```

Or search in the chat list:
- Click on the search box at the top
- Type "cowork-pa"
- Look for the channel/group in the results

### 3. Open the Channel

Click on the "cowork-pa" channel name to open the conversation view.

### 4. Read Recent Messages

Use `get_page_text` or `read_page` to read the most recent messages (last 24 hours recommended).

**Important**: Pete uses this channel to save articles throughout the day for later
reading. Most article links will be posted by Pete himself. Include these — the
digest is Pete's way of getting summaries of articles he bookmarked.

Look for:
- Article links posted by Pete (most common — he saves articles here during the day)
- Articles shared by other channel members
- Important updates or announcements

### 5. Extract Articles

Articles typically appear as:
- URLs with rich preview cards showing:
  - Article title
  - Description/snippet
  - Thumbnail image
  - Source domain
- Shared links from news sites, blogs, Medium, YouTube, etc.

For each article found:
1. Note the URL
2. Note the article title from the preview
3. Note who shared it and when (often Pete himself)
4. Use WebFetch to read the full article content

### 6. Summarize Articles

For each article:
- Generate a 2-3 sentence summary covering:
  - Main topic/thesis
  - Key findings or takeaways
  - Relevance to Pete's work or interests
- Include the source and who shared it

### 7. Post Reports/Highlights (When Requested)

When Pete asks you to post a report or highlight to the "cowork-pa" channel:

1. Locate the message input box at the bottom of the channel
2. Click to focus the input
3. Type the message content
4. Click the send button

## Identifying Articles vs Regular Chat

Refer to `${CLAUDE_PLUGIN_ROOT}/references/petes-interests.md` for topic priorities.

**Include in digest** (prioritise engineering/tech content):
- Engineering blog posts, architecture deep-dives, system design articles
- AI/ML, LLM, and developer tooling articles
- Cloud, DevOps, and platform engineering content
- Open source project announcements and releases
- Technical documentation, tutorials, and research papers
- YouTube videos with engineering/tech content
- Medium posts, Substack newsletters on tech topics

**Skip:**
- Regular chat messages and casual conversation
- Memes or images without links
- Voice messages, status updates
- Personal messages between members
- Non-engineering content (lifestyle, sports, entertainment) unless Pete adds those keywords later

## Error Handling

- **QR code appears**: Stop and inform Pete that he needs to scan the QR code on his phone
- **"Phone not connected"**: Inform Pete to check his phone's internet connection
- **Messages not syncing**: Wait up to 15 seconds, then move on
- **"cowork-pa" channel not found**: Check spelling, ask Pete for the exact channel name
- **Article fetch fails**: Note the URL and title, but continue with other articles
- **Can't load preview**: Use WebFetch with just the URL

## Rate Limiting & Best Practices

- Wait 2-3 seconds between page navigations
- Limit to the 5 most recent articles unless Pete asks for more
- Don't scroll too far back (focus on last 24 hours)
- If there are too many messages, use the search function to filter for links

## Posting Guidelines

When posting to "cowork-pa":
- Keep messages concise and professional
- Use clear formatting (bullet points, headers if needed)
- Never post sensitive information (credentials, private data)
- Include relevant context so other channel members understand
