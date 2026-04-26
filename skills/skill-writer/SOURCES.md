# Sources

This file tracks source material synthesized into `skill-writer`, plus iterative changes over time.

## Current source inventory

| Source | Type | Trust tier | Retrieved | Confidence | Contribution | Usage constraints | Notes |
|---|---|---|---|---|---|---|---|
| `SKILL.md` | local canonical | canonical | 2026-04-19 | high | Baseline orchestration, path model, quality gates | local active skill root | Primary source of current behavior |
| `references/*.md` | local canonical | canonical | 2026-04-19 | high | Detailed path guidance, examples, validation requirements | local active skill root | Includes synthesis/iteration/evaluation paths |
| `SPEC.md` | local canonical | canonical | 2026-04-26 | high | Canonical maintenance contract example for skill intent, scope, evidence model, evaluation, and limitations | local active skill root | Added as the reference implementation for future skill specs |
| `https://agentskills.io/specification` | external canonical spec | canonical | 2026-03-05 | high | Portable skill spec requirements | spec-level constraints take precedence over local preferences | Cross-agent compatibility baseline |
| `https://agentskills.io/specification` | external canonical spec | canonical | 2026-04-26 | high | Confirms optional `scripts/`, `references/`, and `assets/`; focused references; progressive disclosure; one-level file references | spec-level constraints take precedence over local preferences | Re-reviewed for reference architecture update |
| `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices` | external official docs | canonical | 2026-04-26 | high | Concise SKILL.md guidance, split files near 500 lines, one-level references, table of contents for long references, real-usage iteration | Claude-specific examples generalized only when compatible with Agent Skills spec | Re-reviewed for reference architecture and iteration evidence update |
| `https://platform.openai.com/docs/guides/prompt-engineering` | external official docs | canonical | 2026-04-26 | high | Reinforces diverse examples and eval-backed prompt iteration | product-specific examples may evolve; use as general prompt/eval guidance | Redirects to current OpenAI developer docs |
| `https://platform.openai.com/docs/guides/evals` | external official docs | canonical | 2026-04-26 | high | Reinforces eval-first iteration loop: define task, run test inputs, analyze results, improve prompt | product-specific eval API details may evolve | Used to shape working/holdout evidence guidance |
| `https://learn.microsoft.com/en-us/agent-framework/agents/skills` | external implementation docs | secondary | 2026-04-26 | medium | Confirms broad Agent Skills packaging model and optional directories | implementation-specific; lower priority than Agent Skills spec | Cross-check for portability assumptions |
| `https://huggingface.co/docs/hub/model-cards` | external documentation pattern | secondary | 2026-04-26 | high | Model-card sections for intended use, data, evaluation, limitations, and reproducibility | adapted as documentation prior art, not a skill standard | Inspired `SPEC.md` maintenance contract shape |
| `https://huggingface.co/docs/hub/en/model-card-annotated` | external documentation pattern | secondary | 2026-04-26 | high | Annotated intended-use, out-of-scope, risks, limitations, and evaluation sections | adapted as documentation prior art, not a skill standard | Informed SPEC scope and limitations sections |
| `https://cacm.acm.org/research/datasheets-for-datasets/` | research/documentation pattern | secondary | 2026-04-26 | high | Data provenance, collection, composition, intended use, and maintenance transparency | adapted from dataset documentation to skill evidence documentation | Informed source/evidence model and privacy rules |
| `https://diataxis.fr/` | documentation framework | secondary | 2026-04-26 | high | User-need-centered documentation types: tutorial, how-to, reference, explanation | adapted as information architecture prior art, not a skill standard | Informed reference files as lookup needs rather than topic buckets |
| `https://dita-lang.org/` | documentation standard | secondary | 2026-04-26 | high | Topic-oriented technical content patterns: task, concept, reference, troubleshooting | adapted as documentation architecture prior art | Informed reference type table and troubleshooting matrix guidance |
| `https://www.writethedocs.org/guide/writing/docs-principles/` | documentation guidance | secondary | 2026-04-26 | medium | Documentation should be structured for findability, reuse, and user participation | general writing guidance | Cross-check for reference architecture usability |
| `AGENTS.md` | repo convention | canonical | 2026-03-05 | high | Repository-specific workflow requirements | repository-local policy | Registration + validator expectations |
| `README.md` | repo convention | canonical | 2026-03-05 | high | Skill table format and authoring conventions | repository-local policy | Registration and discoverability source |

## Decisions

2. Source breadth is the primary quality lever; synthesis cannot stop early on limited samples.
3. Provenance is stored in `SOURCES.md`, not SKILL header comments.
4. Case-study style examples are required for deeper, reusable synthesis outcomes.
5. Path guidance in `skill-writer` follows repository prior art: avoid host-specific absolute paths, but keep established root variables such as `${CLAUDE_SKILL_ROOT}` when the workspace already standardizes on them.
6. Skill placement defaults to `.agents/skills` unless workspace prior art establishes another location.
7. `SKILL.md` should remain an orchestration/index layer; detailed examples, source findings, rubrics, and domain facts belong in focused references.
8. Persistent iteration evidence should live under `references/evidence/` with working and holdout examples separated, while decisions and changelog entries remain in `SOURCES.md`.
9. Commit logs are an explicit source-discovery path for behavior that docs do not reveal, especially regressions, reversions, migrations, and hard-won edge cases.
10. `SPEC.md` is the root-level maintenance contract for a skill, modeled after model-card and dataset-documentation prior art but scoped to agent-skill intent, sources, evidence, evaluation, limitations, and maintenance.
11. Integration/documentation skills require coverage depth, not fixed reference filenames. The validator should warn on long references instead of enforcing specific reference file names.
12. Reference files should be named and split by lookup need: decision, task, fact lookup, concept, troubleshooting, examples, or evaluation. Generic buckets such as "common use cases" are too vague unless the skill has a concrete lookup reason for them.

## Coverage matrix

| Dimension | Coverage status | Evidence |
|---|---|---|
| SKILL.md vs references placement | complete | Agent Skills spec, Claude best practices, local design principles |
| Reference splitting heuristics | complete | Claude one-level reference guidance, local skill patterns |
| Long reference navigation | complete | Claude table-of-contents guidance, local design principles |
| Source discovery beyond docs | complete | local synthesis depth gates, repository history practices |
| Commit log as source material | complete | local source-discovery guidance added from observed repo workflow needs |
| Positive/negative evidence storage | complete | Claude real-usage iteration guidance, OpenAI eval iteration guidance, local iteration path |
| Working vs holdout examples | complete | OpenAI eval loop guidance, local evaluation path |
| Skill maintenance specification | complete | model cards, datasheets, local `SPEC.md` reference implementation |
| Flexible reference names and length warnings | complete | local validator behavior and reference architecture guidance |
| Lookup-oriented reference architecture | complete | Diataxis user needs, DITA topic types, local reference architecture |

## Open gaps

1. Anthropic upstream source should be periodically re-reviewed for changes and recorded here with new retrieval dates.
2. Add concrete example `SOURCES.md` files in synthesized skills to demonstrate expected depth in practice.
3. Consider adding validator checks for oversized catch-all references if future generated skills keep overloading single files.

## Changelog

- 2026-03-05: Initialized `SOURCES.md` with baseline source pack (local canonical, Codex upstream, Claude upstream, spec, and repo conventions).
- 2026-03-19: Clarified path-resolution guidance so bundled skill references stay skill-root-relative while registration steps are resolved from the repository's active layout.
- 2026-03-19: Made portability a default authoring rule and emphasized avoiding host-specific absolute filesystem paths.
- 2026-04-19: Updated path guidance to preserve repository-standard root variables such as `${CLAUDE_SKILL_ROOT}` instead of banning them outright.
- 2026-04-19: Restored `.agents/skills` as the default authoring target and kept repository-specific layouts as an inspected override rather than the default.
- 2026-04-19: Added explicit prior-art inspection and user-confirmation guidance when the correct skill root is unclear.
- 2026-04-26: Added reference architecture, source discovery, and iteration evidence guidance; updated synthesis, authoring, and iteration paths to prevent overloaded `SKILL.md` and catch-all reference files.
- 2026-04-26: Added `SPEC.md` as the canonical `skill-writer` maintenance specification and added `references/spec-template.md` for future skills.
- 2026-04-26: Removed fixed integration reference filename validation and added length-based reference warnings.
- 2026-04-26: Reworked reference architecture around concrete lookup needs instead of generic topic buckets.
