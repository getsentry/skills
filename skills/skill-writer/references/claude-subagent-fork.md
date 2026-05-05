# Claude Subagent-Fork Skills

Load this when the skill should run in isolated context with `context: fork`.

## Use this file for

- self-contained delegated investigations
- isolated context for focus or permission boundaries
- model or tool specialization where the main thread only needs a summary

## Required contract

1. An actionable task in the skill body.
2. Expected return or summary contract.
3. Explicit reason isolation is useful.
4. Portability note because this is Claude Code-specific.

## Avoid when

1. The skill is passive conventions or reference material.
2. The task depends heavily on the current conversation history.
3. The main value comes from inline collaboration rather than delegation.
