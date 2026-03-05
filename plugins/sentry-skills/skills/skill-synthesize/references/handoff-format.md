# Handoff Format for `skill-writer`

Use markdown, not JSON. Emit the block exactly in this structure and section order.

```markdown
## skill-writer Handoff

### Objective
- One-sentence target outcome.

### Trigger Description Draft
- Proposed `name`: `<skill-name>`
- Proposed `description`: `<what it does>. Use when ...`

### Recommended Structure Tier
- `simple` | `with references` | `with scripts` | `full`
- Why this tier fits.

### Required Workflow
1. Step 1 title and outcome.
2. Step 2 title and outcome.
3. Step 3 title and outcome.

### Supporting Files
- Required references/scripts/assets and why each is needed.

### Registration Checklist (Repo-Specific)
1. Add `plugins/sentry-skills/skills/<name>/SKILL.md`.
2. Add skill to `README.md` table in alphabetical order.
3. Add `Skill(sentry-skills:<name>)` to `.claude/settings.json`.
4. Add skill to allowlist in `plugins/sentry-skills/skills/claude-settings-audit/SKILL.md`.

### Validation Commands
- `uv run plugins/sentry-skills/skills/skill-writer/scripts/quick_validate.py <skill-directory>`
- Any additional checks required by this repository.

### Assumptions
- Explicit assumptions used to complete synthesis.

### Open Gaps
- Unresolved unknowns and next retrieval actions.
```

## Quality bar

- Keep every recommendation traceable to source inventory entries.
- Avoid speculative requirements not supported by sources.
- When gaps remain, state them explicitly instead of guessing.
