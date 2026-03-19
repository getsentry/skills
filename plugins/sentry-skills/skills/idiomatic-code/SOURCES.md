# Sources

This file tracks source material synthesized into `idiomatic-code`, plus the decisions taken from that material.

## Selected example profile

- `plugins/sentry-skills/skills/skill-writer/references/examples/documentation-skill.md`
  - Used as the closest synthesis pattern for a source-backed, reference-heavy skill with intent-based loading and transformed examples.

## Current source inventory

| Source | Type | Trust tier | Retrieved | Confidence | Contribution | Usage constraints | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `AGENTS.md` | repo convention | canonical | 2026-03-17 | high | Registration rules, alias policy, path conventions | repository-local policy | Required local source of truth |
| `README.md` | repo convention | canonical | 2026-03-17 | high | Public skill inventory format and authoring conventions | repository-local policy | Determines README registration shape |
| `plugins/sentry-skills/skills/code-simplifier/SKILL.md` | local adjacent skill | canonical | 2026-03-17 | high | Boundary definition versus generic simplification | repository-local policy | Used to keep trigger boundaries clean |
| `plugins/sentry-skills/skills/security-review/SKILL.md` | local pattern example | canonical | 2026-03-17 | high | Domain-expert skill structure with selective reference loading | repository-local policy | Used as the main structural pattern |
| `plugins/sentry-skills/skills/skill-writer/SKILL.md` | local canonical | canonical | 2026-03-17 | high | Required workflow for creating this skill | repository-local policy | Primary local authoring workflow |
| `plugins/sentry-skills/skills/skill-writer/references/*.md` | local canonical | canonical | 2026-03-17 | high | Synthesis, authoring, description optimization, and validation requirements | repository-local policy | Includes required provenance and artifact expectations |
| `https://orpc.unnoq.com/` | external official docs | canonical | 2026-03-17 | medium | Primary TypeScript exemplar for plain public shapes and clean RPC design | docs may evolve | Anchor exemplar for TypeScript guidance |
| `https://orpc.unnoq.com/docs/migrations/from-trpc` | external official docs | canonical | 2026-03-17 | medium | Confirms object-router and `handler`-oriented design differences | docs may evolve | Supports the skill's oRPC-first bias |
| `https://trpc.io/docs/server/procedures` | external official docs | canonical | 2026-03-17 | medium | Secondary RPC exemplar and comparison point | docs may evolve | Used for contrast and limited positive evidence |
| `https://hono.dev/docs/api/` | external official docs | canonical | 2026-03-17 | medium | Small-core routing and Web-standard-aligned API design | docs may evolve | Positive TypeScript exemplar |
| `https://hono.dev/docs/guides/rpc` | external official docs | canonical | 2026-03-17 | medium | Shows how an RPC surface can remain small on top of Hono | docs may evolve | Supports plain-surface guidance |
| `https://valibot.dev/guides/internal-architecture/` | external official docs | canonical | 2026-03-17 | medium | Pure factory function and plain-object design rationale | docs may evolve | Positive TypeScript exemplar |
| `https://github.com/gvergnaud/ts-pattern` | external upstream README | secondary | 2026-03-17 | medium | Tiny semantic core and naming clarity for fluent APIs | GitHub README, not a formal spec | Positive but narrower TypeScript exemplar |
| `https://github.com/supermacro/neverthrow` | external upstream README | secondary | 2026-03-17 | medium | Explicit result-based failure semantics | GitHub README, not a formal spec | Positive TypeScript exemplar for visible failures |
| `https://ts-rest.com/quickstart` | external official docs | canonical | 2026-03-17 | medium | Contrast example for richer contract-first APIs | docs may evolve | Used to define what is beyond the default simplicity bar |
| `https://docs.nestjs.com/fundamentals/custom-providers` | external official docs | canonical | 2026-03-17 | high | Contrast example for provider, token, and factory-heavy DI surfaces | docs may evolve | Used for machinery-heavy failure mode |
| `https://inversify.io/docs/api/container/` | external official docs | canonical | 2026-03-17 | high | Contrast example for container-managed binding and resolution vocabulary | docs may evolve | Used for machinery-heavy failure mode |
| `https://inversify.io/docs/ecosystem/binding-decorators/` | external official docs | canonical | 2026-03-17 | medium | Confirms decorator-driven registration as a contrast smell when overused | docs may evolve | Supports Inversify contrast guidance |
| `https://stately.ai/docs/setup` | external official docs | canonical | 2026-03-17 | high | Contrast example for concept-heavy state-machine setup vocabulary | docs may evolve | Used for concept-heavy failure mode |
| `https://stately.ai/docs/xstate` | external official docs | canonical | 2026-03-17 | high | Confirms state machines, actors, and orchestration as the public model | docs may evolve | Supports XState contrast guidance |
| `https://gcanti.github.io/fp-ts/` | external official docs | canonical | 2026-03-17 | high | Contrast example for abstraction-first FP vocabulary | docs may evolve | Used for abstraction-first failure mode |
| `https://gcanti.github.io/fp-ts/modules/` | external official docs | canonical | 2026-03-17 | high | Shows breadth of module and type-class surface area | docs may evolve | Supports fp-ts contrast guidance |
| `https://effect.website/` | external official docs | canonical | 2026-03-17 | high | Contrast example for style-shift, learning curve, and extensive API surface | docs may evolve | Used to classify Effect precisely rather than as blanket complexity |
| `https://nextjs.org/docs/app/getting-started/server-and-client-components` | external official docs | canonical | 2026-03-17 | high | Contrast example for server/client split behavior and component-mode boundaries | docs may evolve | Used for Next.js hidden-boundary guidance |
| `https://nextjs.org/docs/app/api-reference/directives/use-client` | external official docs | canonical | 2026-03-17 | high | Confirms file-level client boundary behavior and serialization constraints | docs may evolve | Supports directive-based contrast guidance |
| `https://nextjs.org/docs/app/api-reference/directives/use-server` | external official docs | canonical | 2026-03-17 | high | Confirms file-level and inline server function directives | docs may evolve | Supports server action boundary guidance |
| `https://nextjs.org/docs/app/getting-started/updating-data` | external official docs | canonical | 2026-03-17 | high | Confirms Server Actions as framework-mediated mutation interfaces | docs may evolve | Supports Next.js mutation contrast guidance |
| `https://nextjs.org/docs/app/api-reference/file-conventions` | external official docs | canonical | 2026-03-17 | high | Confirms breadth of file-system conventions affecting behavior | docs may evolve | Supports convention-driven contrast guidance |
| `https://nextjs.org/docs/app/api-reference/file-conventions/intercepting-routes` | external official docs | canonical | 2026-03-17 | medium | Contrast example for routing behavior added by special folder conventions | docs may evolve | Supports advanced route-convention guidance |
| `https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes` | external official docs | canonical | 2026-03-17 | medium | Shows slot-based route composition and special folder semantics | docs may evolve | Supports routing complexity guidance |
| `https://nextjs.org/docs/app/api-reference/file-conventions/route-groups` | external official docs | canonical | 2026-03-17 | medium | Shows route grouping as a positive convention that can become harder to reason about when overused | docs may evolve | Supports nuanced Next.js classification |
| `https://remix.run/docs/en/main/file-conventions/routes` | external official docs | canonical | 2026-03-17 | high | Positive reference for route file naming that is easier to reason about than directive-driven mode switches | docs may evolve | Supports Remix-vs-Next.js naming distinction |
| `https://www.better-auth.com` | external official docs | canonical | 2026-03-17 | medium | Positive reference for explicit auth configuration and a visible client/server split | docs may evolve | Supports better-auth as a secondary TypeScript exemplar |
| `https://www.better-auth.com/docs/concepts/plugins` | external official docs | canonical | 2026-03-17 | medium | Supports plugin additions as visible configuration rather than hidden behavior | docs may evolve | Supports better-auth exemplar guidance |
| `https://requests.readthedocs.io/en/latest/user/quickstart/` | external official docs | canonical | 2026-03-17 | high | Primary Python exemplar for obvious verbs and short examples | docs may evolve | Positive Python anchor |
| `https://www.python-httpx.org/quickstart/` | external official docs | canonical | 2026-03-17 | high | Modern client design with requests-like usability and explicit options | docs may evolve | Positive Python exemplar |
| `https://pluggy.readthedocs.io/en/stable/` | external official docs | canonical | 2026-03-17 | medium | Small extension vocabulary with clear roles | docs may evolve | Positive Python exemplar for extensibility interfaces |
| `https://click.palletsprojects.com/en/stable/` | external official docs | canonical | 2026-03-17 | medium | Clear command/function mapping and readable option names | docs may evolve | Positive Python exemplar |
| `https://docs.python.org/3/library/pathlib.html` | external standard library docs | canonical | 2026-03-17 | medium | Coherent object model and direct naming | Python version may vary | Secondary Python exemplar |

## Decisions

1. `idiomatic-code` is a design and interface skill, not a general simplification skill.
2. TypeScript guidance is biased toward plain object and function APIs rather than fluent magic.
3. oRPC is the primary TypeScript exemplar because its naming and interface shape are closer to the target simplicity bar than ts-rest.
4. ts-rest remains useful as a contrast example for "plain data, but more surface area than needed by default."
5. Python guidance is anchored on requests and HTTPX style APIs with small surfaces and short contract docs.
6. The skill remains documentation-only in v1; no scripts are necessary.
7. Transformed examples are required because abstract advice is too easy to apply shallowly.
8. Named contrast examples are grouped by failure mode, not by a blanket notion of quality.
9. Effect is a style-shift contrast, not simply a "too complex" library.
10. Machinery-heavy and concept-heavy smells are useful warning labels when reviewing local abstractions.
11. Convention-driven design can be good; Next.js is a contrast because some conventions become hidden mode boundaries that alter runtime behavior.
12. The negative lesson from Next.js is not "avoid conventions" but "avoid semantics that depend mainly on directives, file placement, or framework context."
13. Naming conventions can be a positive design tool when they reveal structure directly; Remix route file naming is the cleaner positive reference in this area.
14. The specific problem with Next.js is not its naming conventions but its directive-driven and context-driven semantics.
15. A full pass should pair each major contrast smell with either a positive adjacent exemplar or a transformed rewrite pattern.
16. better-auth is a positive secondary TypeScript exemplar for explicit capability configuration and a visible server/client split, but it is not a primary anchor on the level of oRPC.

## Coverage matrix

| Dimension | Coverage status | Notes |
| --- | --- | --- |
| API surface and behavior contracts | complete | Covered in `references/api-surface.md`, `SKILL.md`, and transformed examples |
| Config/runtime options | complete | Covered in `references/api-surface.md`, `references/principles.md`, and common use cases about option shapes |
| Common use cases | complete | Covered in `references/common-use-cases.md` and `references/transformed-examples.md` |
| Known issues/workarounds | complete | Covered in `references/troubleshooting-workarounds.md` |
| Version/migration variance | complete | Covered by the source set and decision to treat oRPC as the primary bar while using tRPC and ts-rest as comparison and migration context |
| Public surface shape | complete | Covered in `SKILL.md`, `references/principles.md`, and both language exemplar files |
| Naming clarity | complete | Covered in `references/principles.md` and transformed examples |
| Composition model | complete | Covered in the TypeScript and Python exemplar files |
| Docs and comments quality | complete | Covered in `SKILL.md`, `references/principles.md`, and the Python example |
| Failure semantics | complete | Covered in `references/principles.md` and the robust transformed example |
| Negative examples and corrections | complete | Covered in `references/transformed-examples.md` and `references/contrast-exemplars.md` |

## Open gaps

1. Add one more standard-library-style TypeScript exemplar if a future revision needs stronger coverage outside RPC and schema tooling.
2. Add repo-specific transformed examples from real Sentry code if future iterations need tighter local calibration.
3. Add one transformed example that explicitly removes DI/provider machinery from a small module if future iterations need a stronger rewrite pattern.

## Stopping rationale

Additional retrieval was low-yield after oRPC, Hono, Valibot, requests, HTTPX, pluggy, and Click all converged on the same guidance:

- keep the public surface small
- use names the caller can predict
- prefer plain functions and objects
- keep failure behavior visible
- teach through direct examples instead of framework philosophy

At that point, more source collection was mostly producing restatements or more complicated variants of the same ideas.

For the contrast pass, NestJS, InversifyJS, XState, fp-ts, Effect, and ts-rest converged on a second useful conclusion:

- some APIs are difficult because of machinery
- some because of concept load
- some because they assume a different programming style
- some because the contract is explicit but too rich for the common path

That made failure-mode categorization more useful than collecting more named examples.

For the Next.js pass, the official docs confirmed a third useful conclusion:

- convention-driven design is not the problem by itself
- naming conventions can be helpful when they directly reveal structure
- the problem appears when conventions become hidden mode switches
- directives, file placement, and special route folders can make behavior harder to predict than the module interface suggests

That made "convention-driven with hidden mode boundaries" a useful contrast category.

## Changelog

- 2026-03-17: Created `idiomatic-code` with source-backed TypeScript and Python exemplars, transformed examples, and repo registration notes.
- 2026-03-17: Added named contrast examples grouped by failure mode, including machinery-heavy, concept-heavy, abstraction-first, style-shift, and contract-rich categories.
- 2026-03-17: Added Next.js as a nuanced contrast example for convention-driven design with hidden mode boundaries.
- 2026-03-17: Ran a full consistency pass, added Remix as a positive naming reference in TypeScript guidance, and added a transformed example for pulling directive-driven framework boundaries to the edge.
- 2026-03-17: Tightened the trigger description, added explicit should-trigger/should-not-trigger query sets, removed unnecessary client-side directive usage from the framework-boundary example, and added better-auth as a secondary TypeScript exemplar.
