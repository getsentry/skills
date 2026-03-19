---
name: idiomatic-code
description: Designs and rewrites public code interfaces, names, and contract docs to be idiomatic, explicit, and easy to consume. Use when asked to "make this API/interface clearer", "improve naming", "rewrite docstrings/comments", "reduce magic or implicit behavior", "too much DI/factory machinery", "server vs client is confusing", or turn clever public abstractions into plain functions or objects with well-designed interfaces.
---

# Idiomatic Code

Produce code that is absurdly easy to understand and consume.
Optimize first for public interface clarity, explicit behavior, and names that match the caller's mental model.

## Use This Skill For

- Public API and interface design
- Naming functions, types, modules, procedures, and options
- Rewriting abstractions that feel clever, generic, or hard to consume
- Making TypeScript and Python code more explicit and easier to reason about
- Rewriting docstrings, JSDoc, and comments so they explain contract and behavior

Do not use this skill for generic cleanup, formatting, lint-only refactors, or broad code review.
Use `code-simplifier` for general simplification work that is not primarily about interface design.

## Load Only What You Need

| Situation | Read |
| --- | --- |
| TypeScript interfaces, RPC surfaces, or library APIs | `references/principles.md`, `references/api-surface.md`, `references/typescript-exemplars.md`, `references/transformed-examples.md` |
| Python helpers, clients, or library APIs | `references/principles.md`, `references/api-surface.md`, `references/python-exemplars.md`, `references/transformed-examples.md` |
| "How should this read for callers?" or "what should the public contract be?" | `references/api-surface.md`, plus the language-specific exemplar file |
| "Give me a concrete rewrite example" or "show me how to rewrite this" | `references/common-use-cases.md`, `references/transformed-examples.md` |
| "Why does this still feel confusing?" or "what smell am I looking at?" | `references/troubleshooting-workarounds.md`, `references/principles.md` |
| "This has too many factories/providers", "too much DI", or "too much machinery" | `references/contrast-exemplars.md`, `references/troubleshooting-workarounds.md` |
| "This reads like a state machine / DSL / framework", or "this is explicit but still noisy" | `references/contrast-exemplars.md`, `references/principles.md` |
| "This changes behavior depending on file context", "server vs client makes this hard to reason about", or "this framework relies on too much implicit behavior" | `references/contrast-exemplars.md`, `references/troubleshooting-workarounds.md` |
| "Should this skill trigger here?" or "is this really `idiomatic-code` and not `code-simplifier`?" | `references/trigger-sets.md`, `references/principles.md` |
| Naming, comments, JSDoc, or docstrings | `references/principles.md`, `references/transformed-examples.md` |
| Design review of an existing abstraction | `references/principles.md` plus the language-specific exemplar file |

Read `SOURCES.md` only when you need provenance or exemplar rationale.

## Core Standard

The consumer experience is the design surface.

When multiple designs work, choose the one that makes the call site, return value, and failure behavior easiest to predict without reading implementation details.

## Working Method

1. Start from the public surface, not the implementation.
   List the nouns, verbs, inputs, outputs, errors, defaults, and comments a caller sees first.
2. Reduce concept count.
   Remove wrappers, builders, option flags, or indirection that do not buy clear user value.
3. Rename for concrete meaning.
   Prefer domain words over framework words and generic verbs like `run`, `handle`, `execute`, or `process`.
4. Make behavior explicit.
   Show required inputs, optional inputs, side effects, nullability, and expected failure modes in the API shape itself.
5. Prefer plain composition.
   Use plain functions, objects, and data structures before introducing classes, fluent builders, registries, or meta-programming.
6. Rewrite comments and docstrings last.
   Explain contract, invariants, side effects, and failure behavior. Do not narrate line-by-line implementation.

## Design Rules

| Prefer | Avoid |
| --- | --- |
| One obvious way to do the common thing | Multiple entry points for the same job |
| Plain objects and named functions | Clever builders, hidden registration, magic defaults |
| Domain names at the call site | Generic names like `manager`, `service`, `utils`, `data`, `thing` |
| Options that add data, not behavior switches | Boolean flags that change semantics |
| Explicit success and failure shapes | Hidden throws, `null`, or `undefined` with no contract |
| Short contract comments | Comments that restate the code |

## Language Guidance

### TypeScript

- Bias toward oRPC-style surfaces: plain object routers, obvious names, and one predictable handler shape.
- Prefer APIs that read cleanly at the call site over APIs that maximize inference tricks.
- Use `Result`-like return values or small tagged unions when expected failures are part of normal behavior.
- Keep schema and transport details close to the procedure or function they shape.
- When the design starts drifting toward provider graphs, container tokens, state-machine ceremony, or theory-heavy vocabulary, load `references/contrast-exemplars.md` and simplify back toward the caller's mental model.
- When a framework changes semantics through directives, file placement, or routing conventions, make those boundaries explicit in local module interfaces instead of letting hidden mode switches leak everywhere.
- Prefer naming conventions that reveal structure over directives that silently change semantics.

### Python

- Prefer requests and HTTPX style APIs: obvious verbs, obvious arguments, small objects, and clear return values.
- Use keyword-only arguments to make optional behavior explicit.
- Raise named exceptions for exceptional failures; document them briefly in the docstring.
- Keep docstrings short and contract-focused.

## Comments And Docstrings

Good comments and docstrings answer one of these questions:

- What does the caller get back?
- What side effects happen?
- What invariants or preconditions matter?
- Which failures are expected?
- Why is this design intentionally narrower than alternatives?

Avoid comments and docstrings that only translate syntax into English.

## Output Expectations

When rewriting code:

1. Produce the clearer interface first.
2. Preserve behavior unless the user asked for a semantic change.
3. If you changed the public surface, include a short rationale with at most 3 bullets focused on naming, interface shape, and failure behavior.
4. When comments or docstrings are part of the task, include the rewritten versions in the final code.

When reviewing code:

1. Focus findings on interface clarity, naming, concept count, and contract documentation.
2. Do not spend the review on formatting or stylistic nits.
3. Call out when the current abstraction is more complex than its use cases require.

## Boundaries

- Preserve local project conventions when they are already strong, even if they differ from the exemplars.
- Do not introduce an RPC framework, result type, or schema library just because a good example uses it.
- Do not replace a familiar local pattern with a "cleaner" abstraction if the migration cost outweighs the clarity gain.
- If the existing code intentionally hides complexity behind a stable public interface, simplify the public contract first and leave internals alone unless the user asked for deeper refactoring.
