# Authoring Path

Use this path to create or update the skill files.

## SKILL.md requirements

1. Frontmatter must be first line.
2. `name` must match directory.
3. `description` must contain realistic trigger phrases.
4. Keep body imperative and concise.
5. Use SKILL.md as index/orchestration for complex workflows.
6. Apply `references/reference-architecture.md` before adding long sections or new bundled files.
7. Keep bundled-file references relative to the skill root: use `references/...`, `scripts/...`, and `assets/...` for files that ship with the skill.
8. Keep paths portable: do not hardcode host-specific absolute filesystem paths (for example `<home>/...` or `<drive>:\Users\...`) in `SKILL.md` or `references/`.

## Path handling rules

1. Treat the skill directory containing `SKILL.md` as the root for bundled references.
2. Prefer relative references in skill content even when the repository also exposes mirrored or symlinked paths.
3. Reserve repo-root paths for repository registration instructions only (for example `README.md`, `.claude/settings.json`).
4. If the repository has multiple visible layouts for the same skill tree, inspect the workspace and edit the canonical location rather than assuming one layout from a generic template.
5. Follow repository prior art for bundled file paths. If the workspace already standardizes on a root variable such as `${CLAUDE_SKILL_ROOT}`, keep using it consistently instead of inventing a different path model.
6. If the workspace does not have an established provider-specific convention, prefer skill-root-relative references such as `references/...`, `scripts/...`, and `assets/...`.

## Supporting files

Create only files needed to execute the workflow:

- `SPEC.md` for skill intent, scope, source/evidence model, evaluation expectations, limitations, and maintenance rules
- `references/` for domain/process depth
- `references/evidence/` for persistent positive/negative examples and iteration findings
- `scripts/` when repeated automation is needed
- `assets/` for reusable static output artifacts

For workflow/process-heavy skills, also load and apply `references/workflow-patterns.md`
to structure sequencing, conditional branches, and validation loops.

Use focused reference files instead of catch-all documents. Split by lookup need, such as API surface, examples, troubleshooting, source discovery, or evaluation rubric. Do not create a single large reference file that mixes workflow orchestration, source notes, examples, and eval results.

When synthesis is used, include or update `SOURCES.md` for provenance, decision records, coverage, and changelog.

When creating a new skill or materially changing an existing skill, create or update `SPEC.md` from `references/spec-template.md`. Use `../SPEC.md` as the canonical filled example when working from the `skill-writer` references. Keep it as a maintenance artifact: do not duplicate runtime workflow instructions from `SKILL.md`, full provenance tables from `SOURCES.md`, or raw examples from `references/evidence/`.

## Class-specific artifact requirements

### `integration-documentation`

Require coverage for these dimensions, using focused reference files with names that match the skill's domain:

1. API surface and behavior contracts.
2. Configuration/runtime options.
3. Common downstream use cases.
4. Known issues, failure modes, and workarounds.
5. Version and migration variance.

Default minimum depth unless user overrides:

1. At least 6 concrete downstream use cases across the chosen reference files.
2. At least 8 issue/fix or failure/workaround entries across the chosen reference files.

## Example artifact requirements

For authoring/generator skills, references must include transformed examples that are directly usable:

1. happy-path example
2. secure/robust variant
3. anti-pattern + corrected version

Do not accept abstract-only guidance.
Case-study style references are preferred over generic tips.

When improving an existing skill from observed outcomes, store durable examples using `references/iteration-evidence.md`.

## Attribution/provenance

Store full source lists in `SOURCES.md`.

Keep `SKILL.md` free of large attribution blocks.

## Required output

- Updated `SKILL.md`
- Updated `SPEC.md` when required by the change scope
- Updated/added supporting files
- Explanation of major authoring decisions
- Description optimization handoff for trigger-quality pass
