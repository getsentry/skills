# Authoring Path

Use this path to create or update skill files.

## Runtime Writing Rules

1. Frontmatter must be first line.
2. `name` must match the directory.
3. `description` must contain realistic trigger language.
4. Keep runtime guidance imperative and compact.
5. Prefer tables, checklists, templates, and examples over prose.
6. Use `SKILL.md` as the runtime decision layer for complex skills.

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

Subfolders inside `references/` are acceptable only when they make the lookup path clearer.

## File Creation Rules

1. Read `references/reference-architecture.md` before adding bundled files.
2. Create a new reference only when it has a clear "open when..." reason.
3. If you add a bundled reference, add a direct routing entry for it in `SKILL.md`.
4. Do not create catch-all docs that mix workflow, source notes, examples, and eval results.
5. Keep provenance in `SOURCES.md`, not in runtime files.
6. Update `SPEC.md` when the skill contract changes materially.

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
| `evaluator-optimizer` | rubric, stop rule, acceptance condition, evidence handling |
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
- explanation of major authoring decisions
- description-optimization handoff
