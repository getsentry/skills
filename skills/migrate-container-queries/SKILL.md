---
name: migrate-container-queries
description: Guide for migrating viewport media queries (@media, useMedia) to container queries in Sentry's frontend. Use when migrating responsive layout to container queries, replacing @media/useMedia, refactoring styled responsive components to Container/Flex/Grid primitives, or working on the DE container-query migration.
---

# Container Query Migration Guide

Migrate viewport-based responsive logic (`@media` + `useMedia`) to container queries so components respond to their own available space instead of the raw viewport.

> **Always do a visual check.** After every migration, resize the *element* (not just the window) and confirm the layout is identical and flips at the intended width. The token scales differ, so a mechanical swap that compiles can still render wrong.

## Approach: refactor first, swap second

Stop at the first rung that fits. Prefer replacing hand-rolled CSS with primitives over a mechanical token swap.

| Rung | When | Do |
|------|------|-----|
| 1. Primitive props | The `@media` only flips layout (`flex-direction`, `display`, `grid-template`, gap, visibility, width) | Delete the styled component; use `Container`/`Flex`/`Grid`/`Stack` responsive props (`direction={{xs: 'column', md: 'row'}}`) |
| 2. `@container` swap | CSS can't be a prop (descendant selectors, pseudo-elements, `font-size`, complex `grid-template-areas`) | Keep the styled component; swap `@media` → `@container`, `theme.breakpoints.*` → `theme.container.*` |
| 3. `useResponsivePropValue()` | Width is read in JS to branch rendering | Replace `useMedia(...)` with `useResponsivePropValue({...})`; use `useContainerBreakpoint()` only when you need the raw active key |
| 4. Leave as `useMedia` | Genuine media feature, not width | Do nothing — these do not migrate |

## ⚠️ Convert to the nearest container scale

Breakpoint and container scales have **different keys and different pixel values** — this is not a rename. Reusing the same key is the #1 migration bug.

| `theme.breakpoints` | | `theme.container` | |
|---|---|---|---|
| `2xs` | 0px | `zero` | 0px |
| `xs` | 500px | `3xs` | 320px |
| `sm` | 800px | `2xs` | 384px |
| `md` | 992px | `xs` | 448px |
| `lg` | 1200px | `sm` | 512px |
| `xl` | 1440px | `md` | 576px |

**Rule:** find the element's actual rendered width, then pick the `container` token whose pixel value is *nearest* to that width — never the token with the matching key. `breakpoints.sm` (800px) is nowhere near `container.sm` (512px). Confirm the choice with a visual check.

## Keep `useMedia` for genuine media features

Width is the only thing that migrates. Leave `useMedia` in place for:
`prefers-color-scheme`, `prefers-reduced-motion`, `hover`, `pointer`, `max-height` / height-based, `resolution`, `print`.

## container-type: only when no query container is in scope

The app's main content is already wrapped in a query container: `ContentStack` (`#main`) in `views/organizationLayout/index.tsx` sets `containerType="inline-size"` and wraps the routed `<Outlet />`, so product views have a container ancestor. `topBar` has its own, and `#modal-portal` (in `styles/global.tsx`) covers portaled content that lives outside the app tree. **Do not add `container-type: inline-size` reflexively.**

**Default: don't add one.** Bare responsive keys (`{xs: …}`) and `@container` queries already resolve against the nearest ancestor container. Add `container-type` only when this subtree must respond to *its own* width rather than the page's.

When you do add one:

- Use `inline-size` (width only). `size` also queries height, which collapses content unless height is set elsewhere.
- For a reusable component that may or may not already sit inside a container, make it conditional so it doesn't create a redundant one — `containerType={hasParentQueryContainer ? 'normal' : 'inline-size'}` via `useHasContainerQuery()` (see `components/core/breadcrumbList/breadcrumbList.tsx`).

## Examples

### Rung 1 — styled `@media` → primitive props (preferred)

```tsx
// Old — delete the styled component
const Row = styled('div')`
  display: flex;
  flex-direction: row;
  gap: ${p => p.theme.space.md};
  @media (max-width: ${p => p.theme.breakpoints.sm}) {
    flex-direction: column;
  }
`;

// New
import {Flex} from '@sentry/scraps/layout';
<Flex direction={{xs: 'column', sm: 'row'}} gap="md">
```

### Rung 2 — `@media` → `@container` (when it can't be a prop)

```tsx
// Old
@media (max-width: ${p => p.theme.breakpoints.md}) { ... }

// New — swap at-rule AND scale; md breakpoint (992px) → nearest container by real width,
// NOT theme.container.md by matching key
@container (max-width: ${p => p.theme.container.sm}) { ... }
```

### Rung 3 — `useMedia` (width) → `useResponsivePropValue()`

```tsx
// Old
const isNarrow = useMedia(`(max-width: ${theme.breakpoints.sm})`);

// New — resolve a per-breakpoint map against the current container (mirrors rung-1 props)
import {useResponsivePropValue} from '@sentry/scraps/layout';
const isNarrow = useResponsivePropValue({xs: true, sm: false});

// Only when you need the raw active key itself (to log or pass along):
import {useContainerBreakpoint} from '@sentry/scraps/layout';
const breakpoint = useContainerBreakpoint(); // 'zero' | '3xs' | ... | 'xl'
```

## Migration Checklist

- [ ] Rung 1: replace styled `@media` with `Container`/`Flex`/`Grid`/`Stack` responsive props
- [ ] Rung 2 (CSS can't be a prop): `@media` → `@container`, `theme.breakpoints.*` → `theme.container.*`
- [ ] Choose the `container` token nearest the element's real width — never reuse the breakpoint key
- [ ] Rung 3: width `useMedia` → `useResponsivePropValue({...})` (or `useContainerBreakpoint()` for the raw key); keep `useMedia` for non-width media features
- [ ] Add `container-type` only when a subtree must respond to its own width; prefer `inline-size`
- [ ] Confirm a query-container ancestor exists so `@container` resolves (it silently no-ops otherwise)
- [ ] **Visual check:** resize the element and confirm identical output flipping at the intended width
