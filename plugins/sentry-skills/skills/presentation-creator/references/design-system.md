# Sentry Presentation Design System

## Color Palette

### CSS Variables

```css
:root {
  --dark: #1c1028;
  --purple: #6c5fc7;
  --purple-light: #b5aade;
  --purple-bg: #ede8f5;
  --sentry-red: #f55459;
  --red-bg: #fde8e9;
  --green: #2ba185;
  --bg: #faf9fb;
  --card: #f3f1f5;
  --muted: #80708f;
  --border: #dbd6e1;
}
```

### JS Color Constants (for Charts.jsx)

```javascript
const PURPLE = '#6c5fc7';
const PURPLE_LIGHT = '#b5aade';
const RED = '#f55459';
const GREEN = '#2ba185';
const DARK = '#1c1028';
const MUTED = '#80708f';
const BORDER = '#dbd6e1';
const AMBER = '#d4953a';
```

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
.tag-red { background: var(--red-bg); color: var(--sentry-red); }
.tag-green { background: #e0f5ef; color: var(--green); }
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

## Navigation Bar

```css
nav {
  position: fixed; bottom: 0; left: 0; right: 0;
  display: flex; align-items: center; justify-content: center;
  gap: 16px; padding: 14px; background: #fff;
  border-top: 1px solid var(--border); z-index: 5;
}
nav button {
  background: none; border: 1px solid var(--border);
  border-radius: 6px; padding: 4px 14px; cursor: pointer;
  font-family: inherit; font-size: 0.8rem; color: var(--dark);
}
```

### Dot Indicators

```css
.dots { display: flex; gap: 6px; }
.dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--border); cursor: pointer;
  transition: background 0.2s;
}
.dot.on { background: var(--purple); }
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

## Sentry Logo Component

```jsx
function SentryLogo({ size = 32 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 72 66" fill="none">
      <path d="M29 2.3a4.4 4.4 0 0 0-7.6 0L.7 40.2a4.3 4.3 0 0 0 3.8 6.5h9.6a4.3 4.3 0 0 0 3.8-2.2l13-22.6a18 18 0 0 1 8 14.8h-4a14 14 0 0 0-6.7-11.5l-9.4 16.4h-11L25.2 8.3l18 31.3h-5.8a22 22 0 0 0-10.8-18.2l-3.4 5.9a16 16 0 0 1 8.7 12.3H22a10 10 0 0 0-5.4-7.6l-2 3.6a6 6 0 0 1 2 4h-5a2 2 0 0 1-1.6-3l18-31.3 21 36.4h-7.7a26 26 0 0 0-12.8-22.6l-3.4 5.9a20 20 0 0 1 10.6 16.7h-4.6a16 16 0 0 0-8.6-13l-3.4 5.9a10 10 0 0 1 6.5 7.1H16a6 6 0 0 0-3.3-3.6l-1.6 2.8a2 2 0 0 1 .5.8h-2a4.3 4.3 0 0 1-3.8-6.5L25.2 4.6a.4.4 0 0 1 .7 0l22 38.1h5.5L30.7 3.5z"
        fill="currentColor" />
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
