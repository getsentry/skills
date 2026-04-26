# SPEC.md Template

Use this guide to create or update a root-level `SPEC.md` for a skill.

`SPEC.md` is a maintenance specification, not runtime instructions. It explains why the skill exists, what evidence shaped it, what data improves it, how it should be evaluated, and where it should not be used.

Use `../SPEC.md` as the canonical filled example for `skill-writer` itself.

## When To Create Or Update

Create `SPEC.md` when creating a new skill in a repository that accepts maintenance artifacts.

Update `SPEC.md` when changing:

- skill intent, scope, or out-of-scope behavior
- trigger strategy or expected users
- source inventory or synthesis assumptions
- reference architecture or evidence storage
- evaluation approach, acceptance gates, or known limitations
- privacy, security, or data-handling assumptions

For a tiny wording-only fix, update `SOURCES.md` changelog if present; skip `SPEC.md` unless the change affects the contract above.

## Relationship To Other Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Runtime activation and execution instructions loaded by agents. |
| `SPEC.md` | Maintenance contract for humans and agents improving the skill. |
| `SOURCES.md` | Source inventory, decisions, coverage matrix, gaps, and changelog. |
| `EVAL.md` | Repeatable evaluation prompts or runbooks. |
| `references/` | Runtime-loadable domain/process details. |
| `references/evidence/` | Persistent examples and observed behavior used for iteration. |

Keep `SPEC.md` concise. Link to `SOURCES.md`, `EVAL.md`, and focused references instead of duplicating them.

## Template

```markdown
# <Skill Name> Specification

## Intent

Describe the skill's purpose in one or two short paragraphs.

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
- eval results:

Data that must not be stored:

- secrets
- customer data
- private URLs or identifiers that are not needed for reproduction

## Reference Architecture

- `SKILL.md` contains:
- `references/` contains:
- `references/evidence/` contains:
- `scripts/` contains:
- `assets/` contains:

## Evaluation

- Lightweight validation:
- Deeper evaluation:
- Holdout examples:
- Acceptance gates:

## Known Limitations

- ...

## Maintenance Notes

- When to update `SKILL.md`:
- When to update `SOURCES.md`:
- When to update `EVAL.md`:
- When to update `references/evidence/`:
```

## Design Rules

1. Describe intent and maintenance contract; do not add runtime instructions that belong in `SKILL.md`.
2. Summarize source categories and link to `SOURCES.md`; do not duplicate full source tables.
3. Describe evidence classes and storage policy; keep raw examples in `references/evidence/`.
4. Include out-of-scope behavior and known limitations so future edits do not expand the skill accidentally.
5. Include evaluation expectations that explain what "good" means, then link to `EVAL.md` for runnable prompts.
6. Keep private or sensitive evidence redacted; store only what is needed to reproduce and improve behavior.
