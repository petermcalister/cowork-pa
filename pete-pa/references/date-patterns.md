# Date Extraction Patterns

Comprehensive patterns for identifying dates, deadlines, and commitments in email text.

## Explicit Date Formats

| Pattern | Examples |
|---------|----------|
| Full date | "March 15, 2026", "15 March 2026" |
| Short date | "15/03/2026", "03/15/2026", "15-03-2026" |
| Partial date | "March 15", "15th March", "the 15th" |
| ISO format | "2026-03-15" |
| Day + date | "Friday March 15", "Friday the 15th" |

## Relative Date Expressions

| Pattern | Resolution |
|---------|-----------|
| "today", "this afternoon" | Current date |
| "tomorrow", "tomorrow morning" | Current date + 1 |
| "next [day]" | Next occurrence of that weekday |
| "this [day]" | This week's occurrence |
| "in [N] days/weeks/months" | Current date + N units |
| "end of [month/week/quarter]" | Last day of the period |
| "beginning of [month]" | 1st of that month |
| "mid-[month]" | 15th of that month |

## Deadline Indicators

These phrases signal a date is a deadline or commitment:

- "due by", "due on", "due date"
- "deadline", "deadline is"
- "submit by", "submit before"
- "no later than", "NLT"
- "by end of day", "by EOD", "by COB"
- "RSVP by", "respond by"
- "expires on", "expiration date"
- "must be completed by"
- "final date for"

## Meeting / Appointment Indicators

- "let's meet on", "let's schedule for"
- "how about [day] at [time]"
- "appointment on", "appointment for"
- "booked for", "reserved for"
- "interview on", "call scheduled for"
- "catch up on [day]"

## Event / Social Indicators

- "you're invited to", "invitation to"
- "save the date"
- "join us on", "join us for"
- "party on", "celebration on"
- "birthday on", "birthday is"
- "anniversary on"

## Time Patterns

| Pattern | Examples |
|---------|----------|
| 12-hour | "3pm", "3:00 PM", "3:30pm" |
| 24-hour | "15:00", "15:30" |
| Descriptive | "morning", "afternoon", "evening", "noon", "midnight" |
| Range | "2-3pm", "between 10 and 11", "10am to noon" |

## Confidence Scoring

- **HIGH**: Explicit date + deadline/meeting indicator + specific time
- **MEDIUM**: Explicit date without time, or relative date with clear context
- **LOW**: Vague relative dates ("sometime next week"), inferred deadlines
