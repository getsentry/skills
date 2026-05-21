# SPEC — triage-frontend-issues

## Intent

Reduce noise in the `sentry/javascript` issue queue by archiving issues whose root cause is outside our code: third-party libraries, browser/OS quirks, customer-environment interference, transient backend 5xx, test/synthetic events, and single-event flukes.

The skill never resolves, never assigns, never deletes — only archives, only with `untilEscalating`, only after explicit user approval.

## Scope

- **In scope:** the Sentry `javascript` project under the `sentry` organization. Archive-only triage of unresolved issues.
- **Out of scope:** any other project. Any non-archive status change (resolve, assign, delete, escalate). Any auto-apply mode without confirmation. Any change to issue ownership routing. Anything outside Sentry MCP.

## Trigger Context

- User explicitly invokes the skill (`/triage-frontend-issues`) or natural language: "triage the javascript project", "archive non-actionable issues", "clean up the unresolved queue".
- User pastes a `sentry/javascript` issue URL or short ID and asks for a triage decision.

## Source / Evidence Model

The category taxonomy in `references/archive-criteria.md` was synthesized from observed historical archive activity in the `sentry/javascript` project. The activity feed for archived issues was fetched and inspected to determine:

- which `ignoreMode` was used (consistent across the population — drove Hard Rule 3 in `SKILL.md`)
- which kinds of issues are archived versus resolved
- which top-frame and title patterns reliably correspond to non-actionable noise

Boundary cases were established by inspecting `set_resolved` actions in the same project to identify what the team treats as actionable. Specific counts and per-engineer activity are not captured in this repository.

## Reference Architecture

```
triage-frontend-issues/
├── SKILL.md                          # runtime instructions (router)
├── SPEC.md                           # this file (maintenance contract)
└── references/
    └── archive-criteria.md           # category taxonomy with recognition heuristics
```

Runtime always reads `SKILL.md`. The criteria reference is loaded during step 2 (classification). SPEC is not loaded at runtime.

## Evaluation Expectations

A future iteration of this skill should be evaluated against:

1. **Precision on positive cases.** Re-run the skill against historical archived issues and confirm it would archive them with a matching category.
2. **Precision on negative cases.** Re-run against historical resolved issues. The skill must mark these `skip`, never `archive`.
3. **Reason quality.** Sampled archive `reason` strings should name a category from the taxonomy and identify a concrete signal (library, API, endpoint).
4. **No-op safety.** With `cancel` reply, no `update_issue` calls are made.

Hold-out evaluation set should be maintained at `references/evidence/` (not created yet; add when the first false positive is observed).

## Known Limitations

- The skill reads issue metadata via Sentry MCP, but the MCP's `get_sentry_resource` output does not surface the activity feed.
- Determining "who last touched this issue" requires HTTP API calls, which the skill does not perform — it defers to the user when an issue's history matters.
- The skill cannot inspect the full stack trace in machine-readable form; it relies on what `get_sentry_resource` returns in its formatted output.
- Edge cases where the top frame is buried may be misclassified — those are intentionally routed to `needs-human`.
- Title pattern matching is heuristic. Novel third-party libraries or browser quirks will not match existing patterns and should be added to `references/archive-criteria.md` after the first occurrence.
- The category taxonomy is sourced from a single project (`sentry/javascript`). Applying it to a different project requires re-validating the categories.

## Maintenance Notes

- When the user flags a misclassification, capture the example, decide whether the criteria need updating, and update `references/archive-criteria.md`.
- Re-validate the criteria periodically by sampling recent archives and confirming the patterns still apply.
- If Sentry adds new `ignoreMode` options or changes the `update_issue` API surface, update the Hard Rules and the `update_issue` call snippet in `SKILL.md`.
- Do not expand the skill's scope beyond archiving. Resolution, assignment, and deletion belong to other workflows.
