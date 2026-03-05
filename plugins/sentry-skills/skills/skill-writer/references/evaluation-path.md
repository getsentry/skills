# Evaluation Path

Use this path to verify that skill behavior improves outcomes.

## Default approach (lightweight, guidance-only)

Use this by default when a full eval pass is not requested:

1. Define representative prompts for the target skill task.
2. Compare observed behavior before/after edits in concise notes.
3. Mark outcomes as improved, unchanged, or regressed.
4. Record unresolved weaknesses and next steps.

For `integration-documentation` and `skill-authoring` skills, include a concise depth rubric:

1. API surface coverage: pass/fail.
2. Known issues/workarounds coverage: pass/fail.
3. Common use-case coverage: pass/fail.
4. Gap handling quality (explicit next retrieval actions for partials): pass/fail.

## Deeper eval playbook (optional)

Use this only when:

1. The user requests rigorous evals.
2. The skill is high-risk or high-cost if wrong.
3. You need regression-tracking over time.

Suggested workflow:

1. Build a prompt set with positives, implicit triggers, and negatives.
2. Capture deterministic run traces (for example `codex exec --json`).
3. Apply machine-checkable rubric/schema checks (for example `--output-schema` where applicable).
4. Compare baseline vs updated behavior and report deltas.

## Optional quantitative benchmark

Run only when explicitly requested or when objective scoring is practical.

1. Define baseline (without skill guidance).
2. Define with-skill run.
3. Use the same prompt set and scoring rubric for both.
4. Report deltas and confidence in the result.

Do not block completion on deeper evals unless the user asks for them.

## Canonical eval prompts

Keep reusable, copy/paste eval prompts in `../EVAL.md`.
Use those prompts when you need a repeatable depth check against `skill-writer`.

## Agent-agnostic requirement

Keep evaluation instructions tool-agnostic so they work in both Codex and Claude environments.

## Required output

- Qualitative evaluation summary (recommended default)
- Deeper eval or quantitative summary (optional, if run)
- Final acceptance decision and residual risks
