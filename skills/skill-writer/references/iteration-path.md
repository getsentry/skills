# Iteration Path

Use this path when improving a skill based on outcomes and examples.

## Example intake

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

## Required output

- Example intake summary
- Behavior deltas
- Updated artifacts
- Replay summary
