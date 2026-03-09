# Recharts Patterns for Sentry Presentations

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

Best for showing volume breakdowns over time (accepted vs sampled vs dropped).

```jsx
<ResponsiveContainer width="100%" height={320}>
  <ComposedChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
    <CartesianGrid {...grid} />
    <XAxis dataKey="label" {...ax} />
    <YAxis {...ax} />
    <Tooltip />
    <Area type="monotone" dataKey="accepted" stackId="1"
      fill={GREEN} stroke={GREEN} fillOpacity={0.7} />
    <Area type="monotone" dataKey="sampled" stackId="1"
      fill={PURPLE} stroke={PURPLE} fillOpacity={0.5} />
    <Area type="monotone" dataKey="dropped" stackId="1"
      fill={RED} stroke={RED} fillOpacity={0.5} />
    <ReferenceLine y={300} stroke={AMBER} strokeDasharray="6 3"
      label={{ value: 'Threshold', fill: AMBER, fontSize: 11 }} />
  </ComposedChart>
</ResponsiveContainer>
```

### 2. Bar Chart (Grouped/Stacked)

Best for discrete comparisons (before/after, per-category).

```jsx
<ResponsiveContainer width="100%" height={280}>
  <BarChart data={data}>
    <CartesianGrid {...grid} />
    <XAxis dataKey="name" {...ax} />
    <YAxis {...ax} />
    <Bar dataKey="before" fill={PURPLE_LIGHT} radius={[3, 3, 0, 0]} />
    <Bar dataKey="after" fill={PURPLE} radius={[3, 3, 0, 0]} />
  </BarChart>
</ResponsiveContainer>
```

### 3. Line/Area Curve Chart

Best for showing mathematical relationships (rate curves, thresholds).

```jsx
<ResponsiveContainer width="100%" height={300}>
  <ComposedChart data={curveData}>
    <CartesianGrid {...grid} />
    <XAxis dataKey="x" {...ax} label={{ value: 'Incoming (t/s)', ... }} />
    <YAxis {...ax} domain={[0, 100]} label={{ value: 'Rate %', ... }} />
    <Area type="monotone" dataKey="rate" fill={PURPLE} fillOpacity={0.15} stroke={PURPLE} strokeWidth={2} />
  </ComposedChart>
</ResponsiveContainer>
```

### 4. Temporal Scenario Chart (stepAfter)

Best for showing discrete rule updates with lag (e.g., 10-minute sampling intervals).

Use `type="stepAfter"` for curves that change in discrete steps:

```jsx
<Area type="stepAfter" dataKey="accepted" stackId="1"
  fill={GREEN} stroke={GREEN} fillOpacity={0.6} />
<Area type="stepAfter" dataKey="hardBlocked" stackId="1"
  fill={RED} stroke="none" fillOpacity={0.5} />
```

### 5. Reference Lines and Areas

```jsx
{/* Threshold line */}
<ReferenceLine y={300} stroke={AMBER} strokeDasharray="6 3" />

{/* Shaded zone */}
<ReferenceArea x1="03:00" x2="03:10" fill={GREEN} fillOpacity={0.08}
  label={{ value: '~10 min', fill: GREEN, fontSize: 11 }} />
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

Horizontal bar showing zones (Normal, Sampling, Hard Limit):

```jsx
function ZoneDiagram({ zones }) {
  return (
    <div className="zone-diagram">
      {zones.map((z, i) => (
        <div key={i} className={`zone zone-${z.color}`} style={{ flex: z.flex }}>
          <div className="zone-name">{z.name}</div>
          <div className="zone-desc">{z.desc}</div>
        </div>
      ))}
    </div>
  );
}
```

CSS:
```css
.zone-diagram { display: flex; gap: 2px; border-radius: 8px; overflow: hidden; }
.zone { padding: 12px 16px; color: #fff; }
.zone-green { background: #2ba185; }
.zone-purple { background: #6c5fc7; }
.zone-red { background: #f55459; }
.zone-amber { background: #d4953a; }
```

### Trace Diagram

Visual span representation for distributed traces:

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
                flex: s.w, background: s.bg || PURPLE,
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
function Sparkline({ seed = 0, bars = 14, color = PURPLE }) {
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
