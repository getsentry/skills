# Skill Writer Eval Notes

Brief runbook for re-running the isolated `skill-writer` eval.

## Prompt Source

Use the prompt in [EVAL.md](./EVAL.md), section `Integration/Documentation Depth Eval`.

## Isolated Subagent Run

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

Where `<eval-prompt-file>` contains the exact eval prompt from `EVAL.md`.

## Verification

Validate the generated skill output:

```bash
uv run "<repo-root>/plugins/sentry-skills/skills/skill-writer/scripts/quick_validate.py" \
  /tmp/sentry-skills-eval-run/plugins/sentry-skills/skills/pi-agent-integration-eval \
  --skill-class integration-documentation \
  --strict-depth
```
