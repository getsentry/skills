# Authoring Path

Use this path to create or update the skill files.

## SKILL.md requirements

1. Frontmatter must be first line.
2. `name` must match directory.
3. `description` must contain realistic trigger phrases.
4. Keep body imperative and concise.
5. Use SKILL.md as index/orchestration for complex workflows.
6. Keep paths portable: do not hardcode host-specific absolute filesystem paths (for example `<home>/...` or `<drive>:\Users\...`) in `SKILL.md` or `references/`.

## Supporting files

Create only files needed to execute the workflow:

- `references/` for domain/process depth
- `scripts/` when repeated automation is needed
- `assets/` for reusable static output artifacts

For workflow/process-heavy skills, also load and apply `references/workflow-patterns.md`
to structure sequencing, conditional branches, and validation loops.

When synthesis is used, include or update `SOURCES.md` for provenance, decision records, coverage, and changelog.

## Class-specific artifact requirements

### `integration-documentation`

Require these reference artifacts:

1. `references/api-surface.md`
2. `references/common-use-cases.md`
3. `references/troubleshooting-workarounds.md`

Default minimum depth unless user overrides:

1. `common-use-cases.md`: at least 6 concrete downstream use cases.
2. `troubleshooting-workarounds.md`: at least 8 issue/fix entries.

## Example artifact requirements

For authoring/generator skills, references must include transformed examples that are directly usable:

1. happy-path example
2. secure/robust variant
3. anti-pattern + corrected version

Do not accept abstract-only guidance.
Case-study style references are preferred over generic tips.

## Attribution/provenance

Store full source lists in `SOURCES.md`.

Keep `SKILL.md` free of large attribution blocks.

## Required output

- Updated `SKILL.md`
- Updated/added supporting files
- Explanation of major authoring decisions
- Description optimization handoff for trigger-quality pass
