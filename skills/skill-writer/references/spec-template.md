# SPEC.md Template

Use this guide to create or update a root-level `SPEC.md`.

## Use `SPEC.md` For

- intent
- scope
- trigger context
- evidence model
- validation expectations
- limitations
- maintenance rules

Do not put runtime instructions or full provenance tables here.

## Update `SPEC.md` When

- intent or scope changes
- trigger strategy changes
- evidence sources or storage policy changes
- reference architecture changes
- validation gates change
- privacy, security, or data-handling assumptions change

For tiny wording-only fixes, update `SOURCES.md` changelog instead.

## Relationship To Other Files

| File | Purpose |
|------|---------|
| `SKILL.md` | runtime activation and execution |
| `SPEC.md` | maintenance contract |
| `SOURCES.md` | source inventory, decisions, gaps, changelog |
| `references/` | runtime-loadable depth |
| `references/evidence/` | persistent iteration examples |

## Template

```markdown
# <Skill Name> Specification

## Intent

<1-2 short paragraphs>

## Scope

In scope:
- ...

Out of scope:
- ...

## Users And Trigger Context

- Primary users:
- Common user requests:
- Should not trigger for:

## Runtime Contract

- Required first actions:
- Required outputs:
- Non-negotiable constraints:
- Expected bundled files loaded at runtime:

## Source And Evidence Model

Authoritative sources:
- ...

Useful improvement sources:
- positive examples:
- negative examples:
- commit logs/changelogs:
- issue or PR feedback:
- validation results:

Data that must not be stored:
- secrets
- customer data
- private URLs or identifiers not needed for reproduction

## Reference Architecture

- `SKILL.md` contains:
- `references/` contains:
- `references/evidence/` contains:
- `scripts/` contains:
- `assets/` contains:

## Validation

- Lightweight validation:
- Deeper validation:
- Holdout examples:
- Acceptance gates:

## Known Limitations

- ...

## Maintenance Notes

- When to update `SKILL.md`:
- When to update `SOURCES.md`:
- When to update `references/evidence/`:
```

## Design Rules

1. Keep `SPEC.md` concise.
2. Link to `SOURCES.md` or refs instead of duplicating them.
3. Keep raw examples in `references/evidence/`.
4. Keep sensitive data redacted.
