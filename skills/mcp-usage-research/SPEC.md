# MCP Usage Research Specification

## Intent

Give Sentry teams a UX-research-style view of how their MCP server is *actually* used, for usage that is purely programmatic (AI agents and API clients) and therefore invisible to browser session replays. It is the server-side counterpart to `replay-ux-research`: same questions (who, what jobs, what friction, what to fix), different evidence (spans in the `mcp-server` project instead of recorded sessions).

## Scope

In scope:
- MCP server usage recorded as `mcp.server` spans in the `sentry` org's `mcp-server` project.
- Tool/method distributions, client and transport mix, version spread.
- Per-`user.id` journey reconstruction, error/failure analysis, latency, retry/abandonment.

Out of scope:
- Browser/UI usage — that is `replay-ux-research`.
- Non-MCP public REST API usage. **Extension point**: the same skill shape (baseline distribution → drill-down → journeys → friction → report) applies to REST-API telemetry once its data source is identified (likely `http.server` spans in the relevant API project). When adding it, add a sibling data-model reference and a scope branch; keep MCP and REST sections of any report separate.

## Users And Trigger Context

- Primary users: Sentry engineers/PMs who own the MCP server or its tools.
- Common user requests: "how is the MCP server used", "which tools/clients are most popular", "MCP error rates", "how do agents use our MCP server".
- Should not trigger for: browser UX questions (use `replay-ux-research`), generic Sentry issue triage, or non-Sentry MCP servers.

## Runtime Contract

- Required first actions: confirm Sentry MCP is authenticated; load `references/mcp-data-model.md` before querying.
- Required outputs: a report following `references/output-template.md`, citing real numbers and Sentry query/trace links.
- Non-negotiable constraints: never enumerate raw `user.id`s or user emails; separate remote (`WorkerTransport`) from local (`stdio`) populations; distinguish broken capabilities from user friction.
- Expected bundled files loaded at runtime: `references/mcp-data-model.md`, `references/output-template.md`.

## Source And Evidence Model

Authoritative sources:
- `mcp.server` spans (`mcp-server` project, `spans` dataset) via `search_events`.
- Underlying exceptions via `search_issues` / `get_sentry_resource` for failure root-cause.

Data that must not be stored:
- Raw `user.id` lists, user emails, secrets, or any customer data. Anonymize to "User A/B/C" in outputs.

## Reference Architecture

- `SKILL.md` contains: the runtime workflow (scope → baseline → drill-down → journeys → lenses → report).
- `references/` contains: `mcp-data-model.md` (span schema, attributes, query templates, gotchas) and `output-template.md` (report structure).

## Validation

- Lightweight: queries return non-empty aggregates for `span.op:mcp.server`; report sections are populated with real numbers.
- Deeper: at least one failing tool is root-caused via an issue/trace link; remote vs local split is reported.
- Acceptance gates: no raw identifiers in output; broken-capability vs user-friction distinction made.

## Known Limitations

- No native MCP session attribute; journeys are approximate (`user.id` + timestamp).
- `internal_error` conflates server bugs, client cancellations, auth, and validation errors.
- Mixed audience: spans include Sentry-internal/dogfood usage with no clean employee filter.
- Span attribute names are point-in-time; re-verify if queries return empty.

## Maintenance Notes

- Update `SKILL.md`: when the workflow or lenses change, or when REST-API scope is added.
- Update `references/mcp-data-model.md`: when span attribute names, `span.op` values, or connection facts change (the MCP instrumentation evolves).
- Update `references/output-template.md`: when the report's required sections change.
