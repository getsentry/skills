# Reference Architecture

Use this guide before adding bundled files or long sections to `SKILL.md`.

## Router Rule

- `SKILL.md` is the router.
- References are lookup leaves.
- `SPEC.md` is the maintenance contract.
- `SOURCES.md` stores provenance and decisions.
- `EVAL.md` stores reusable eval prompts or runbooks.

## Lookup Test

Before creating a reference, finish this sentence:

- "I need to decide X, so read `...`."
- "I need to do Y, so read `...`."
- "I need to diagnose Z, so read `...`."

If the sentence sounds like "I need context" or "I need patterns", the file is too vague.

## Placement Table

| Put it in... | When it belongs there |
|--------------|-----------------------|
| `SKILL.md` | every run needs it |
| `references/` | only some branches need it |
| `SPEC.md` | it explains maintenance, scope, or evidence policy |
| `SOURCES.md` | it is provenance, a decision record, or a gap |
| `EVAL.md` | it is a reusable eval prompt or grading runbook |

## Reference Types

| Need | Shape |
|------|-------|
| choose a path | decision guide |
| execute a procedure | task guide |
| look up exact facts | reference table |
| diagnose a failure | troubleshooting matrix |
| imitate quality | example set |
| judge completeness | evaluation rubric |

## Naming Rules

- Name files for the question or action they answer.
- Good: `mode-selection.md`, `output-contracts.md`, `routing-workflows.md`
- Bad: `notes.md`, `context.md`, `patterns.md`, `research.md`
- Use subfolders only when the subtree name clarifies the lookup path.

## Split Rules

Create a new reference when:

- the content is only needed after a branch decision
- the content has one dominant type
- the section would make `SKILL.md` harder to scan
- the file is approaching 100 lines and contains multiple lookup needs

Keep content in `SKILL.md` when:

- every invocation needs it
- it is short
- moving it would force unnecessary file loads

## Final Checks

1. Every runtime reference has a direct "open when..." reason in `SKILL.md`.
2. The filename tells the agent why to open it.
3. No required instruction is hidden only in an optional reference.
4. No reference has become a second `SKILL.md`.
