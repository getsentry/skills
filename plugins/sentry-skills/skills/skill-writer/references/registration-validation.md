# Registration and Validation

Apply repository registration and quality checks before completion.

## Registration checklist

1. Create/update `plugins/sentry-skills/skills/<name>/SKILL.md`.
2. Add/update canonical skill in `README.md` Available Skills table (alphabetical; exclude alias/symlink entries).
3. Add/update `Skill(sentry-skills:<name>)` in `.claude/settings.json`.
4. Add/update skill allowlist in `plugins/sentry-skills/skills/claude-settings-audit/SKILL.md`.

## Validation checklist

1. Run:

```bash
uv run plugins/sentry-skills/skills/skill-writer/scripts/quick_validate.py <path/to/skill-directory> --strict-depth
```

2. Confirm for authoring/generator skills:
- transformed examples exist in references (happy-path, secure/robust, anti-pattern+fix)
- synthesis depth gates are satisfied
- selected example profile requirements are satisfied and reported

3. Confirm for integration/documentation skills:
- `references/api-surface.md` exists
- `references/common-use-cases.md` exists with sufficient depth
- `references/troubleshooting-workarounds.md` exists with sufficient depth
- `SKILL.md` and `references/*.md` avoid host-specific absolute filesystem paths

4. Confirm evaluation outputs as applicable:
- lightweight qualitative summary (recommended default)
- qualitative depth rubric status for API/workaround/use-case/gap handling (recommended for integration/documentation and skill-authoring)
- deeper eval or quantitative summary only if user requested benchmark mode or risk warrants it

5. Reject shallow handoffs that omit required artifacts.

## Required output

- Registration changes summary
- Validator output
- Evaluation summary status
- Any residual risks or open gaps
