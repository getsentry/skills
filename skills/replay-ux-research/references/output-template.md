# Day in the Life: [Product Area] Users

## Overview

**Objective**: Understand how external users interact with [product area] — what they're trying to do, how they navigate, and where they hit friction.

**Scope**: [N] replays from external users, [time range], prod environment
**Date**: [today's date]
**Method**: Analyzed session replay metadata (page views, navigation breadcrumbs, engagement signals) from Sentry's dogfooding org. Replays are from non-employee users only. See [Methodology & Data](#methodology--data) for sample details and limitations.

## Key Findings

1. [Most important UX finding — 1-2 sentences]
2. [Second finding]
3. [Third finding]
(aim for 4-6 findings)

## Recommendations

Concrete, prioritized suggestions based on the evidence below:

1. **[Recommendation]** — [which finding(s) this addresses, expected impact]
2. ...

---

## What Users Are Trying to Do

Jobs-to-be-done inferred from user behavior — search queries, filter combinations, sort orders, and navigation patterns observed across replays. These reveal user intent in their own words:

- `query=is:unresolved assigned:me` — [N users, triaging own assigned issues]
- `sort=date` — [N users, looking at most recent]
- [Navigation pattern] — [N users, what this suggests about their goal]

Include this section when URL params or behavioral patterns reveal clear user intent. Omit if the product area doesn't have meaningful search/filter interactions.

## How Users Arrive & Navigate

### Entry Points

Breakdown of how users arrive (e.g., "60% from Slack alert links, 25% direct/bookmark, 15% navigated from another page"). Cite referrer evidence from URL query params.

### Journey Pattern 1: [Name] (N/total replays)

[Describe the common navigation flow. What pages, in what order, how long. Did users appear to complete their task?]

**Example**: [Link to representative replay] — [brief description of what this user did]

### Journey Pattern 2: [Name] (N/total replays)

...

## Friction & Pain Points

### [Pain point 1]

- **Signal**: [rage clicks / dead clicks / errors / hesitation / thrashing / retry loop]
- **Where**: [specific page or interaction]
- **Impact classification**: [Likely blocking / Likely degrading / Unclear] — [behavioral evidence: what users did after]
- **Issue context**: [Sentry issue ID, total event/user count, assigned?]
- **Evidence**: [links to 2-3 replays showing this] — _watch these to confirm impact_
- **Severity**: [how many users hit this in the sample]

### [Pain point 2]

...

### Background Errors (likely silent)

Errors observed in replays where user behavior showed no signs of impact. Listed for completeness; watch linked replays to verify.

- [Issue ID] — [description] — [N replays] — [why classified as silent: user continued normally, no behavioral change]

## Feature Discovery & Gaps

- **Features actively used**: [list features/sub-pages users navigated to — filters, search, sort, bulk actions, etc.]
- **Features ignored**: [features available but not used by any observed users]
- **Possible workarounds observed**: [any unexpected navigation suggesting a missing feature or confusing flow]

## Notable Replays

3-5 particularly interesting or illustrative replays:

1. [Replay link] — [Why it's notable: great example of X, shows unusual pattern Y, etc.]
2. ...

---

## Methodology & Data

### Sample Composition

| Type                       | Count | %   | Notes                                                                                   |
| -------------------------- | ----- | --- | --------------------------------------------------------------------------------------- |
| `session` (random sample)  |       |     | Representative of normal browsing                                                       |
| `buffer` (event-triggered) |       |     | Triggered by error, feedback submission, checkout, etc. — biased toward notable moments |

[If heavily skewed toward buffer replays, note that findings over-represent error/action moments vs typical browsing.]

### Session Characteristics

| Metric                         | Value |
| ------------------------------ | ----- |
| Median duration                |       |
| Sessions with errors           |       |
| Sessions with rage clicks      |       |
| Sessions with dead clicks      |       |
| Top browsers                   |       |
| Top devices                    |       |
| Unique orgs represented        |       |
| Estimated task completion rate |       |

### Limitations

- **Sample size**: [N] replays over [time range]; this is directional, not statistically significant
- **Sampling bias**: Replays are captured at ~5% session sample rate, plus 100% on errors. [Note session/buffer split and what it means for representativeness]
- **Breadcrumb depth**: Activity breadcrumbs vary in richness per replay — some sessions have sparse data, limiting journey reconstruction
- **No click-level detail**: Breadcrumbs show page views and fetch calls but not every UI interaction. Rage/dead click counts are available but not the specific elements clicked
- **Single time window**: This is a snapshot, not a trend. Run again at different times to compare.
- [Add any other limitations specific to this run]

## Appendix: All Replays Analyzed

| #   | Replay | Domain | Duration | Type           | Pages | Errors | Rage | Dead |
| --- | ------ | ------ | -------- | -------------- | ----- | ------ | ---- | ---- |
| 1   | [link] | ...    | ...      | session/buffer | ...   | ...    | ...  | ...  |
