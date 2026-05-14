# Argument-Driven Skill Layout

Use this layout when the skill is normally invoked with explicit inputs such as issue numbers, paths, modes, or targets.

## Choose this layout when

- the user supplies parameters directly
- empty-input behavior needs to be defined
- manual invocation is safer than automatic activation

## Common layout

```yaml
---
name: fix-issue
description: Fix a GitHub issue by number. Use when asked to fix or resolve a specific issue.
argument-hint: "[issue-number]"
disable-model-invocation: true
---
```

## Required contract

1. Document expected arguments and empty-input behavior.
2. Use manual-only invocation when side effects are substantial.
3. Use named or positional arguments only when they improve clarity.
4. Add portability notes if the argument syntax depends on provider-specific mechanics.

## Also load

- `references/claude-argument-substitutions.md` when using Claude Code substitutions or named arguments
- `references/claude-frontmatter-invocation.md` when invocation control needs provider-specific fields
