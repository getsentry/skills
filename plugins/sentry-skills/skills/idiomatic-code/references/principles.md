# Principles

Use this rubric to design or rewrite code so the interface is obvious before the implementation is inspected.

## Public Surface First

Start with the code a consumer reads first:

- exported functions
- procedure names
- public object keys
- constructor arguments
- option names
- return values
- docstrings and comments

If the call site is confusing, the design is confusing.

## Naming

Names should tell the consumer what the code means, not how it is implemented.

| Prefer | Instead of |
| --- | --- |
| `createInvoice` | `executeInvoiceFlow` |
| `listMembers` | `handleMembers` |
| `retry` | `shouldTryAgain` |
| `timeoutMs` | `configValue` |
| `organizationId` | `contextId` |

Rules:

- Use domain nouns and verbs.
- Make similar operations read like a family.
- Avoid "manager", "service", "helper", "util", "processor", and "data" unless they name a real domain concept.
- Split overloaded functions before inventing generic names.

## Interface Shape

Choose the smallest interface that makes the common case obvious.

Prefer:

- one clear entry point per job
- objects when a named shape helps readability
- positional arguments only when there are one or two obvious inputs
- keyword-only or named options for optional behavior
- separate functions or procedures when behavior truly changes

Avoid:

- one function with many booleans
- option bags that mix identity, behavior flags, and transport details
- classes with one public method
- builders that exist only to hide required parameters

## Explicit Behavior

The interface should answer these questions without digging through the body:

- What inputs are required?
- What is optional?
- What shape comes back?
- What can fail?
- Which failures are part of normal behavior?
- What side effects happen?

If the answer depends on hidden conventions, make it explicit in code or docs.

## Failure Semantics

Make expected failures visible.

Prefer:

- named exceptions in Python
- tagged unions or `Result` types in TypeScript when failures are normal outcomes
- narrow error categories over generic strings
- short comments or docstrings that name expected failures

Avoid:

- `return null` with no contract
- one catch-all `Error`
- silently swallowing failures
- making callers infer whether a function throws

## Comments And Docstrings

Good contract comments are short and specific.

Use comments and docstrings to describe:

- return contract
- side effects
- invariants
- expected failures
- why the API is intentionally constrained

Do not use comments and docstrings to:

- paraphrase the next line
- narrate obvious control flow
- explain internal mechanics the caller does not need

## Pressure Test

Before finalizing a rewrite, answer these questions:

1. Could a new caller predict how to use this from the names alone?
2. Is there one obvious path through the public API?
3. Are behavior-changing flags gone or at least clearly named?
4. Does the interface show how failure works?
5. Do comments and docstrings explain contract instead of implementation?
6. Would the code still feel clear if the caller never read the implementation body?
