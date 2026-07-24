# MCP Usage Research: [Scope]

## Overview

**Objective**: Understand how [scope — all usage / tool X / client Y] of Sentry's MCP server is used: what's called, by whom, in what sequences, and where it fails.

**Scope**: [scope], [time range]
**Date**: [today's date]
**Method**: Analyzed `mcp.server` spans in the `mcp-server` project (org `sentry`). Distributions are from aggregate counts (100% of traffic); journeys are reconstructed per `user.id` from sampled rows. See [Methodology & Data](#methodology--data).

## Key Findings

1. [Most important finding — 1-2 sentences, with a number]
2. ...
(aim for 4-6)

## Recommendations

1. **[Recommendation]** — [which finding it addresses, expected impact, likely owner]
2. ...

---

## Adoption & Population

### Client / Agent Mix

| Client | Calls | % | Notes |
| ------ | ----- | - | ----- |
| claude-code | | | |
| cursor-vscode / Cursor | | | |
| codex-mcp-client | | | |
| ... | | | |

[Is usage concentrated in a few clients or broad? Note any large unknown/long-tail clients.]

### Local vs Remote

| Transport | Calls | % | Population |
| --------- | ----- | - | ---------- |
| `WorkerTransport` | | | Hosted / remote |
| `stdio` | | | Local install (developers) |

[Call out behavioral differences between the two populations.]

### Version Spread

[Are clients on current versions? Any notable stale-version tails?]

## What Users Do

### Top Tools

| Tool | Calls | % of `tools/call` | Error rate |
| ---- | ----- | ----------------- | ---------- |
| | | | |

[The head of this list is effectively the product. What share do the top 5 own?]

### Method Mix

[Ratio of `tools/call` to discovery (`tools/list`, `resources/list`, `prompts/list`) and housekeeping (`ping`, `initialize`). High discovery-without-calls = clients polling but not acting.]

### Workflows (Tool Chains)

Common back-to-back tool sequences reconstructed from user journeys:

- `find_organizations` → `find_projects` → `search_issues` — [N users, what job this accomplishes]
- ...

## Friction & Failure

### Broken Capabilities (likely always failing)

Methods/tools with persistent high error rates — these are bugs, not user friction.

- `[method/tool]` — [error rate], [error count] — [underlying issue + link if investigated]

### Failing Tools (user-impacting)

| Tool | Error rate | Error count | Classification | Underlying issue |
| ---- | ---------- | ----------- | -------------- | ---------------- |
| | | | broken / flaky / user-driven | [issue ID + link] |

[For each significant failure, note: what the error is, how many users/events it affects, whether it's assigned. Link the Sentry issue/trace.]

### Latency

| Tool | p50 | p95 | Notes |
| ---- | --- | --- | ----- |
| | | | |

[Slow tools hurt agent loops. Flag p95 outliers. Use percentiles — extreme multi-minute outliers exist.]

### Retry Loops & Abandonment

- **Retry loops**: [tools repeatedly called by one user in quick succession, often after errors]
- **Abandonment**: [share of `initialize` sessions with no following `tools/call` — clients that connect but never invoke]

## Notable Journeys

3-5 illustrative `user.id` sequences (anonymized):

1. **User A** ([client]) — [sequence summary + what it reveals] — [trace/query link]
2. ...

---

## Methodology & Data

### Sample & Coverage

| Item | Value |
| ---- | ----- |
| Time range | |
| Total `mcp.server` spans | |
| Distinct `user.id`s | |
| Distinct clients | |
| Transport split (remote / local) | |

### Limitations

- **No native session**: each request is its own trace; journeys are reconstructed by grouping `user.id` over time and are approximate.
- **`internal_error` ≠ server bug**: may include client cancellations, auth failures, and validation errors. Root cause confirmed only where noted.
- **Mixed audience**: the sample includes Sentry-internal/dogfood usage; there is no clean employee filter on spans. [State whether any filtering was applied.]
- **Local traffic identity**: `stdio` traffic may lack a stable `user.id`, under-representing local-user journeys.
- **Snapshot, not trend**: a single time window. Re-run at other times to compare.

### Appendix: Tool Call Distribution

| Tool / Method | Calls | OK | Error | Error % |
| ------------- | ----- | -- | ----- | ------- |
| | | | | |
