---
name: flowchart-maker
description: Use this skill to draw flow-chart illustrations for engineering blog posts — system diagrams, request paths, retry loops, swimlanes. Contains the full token set, node/edge markup primitives, and composition rules for a flat-editorial, line-drawn figure style. Output is plain HTML/CSS (no libraries), exportable to PNG or SVG. Includes `flowfig.py`, which renders a Mermaid flowchart spec into this style.
user-invocable: true
---

# Flow figures

A line-drawn, flat-editorial illustration system for explaining how a system works to other engineers. Figures are built from a fixed vocabulary — five node types, four edge types, three marks — laid out on CSS grid. Nothing is hand-drawn; nothing is bespoke.

## Generator: `flowfig.py`

Prefer the generator over hand-written markup. Write a Mermaid flowchart to a `.mmd` file, then run the bundled script from the repository root:

```bash
uv run ${CLAUDE_SKILL_ROOT}/scripts/flowfig.py figure.mmd                          # writes figure.html
uv run ${CLAUDE_SKILL_ROOT}/scripts/flowfig.py figure.mmd --png figure.png --scale 2
```

- Requires the `uv` CLI (https://docs.astral.sh/uv/getting-started/installation/). The script has no dependencies beyond the Python standard library, so `python3` works too.
- `--png` needs Google Chrome or Chromium on the machine and takes a few seconds per figure. Without a browser, deliver the HTML and tell the user to screenshot the plate at 2x.
- The script prints the output path on success and rule violations on stderr. A parse error names the offending statement; fix the spec and rerun.
- Rubik is embedded from `assets/fonts/rubik-latin.woff2` (SIL Open Font License, see `assets/fonts/OFL.txt`), so the output needs no network.
- Example specs with rendered PNGs live in `references/examples/`. Open one when unsure how a pattern should look.

Supported Mermaid subset:

```
%% note: An annotation rendered inside the plate.
%% steps: queue, send, ok          numbered badges in reading order
%% width: 1200                     max plate width in px
graph LR                           or: flowchart TD
  queue[(Queue)] --> send[Send webhook<br/>POST · 10s timeout]:::focus
  send --> ok{2xx?}
  ok -- yes --> done((Delivered))
  ok -- no --> retry[Backoff<br/>attempt < 5]:::warn
  retry -.->|requeue| queue
  retry --x dead([Dead letter]):::fail
  subgraph ingest [Ingest tier]     dashed group boundary, may nest
    a --> b
  end
```

- Shapes: `[process]`, `([terminal])`, `((filled end state))`, `[(store)]`, `{decision}`.
- Text after `<br/>` becomes the mono sub-label.
- Edges: `-->` solid, `-.->` dashed, `--x` failure (pink). An edge into a `fail` node is pink too.
- Labels: `-->|label|` or `-- label -->`. A bracketed label `-->|[40 ms]|` renders as a yellow measurement chip.
- Tones: `:::focus`, `:::warn`, `:::fail`, or `class a,b focus`.
- Layout hints: `:::below` forces a node under its parent, `:::beside` forces it to the next column. By default a non-primary successor with no outgoing edges drops below its parent; everything else goes right.
- Figures carry no title, number, legend, or caption. The host page supplies those. Put what the reader must know into node labels and the optional `%% note:`.
- The tool warns on stderr when a figure breaks a rule: more than nine nodes, more than three accented nodes, an upward failure edge, or overlapping edges.

Edit the generated HTML only for one-off tweaks. Change the spec for anything structural.

## Tokens

```css
:root {
  /* ink & paper */
  --ink:        #2B2233;  /* strokes, node titles */
  --muted:      #80708F;  /* mono labels, lane names */
  --body:       #4D4158;  /* captions, annot */
  --rule:       #E0DCE5;  /* hairlines, grid overlay */
  --wash:       #F5F3F7;  /* swimlane bands */
  --paper:      #FAF9FB;  /* page */
  --plate:      #FFFFFF;  /* figure background, node fill */

  /* signal — use sparingly */
  --accent:     #6C5FC7;  /* the node the paragraph is about */
  --accent-ink: #4D3FA3;  /* mono label on accent fill */
  --accent-fill:#EFEBFA;
  --accent-line:#C6BEEB;  /* dashed boundaries */
  --warn:       #FFC227;  /* attention — the slow or costly step */
  --warn-ink:   #7A5200;
  --warn-fill:  #FFF4D4;
  --warn-line:  #F5DFA3;
  --fail:       #FF45A8;  /* failure paths only */
  --fail-ink:   #B01B70;
  --fail-fill:  #FFEBF5;

  /* geometry */
  --stroke: 2.5px;        /* node + edge strokes */
  --stroke-plate: 3px;
  --r-node: 10px;
  --r-plate: 18px;
  --shadow-node: 4px 4px 0;   /* hard offset, no blur — colour = ink, or the node's own accent */
  --shadow-plate: 8px 8px 0;
  --unit: 8px;            /* all spacing is a multiple */
}
```

Fonts: **Rubik** (500/600/700) for titles, captions, node labels. **Monaco** (`Monaco, Menlo, 'Ubuntu Mono', monospace` — no webfont) for every small label — always uppercase, `letter-spacing: .08em–.12em`, 11px.

Type scale: node title 17/700 · secondary node title 16/700 · caption 16/500 · annotation 15/500 · mono label 12/500 caps (700 for eyebrows).

## Primitives

Copy these verbatim. All values are literal — do not round them.

**Process node** (the default)
```html
<div style="display:flex;flex-direction:column;gap:5px;padding:13px 15px;border:2.5px solid #2B2233;border-radius:10px;background:#FFFFFF;box-shadow:4px 4px 0 #2B2233;">
  <div style="font:600 15px/1.2 'Rubik',-apple-system,system-ui,sans-serif;">Relay</div>
  <div style="font:400 11px/1.3 Monaco,Menlo,'Ubuntu Mono',monospace;letter-spacing:.05em;color:#80708F;">auth · rate limit</div>
</div>
```

**Focus node** — same, but `border:2.5px solid #2B2233; background:#EFEBFA; box-shadow:4px 4px 0 #6C5FC7;` and the sub-label in `#4D3FA3`. Max two per figure.

**Attention node** — same, but `border:2.5px solid #2B2233; background:#FFF4D4; box-shadow:4px 4px 0 #FFC227;` and the sub-label in `#7A5200`. Marks the slow, costly, or noisy step — never an error.

**Failure node** — same, but `border:2.5px solid #2B2233; background:#FFEBF5; box-shadow:4px 4px 0 #FF45A8;` and the sub-label in `#B01B70`.

**Terminal** — `padding:13px 24px; border:2.5px solid #2B2233; border-radius:999px; box-shadow:4px 4px 0 #2B2233;`. Filled (`background:#2B2233; color:#FFFFFF;`) for the end state.

**Decision** — a rotated square with counter-rotated text:
```html
<div style="width:106px;height:106px;border:2.5px solid #2B2233;background:#EFEBFA;box-shadow:4px 4px 0 #6C5FC7;transform:rotate(45deg);display:flex;align-items:center;justify-content:center;">
  <div style="transform:rotate(-45deg);font:600 13px/1.15 'Rubik',-apple-system,system-ui,sans-serif;text-align:center;">2xx?</div>
</div>
```
Wrap it in a fixed-height flex cell (~154px) so the rotation doesn't disturb the grid.

**Store** — `padding:19px 21px; border:2.5px solid #2B2233; border-radius:50%/18px;` (the cylinder).

**Edge, horizontal** — a flex row: line + CSS-triangle head.
```html
<div style="display:flex;align-items:center;">
  <div style="flex:1;height:3px;background:#2B2233;"></div>
  <div style="width:0;height:0;border-left:12px solid #2B2233;border-top:8px solid transparent;border-bottom:8px solid transparent;"></div>
</div>
```

**Edge, vertical** — flex column: `<div style="flex:1;width:3px;background:#2B2233;">` + head `border-top:12px solid #2B2233; border-left:8px solid transparent; border-right:8px solid transparent;`. Flip the head's border side to point up.

**Edge variants** — dashed for async/deferred/conditional (`border-top:3px dashed` horizontally, `border-left:3px dashed` vertically); `#FF45A8` for failure; labelled = stack an 11px mono caps label above the line in the same cell.

**Marks** — step badge: `width:30px;height:30px;border-radius:999px;background:#6C5FC7;color:#FFFFFF;border:2.5px solid #2B2233;font:700 13px/25px Monaco,Menlo,'Ubuntu Mono',monospace;text-align:center;`. Annotation: a 3px accent vertical rule + 15px body sentence. Measurement chip: `padding:3px 7px;border-radius:3px;background:#FFC227;font:500 10px/1.3 Monaco,monospace;letter-spacing:.05em;color:#2B2233;` — stack it above an edge to label latency or volume. Group boundary: `border:2.5px dashed #C6BEEB;border-radius:14px;`.

**Figure plate** — `background:#FFFFFF;border:3px solid #2B2233;border-radius:18px;box-shadow:8px 8px 0 #2B2233;padding:46px 38px;`. No caption, figure number, or legend below the plate. The page that embeds the figure supplies those.

## Layout method

Never absolutely position edges. Use one CSS grid per figure with **alternating node and edge columns**, named `grid-template-areas`, and `align-items:center`:

```css
grid-template-columns: minmax(146px,1fr) 76px minmax(146px,1fr) 76px minmax(146px,1fr);
grid-template-rows: auto 60px auto;
grid-template-areas:
  'sdk  e1  relay  e2  queue'
  '.    .   v1     .   .'
  '.    .   reject .   .';
```

Edge cells are 68–76px wide / 58–62px tall (the 12px arrowheads need the room). L-shaped return edges are two orthogonal segments in adjacent cells (a half-width horizontal stub in the node's own column, then a vertical segment in the row above). Swimlane bands are full-row divs placed with explicit `grid-column:1/-1; grid-row:N;` **before** the node cells in source order, with `margin:-14px 0` to bleed past the nodes.

## Three patterns

1. **Linear path with branches** — one left-to-right spine, exceptions dropped below. The default; use for "what happens to a request".
2. **Decision with a loop back** — one diamond, one dashed orthogonal return edge. Use for retries, polling, reconciliation.
3. **Swimlanes with numbered steps** — lanes for tiers, badges for reading order. Use when the point is which tier owns which step. (Not yet supported by the generator; hand-write the lane bands.)

## Rules

- One idea per figure. Two sentences to describe it means two figures.
- No titles, numbers, legends, or captions inside the figure. Labels on nodes and edges must stand on their own.
- Nine nodes, hard cap. Past nine, split it or collapse a group into one node with a dashed boundary.
- Accent is scarce — blurple marks only the node(s) the surrounding paragraph is about; yellow marks the one that costs time; pink is exceptions only. Never more than three accented nodes in one figure.
- Orthogonal edges only. No diagonals, no curves, no crossings.
- Edge labels are mono, caps, two or three words. Sentences go in the caption or annotation.
- Flow reads left, then down. Never route a failure upward.
- Every node and plate carries a hard offset shadow, never a blurred one. Node shadows are 4px ink — or the node's own accent when it is a focus/attention/exception node. Plates are 8px ink.
- Light mode only — this system has no dark variant. Don't invent one; ask.
- Never hand-draw SVG illustration. Every shape here is a bordered div, a CSS triangle, or a rotated square.

## Export

Figures are plain HTML/CSS, so screenshot the plate element at 2–3× for PNG, leaving room for the 8px offset shadow (transparent-safe: the plate is opaque white). `flowfig.py --png` does this through headless Chrome. For SVG, redraw the same geometry as `<rect>`/`<line>`/`<polygon>` at the same literal values — the 2.5px stroke, 10px radius and hard offset shadow carry the style. Target 1200–1600px wide for full-width in-post figures.
