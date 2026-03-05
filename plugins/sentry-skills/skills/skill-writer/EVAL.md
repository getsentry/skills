# Skill Writer Eval Prompts

Use these prompts when deeper evaluation matters (high-risk, regression tracking, or explicit request).
These are optional guidance artifacts, not required outputs for every skill.

## Integration/Documentation Depth Eval

```text
Use `sentry-skills:skill-writer` to synthesize a new skill named `pi-agent-integration-eval` for working with `@mariozechner/pi-agent-core` as a consumer in downstream libraries.

Primary objective: produce a non-surface-level integration skill that covers API surface, known issues/workarounds, and common real-world use cases.

Scope:
- Source root: `<pi-mono-root>/packages/agent`
- This is for USING Pi in another library, not editing Pi internals.

Mandatory source retrieval:
- README, CHANGELOG
- `src/index.ts`, `src/agent.ts`, `src/agent-loop.ts`, `src/types.ts`, `src/proxy.ts`
- `test/agent.test.ts`, `test/agent-loop.test.ts`
- In-repo usage scan for key APIs (for example Agent, agentLoop, streamProxy, convertToLlm, transformContext, steer, followUp, continue)

Required depth artifacts:
- `references/api-surface.md`
- `references/common-use-cases.md` (at least 6 concrete downstream use cases)
- `references/troubleshooting-workarounds.md` (at least 8 failure modes with fixes/workarounds)
- `references/integration-patterns.md` (happy path, robust variant, anti-pattern + correction)

Depth gates (hard fail if missing):
- Coverage matrix includes: API surface, options/config, runtime lifecycle, event semantics, queue semantics, failure modes, version variance, downstream usage patterns.
- Any partial coverage includes explicit next retrieval actions.
- Qualitative depth rubric includes pass/fail for API/workaround/use-case/gap handling.
- Run validator and report output.

Output sections:
1) Summary
2) Changes Made
3) Validation Results
4) Open Gaps
```

## Pass/Fail Rubric

Pass only if all required artifacts exist and have the requested depth.
Fail if API mapping is partial, workaround guidance is shallow, or use cases are generic and not actionable.
Fail if completion is claimed with unresolved high-impact gaps and no next retrieval actions.

## Optional Deep-Eval Pattern

When you need stronger confidence, run this sequence:

1. Use a fixed prompt set (positives + negatives).
2. Capture deterministic traces (`codex exec --json`).
3. Apply rubric/schema checks where practical (`--output-schema`).
4. Compare baseline vs candidate and report deltas.

## Isolated Eval Runbook

Run the eval in a temporary isolated workspace (copy of repo in `/tmp`):

```bash
EVAL_DIR=/tmp/sentry-skills-eval-run
rm -rf "$EVAL_DIR"
mkdir -p "$EVAL_DIR"
rsync -a "<repo-root>/"/ "$EVAL_DIR"/

codex exec \
  --ephemeral \
  --full-auto \
  --sandbox workspace-write \
  --skip-git-repo-check \
  --add-dir "<pi-mono-root>" \
  -C "$EVAL_DIR" \
  "$(cat <eval-prompt-file>)"
```

Where `<eval-prompt-file>` contains the exact eval prompt from this file.

Validate the generated skill output:

```bash
uv run "<repo-root>/plugins/sentry-skills/skills/skill-writer/scripts/quick_validate.py" \
  /tmp/sentry-skills-eval-run/plugins/sentry-skills/skills/pi-agent-integration-eval \
  --skill-class integration-documentation \
  --strict-depth
```
