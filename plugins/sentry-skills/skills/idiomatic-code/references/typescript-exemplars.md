# TypeScript Exemplars

Use these examples to calibrate what good and bad interface design look like.
Do not treat them as templates to copy verbatim.

## Primary Anchor: oRPC

Why it matters:

- The public surface stays close to plain objects and named procedures.
- Routers read like data, not framework ceremony.
- Procedure handlers have one obvious place where behavior lives.
- Naming stays close to the consumer view of the system.

What makes oRPC a strong positive example:

- plain object router shapes
- one predictable handler shape
- names that read cleanly at the call site
- transport and schema details attached close to the procedure they describe

Why it is still not a template:

- framework adoption when a plain module API is enough
- inferred complexity that obscures domain names

## Positive Secondary Examples

### tRPC

What makes this a good example:

- reusable base procedures for shared auth or context
- simple router and procedure families with consistent naming

What to avoid:

- stacking builders until a simple procedure becomes hard to scan
- allowing the framework vocabulary to dominate domain vocabulary

### Hono

What makes this a good example:

- tiny core API with obvious verbs
- route definitions that read in straight lines
- heavy reuse of Web Platform concepts instead of custom wrappers

What to avoid:

- accumulating too much app wiring in one chain
- mixing routing, validation, and business logic into one unreadable block

### Remix

What makes this a good example:

- route file naming that carries structure directly in the filename
- conventions that are easy to scan because they describe organization more than runtime mode
- colocated route behavior that still reads like normal module boundaries

What to avoid:

- treating framework file conventions as the local default where plain module names would be clearer
- turning naming conventions into hidden execution semantics

### better-auth

What makes this a good example:

- explicit configuration of enabled auth capabilities
- a clear split between server-side auth configuration and client-side auth usage
- plugin additions that are visible in config instead of hidden behind framework magic

What to avoid:

- treating the whole auth framework surface as the local default when a module only needs a few named operations
- letting plugin or auth-library vocabulary replace the application's own domain terms

### Valibot

What makes this a good example:

- plain object literals and pure factory functions
- modular building blocks with explicit composition
- small API pieces that stay predictable when combined

What to avoid:

- exposing internal composition mechanics to consumers
- adding schema helpers that save keystrokes but obscure intent

### ts-pattern

What makes this a good example:

- tiny semantic core
- names that explain the flow by themselves: `match`, `with`, `otherwise`, `exhaustive`

What to avoid:

- introducing pattern matching where simple `if` or `switch` is clearer
- chaining so much logic that the branch structure disappears

### neverthrow

What makes this a good example:

- explicit success and failure values
- narrow, composable result vocabulary

What to avoid:

- wrapping every trivial function in `Result`
- replacing straightforward exceptions when failure is truly exceptional

## Contrast Example: ts-rest

What is useful:

- contract-first design with plain data shapes
- explicit request and response structure

Why it is a contrast, not the default bar for this skill:

- the contract surface is richer and more configuration-heavy than the target simplicity bar
- names and concepts can become less obvious once headers, params, metadata, and response maps all accumulate

Use ts-rest as evidence that plain-data contracts can scale.
Do not treat its complexity level as the default interface target when a smaller surface would do.

## TypeScript Heuristics

If you are rewriting a TypeScript API, prefer this order of choices:

1. plain named function
2. small object of named functions or procedures
3. a narrow builder only when it materially improves correctness

For application structure, prefer naming conventions that reveal shape directly over directives or framework context that silently change semantics.

Reach for classes, fluent chains, or meta-programming only when they pay for themselves in clarity at the call site.
