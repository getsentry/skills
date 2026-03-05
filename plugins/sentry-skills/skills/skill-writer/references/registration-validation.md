# Registration and Validation

Apply repository registration and quality checks before completion.

## Registration checklist

1. Create/update `plugins/sentry-skills/skills/<name>/SKILL.md`.
2. Add/update skill in `README.md` Available Skills table (alphabetical).
3. Add/update `Skill(sentry-skills:<name>)` in `.claude/settings.json`.
4. Add/update skill allowlist in `plugins/sentry-skills/skills/claude-settings-audit/SKILL.md`.

## Validation checklist

1. Run:

```bash
uv run plugins/sentry-skills/skills/skill-writer/scripts/quick_validate.py <path/to/skill-directory>
```

2. Confirm for authoring/generator skills:
- transformed examples exist in references (happy-path, secure/robust, anti-pattern+fix)
- synthesis depth gates are satisfied
- selected example profile requirements are satisfied and reported

3. Confirm evaluation outputs are present:
- qualitative eval summary (mandatory)
- quantitative summary only if user requested benchmark mode

4. Reject shallow handoffs that omit required artifacts.

## Required output

- Registration changes summary
- Validator output
- Evaluation summary status
- Any residual risks or open gaps
