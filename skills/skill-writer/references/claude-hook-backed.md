# Claude Hook-Backed Skills

Load this when the skill uses Claude Code hooks for deterministic enforcement around tool or lifecycle events.

## Use this file for

- pre-tool validation for risky commands
- post-edit formatting or linting
- scoped guardrails around specific tool events

## Required contract

1. Narrow event and matcher scope.
2. Explicit side-effect boundaries.
3. Fallback behavior when hooks are unavailable.
4. Security note for shell execution, path handling, and sensitive files.

## Security rules

1. Command hooks run with full user permissions.
2. Validate and sanitize inputs.
3. Use absolute paths for scripts inside the hook definition.
4. Avoid sensitive files such as `.env`, `.git/`, and keys.
5. Test hooks before treating them as trusted enforcement.

## Async note

Async hooks cannot block the action that triggered them; they are not a substitute for synchronous validation.
