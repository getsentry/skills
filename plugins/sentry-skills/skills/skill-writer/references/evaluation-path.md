# Evaluation Path

Use this path to verify that skill behavior improves outcomes.

## Mandatory qualitative evaluation

Always run this:

1. Define representative prompts for the target skill task.
2. Compare observed behavior before/after edits in concise notes.
3. Mark outcomes as improved, unchanged, or regressed.
4. Record unresolved weaknesses and next steps.

For `integration-documentation` and `skill-authoring` skills, include a depth rubric:

1. API surface coverage: pass/fail.
2. Known issues/workarounds coverage: pass/fail.
3. Common use-case coverage: pass/fail.
4. Gap handling quality (explicit next retrieval actions for partials): pass/fail.

## Optional quantitative benchmark (opt-in)

Run only when explicitly requested or when objective scoring is practical.

1. Define baseline (without skill guidance).
2. Define with-skill run.
3. Use the same prompt set and scoring rubric for both.
4. Report deltas and confidence in the result.

Do not block completion on quantitative benchmarking unless the user asks for it.

## Canonical eval prompts

Keep reusable, copy/paste eval prompts in `../EVAL.md`.
Use those prompts when you need a repeatable depth check against `skill-writer`.

## Agent-agnostic requirement

Keep evaluation instructions tool-agnostic so they work in both Codex and Claude environments.

## Required output

- Qualitative eval summary (mandatory)
- Quantitative benchmark summary (optional, if run)
- Final acceptance decision and residual risks
