# Claude Argument Substitutions

Load this when the skill uses Claude Code argument fields or substitution variables.

## Supported substitutions

- `$ARGUMENTS`
- `$ARGUMENTS[N]`
- `$N`
- named arguments such as `$issue` when `arguments` is declared
- `${CLAUDE_SESSION_ID}`
- `${CLAUDE_EFFORT}`
- `${CLAUDE_SKILL_DIR}`

## Required contract

1. Document expected arguments and empty-input behavior.
2. Add quoting-aware examples for multi-word input when ambiguity is likely.
3. Use manual-only invocation for side-effect-heavy argument-driven skills.
4. Add portability notes because this syntax is Claude Code-specific.
