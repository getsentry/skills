# MCP Server Span Data Model

How MCP usage is recorded in Sentry, and the queries to read it. Verified 2026-06-12 against the `sentry` org's `mcp-server` project. These are point-in-time facts — re-verify attribute names if a query returns unexpectedly empty.

## Connection facts

| Field | Value |
| ----- | ----- |
| Org slug | `sentry` |
| Region URL | `https://us.sentry.io` |
| Project slug | `mcp-server` |
| Dataset | `spans` |
| Unit of analysis | `span.op:mcp.server` (one span per MCP JSON-RPC request) |

There are sibling projects (`mcp-server-test`, `mcp-server-connect-demo`, `spotlight-mcp-server-instrumentation`) — use **`mcp-server`** for production usage.

## Span operations (`span.op`)

| `span.op` | Meaning |
| --------- | ------- |
| `mcp.server` | **Primary unit.** One per inbound MCP request (initialize, tools/list, tools/call, ping, etc.). |
| `mcp.notification.client_to_server` | Client→server notifications. |
| `mcp.execute_tool` | Inner tool-execution span. Note: `mcp.tool.name` is **null** here — get the tool name from the parent `mcp.server` span's `span.description`. |
| `http.server` / `http.client` | Underlying HTTP transport spans (not MCP-semantic). |
| `gen_ai.*` | LLM/agent spans from server-side AI tooling (e.g. Seer). Not user-facing MCP calls. |

## Key attributes on `mcp.server` spans

| Attribute | Example values | Use |
| --------- | -------------- | --- |
| `span.description` | `tools/call search_events`, `tools/list`, `initialize`, `ping` | **Method + tool name.** Best grouping key for "what was called". |
| `mcp.method.name` | `tools/call`, `tools/list`, `initialize`, `ping`, `resources/list`, `prompts/list`, `notifications/initialized` | The JSON-RPC method. May be null on some rows. |
| `mcp.transport` | `WorkerTransport` (remote/hosted), `stdio` (local install), `null` | Splits the user population. |
| `mcp.client.name` | `claude-code`, `cursor-vscode`, `Cursor`, `codex-mcp-client`, `Anthropic/ClaudeAI`, `Replit-Agent-MCP-Client`, `CodeRabbit` | Which agent/client. **Only set on `initialize` spans — null on `tools/call` and most other methods.** To attribute a tool call to a client, join via `user.id` to that user's `initialize` span. |
| `mcp.client.version` | `2.1.175`, `1.0.0` | Version spread / stale installs. |
| `span.status` | `ok`, `internal_error`, `unknown` | Friction signal. `internal_error` = failed call. `unknown` often = in-flight/streaming. |
| `span.duration` | milliseconds | Latency. Has extreme outliers (multi-minute) — use percentiles, not averages. |
| `user.id` / `user` | `1234567`, `id:1234567` | Authenticated Sentry account id — the "who" and the journey key. |
| `timestamp` | ISO 8601 | Order calls to reconstruct sequences. |

**Attributes that do NOT exist / are unreliable:**
- `mcp.tool.name` — null; use `span.description`.
- `mcp.session.id` — does not exist. Each call is its own trace; group by `user.id` + `timestamp` for journeys.

## Tool-call arguments (`mcp.request.argument.*`)

The arguments a client passed to a `tools/call` are captured as per-parameter attributes named `mcp.request.argument.<paramName>`, where the attribute *value* is the JSON-encoded argument (strings arrive quoted, e.g. `"resolved"`). This lets you analyze **what** agents do, not just which tool they called. Attribute names mirror the tool's input schema, so they vary per tool — e.g. for `update_issue`: `mcp.request.argument.status`, `mcp.request.argument.issueId`, `mcp.request.argument.organizationSlug`; for `search_events`: `mcp.request.argument.query`, `mcp.request.argument.dataset`.

Use this to characterize usage and find bulk/loop opportunities:
```
query:  span.op:mcp.server span.description:"tools/call update_issue"
fields: ["mcp.request.argument.status", "count()"]
sort:   -count()
```

Caveats:
- Only arguments the client actually sent are present; omitted optional params are absent (use `has:mcp.request.argument.<param>` to filter). A grouping will show `null` for rows where that param wasn't passed.
- Values are JSON-encoded (quoted strings). Don't assume the exact attribute name — confirm it by first fetching a few individual rows with candidate fields, since names depend on the tool's schema and may change as tools evolve.
- Treat argument values as potentially sensitive (they can contain user queries, IDs, free text). Do not reproduce raw values verbatim in reports beyond what's needed to make the point.

## Query templates

All via `search_events` with `organizationSlug:'sentry'`, `projectSlug:'mcp-server'`, `dataset:'spans'`, `regionUrl:'https://us.sentry.io'`. Pass explicit `fields` to avoid the agent guessing the wrong column.

**Tool/method distribution (baseline):**
```
query:  span.op:mcp.server
fields: ["span.description", "count()"]
sort:   -count()
```

**Client mix:**
```
query:  span.op:mcp.server has:mcp.client.name
fields: ["mcp.client.name", "mcp.client.version", "count()"]
sort:   -count()
```

**Transport split:**
```
query:  span.op:mcp.server
fields: ["mcp.transport", "count()"]
sort:   -count()
```

**Per-tool reliability (one tool):**
```
query:  span.op:mcp.server span.description:"tools/call search_events"
fields: ["span.status", "count()"]
sort:   -count()
```

**Per-tool latency:**
```
query:  span.op:mcp.server span.description:"tools/call search_events"
fields: ["p50(span.duration)", "p95(span.duration)", "count()"]
```

**One user's journey (sequence):**
```
query:  span.op:mcp.server user.id:<id>
fields: ["timestamp", "span.description", "span.status", "span.duration"]
sort:   timestamp
```

**Active users to sample:**
```
query:  span.op:mcp.server mcp.method.name:tools/call
fields: ["user.id", "count()"]
sort:   -count()
```

## Gotchas

- **The `search_events` agent rewrites natural-language queries** and may substitute the wrong field (it guessed `gen_ai.tool.name` and `has:gen_ai.tool.name` during development, returning zero rows). Prefer explicit Sentry search syntax in `query` plus explicit `fields`. If a result is surprisingly empty, check whether the agent's "Executed Search" line changed your filter.
- **Aggregates cover all traffic; detail rows are sampled.** Use `count()` groupings for distributions and reliability; use individual-row fetches only for journey reconstruction and examples.
- **`internal_error` is not always a server bug.** It can include client cancellations, auth failures, and validation errors. Confirm root cause via `search_issues`/`get_sentry_resource` before calling a tool "broken".
- **Some methods are near-100% error** (e.g. `resources/list`, `prompts/list`, `resources/templates/list` showed high `internal_error`). Treat persistent full-method failure as a broken capability to flag, distinct from per-tool user friction.
- **Local (`stdio`) traffic** may lack a stable `user.id` and is a different population from hosted (`WorkerTransport`). Report them separately.
- **Employee/dogfood traffic is mixed in.** Unlike replays, there is no clean email-domain filter on spans. If the user wants external-only usage, check at runtime whether a `user.email` attribute is available to filter; otherwise state that the sample includes Sentry-internal usage.
