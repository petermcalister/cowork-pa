# WhatsApp & Telegram Browser Navigation Guide

Step-by-step instructions for reading messaging channels via Chrome browser tools.

## WhatsApp Web

### Prerequisites
- Pete must be signed into web.whatsapp.com in Chrome
- The browser session must be linked to his phone

### Workflow

1. **Navigate**: Go to `https://web.whatsapp.com`
2. **Wait for load**: The page may take a few seconds to sync. Wait for the chat list.
3. **Find channels/groups**: Use `find` tool to locate specific group names or channels
4. **Open a channel**: Click on the channel/group name in the sidebar
5. **Read messages**: Use `get_page_text` or `read_page` to read recent messages
6. **Extract articles**: Look for shared links (URLs) in messages
   - Links often appear with preview cards (title, description, thumbnail)
   - Note the URL, title, and which group it came from
7. **Summarize articles**: For each article URL:
   - Use WebFetch to read the article content
   - Generate a 2-3 sentence summary
   - Note the source channel/group

### Identifying Articles vs Chat

Articles are typically:
- URLs with preview cards
- Shared from news sites, blogs, or media outlets
- Often shared without much additional commentary
- May have YouTube links, Medium posts, news articles, etc.

Skip:
- Regular chat messages
- Memes, images without links
- Voice messages
- Status updates

## Telegram Web

### Prerequisites
- Pete must be signed into web.telegram.org in Chrome

### Workflow

1. **Navigate**: Go to `https://web.telegram.org/k/` (K-version is more reliable)
2. **Wait for load**: Let the interface fully render
3. **Find channels**: Use `find` tool to locate channels in the left sidebar
4. **Open a channel**: Click on the channel name
5. **Read posts**: Use `get_page_text` to read recent channel posts
6. **Extract articles**: Same approach as WhatsApp — look for URLs and preview cards
7. **Summarize**: Fetch and summarize each article

### Telegram Channel Types

- **Channels** (broadcast): Usually contain articles, news, curated content — PRIMARY TARGET
- **Groups** (chat): May contain articles mixed with discussion
- **Bots**: Skip unless Pete specifically mentions one

## Common Error Handling

- If QR code scan is required, stop and inform Pete
- If the page shows "Phone not connected" (WhatsApp), inform Pete
- If messages haven't synced, wait up to 15 seconds, then move on
- If a specific channel can't be found, skip it and note in the briefing
- For article fetch failures, note the URL and move on

## Rate Limiting

- Don't rapid-fire navigate between many channels
- Wait 2-3 seconds between page navigations
- Limit to the 5 most recent articles per channel unless Pete asks for more
