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

### Step 3: Extract Unread Emails

Filter for unread emails from the last 24 hours.
For each unread email:
1. Note the sender, subject, and preview
2. If the preview mentions a date, deadline, or commitment, flag it
3. Classify priority: HIGH (from known contacts, urgent keywords), MEDIUM, LOW

### Step 4: Read Important Emails (Optional)

If Pete wants more detail on specific emails:
1. Click on the email in the list
2. Use `read_page` or `get_page_text` to read the full body
3. Extract any dates, times, locations, or action items

## Date Extraction Patterns

Look for these patterns in email bodies:
- Explicit dates: "March 15", "15/03/2026", "next Tuesday"
- Deadlines: "due by", "deadline", "by end of", "no later than"
- Meetings: "let's meet", "can we schedule", "how about [day/time]"
- Events: "invited to", "RSVP", "save the date"

## Error Handling

- If Outlook shows a CAPTCHA or verification, stop and inform Pete
- If the inbox is empty or the page structure is unexpected, try refreshing once
- If still failing, skip Outlook and note it in the briefing
