---
name: migrate-container-queries
description: Guide for migrating viewport media queries (@media, useMedia) to container queries in Sentry's frontend. Use when migrating responsive layout to container queries, replacing @media/useMedia, refactoring styled responsive components to Container/Flex/Grid primitives, or working on the DE container-query migration.
---

# Container Query Migration Guide

Migrate viewport-based responsive logic (`@media` + `useMedia`) to container queries so components respond to their own available space instead of the raw viewport. Reference migration: trace-view PR getsentry/sentry#120315.

## Approach: refactor first, swap second

Work down this ladder — stop at the first rung that fits. Prefer replacing hand-rolled CSS with primitives over a mechanical token swap.

| Rung | When | Do |
|------|------|-----|
| 1. Primitive props | The `@media` only flips layout (`flex-direction`, `display`, `grid-template`, gap, visibility, width) | Delete the styled component; use `Container`/`Flex`/`Grid`/`Stack` responsive props (`direction={{xs: 'column', md: 'row'}}`) |
| 2. `@container` swap | CSS can't be a prop (descendant selectors, pseudo-elements, `font-size`, complex `grid-template-areas`) | Keep the styled component; swap `@media` → `@container`, `theme.breakpoints.*` → `theme.container.*` |
| 3. `useContainerBreakpoint()` | Width is read in JS to branch rendering | Replace `useMedia(...)` with `useContainerBreakpoint()` |
| 4. Leave as `useMedia` | Genuine media feature, not width (see below) | Do nothing — these do not migrate |

## ⚠️ Breakpoints and container scales are NOT the same

The token scales have **different keys and different pixel values**. This is not a rename.

| `theme.breakpoints` | | `theme.container` | |
|---|---|---|---|
| `2xs` | 0px | `zero` | 0px |
| `xs` | 500px | `3xs` | 320px |
| `sm` | 800px | `2xs` | 384px |
| `md` | 992px | `xs` | 448px |
| `lg` | 1200px | `sm` | 512px |
| `xl` | 1440px | `md` | 576px |

Pick the `container` token that matches the element's **actual rendered width**, not the same key. `breakpoints.sm` (800px) is nowhere near `container.sm` (512px). Getting this wrong is the #1 migration bug — the trace PR's original code "compared a container measurement to the wrong (breakpoint) scale."

## container-type: only when no query container is in scope

A root query container is already declared in `styles/global.tsx`, and app layout containers (`organizationLayout`, `topBar`, modal portal) provide others. **Do not add `container-type: inline-size` reflexively.**

- Bare responsive keys (`{xs: …}`) already resolve against the nearest container.
- Add a container only when this subtree needs its own local one.
- Prefer `inline-size` (width only); `size` also contains height and collapses content unless height comes from elsewhere.
- Conditional pattern (see `components/core/breadcrumbList/breadcrumbList.tsx`): `containerType={hasParentQueryContainer ? 'normal' : 'inline-size'}` via `useHasContainerQuery()`.

## Keep `useMedia` for genuine media features

Width is the only thing that migrates. Leave `useMedia` in place for:

`prefers-color-scheme`, `prefers-reduced-motion`, `hover`, `pointer`, `max-height` / height-based, `resolution`, `print`.

## Examples

### Rung 1 — styled `@media` → primitive props (preferred)

**Old:**

```tsx
const Row = styled('div')`
  display: flex;
  flex-direction: row;
  gap: ${p => p.theme.space.md};
  @media (max-width: ${p => p.theme.breakpoints.sm}) {
    flex-direction: column;
  }
`;
```

**New** — delete the styled component:

```tsx
import {Flex} from '@sentry/scraps/layout';

<Flex direction={{xs: 'column', sm: 'row'}} gap="md">
```

### Rung 2 — `@media` → `@container` (when it can't be a prop)

**Old:**

```tsx
const Panel = styled('section')`
  @media (max-width: ${p => p.theme.breakpoints.md}) {
    grid-template-columns: 1fr;
  }
`;
```

**New** — swap the at-rule and the scale (md breakpoint 992px ≈ container `sm`/`md`, choose by real width):

```tsx
const Panel = styled('section')`
  @container (max-width: ${p => p.theme.container.sm}) {
    grid-template-columns: 1fr;
  }
`;
```

### Rung 3 — `useMedia` (width) → `useContainerBreakpoint()`

**Old:**

```tsx
const isNarrow = useMedia(`(max-width: ${theme.breakpoints.sm})`);
return isNarrow ? <Stacked /> : <SideBySide />;
```

**New:**

```tsx
import {useContainerBreakpoint} from '@sentry/scraps/layout';

const breakpoint = useContainerBreakpoint(); // active container key: 'zero' | '3xs' | ... | 'xl'
const isNarrow = ['zero', '3xs', '2xs', 'xs'].includes(breakpoint);
```

### Anti-pattern — blind key rename

```tsx
// ❌ Same key, wrong pixel value — sm breakpoint (800px) ≠ sm container (512px)
@container (max-width: ${p => p.theme.container.sm}) // was breakpoints.sm

// ✅ Choose the container token matching the element's real width; verify in the browser
```

## Verify

- `@container` silently no-ops if there is no query-container ancestor — confirm one exists (root, layout, or a local `containerType`).
- Resize the element (not just the window) and confirm the breakpoint flips at the intended width.
- Visual output must be identical; the DOM/CSS diff may be larger (a deleted styled component is the intended outcome, not scope creep).

## Migration Checklist

- [ ] Prefer rung 1: replace styled `@media` with `Container`/`Flex`/`Grid`/`Stack` responsive props
- [ ] Rung 2 only when CSS can't be a prop: `@media` → `@container`, `theme.breakpoints.*` → `theme.container.*`
- [ ] Choose the `container` token by real width — do NOT reuse the breakpoint key
- [ ] Replace width `useMedia` → `useContainerBreakpoint()`; keep `useMedia` for non-width media features
- [ ] Add `container-type` only if no query container is already in scope; prefer `inline-size`
- [ ] Confirm a query-container ancestor exists so `@container` resolves
- [ ] Verify visually identical output by resizing the element
