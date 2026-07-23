# Container Query Migration Guide Specification

## Intent

Give Sentry frontend engineers a reliable, low-risk path for converting viewport-based responsive logic (`@media`, `useMedia`) to container queries, so components respond to their own available width instead of the raw viewport. The dominant failure mode this skill guards against is reusing a breakpoint key as a container key: the two scales share names but not pixel values.

## Scope

In scope:
- Migrating `@media` CSS and `useMedia` width checks to container-query equivalents.
- Choosing between primitive layout props, `@container` CSS, and `useContainerBreakpoint()`.
- Mapping a breakpoint width to the *nearest* container token by pixel value.
- Deciding when to add `container-type`.

Out of scope:
- Non-width media features (`prefers-*`, `hover`, `pointer`, `resolution`, height-based, `print`) — these stay on `useMedia`.
- Building the container-query primitives or theme tokens themselves.
- General responsive-design guidance unrelated to the container-query migration.

## Users And Trigger Context

- Primary users: Sentry frontend engineers working the DE container-query migration.
- Common user requests: "migrate this to container queries", "replace `@media`/`useMedia`", "refactor these styled responsive components to primitives".
- Should not trigger for: non-width media-feature work, or new responsive code that is not a migration.

## Runtime Contract

- Required first actions: identify the lowest rung that fits (primitive prop → `@container` → `useContainerBreakpoint()` → leave as `useMedia`).
- Required outputs: migrated code plus a nearest-scale token choice justified by the element's real rendered width.
- Non-negotiable constraints:
  - Convert to the container token *nearest* the element's real width; never reuse the breakpoint key.
  - Always perform a visual check by resizing the element after migrating.
  - Keep `useMedia` for genuine (non-width) media features.
- Expected bundled files loaded at runtime: `SKILL.md` only.

## Source And Evidence Model

Authoritative sources:
- Reference migration PR getsentry/sentry#120315 (trace-view).
- Sentry theme token definitions (`theme.breakpoints`, `theme.container`).
- `components/core/breadcrumbList/breadcrumbList.tsx` (conditional `container-type` pattern).

Useful improvement sources:
- positive examples: merged migration PRs that pass visual review.
- negative examples: PRs that mismatched breakpoint/container scales.
- issue or PR feedback: reviewer comments on wrong-scale or missing-container-ancestor bugs.

Data that must not be stored: secrets, customer data, private URLs or identifiers not needed for reproduction.

## Reference Architecture

- `SKILL.md` contains: the full runtime guide (rung ladder, scale table + nearest-scale rule, examples, checklist).
- `references/` contains: nothing yet; add only if a rung needs depth beyond the inline guide.

## Validation

- Lightweight validation: `uv run scripts/quick_validate.py skills/migrate-container-queries`.
- Deeper validation: manual visual check by resizing the migrated element.
- Acceptance gates: token choice is the nearest container scale by pixel value; a query-container ancestor exists; output is visually identical.

## Known Limitations

- The breakpoint→container mapping requires knowing the element's real rendered width, which the skill cannot measure for the agent — the engineer must confirm it in the browser.
- `@container` silently no-ops without a query-container ancestor; the skill flags this but cannot detect it statically.

## Maintenance Notes

- Update `SKILL.md` when the token scales change, primitives gain/lose props, or a new rung is needed.
- Update `SPEC.md` when intent, scope, the non-negotiable constraints, or the evidence model change.
