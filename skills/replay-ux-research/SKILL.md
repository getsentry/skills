---
name: replay-ux-research
description: Analyze Sentry session replays to surface UX patterns, pain points, and user journeys for a given product area. Use when asked to "show me how users use", "day in the life", "UX research", "replay research", "how do customers use", "what's the user experience like for", "watch replays of", "analyze replays for", "user behavior on", or "replay UX audit" for any Sentry product surface.
argument-hint: '<product-area>'
---

# Replay UX Research

Analyze session replays from real external users of sentry.io to surface UX patterns, pain points, and representative journeys for a given product area. This uses Sentry's own dogfooding org.

## Inputs

`$ARGUMENTS` is the product area to research (e.g., "issues", "alerts", "dashboards", "performance", "replays", "crons", "releases", "insights").

If `$ARGUMENTS` is empty, ask the user which product area to research.

## Prerequisites

This skill requires the Sentry MCP server to be connected. The following tools are used:
- `search_events` — Search for session replays
- `get_replay_details` — Get detailed replay information
- `search_issues` — Look up error issues
- `get_sentry_resource` — Fetch issue details from URLs

If these tools are not available, ask the user to connect the Sentry MCP server before proceeding.

## Step 1: Map product area to URL patterns

Read `references/product-areas.md` and find the URL patterns for the requested area.

If the product area is not listed, infer a URL pattern from the area name. Most Sentry product areas follow the pattern `/<area-name>/` in the URL path. The reference file may not cover newer product areas — confirm your assumption with the user if unclear.

## Step 2: Search for replays

Search for replays from external (non-Sentry-employee) users. 25 replays is a good starting point — go deeper if the product area is complex, if early patterns are ambiguous, or if the user wants a more comprehensive picture.

Start with last 24 hours — extend to 48h or 7d if needed to reach your target count. Run multiple `search_events` calls if needed. Use `limit: 50` per call.

**If you can't find enough replays** (fewer than 10 even at 7 days), tell the user what you found and ask them to help iterate — they may suggest broader URL patterns, a different time range, or a related product area to include.

**Query construction:**

Use natural language queries like:

```
replays from the last 24 hours where url contains "/<area-path>" excluding user emails ending in @sentry.io and @getsentry.com
```

Key filters:

- **Time range**: last 24 hours (extend if needed)
- **URL pattern**: match the product area paths from Step 1
- **Exclude employees**: `-user.email:*@sentry.io -user.email:*@getsentry.com`
- **Environment**: prod

Do NOT pass a `projectSlug` filter — replays span the whole org.

## Step 3: Get replay details

Call `get_replay_details` for each replay found in Step 2. Run these calls in parallel batches for speed.

For each replay, capture:

- **User**: email domain only (the API returns full emails — never include these in output)
- **Journey**: ordered list of pages visited (from URLs and activity breadcrumbs)
- **Duration**: total session length
- **Replay type**: `session` (randomly sampled from normal browsing) vs `buffer` (triggered by an event — error, manual flush, or specific user action like submitting feedback or going through checkout). Note this distinction in your analysis since buffer replays are biased toward error/action moments, not typical browsing.
- **Entry context**: first URL tells you how they arrived — look for referrer signals like `referrer=slack`, `notification_uuid`, `alert_rule_id` in query params (Slack notification), email link patterns, or bare URLs (bookmark/direct nav)
- **Engagement signals**: error count, rage clicks, dead clicks, warning count
- **Browser/OS/Device**: for device distribution context
- **Activity breadcrumbs**: page views, navigation patterns, key interactions

## Step 4: Investigate significant errors

After collecting replay details, identify errors that appear in multiple replays or seem likely to affect the user experience. For each significant error:

1. **Triage by frequency**: If the same issue ID (e.g., `JAVASCRIPT-33RM`) appears in 3+ replays, it's worth investigating.
2. **Check the issue in Sentry**: Use `search_issues` to find the issue, or `get_sentry_resource` with the issue URL from the replay details. Understand:
   - What is the error? (message, stack trace context)
   - How many total users/events does it affect? (beyond just this replay sample)
   - Is it assigned or being worked on?
3. **Infer user-facing impact from behavioral signals**: We cannot see the rendered page content through replay metadata — only by watching the replay in-browser. Instead, infer impact from what users did _after_ the error:
   - **Retried the same action** → they likely saw a failure and tried again
   - **Navigated away immediately** → they were blocked or gave up
   - **Continued their flow normally** → the error may be silent/cosmetic
   - **Rage-clicked or dead-clicked after** → the UI may have become unresponsive
   - **Spent a long time on the page after** → they may be reading an error message or confused
   - **No behavioral change at all** → error was likely invisible to the user
4. **Classify each error** based on this evidence:
   - **Likely blocking**: Error + user retried/left/couldn't continue. High confidence of user impact.
   - **Likely degrading**: Error + user continued but with unusual behavior. Moderate confidence.
   - **Likely silent**: Error fired but user behavior was unaffected. Low confidence of user impact.
   - **Unclear**: Not enough behavioral signal to judge. Flag for manual replay review.

   Always note the confidence level and recommend watching specific replays to confirm. Link directly to the replay URL for each classified error.

Include this classification in the Friction & Pain Points section. Don't report likely-silent errors as pain points — list them in a separate "Background Errors (likely silent)" subsection for completeness.

## Step 5: Analyze patterns

Look at the replays through these UX research lenses:

### Behavioral patterns

1. **Common journeys**: What navigation paths do users take? What's the typical flow?
2. **Entry points**: How do users arrive? Categorize: alert notification (Slack/email), direct bookmark, organic navigation from another page. The first URL's query params reveal this.
3. **Task completion**: Did the user appear to accomplish a goal, or did they wander/abandon? Signs of completion: navigating to a detail view then leaving. Signs of abandonment: short session, back-and-forth navigation, leaving from the same page they entered.
4. **Time on task**: How long do users spend on key pages before acting?

### Friction & discovery

1. **Friction signals**: Rage clicks, dead clicks, errors — but also _hesitation_ (visiting the same page repeatedly), _thrashing_ (rapid back-and-forth between pages), and _retry loops_ (repeating the same action sequence).
2. **Feature discovery**: Are users finding sub-features (filters, search, sort, bulk actions) or only using the primary view? Look at URL query params and breadcrumbs for evidence of feature use.
3. **User intent signals**: Mine URL query params for search terms, filter values, sort orders, and date ranges users set. These are the closest thing to verbatim user "quotes" — they reveal what users are looking for in their own words. (e.g., `query=is%3Aunresolved+assigned%3Ame` tells you the user is triaging their own assigned issues.)
4. **Workarounds**: Any unexpected navigation patterns that suggest a missing feature or confusing flow? (e.g., going to settings mid-task, opening multiple pages in sequence that could be one view)
5. **Error recovery**: When users encounter errors, do they recover and continue or abandon?

### Context

1. **Replay trigger mix**: What proportion are `session` (random sample) vs `buffer` (event-triggered)? Buffer replays show moments where something notable happened (error, feedback submission, checkout, etc.) — they're valuable for friction analysis but aren't representative of typical browsing. Call out this bias when drawing conclusions.
2. **Return visitors**: Do any email domains appear in multiple replays? Repeat visitors suggest habitual usage — their journeys may reveal power-user patterns or persistent pain points they've learned to work around.
3. **User diversity**: Are replays from many different orgs/companies or concentrated? Are there differences in behavior by org?
4. **Device/browser distribution**: What are users primarily using?
5. **Drop-off points**: Where do users leave or navigate away?

## Step 6: Write the report

Use the template in `references/output-template.md`. Be specific — cite individual replays as evidence for each pattern. Link to replay URLs so the reader can watch the replay themselves.

**Privacy**: Never include full user email addresses in the report. Use anonymized identifiers like "user from [company domain]" or "User A, B, C."
