---
name: brand-guidelines
description: Write copy following Sentry brand guidelines. Use when writing UI text, error messages, empty states, onboarding flows, 404 pages, documentation, marketing copy, or any user-facing content. Covers both Plain Speech (default) and Sentry Voice tones.
---

# Brand guidelines

Write user-facing copy following Sentry's brand guidelines.

## Tone selection

Choose the appropriate tone based on context:

| Use plain speech | Use Sentry Voice |
|------------------|------------------|
| Product UI (titles, buttons, labels, filters, search, tables) | 404 and 500 pages |
| Documentation | Empty states with an actionable first line |
| Error messages, toasts, alerts, and callouts | Product tours and occasional onboarding copy |
| Settings pages | Loading states of 30 seconds or longer |
| Transactional emails and Seer responses | "What's New" announcements |
| Help text | Marketing copy |

**Default to Plain Speech** unless the context specifically calls for personality.
Use personality sparingly in onboarding and empty states. Keep task instructions clear and put the information users need before any joke. Reserve loading-state humor for waits of 30 seconds or longer.

## Plain speech (default)

Plain Speech is clear, direct, and functional. Use it for most UI elements.

### Rules

1. **Be concise** - Use the fewest words needed without removing useful information
2. **Be direct** - Tell users what to do, not what they can do
3. **Use active voice** - "Save your changes" not "Your changes will be saved"
4. **Avoid jargon** - Use simple words; explain or link to unfamiliar concepts
5. **Be specific** - "3 errors found" not "Some errors found"
6. **Be accurate** - Avoid aspirational claims and preserve uncertainty when the outcome is uncertain

### Examples

| Instead of | Write |
|------------|-------|
| "Click here to save your changes" | "Save" |
| "You can filter results by date" | "Filter by date" |
| "An error has occurred" | "Something went wrong" |
| "Please enter a valid email address" | "Enter a valid email" |
| "Are you sure you want to delete?" | "Delete this item?" |

## Sentry Voice

Sentry Voice adds personality in appropriate moments. It's empathetic, self-aware, and occasionally snarky.

### Principles

1. **Empathetic snark** - Direct frustration at the situation, never the user
2. **Self-aware** - Acknowledge the absurdity of software
3. **Fun but functional** - Personality should enhance, not obscure meaning
4. **Earned moments** - Only use when users have time to appreciate it

### Examples

**404 pages:**
> "This page doesn't exist. Maybe it never did. Maybe it was a dream. Either way, let's get you back on track."

**Empty states:**
> "Create your first project to start tracking errors. Enjoy the peace and quiet while it lasts."

**Onboarding:**
> "Let's get your first error. Don't worry, it's not as scary as it sounds."

**Loading states:**
> "Crunching the numbers..."
> "Fetching your data..."

### When to avoid Sentry Voice

- Error messages (users are frustrated)
- Settings pages (users are focused)
- Documentation (users need information)
- Billing/payment flows (users need trust)

## General rules

### Spelling and grammar

- Use **American English** spelling (color, not colour)
- Use **Sentence case** for headings, page titles, body text, buttons, and labels, including chart axes, legends, table headers, sidebar items, and default widgets
- Preserve proper nouns, canonical product names (Sentry, Session Replay), acronyms, and technical notation

### Punctuation

- **Use exclamation marks sparingly** and avoid unusual punctuation such as interrobangs
- **No periods** in headings, short UI labels, or button text; keep question marks for questions
- **Use periods** in complete sentences and help text
- **No ALL CAPS** for ordinary words; preserve acronyms (API, SDK, URL) and canonical names
- Remove `text-transform: uppercase` from product UI

### Word choices

| Avoid | Prefer |
|-------|--------|
| Please | (omit) |
| Sorry | (be specific about the problem) |
| Error occurred | Something went wrong |
| Invalid | (explain what's wrong) |
| Success! | (describe what happened) |
| Oops | (be specific) |

## Dash usage

| Type | Use | Example |
|------|-----|---------|
| Hyphen (`-`) | Compound words and compound numbers | "self-serve", "sixty-five" |
| En dash (`&ndash;`) | Time ranges, without spaces | `2020&ndash;2022` |
| Em dash (`&mdash;`) | A break in a sentence or a parenthetical aside | `Errors&mdash;even small ones&mdash;matter` |

Use the appropriate dash character or HTML entity, rather than repeated hyphens. Use colons and semicolons only when their meaning is clear.

## UI element guidelines

### Buttons

- Use action verbs: "Save", "Delete", "Create"
- Be specific: "Create project" not just "Create"
- Follow the [Icons + CTA copy table](https://sentry.sentry.io/scraps/core/button#icons) for established terms and icons. Use "Create [object]" with a plus icon for dashboards, views, and monitors; use "Edit" with a pencil icon for dashboards, views, monitors, and automations
- Max 2-3 words when possible
- No periods; use question marks only for questions and exclamation marks sparingly

### Error messages

1. Say what happened
2. Say why (if helpful)
3. Say what to do next

**Good:** "Could not save changes. Check your connection and try again."
**Bad:** "Error: Save failed."

### Empty states

1. Start with an actionable line that explains what belongs here and how to populate it
2. Add Sentry Voice only when it helps; keep humor in a heading or second sentence without obscuring the action

**Good:** "No projects yet. Create your first project to start tracking errors."

### Confirmation dialogs

- Make the action clear in the title
- Explain consequences if destructive
- Use specific button labels ("Delete project", not "OK")

### Tooltips and help text

- Keep under 2 sentences
- Explain the "why", not just the "what"
- Link to docs for complex topics

## Anti-patterns

Avoid these common mistakes:

- **Robot speak:** "Item has been successfully deleted" -> "Deleted"
- **Passive voice:** "Changes were saved" -> "Changes saved"
- **Unnecessary words:** "In order to" -> "To"
- **Unsupported certainty:** Use "may" or "might" when an outcome is uncertain; use "will" only when it is certain
- **Double negatives:** "Not unlike..." -> "Similar to..."
- **Marketing speak in UI:** "Supercharge your workflow" -> "Speed up your workflow"

## References

- [In-app content and voice guidance](https://github.com/getsentry/sentry/blob/master/static/app/components/core/principles/content-and-voice/contentAndVoice.mdx)
- [Sentry voice guide](https://live.standards.site/sentry/voice)
- [Sentry Frontend Handbook](https://develop.sentry.dev/frontend/)
