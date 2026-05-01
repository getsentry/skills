# Skill Writer Eval Prompts

Use these prompts when deeper evaluation matters (high-risk, regression tracking, or explicit request).
These are optional guidance artifacts, not required outputs for every skill.

## Advanced Shape Selection Eval

```text
Update or create the requested skill and select the simplest adequate execution shape.

For every scenario:
- name the skill class
- name the primary execution shape
- explain why simpler shapes were rejected only if you choose an advanced shape
- add portability notes if you use provider-specific mechanics

Scenarios:

1. "Create a skill that triages billing, refund, and technical-support requests into distinct downstream guidance."
Expected shape signal: `router`

2. "Create a skill that gives SQL naming conventions and query-style preferences for this repo."
Expected shape signal: `inline-guidance` or `reference-backed-expert`, not router or subagent

3. "Create a skill that runs a self-contained investigation in isolated context and returns a concise findings summary."
Expected shape signal: `subagent-fork`

4. "Create a skill that must block risky Bash commands with deterministic validation before they run."
Expected shape signal: `hook-backed`

5. "Create a skill that drafts a proposal, critiques it against a rubric, and revises until it passes."
Expected shape signal: `evaluator-optimizer`

Hard fail if:
- no explicit execution shape is selected
- an advanced shape is chosen without justification
- a provider-specific mechanic is used without portability notes
- a passive guidance skill is incorrectly put into `context: fork`
- a bundled reference file is added without a direct routing entry in `SKILL.md`
```

## Integration/Documentation Depth Eval

```text
Synthesize a new skill named `pi-agent-integration-eval` for working with `@mariozechner/pi-agent-core` as a consumer in downstream libraries.

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
- focused references covering API surface, at least 6 concrete downstream use cases, and at least 8 failure modes with fixes/workarounds
- a focused integration-patterns or examples reference with happy path, robust variant, and anti-pattern + correction

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
Fail if the selected execution shape is more complex than necessary and the writeup does not justify it.
Fail if bundled reference files are hidden behind vague bucket docs instead of clear routed leaves.

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

**Requires**: The `uv` CLI for python package management, install guide at https://docs.astral.sh/uv/getting-started/installation/

```bash
uv run "<skill-writer-root>/scripts/quick_validate.py" \
  /tmp/sentry-skills-eval-run/.agents/skills/pi-agent-integration-eval \
  --skill-class integration-documentation \
  --strict-depth
```
