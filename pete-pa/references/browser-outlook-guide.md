# Outlook Browser Navigation Guide

Step-by-step instructions for reading Pete's Outlook inbox via Chrome browser tools.

## Prerequisites

- Pete must be signed into outlook.live.com in Chrome
- The Claude in Chrome extension must be active

## Workflow

### Step 1: Navigate to Outlook

```
Navigate to https://outlook.live.com/mail/0/inbox
```

Wait for the page to fully load. If a sign-in page appears, stop and tell Pete
he needs to sign in manually.

### Step 2: Read the Inbox

Use `read_page` with filter "all" to get the inbox contents.
Look for the mail list area — each email typically shows:
- Sender name
- Subject line
- Preview text
- Timestamp
- Read/unread status (unread items are typically bold)

### Step 3: Filter and Extract Unread Emails

Filter for unread emails from the last 24 hours.
Refer to `${CLAUDE_PLUGIN_ROOT}/references/petes-interests.md` for filtering rules.

**Skip entirely** — do not include in results:
- Marketing emails, promotional offers, sale notifications
- Phishing/scam emails ("verify your account", suspicious links)
- Automated service notifications (build alerts, PR merged, etc.)
- Social media notifications (LinkedIn, Twitter/X, Facebook)

**For each remaining unread email:**
1. Note the sender, subject, and preview
2. If the preview mentions a date, deadline, or commitment, flag it
3. Classify priority: HIGH (from known contacts, urgent keywords), MEDIUM, LOW

### Step 4: Read Important Emails (Optional)

If Pete wants more detail on specific emails:
1. Click on the email in the list
2. Use `read_page` or `get_page_text` to read the full body
3. Extract any dates, times, locations, or action items

## Date Extraction Patterns

For comprehensive date extraction patterns, refer to `${CLAUDE_PLUGIN_ROOT}/references/date-patterns.md`.

## Error Handling

- If Outlook shows a CAPTCHA or verification, stop and inform Pete
- If the inbox is empty or the page structure is unexpected, try refreshing once
- If still failing, skip Outlook and note it in the briefing
