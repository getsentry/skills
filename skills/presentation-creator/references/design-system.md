# Sentry Presentation Design System

## Color Palette

### Color Philosophy

Use two distinct color sets:

1. **Semantic colors** — Only when the color itself carries meaning (good/bad, success/failure, warning). Do not use these for arbitrary data grouping.
2. **Categorical colors** — For distinguishing data series, groups, or categories where color has no inherent meaning. Inspired by Tableau's palette for maximum distinguishability.

### CSS Variables

```css
:root {
  /* ── UI chrome ── */
  --dark: #1c1028;
  --purple: #6c5fc7;
  --purple-light: #b5aade;
  --purple-bg: #ede8f5;
  --bg: #faf9fb;
  --card: #f3f1f5;
  --muted: #80708f;
  --border: #dbd6e1;

  /* ── Semantic (use ONLY when meaning applies) ── */
  --semantic-green: #2ba185;   /* positive, success, good */
  --semantic-red: #f55459;     /* negative, failure, bad */
  --semantic-amber: #d4953a;   /* warning, caution, moderate */
  --semantic-green-bg: #e0f5ef;
  --semantic-red-bg: #fde8e9;
  --semantic-amber-bg: #fdf3e4;
}
```

### JS Color Constants (for Charts.jsx)

```javascript
// ── UI / chrome ──
const DARK = '#1c1028';
const MUTED = '#80708f';
const BORDER = '#dbd6e1';

// ── Categorical palette (Tableau-inspired) ──
// Use for data series, groups, and categories where color is just a label.
const CAT = [
  '#4e79a7',  // steel blue
  '#f28e2b',  // orange
  '#e15759',  // coral
  '#76b7b2',  // teal
  '#59a14f',  // green
  '#edc948',  // gold
  '#b07aa1',  // mauve
  '#ff9da7',  // pink
  '#9c755f',  // brown
  '#bab0ac',  // gray
];

// ── Semantic (use ONLY when the color conveys meaning) ──
const SEM_GREEN = '#2ba185';   // positive / success / good
const SEM_RED = '#f55459';     // negative / failure / bad
const SEM_AMBER = '#d4953a';   // warning / caution
```

### When to use which

| Scenario | Palette | Example |
|----------|---------|---------|
| Bar chart comparing 7 SKU types | `CAT[0]`–`CAT[6]` | Each SKU gets a distinct hue, none implies "good" or "bad" |
| Stacked area: accepted vs dropped | Semantic | green = accepted (good), red = dropped (bad) |
| Heatmap cells: adopted vs not | Semantic | green dot = adopted, empty = not |
| Before/after comparison | `CAT[0]` / `CAT[1]` | Two neutral colors, neither implies better |
| Priority columns: Protect / Grow / Expand | Semantic | green = protect, amber = grow, red = expand gaps |
| Multiple org lines on same chart | `CAT` | Each org gets next color in sequence |

## Typography

**Font**: Rubik (Google Fonts) with system-ui fallback.

```css
body {
  font-family: 'Rubik', system-ui, -apple-system, sans-serif;
  color: var(--dark);
  background: var(--bg);
  line-height: 1.7;
  font-size: 0.9rem;
}
```

| Element | Size | Weight | Extra |
|---------|------|--------|-------|
| h1 | 2.5rem | 700 | letter-spacing: -0.03em |
| h2 | 1.55rem | 600 | letter-spacing: -0.02em |
| h3 | 1rem | 600 | — |
| subtitle | 0.95rem | 400 | max-width: 620px, color: var(--muted) |
| body | 0.9rem | 400 | line-height: 1.7 |

## Slide System CSS

```css
.progress {
  position: fixed; top: 0; left: 0; height: 3px;
  background: var(--purple); transition: width 0.3s; z-index: 10;
}

.slide {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  opacity: 0; pointer-events: none;
  transition: opacity 0.45s ease;
}
.slide.active { opacity: 1; pointer-events: auto; }

.slide-content {
  width: 100%; max-width: 880px;
  padding: 60px 40px 100px;
}
```

## Tags

Used on every slide to label the category (Background, Problem, Proposal, etc.).

```css
.tag {
  display: inline-block; font-size: 0.66rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.08em;
  padding: 4px 10px; border-radius: 4px;
  margin-bottom: 8px;
}
.tag-purple { background: var(--purple-bg); color: var(--purple); }
.tag-red { background: var(--semantic-red-bg); color: var(--semantic-red); }
.tag-green { background: var(--semantic-green-bg); color: var(--semantic-green); }
.tag-amber { background: var(--semantic-amber-bg); color: var(--semantic-amber); }
```

## Layout Utilities

```css
.cols { display: flex; gap: 40px; max-width: 1060px; }
.col { flex: 1; }

.cards { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.card {
  background: #fff; border: 1px solid var(--border);
  border-radius: 8px; padding: 17px;
}

.chart-wrap { max-width: 920px; margin: 0 auto; }
```

## Animations

```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.anim h2, .anim .subtitle, .anim .cols,
.anim .cards, .anim .chart-wrap, .anim table,
.anim .zone-diagram, .anim ul {
  opacity: 0; animation: fadeUp 0.5s ease both;
}

.anim .d1 { animation-delay: 0.1s; }
.anim .d2 { animation-delay: 0.2s; }
.anim .d3 { animation-delay: 0.3s; }
```

Add the `.anim` class to `.slide-content` only when the slide is active. Use `.d1`, `.d2`, `.d3` on child elements for staggered entrance.

## Persistent Glyph Watermark

Every slide shows a small, low-contrast Sentry glyph in the top-left corner. Use the exact path from `${CLAUDE_SKILL_ROOT}/references/sentry-glyph.svg`.

```css
.glyph-watermark {
  position: fixed; top: 20px; left: 24px; z-index: 8;
  opacity: 0.12; pointer-events: none;
  display: flex; align-items: center; gap: 10px;
}
.watermark-title {
  font-size: 1.1rem; font-weight: 600;
  letter-spacing: -0.01em;
  line-height: 1;
}
```

Hidden on the title slide (slide 0), shown on all others:

```jsx
{cur > 0 && (
  <div className="glyph-watermark">
    <SentryGlyph size={50} />
    <span className="watermark-title">Presentation Title</span>
  </div>
)}
```

## Navigation

Navigation sits at the bottom of the viewport with **no border, no background separation** — it floats transparently over the slide. Always show the slide number as `{current} / {total}`.

```css
nav {
  position: fixed; bottom: 0; left: 0; right: 0;
  display: flex; align-items: center; justify-content: center;
  gap: 16px; padding: 14px;
  z-index: 5;
}
nav button {
  background: none; border: none;
  cursor: pointer; font-family: inherit;
  font-size: 0.8rem; color: var(--muted);
  padding: 4px 8px;
}
nav button:hover { color: var(--dark); }
nav button:disabled { opacity: 0.2; cursor: default; }
.slide-number {
  font-size: 0.75rem; color: var(--muted);
  font-variant-numeric: tabular-nums;
}
```

### Dot Indicators

```css
.dots { display: flex; gap: 6px; }
.dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--border); cursor: pointer;
  transition: background 0.2s;
}
.dot.on { background: var(--purple); }
```

### Nav Component

```jsx
function Nav({ cur, total, go, setCur }) {
  return (
    <nav>
      <button onClick={() => go(-1)} disabled={cur === 0}>←</button>
      <div className="dots">
        {Array.from({ length: total }, (_, i) => (
          <div key={i} className={`dot${i === cur ? ' on' : ''}`} onClick={() => setCur(i)} />
        ))}
      </div>
      <button onClick={() => go(1)} disabled={cur === total - 1}>→</button>
      <span className="slide-number">{cur + 1} / {total}</span>
    </nav>
  );
}
```

## Icons

Use Material Symbols Outlined for icons:

```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap" rel="stylesheet" />
```

```jsx
<span className="material-symbols-outlined">chevron_right</span>
```

## Comparison Tables

```css
.compare { width: 100%; border-collapse: collapse; }
.compare th {
  text-align: left; font-weight: 600;
  padding: 10px 14px; border-bottom: 2px solid var(--border);
}
.compare td { padding: 10px 14px; border-bottom: 1px solid #f0edf3; }
```

## Sentry Logo

**Do NOT hardcode the Sentry logo as inline SVG.** Read the official SVGs from the skill references directory:

- **Full wordmark**: `${CLAUDE_SKILL_ROOT}/references/sentry-logo.svg` — the "Sentry" logotype with glyph. Use on title slides.
- **Glyph only**: `${CLAUDE_SKILL_ROOT}/references/sentry-glyph.svg` — the standalone glyph mark. Use for compact branding.

Read the SVG file contents and embed them as a React component using `dangerouslySetInnerHTML` or by extracting the `<path>` data:

```jsx
// Read the SVG file, extract the content, and embed it:
function SentryLogo({ width = 120 }) {
  // The SVG content should be read from references/sentry-logo.svg
  // and embedded directly — never use a hardcoded approximation.
  return (
    <svg viewBox="0 0 200 44" width={width} fill="none" aria-hidden="true">
      {/* paste exact path data from sentry-logo.svg */}
    </svg>
  );
}

function SentryGlyph({ size = 32 }) {
  return (
    <svg viewBox="0 0 72 66" width={size} height={size} aria-hidden="true">
      {/* paste exact path data from sentry-glyph.svg */}
    </svg>
  );
}
```

## Wrapup Column Variants

For summary/decision slides with multi-column layouts:

```css
.wrapup-col--muted { border-top: 3px solid #80708f; }
.wrapup-col--muted h3 { color: #3e3450; }
.wrapup-col--muted li::before {
  content: 'chevron_right';
  font-family: 'Material Symbols Outlined';
  color: #80708f;
}
```
