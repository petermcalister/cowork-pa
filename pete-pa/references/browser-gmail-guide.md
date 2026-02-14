# Gmail Browser Navigation Guide

Step-by-step instructions for reading Pete's Gmail inbox via Chrome browser tools.

## Prerequisites

- Pete must be signed into mail.google.com in Chrome
- The Claude in Chrome extension must be active

## Workflow

### Step 1: Navigate to Gmail

```
Navigate to https://mail.google.com/mail/u/0/#inbox
```

Wait for the page to fully load. If a sign-in page appears, stop and tell Pete
he needs to sign in manually.

### Step 2: Read the Inbox

Use `read_page` with filter "all" to get the inbox contents.
The inbox list typically shows:
- Sender name (bold if unread)
- Subject line
- Message preview/snippet
- Timestamp
- Star/importance markers

### Step 3: Filter for Unread Emails

Focus on unread emails from the last 24 hours.
Unread messages appear in **bold** in the mail list.

To search for specific timeframes, use Gmail's search bar:
1. Use `find` to locate the search input at the top of the page
2. Type a search query such as:
   - `is:unread newer_than:1d` — unread from last 24 hours
   - `is:unread newer_than:7d` — unread from last 7 days
   - `is:starred` — starred/flagged messages
3. Press Enter to filter

### Step 4: Extract Email Details

For each unread email in the inbox list:
1. Note the sender, subject, and preview snippet
2. If the preview mentions a date, deadline, or commitment, flag it
3. Classify priority:
   - **HIGH**: From known contacts, urgent keywords, starred
   - **MEDIUM**: Work-related, contains dates/deadlines
   - **LOW**: Newsletters, notifications, promotions

### Step 5: Read Full Emails (Optional)

If Pete wants more detail or if date extraction is needed:
1. Click on the email row to open it
2. Use `get_page_text` to read the full email body
3. Extract any dates, times, locations, or action items
4. Use the browser back button or click "Inbox" to return to the list

### Step 6: Search for Specific Content

To find emails containing dates or commitments:
1. Use the search bar with queries like:
   - `deadline` or `due by` — deadline-related emails
   - `meeting` or `appointment` — meeting-related
   - `RSVP` or `invitation` — event invitations
   - `from:specific@email.com` — from a specific sender

## Date Extraction Patterns

For comprehensive date extraction patterns, refer to `${CLAUDE_PLUGIN_ROOT}/references/date-patterns.md`.

## Error Handling

- If Gmail shows a CAPTCHA or verification prompt, stop and inform Pete
- If the inbox layout is unexpected (e.g. tabbed inbox), try navigating directly to `#inbox`
- If the page is slow to load, wait up to 15 seconds before retrying
- If still failing, skip Gmail and note it in the briefing
