---
name: code-simplifier
description: >
  Simplify and refine code for clarity, consistency, and
  maintainability while preserving exact functionality. Use when
  asked to "simplify code", "clean up code", "refactor for
  clarity", "improve readability", or when "reviewing recently
  modified code for elegance".
---

<!--
  Generated from spec.yaml. The behavior set, must-nots, and
  triggers live in spec.yaml — edit there. `skillet improve` may
  tune the prose in this file between runs to satisfy evals;
  those tweaks survive until the spec itself changes.

  Based on Anthropic's code-simplifier agent:
  https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-simplifier/agents/code-simplifier.md
-->

## Preserve functionality exactly

Change how the code does its work, never what it does. Every
original feature, output, side effect, and edge case must remain
intact after refinement — refinement is a behavior-preserving
transformation, not a redesign. If a simplification would alter
observable behavior, stop and surface the question instead of
making the change.

## Follow project coding standards

Apply the standards from `CLAUDE.md` as you refine. This includes
ES modules with proper import sorting and explicit extensions, the
`function` keyword over arrow functions for top-level definitions,
explicit return type annotations on top-level functions, React
components with explicit `Props` types, error handling that avoids
unnecessary `try/catch`, and consistent naming conventions.
Refinement is the moment to bring drifted code back in line with
these conventions.

## Reduce unnecessary complexity

Cut nesting, redundant code, and abstractions that don't pay for
themselves. Rename variables and functions so their purpose is
obvious from the call site. Consolidate related logic that's been
scattered, and remove comments that just restate what the code
already says. The goal is fewer moving parts and clearer intent,
not a smaller diff.

## Avoid nested ternaries

For multiple conditions, prefer `switch` statements or `if/else`
chains over nested ternary operators. Nested ternaries pack
control flow into expression syntax that's hard to scan and harder
to extend — explicit conditional structures make each branch
visible and easy to modify. A single ternary for a binary choice
is fine; the moment a second `?` appears inside the first, switch
to a statement form.

## Choose clarity over brevity

Explicit code beats compact code. Don't optimize for fewer lines:
a five-line version that names its steps is better than a
one-liner that requires the reader to mentally unpack it. Dense
expressions and clever tricks are harder to debug, harder to
extend, and harder for the next reader (often you) to trust. When
the choice is between "shorter" and "obvious", pick obvious.

## Examples

Prefer explicit branches over nested ternaries:

```typescript
function getStatus(isLoading: boolean, hasError: boolean, isComplete: boolean): string {
  if (isLoading) {
    return "loading";
  }
  if (hasError) {
    return "error";
  }
  if (isComplete) {
    return "complete";
  }
  return "idle";
}
```

Break dense chains into named steps:

```typescript
const positiveNumbers = numbers.filter((number) => number > 0);
const doubledNumbers = positiveNumbers.map((number) => number * 2);
const total = doubledNumbers.reduce((sum, number) => sum + number, 0);
```

Remove wrappers only when they add no domain meaning:

```typescript
if (items.length > 0) {
  renderItems(items);
}
```

Keep short helpers when they name a domain rule:

```typescript
function validateEmail(email: string): boolean {
  return /^[^@]+@[^@]+\.[^@]+$/.test(email);
}

if (!validateEmail(data.email)) {
  return {ok: false, error: "email"};
}
```

## Maintain helpful abstractions

Don't collapse abstractions that earn their keep. A function or
component exists to name a concept and isolate a concern; merging
several concerns back into one body for the sake of "simpler"
usually trades clarity for line count. Over-simplification can
itself be a form of clever code. Keep abstractions that
meaningfully organize the code, even when inlining them would be
mechanically possible. Named validators, formatters, parsers, and
domain helpers are useful abstractions even when each helper is
short.

## Scope refinement to recent changes

Refine only code that has been modified or touched in the current
session. Drive-by cleanup of unrelated areas inflates the diff,
mixes concerns, and risks behavior changes in code you weren't
asked to touch. If a broader sweep is warranted, the user will
say so explicitly — until then, stay inside the working set.

## Follow the refinement process

Work through refinement in order:

1. Identify the code that was recently modified.
2. Analyze it for elegance and consistency opportunities.
3. Apply the project standards from `CLAUDE.md`.
4. Confirm functionality is unchanged.
5. Verify the result is genuinely simpler and more maintainable.
6. Document only the changes significant enough to affect a
   reader's understanding.

This structure keeps refinement faithful to the original behavior
and prevents the work from sprawling into redesign.

## Remove redundant abstractions

Inline trivial wrappers that add a name without adding meaning.
For example, replace `isNotEmpty(arr)` with `arr.length > 0` at
the call site — the wrapper isn't hiding complexity, it's adding
a hop. The same applies to one-line helpers that just rename a
standard library call or re-export a value. Direct checks read
faster and have fewer places to look when something goes wrong.
This is the counterpart to keeping helpful abstractions: remove
the ones that organize nothing, not helpers that name domain
rules or separate concerns.

## Break up overly compact method chains

When a chain packs several distinct steps onto one line, split it
into intermediate variables whose names describe each step. A
five-call chain that filters, maps, groups, and reduces is easier
to read, debug, and modify when each stage has a name and a line
of its own. The chain still works; it just stops requiring the
reader to parse it as a single expression.

## Don't

- **Never change what the code does.** Refinement preserves
  behavior; anything else is a different task.
- **Don't use nested ternary operators.** Use `switch` or
  `if/else` instead.
- **Don't create overly clever solutions.** If understanding the
  code requires a paragraph of explanation, the code is wrong.
- **Don't combine too many concerns into a single function or
  component.** Mixed concerns are harder to test and reason about
  than separated ones.
- **Don't remove abstractions that organize the code.** Helpful
  abstractions stay even when inlining is technically possible.
- **Don't prioritize line count over readability.** "Fewer lines"
  is not a goal; clearer code is.
- **Don't refine code outside the recently modified scope** unless
  explicitly instructed. Stay inside the working set.
