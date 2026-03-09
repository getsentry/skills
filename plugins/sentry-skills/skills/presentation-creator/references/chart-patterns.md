# Recharts Patterns for Sentry Presentations

## Color Usage Rules

**Categorical palette** — for data series, groups, categories where color is just a distinguisher:
```javascript
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
```

**Semantic colors** — ONLY when the color itself carries meaning:
```javascript
const SEM_GREEN = '#2ba185';   // positive / success / good
const SEM_RED = '#f55459';     // negative / failure / bad
const SEM_AMBER = '#d4953a';   // warning / caution
```

**Rule of thumb**: If you could swap two colors without losing information, use `CAT`. If swapping would confuse the meaning (e.g., making "errors" green), use semantic.

## Shared Configuration

### Axis and Grid Defaults

```javascript
const ax = {
  axisLine: { stroke: BORDER },
  tickLine: false,
  tick: { fill: MUTED, fontSize: 11, fontFamily: 'Rubik, system-ui' }
};

const grid = {
  strokeDasharray: '3 3',
  stroke: '#f0edf3',
  vertical: false
};
```

### Tooltip Styling

```javascript
<Tooltip
  contentStyle={{
    background: '#fff',
    border: `1px solid ${BORDER}`,
    borderRadius: 6,
    fontSize: 12,
    fontFamily: 'Rubik, system-ui'
  }}
/>
```

## Common Chart Types

### 1. Stacked Area Chart (ComposedChart)

Best for showing volume breakdowns over time.

When the series have inherent good/bad semantics (accepted vs dropped), use semantic colors:

```jsx
<Area type="monotone" dataKey="accepted" stackId="1"
  fill={SEM_GREEN} stroke={SEM_GREEN} fillOpacity={0.7} />
<Area type="monotone" dataKey="dropped" stackId="1"
  fill={SEM_RED} stroke={SEM_RED} fillOpacity={0.5} />
```

When the series are neutral categories (e.g., different SDK types, regions), use categorical:

```jsx
<Area type="monotone" dataKey="javascript" stackId="1"
  fill={CAT[0]} stroke={CAT[0]} fillOpacity={0.6} />
<Area type="monotone" dataKey="python" stackId="1"
  fill={CAT[1]} stroke={CAT[1]} fillOpacity={0.6} />
<Area type="monotone" dataKey="ruby" stackId="1"
  fill={CAT[2]} stroke={CAT[2]} fillOpacity={0.6} />
```

### 2. Bar Chart (Grouped/Stacked)

For discrete comparisons. Use `CAT` colors unless the bars represent good/bad outcomes.

```jsx
<ResponsiveContainer width="100%" height={280}>
  <BarChart data={data}>
    <CartesianGrid {...grid} />
    <XAxis dataKey="name" {...ax} />
    <YAxis {...ax} />
    <Bar dataKey="seriesA" fill={CAT[0]} radius={[3, 3, 0, 0]} />
    <Bar dataKey="seriesB" fill={CAT[1]} radius={[3, 3, 0, 0]} />
  </BarChart>
</ResponsiveContainer>
```

For a single-series bar chart where all bars represent the same metric, use a single `CAT` color uniformly — do NOT alternate colors per bar unless the bars represent distinct categories.

### 3. Line/Area Curve Chart

Best for showing mathematical relationships (rate curves, thresholds).

```jsx
<ResponsiveContainer width="100%" height={300}>
  <ComposedChart data={curveData}>
    <CartesianGrid {...grid} />
    <XAxis dataKey="x" {...ax} label={{ value: 'Incoming (t/s)', ... }} />
    <YAxis {...ax} domain={[0, 100]} label={{ value: 'Rate %', ... }} />
    <Area type="monotone" dataKey="rate" fill={CAT[0]} fillOpacity={0.15} stroke={CAT[0]} strokeWidth={2} />
  </ComposedChart>
</ResponsiveContainer>
```

### 4. Temporal Scenario Chart (stepAfter)

Best for showing discrete rule updates with lag. Use semantic colors when steps represent accept/reject:

```jsx
<Area type="stepAfter" dataKey="accepted" stackId="1"
  fill={SEM_GREEN} stroke={SEM_GREEN} fillOpacity={0.6} />
<Area type="stepAfter" dataKey="hardBlocked" stackId="1"
  fill={SEM_RED} stroke="none" fillOpacity={0.5} />
```

### 5. Reference Lines and Areas

```jsx
{/* Threshold line — semantic amber for "warning" boundary */}
<ReferenceLine y={300} stroke={SEM_AMBER} strokeDasharray="6 3" />

{/* Shaded zone — semantic green for "safe" region */}
<ReferenceArea x1="03:00" x2="03:10" fill={SEM_GREEN} fillOpacity={0.08}
  label={{ value: '~10 min', fill: SEM_GREEN, fontSize: 11 }} />
```

## Data Generation Patterns

### Gaussian Spike

```javascript
function gaussian(x, center, width, height) {
  return height * Math.exp(-((x - center) ** 2) / (2 * width ** 2));
}
```

### Sinusoidal Daily Pattern

```javascript
const base = 200 + 50 * Math.sin((i / 144) * Math.PI * 2 - Math.PI / 2);
```

### Exponential Adaptation Lag

```javascript
const lagFactor = Math.min(1, (i - spikeStart) / lagIntervals);
const effectiveRate = prevRate + (targetRate - prevRate) * lagFactor;
```

### useMemo for Data

Always wrap data generation in `useMemo`:

```javascript
const data = useMemo(() => {
  return Array.from({ length: 144 }, (_, i) => {
    // generate point
    return { label, incoming, accepted, sampled };
  });
}, []);
```

## Custom Diagram Components

### Zone Diagram

Horizontal bar showing zones. Use semantic colors ONLY when zones carry meaning (e.g., Normal=green, Danger=red). For neutral categories, use `CAT`:

```jsx
function ZoneDiagram({ zones }) {
  return (
    <div className="zone-diagram">
      {zones.map((z, i) => (
        <div key={i} style={{ flex: z.flex, background: z.color, padding: '12px 16px', color: '#fff' }}>
          <div className="zone-name">{z.name}</div>
          <div className="zone-desc">{z.desc}</div>
        </div>
      ))}
    </div>
  );
}
```

```css
.zone-diagram { display: flex; gap: 2px; border-radius: 8px; overflow: hidden; }
```

### Trace Diagram

Visual span representation for distributed traces. Use `CAT` for different services:

```jsx
function TraceDiagram({ rows }) {
  return (
    <div className="trace-diagram">
      {rows.map((r, i) => (
        <div key={i} className="trace-row">
          <span className="trace-label">{r.label}</span>
          <div className="trace-bar">
            {r.spans.map((s, j) => (
              <div key={j} style={{
                flex: s.w, background: s.bg || CAT[j % CAT.length],
                opacity: s.opacity ?? 1,
                borderRadius: 3
              }} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
```

### Sparkline (Mini SVG Chart)

```jsx
function Sparkline({ seed = 0, bars = 14, color = CAT[0] }) {
  const h = Array.from({ length: bars }, (_, i) =>
    20 + ((seed * 17 + i * 31) % 60)
  );
  return (
    <svg width={bars * 5} height={40} style={{ verticalAlign: 'middle' }}>
      {h.map((v, i) => (
        <rect key={i} x={i * 5} y={40 - v * 0.4} width={3.5}
          height={v * 0.4} rx={1} fill={color} opacity={0.7} />
      ))}
    </svg>
  );
}
```

## Chart Container Pattern

Always wrap charts in a container div:

```jsx
<div className="chart-wrap d2">
  <ResponsiveContainer width="100%" height={320}>
    {/* chart */}
  </ResponsiveContainer>
  <p style={{ fontSize: '0.8rem', color: MUTED, textAlign: 'center', marginTop: 8 }}>
    Chart annotation or description
  </p>
</div>
```

## Responsive Sizing

- Default chart height: 280-340px
- Side-by-side charts: 260-300px each
- Mini/sparkline charts: 80-120px
- Always use `ResponsiveContainer` with `width="100%"`
- Set explicit `margin` on the chart component for axis label space
