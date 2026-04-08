# API Surface

Use this reference when the user is shaping a public interface, not just refactoring internal implementation.

## Surface Checklist

Before rewriting anything, identify:

- the exported nouns
- the exported verbs
- the input shape
- the output shape
- default behavior
- expected failures
- side effects
- the one most common call site

If any of these are hard to describe in one short sentence, the public surface is probably too complicated.

## Design Targets

### Functions

Prefer named functions when the job can be described in one verb:

- `listMembers`
- `createInvoice`
- `retryDelivery`

Use one obvious input shape.
Avoid mixing identity, behavior flags, and transport details in one loose options bag.

### Procedure Collections

Prefer a small object of named procedures when the consumer needs a family of related operations:

- `memberRouter.list`
- `memberRouter.invite`
- `memberRouter.remove`

This is usually clearer than one `execute` function with an `action` field.

### Types And Options

Keep input types close to the function or procedure they describe.
Prefer option names that explain behavior directly:

- `notify`
- `includeTeams`
- `timeoutMs`
- `retry`

Avoid names that require implementation knowledge:

- `config`
- `payload`
- `contextId`
- `mode`

### Errors

Public APIs must make failure behavior visible.

Use:

- named exceptions in Python
- tagged unions or `Result` types in TypeScript for expected failures
- short docstrings or JSDoc that name expected failures

## Decision Rules

Choose the narrowest public shape that satisfies the common case:

1. one named function
2. small object of named functions or procedures
3. stateful object only when state is a real part of the contract

Move to the next option only when the simpler one stops being clear.

## Review Questions

Ask these before finalizing:

1. Can a caller guess the right entry point from the name alone?
2. Is there one obvious common path?
3. Are optional knobs clearly named?
4. Is failure behavior visible?
5. Would the interface still make sense in a code sample with no prose around it?
