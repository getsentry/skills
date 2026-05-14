# Source Adaptation

Use this when turning an upstream prompt, workflow, rubric, benchmark, guide, or docs set into a reusable skill.

## Goal

Preserve the source's useful intent while rewriting the runtime shape for this repository, the Agent Skills format, and the selected execution shape.

## Adaptation Checklist

Use the rows that affect runtime behavior, maintenance, or legal/attribution handling. Do not fill every row mechanically for trivial sources.

| Decision | Record |
|----------|--------|
| source intent | what behavior the source is trying to cause |
| local target | what the generated skill should cause in this repo or agent environment |
| fidelity boundary | what must stay equivalent to the source |
| local replacement | what should be rewritten to match local conventions |
| omitted material | what was not carried forward and why |
| provenance | source URL/path, version or commit when available, trust tier, confidence, and usage constraints |
| rights and attribution | license, notice, attribution, or excerpt limits that affect bundled files |

## Rewrite Rules

1. Do not copy the source's section structure unless that structure improves runtime behavior.
2. Convert narrative instructions into decisions, checklists, examples, or output contracts.
3. Replace source-specific tool names, paths, severity labels, or provider assumptions with local equivalents unless fidelity requires them.
4. Keep provenance, rights notes, source versions, and fidelity tradeoffs in `SOURCES.md`.
5. Keep only instructions that help the agent decide, do, or verify the task at runtime.
6. If preserving benchmark or comparison behavior, state the invariant criteria and avoid tuning to expected answers.

## Precision Check

Before authoring, answer:

1. Which existing local rule should replace a source rule?
2. Which source rule is too broad, stale, provider-specific, or non-runtime?
3. Which added instruction prevents a concrete mistake that existing guidance does not cover?
4. Which source detail belongs in `SOURCES.md`, `SPEC.md`, or a focused reference instead of `SKILL.md`?

If these answers are weak, tighten an existing file instead of adding new guidance.
