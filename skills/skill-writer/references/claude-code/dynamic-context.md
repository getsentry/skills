# Claude Dynamic Context Injection

Load this when the skill uses Claude Code shell preprocessing with ``!`command` `` or fenced ````!` blocks.

## Use this file for

- stable, high-signal preprocessing
- small dynamic snippets that are cheaper than adding a full script

## Use sparingly

1. Only inject output that is stable, high-signal, and cheap.
2. Never inject large or noisy output.
3. Prefer a normal script or tool call when that is easier to reason about.

Treat this as preprocessing, not model behavior, and add portability notes because it is Claude Code-specific.
