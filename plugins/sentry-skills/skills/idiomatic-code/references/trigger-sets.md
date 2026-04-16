# Trigger Sets

Use this reference to keep `idiomatic-code` discoverable without letting it eat generic cleanup prompts that should go to `code-simplifier`.

## Should Trigger

- "Make this API easier to consume."
- "Improve the naming on this interface."
- "Rewrite these docstrings so the contract is obvious."
- "This abstraction has too much magic."
- "There is too much DI / too many factories here."
- "Server vs client is making this hard to reason about."
- "This framework behavior feels too implicit."
- "Turn this clever public abstraction into plain functions."
- "This server action interface is confusing."
- "Help me make this library surface more explicit."

## Should Not Trigger

- "Clean up this code."
- "Reduce duplication in this module."
- "Refactor this for readability."
- "Fix the failing tests."
- "Find bugs in this PR."
- "Security review this diff."
- "Make this faster."
- "Format this file."
- "Fix the type errors."
- "Write tests for this."

## Description Edits

- Tightened the description around public interfaces, naming, and contract docs.
- Added trigger phrases for magic, implicit behavior, DI/factory machinery, and server/client confusion.
- Removed broad wording that drifted toward generic cleanup territory already covered by `code-simplifier`.
