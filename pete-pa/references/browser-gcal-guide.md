# Google Calendar Browser Navigation Guide

Step-by-step instructions for reading and creating events in Pete's Google Calendar via Chrome browser tools.

## Prerequisites

- Pete must be signed into calendar.google.com in Chrome
- The Claude in Chrome extension must be active

## Part 1: Reading Events

### Step 1: Navigate to Google Calendar

```
Navigate to https://calendar.google.com
```

Wait for the page to fully load. If a sign-in page appears, stop and tell Pete
he needs to sign in manually.

### Step 2: Set the View

Google Calendar can show different views. For the morning briefing:
- **Day view**: Best for today's events — navigate to the day view if not already there
- **Week view**: Best for upcoming 7 days overview

To switch views, use `find` to locate the view selector (typically top-right)
and click Day, Week, or Month as needed.

### Step 3: Read Today's Events

1. Use `read_page` to get the calendar contents
2. Events appear as blocks on the time grid, each showing:
   - Event title
   - Start and end time
   - Calendar colour (for different calendars)
   - Location (if set)
3. All-day events appear at the top of the day column

### Step 4: Read Upcoming Days

To check the next 7 days for birthdays and events:
1. Switch to **Week view** if not already
2. Use `read_page` or `get_page_text` to read all visible events
3. If you need to see the next week, click the forward arrow to advance

### Step 5: Search for Specific Events

To find birthdays, anniversaries, or specific events:
1. Use `find` to locate the search icon (magnifying glass) at the top
2. Click it to open the search bar
3. Type search terms: "birthday", "bday", "anniversary", or a person's name
4. Press Enter to see results
5. Use `read_page` or `get_page_text` to read the search results

## Part 2: Creating Events

### Step 1: Open the Event Creation Form

Option A — Quick create:
1. Click the "+" or "Create" button (usually top-left area)
2. This opens the quick event creation form

Option B — Full form:
1. Click "+" or "Create"
2. Then click "More options" to expand to the full form

### Step 2: Fill in Event Details

Use `find` and `form_input` to populate the fields:

1. **Title**: Enter the event name (e.g. "Project deadline", "Sarah's Birthday")
2. **Date**: Set the start date
   - For all-day events (birthdays, deadlines): toggle "All day" on
   - For timed events: set start and end time
3. **Description**: Add context, such as:
   - Source: "Extracted from email by [Sender] — [Subject]"
   - Any relevant details from the email
4. **Reminders**: Set appropriate reminders
   - Deadlines: 1 day before
   - Meetings: 1 hour before
   - Birthdays: 1 week before

### Step 3: Set Recurrence (Optional)

For birthdays and anniversaries:
1. Click the recurrence/repeat option
2. Select "Annually" or "Every year"
3. Confirm the recurrence pattern

### Step 4: Save the Event

1. Use `find` to locate the "Save" button
2. Click Save
3. Verify the event appears on the calendar by checking the relevant date

## Error Handling

- If the calendar shows a different account, inform Pete and ask which account to use
- If event creation fails (form doesn't submit), capture the event details and present them to Pete so he can add manually
- If the calendar is in a non-English locale, element labels may differ — use `read_page` to identify the correct buttons
- If the page is slow, wait up to 15 seconds before retrying
- Never modify or delete existing events unless Pete explicitly asks

## Tips

- Google Calendar often uses hover and click interactions — use `find` to locate elements by their purpose rather than specific coordinates
- The "Birthdays" calendar (from Google Contacts) is a separate calendar — make sure it's visible in the sidebar if Pete wants contact birthdays
- Colour-coded calendars can help distinguish personal vs work events
