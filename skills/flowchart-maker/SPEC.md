# Flowchart Maker Specification

## Intent

Produce flow-chart illustrations for engineering blog posts in one fixed visual style: flat-editorial, line-drawn, built from five node types, four edge types and three marks on a CSS grid. The style is encoded twice so it cannot drift: as literal markup primitives in `SKILL.md` for hand-written figures, and as `scripts/flowfig.py`, which renders a Mermaid flowchart subset into the same markup and exports PNG through headless Chrome.

## Scope

In scope:
- System diagrams, request paths, retry loops, grouped tiers, and top-down decision flows with nine nodes or fewer.
- The design tokens, node and edge primitives, layout method and composition rules of the style.
- A deterministic renderer for a Mermaid flowchart subset, with HTML and PNG output.

Out of scope:
- Sequence, class, state, ER or Gantt diagrams. Use `mermaid-layout` for those.
- Charts and data visualizations.
- A dark variant. The style is light mode only.
- Swimlane bands. The generator does not draw them; hand-write the lane markup from `SKILL.md`.

## Users And Trigger Context

- Primary users: engineers and agents illustrating how a system works in a blog post, design doc or internal explainer.
- Common user requests: "draw a figure of the request path", "make an illustration of the retry loop", "render this flowchart in the blog style", "turn this Mermaid graph into a figure", "export the diagram as PNG".
- Should not trigger for: plain Mermaid source meant for a markdown renderer, sequence or class diagrams, charts, slides, UI mockups.

## Runtime Contract

- Required first actions: write the figure as a Mermaid flowchart spec, then run `scripts/flowfig.py` on it. Fall back to hand-written primitives only for what the generator cannot draw.
- Required outputs: an HTML file with the plate, and a PNG when the user wants an image. Report the output paths.
- Non-negotiable constraints:
  - Nine nodes at most, three accented nodes at most, orthogonal edges, hard offset shadows, light mode only.
  - No figure title, number, legend or caption inside the figure. The host page supplies those.
  - Plain-language labels when the audience is outside the team. Internal names go in the prose, not the figure.
  - Never hand-draw SVG shapes.
- Expected bundled files loaded at runtime: `SKILL.md`. The script runs from `scripts/`. `references/examples/` is opened only when a pattern needs a visual reference.

## Source And Evidence Model

Authoritative sources:
- `SKILL.md` token set and primitives, originally produced with Claude Design as a reference implementation.
- The Mermaid flowchart syntax (https://mermaid.js.org/syntax/flowchart.html) for the accepted spec subset.

Useful improvement sources:
- positive examples: figures accepted into published posts without layout edits.
- negative examples: overlapping edges, clipped labels, plates wider than the host column, figures that needed hand edits after rendering.
- commit logs/changelogs: layout and router changes in `scripts/flowfig.py`.
- issue or PR feedback: requests for unsupported Mermaid syntax or new patterns.
- eval results: the three example specs re-rendered after every script change.

Data that must not be stored:
- Customer or organization identifiers in example specs. Use generic service names.
- Secrets or internal hostnames in labels.

## Reference Architecture

- `SKILL.md` contains: generator usage, the supported Mermaid subset, tokens, primitives, layout method, the three patterns, rules and export notes.
- `references/examples/` contains: three example specs (`.mmd`) with their rendered PNGs, one per pattern.
- `scripts/flowfig.py` contains: the parser, layered layout, orthogonal edge router, HTML renderer and Chrome PNG export. Standard library only.
- `assets/fonts/` contains: the Rubik latin subset embedded into every output, with its SIL Open Font License text.

## Evaluation

- Lightweight validation: render the three example specs and inspect the PNGs. Edges must meet node borders, labels must not overlap nodes, and the plate must not clip.
- Deeper evaluation: render a spec with a back edge, a merge from a lower row and nested groups. The script must print no overlap warning.
- Holdout examples: none stored yet.
- Acceptance gates: the script exits zero on all example specs, `uv run scripts/quick_validate.py` from `skill-writer` passes, and the rendered examples match the style rules in `SKILL.md`.

## Known Limitations

- Swimlanes and step badges inside lanes are not generated.
- Edge labels wider than an edge cell (about nine mono characters) crowd the next node. Prefer two short words.
- The router picks the first conflict-free orthogonal path and warns when none exists. It does not optimize crossings globally.
- PNG export depends on a local Chrome or Chromium binary and kills the browser once the file is complete, because headless Chrome does not exit reliably.

## Maintenance Notes

- When to update `SKILL.md`: a token, primitive or rule of the style changes, or the script accepts new syntax.
- When to update `SOURCES.md`: not kept for this skill. Record source changes in the PR description.
- When to update `EVAL.md`: not kept for this skill. The example specs are the evaluation set.
- When to update `references/evidence/`: when a figure needed hand edits after rendering, store the spec and the fix as a negative example.
