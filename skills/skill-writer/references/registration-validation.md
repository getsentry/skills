# Registration and Validation

Apply registration and quality checks before completion.

## Registration checklist

1. Inspect the workspace and identify the active skill layout before editing files.
2. Create/update `<skill-root>/SKILL.md` and any bundled `references/`, `scripts/`, or `assets/` beneath that root.
3. By default, create or update the skill under `.agents/skills/<name>/`.
4. If the workspace clearly uses a different canonical layout, follow that layout instead of forcing `.agents/skills/`.
5. Only apply repository-specific registration steps when the workspace conventions explicitly require them.

When a repository does maintain its own skill catalog, verify and update any required registration files such as:

- public skill inventories or tables
- project or plugin settings files
- allowlists used by other skills or automation

For this repository today:

- default authoring target remains `.agents/skills/`
- `.agents/skills` is a symlinked mirror of canonical repo-root `skills/`
- `plugins/sentry-skills/skills` is another mirror of that same tree for plugin consumers
- repository-level registration files still live at `README.md` and `.claude/settings.json`

## Validation checklist

1. Run:

```bash
uv run scripts/quick_validate.py <path/to/skill-directory> --strict-depth
```

Use the skill-root-relative form above when running from the `skill-writer` directory.
If you must run the validator from another working directory, convert both paths to the correct relative path from that directory instead of introducing absolute or host-specific paths into the skill docs.

2. Confirm for authoring/generator skills:
- transformed examples exist in references (happy-path, secure/robust, anti-pattern+fix)
- synthesis depth gates are satisfied
- selected example profile requirements are satisfied and reported

3. Confirm for integration/documentation skills:
- `references/api-surface.md` exists
- `references/common-use-cases.md` exists with sufficient depth
- `references/troubleshooting-workarounds.md` exists with sufficient depth
- `SKILL.md` and `references/*.md` avoid host-specific absolute filesystem paths

4. Confirm portability for skills that are expected to be portable by default:
- bundled file references use skill-root-relative paths such as `references/...`, `scripts/...`, or `assets/...`
- provider-specific path variables (for example `${CLAUDE_SKILL_ROOT}`) are absent unless the skill is intentionally provider-specific
- provider-specific behavior, if any, is labeled as compatibility guidance rather than the primary workflow

5. Confirm evaluation outputs as applicable:
- lightweight qualitative summary (recommended default)
- qualitative depth rubric status for API/workaround/use-case/gap handling (recommended for integration/documentation and skill-authoring)
- deeper eval or quantitative summary only if user requested benchmark mode or risk warrants it

6. Reject shallow handoffs that omit required artifacts.

## Required output

- Registration changes summary
- Validator output
- Evaluation summary status
- Any residual risks or open gaps
