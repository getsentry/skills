# Authoring Path

Use this path to create or update skill files.

## Runtime Writing Rules

1. Frontmatter must be first line.
2. `name` must match the directory.
3. `description` must contain realistic trigger language.
4. Keep runtime guidance imperative and compact.
5. Prefer tables, checklists, templates, and examples over prose.
6. Use `SKILL.md` as the runtime decision layer for complex skills.

## Precision Pass

Run the pre-edit check before creating new sections, references, scripts, or assets.

| Question | Required answer |
|----------|-----------------|
| What behavior should change? | one concrete behavior delta |
| What existing rule can be narrowed or replaced? | file and section, or `none` with reason |
| What can be removed or moved out of runtime? | obsolete, duplicate, provenance, or maintenance-only content |
| Why is any new artifact necessary? | branch, lookup, automation, template, or validation need |

Prefer editing existing guidance when it can express the behavior without making that guidance broader.

After any skill artifact changes, run the post-change pass:

1. Re-read changed `SKILL.md` and routed references as a user of the skill would.
2. Remove or narrow any rule made redundant by the change.
3. Move provenance, rationale, or maintenance-only notes out of runtime files.
4. Confirm every added line changes an agent decision, action, or verification step.
5. Record the precision result in the final output as `replaced`, `narrowed`, `moved`, `deleted`, or `added with reason`.

This is a judgment pass. Do not add validators or rigid checklists solely to make the precision pass machine-checkable.

## Path Rules

1. Treat the skill directory as the root for bundled files.
2. Use `references/...`, `scripts/...`, and `assets/...` paths by default.
3. Reserve repo-root paths for registration instructions only.
4. Follow repo prior art if the workspace already standardizes on a provider-specific path variable.
5. Avoid host-specific absolute filesystem paths.

## Supporting Files

Create only what the skill needs:

| File or dir | Use |
|-------------|-----|
| `SPEC.md` | maintenance contract |
| `references/` | optional depth loaded by route |
| `references/evidence/` | persistent iteration examples |
| `scripts/` | repeatable automation or validation |
| `assets/` | reusable templates or static artifacts |

Keep runtime references as direct children of `references/`. Use clear filename prefixes instead of nested folders when references are related.

## File Creation Rules

1. Read `references/reference-architecture.md` before adding bundled files.
2. Create a new reference only when it has a clear "open when..." reason and cannot be handled by tightening an existing reference.
3. If you add a bundled reference, add a direct routing entry for it in `SKILL.md`.
4. Do not create catch-all docs that mix workflow, source notes, examples, and validation results.
5. Keep provenance in `SOURCES.md`, not in runtime files.
6. Update `SPEC.md` when the skill contract changes materially.
7. Do not add nested runtime reference folders unless the content is non-runtime evidence or static assets.

## Class-Specific Requirements

### `integration-documentation`

Require focused coverage for:

1. API surface and behavior contracts
2. config/runtime options
3. common downstream use cases
4. known issues and workarounds
5. version or migration variance

Default minimum depth:

1. at least 6 concrete downstream use cases
2. at least 8 issue/fix or failure/workaround entries

## Shape-Specific Requirements

| Shape | Require |
|-------|---------|
| `router` | route criteria, fallback, per-route contract, misroute recovery |
| `script-backed-workflow` | documented scripts, non-interactive execution, structured output, fallback |
| `parallelization` / `orchestrator-workers` | unit of work, worker output schema, merge rule, stop condition |
| `subagent-fork` | actionable task, return contract, isolation reason, portability note |
| `hook-backed` | event scope, side-effect boundary, fallback, safety note |
| `asset-template` | asset routing, placeholder guidance, validation checklist when needed |
| `argument-driven` | expected arguments, empty-input behavior, manual-only use when risky |

## Example Requirements

Authoring or generator skills should include:

1. happy-path example
2. secure or robust variant
3. anti-pattern plus correction

Do not accept abstract-only guidance when a concrete example is needed.

## Required Output

- updated `SKILL.md`
- updated `SPEC.md` when required
- updated or added supporting files
- precision-pass decision: replaced, narrowed, moved, deleted, or added with reason
- explanation of major authoring decisions
- description-optimization handoff
