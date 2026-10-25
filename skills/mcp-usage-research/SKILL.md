---
name: mcp-usage-research
description: Analyze how real users and AI agents use Sentry's MCP server to surface usage patterns, popular tools, client mix, friction, and failure points. Use when asked "how is the MCP server used", "MCP usage research", "MCP tool usage", "which MCP clients", "how do agents use our MCP server", "MCP server adoption", "what tools are called most", "MCP error rates", "tool call analysis", or "API/MCP usage research". Server-side analog of replay-ux-research for programmatic (non-browser) usage.
argument-hint: '<scope: a tool name, client, or "all">'
---

# MCP Usage Research

Analyze server-side telemetry from Sentry's MCP server to understand how external users and AI agents actually use it — which tools they call, in what sequences, from which clients, and where they hit errors or friction. This is the API/MCP analog of `replay-ux-research`: there are no browser replays, so the evidence is spans in the `mcp-server` project rather than recorded sessions.

## Inputs

`$ARGUMENTS` is the research scope. It can be:

- A **single tool** (e.g., `search_events`, `search_issues`) — deep-dive one tool's usage and reliability.
- A **client** (e.g., `claude-code`, `cursor-vscode`, `codex-mcp-client`) — how one client/agent uses the server.
- A **theme** (e.g., "errors", "adoption", "onboarding funnel").
- `all` or empty — a broad usage overview across the whole server.

If `$ARGUMENTS` is empty, ask the user what scope to research, offering the options above.

## Prerequisites

This skill requires the Sentry MCP server to be connected and authenticated. Tools used:

- `search_events` — query spans in the `mcp-server` project (the core data source)
- `search_issues` / `get_sentry_resource` — investigate errors behind failing tool calls
- `find_projects` — confirm the `mcp-server` project slug if needed

If these tools are unavailable, ask the user to connect/authenticate the Sentry MCP server before proceeding. Read `references/mcp-data-model.md` for the exact org, project, dataset, span schema, and query templates — **load it before running any query**.

## Step 1: Frame the scope and pull the usage baseline

Read `references/mcp-data-model.md`. Establish the baseline before drilling in:

1. **Tool/method distribution** — group `span.op:mcp.server` by `span.description` to see which methods and tools dominate (the description holds method + tool, e.g. `tools/call search_events`; `mcp.tool.name` is null, do not use it).
2. **Client mix** — group by `mcp.client.name` / `mcp.client.version` to see which agents/clients drive usage (claude-code, Cursor, codex, Replit, CodeRabbit, etc.).
3. **Transport mix** — group by `mcp.transport` to split **remote/hosted** (`WorkerTransport`) from **local install** (`stdio`). These are different user populations; report them separately.

Start with the last 24 hours. Extend to 7d or 30d if volume is low or you want trend context. Use aggregate queries (`count()`) for distributions — they are cheap and cover 100% of traffic, unlike the sampled detail rows.

## Step 2: Scope-specific drill-down

Narrow to `$ARGUMENTS`:

- **Single tool**: filter `span.description:"tools/call <tool>"`. Pull call volume, the ok vs `internal_error` split (`span.status`), duration percentiles, and which clients call it.
- **Client**: filter `mcp.client.name:<client>`. Pull that client's tool distribution, method mix, error rate, and version spread.
- **Theme / all**: keep the cross-cutting baseline from Step 1 and prioritize the lenses in Step 4.

## Step 3: Reconstruct journeys (sequences)

There is **no session attribute** — each MCP request is its own trace. Reconstruct journeys by grouping a user's calls over time:

1. Pick active users via `user.id` (the authenticated Sentry account id; it is the closest thing to a "who").
2. For a sample of high-activity `user.id`s, pull their `span.op:mcp.server` rows ordered by `timestamp` and read the `span.description` sequence.
3. Identify common patterns:
   - **Onboarding funnel**: `initialize` → `tools/list` → first `tools/call`. Where do users stop? Many `initialize` with no follow-up `tools/call` = clients that connect but never invoke a tool.
   - **Tool chains**: which tools are called back-to-back (e.g., `find_organizations` → `find_projects` → `search_issues`). These reveal real workflows.
   - **Retry loops**: the same tool called repeatedly in quick succession by one user, especially after an `internal_error` — a friction signal.

Always note this is a per-`user.id` reconstruction, not a true session, and that local `stdio` traffic may lack a stable `user.id`.

## Step 4: Analyze usage through these lenses

### Adoption & population
1. **Client/agent mix**: which clients dominate, and is usage concentrated or broad? Note long-tail/unknown clients.
2. **Local vs remote**: `stdio` (developers running it locally) vs `WorkerTransport` (hosted). Different needs; call out the split.
3. **Version spread**: are users on current client versions, or stuck on old ones (a sign of stale installs)?

### What users do
1. **Tool popularity**: the head of the `tools/call` distribution is the product. What are the top 5 tools and what share of calls do they own?
2. **Method mix**: ratio of `tools/call` to discovery calls (`tools/list`, `resources/list`, `prompts/list`) and housekeeping (`ping`, `initialize`). A high discovery-to-call ratio can mean clients poll without acting.
3. **Workflows**: the tool chains from Step 3 — what jobs are users getting done?

### Friction & failure
1. **Error rates**: per tool and per method, the `span.status:internal_error` share. Rank tools by both error *rate* and absolute error *count*. Some methods (e.g. `resources/list`, `prompts/list`) may be near-100% error — flag these as broken capabilities, not user friction.
2. **Latency**: duration percentiles (p50/p95) per tool. Slow tools hurt agent loops. Note that a few extreme outliers (multi-minute durations) exist — prefer percentiles over averages.
3. **Retry/abandonment**: retry loops and `initialize`-without-`tools/call` from Step 3.
4. **Investigate top failures**: for the highest-impact failing tools, use `search_issues` (project `mcp-server`) or `get_sentry_resource` on an issue/trace to find the underlying exception, how many users/events it affects, and whether it's being worked on. Classify each as **broken** (high error rate, likely always fails), **flaky** (intermittent), or **user-driven** (bad input / expected validation errors).

## Step 5: Write the report

Use the template in `references/output-template.md`. Be specific — cite real numbers (call counts, error rates, percentiles) and link to the Sentry query/trace URLs returned by `search_events` so the reader can verify. Separate remote and local populations where they differ. Distinguish **broken capabilities** from **user friction** — they have different owners and fixes.

**Privacy**: `user.id` is a numeric Sentry account identifier. Do not enumerate raw `user.id`s in the report — anonymize to "User A/B/C" or describe by client/behavior. Never include user emails.
