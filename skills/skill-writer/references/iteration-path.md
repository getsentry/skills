# Iteration Path

Use this path when improving a skill based on outcomes and examples.

## Example intake

Read `references/iteration-evidence.md` when examples should be persisted across future skill revisions.

Capture example records with:

- label (`positive` or `negative`)
- example kind (`true-positive`, `false-positive`, `fix`, `regression`, `edge-case`)
- evidence origin (`human-verified`, `mixed`, `synthetic`)
- anonymized content
- source provenance pointer (where the example came from)

## Replay and evaluation

1. Evaluate against working set.
2. Evaluate against holdout set.
3. Record improved/unchanged/regressed outcomes.
4. Confirm both positive and negative behavior changed in the expected direction.

## Improvement rules

1. Prioritize fixes for repeated negative patterns.
2. Preserve behavior that consistently succeeds on positives.
3. Update transformed examples when guidance changes.
4. Record deltas in `SOURCES.md` changelog.
5. Expand input collection when failures indicate coverage gaps.
6. Store durable positive/negative examples in `references/evidence/` instead of overloading `SKILL.md`, `SOURCES.md`, or a generic reference file.
7. Keep holdout examples separate from working examples until validation is complete.
8. Update `SPEC.md` when iteration changes the skill's intended scope, evidence model, evaluation gates, or known limitations.

## Required output

- Example intake summary
- Behavior deltas
- Updated artifacts
- Replay summary
