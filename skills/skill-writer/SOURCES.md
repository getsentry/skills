# Sources

This file tracks source material synthesized into `skill-writer`, plus iterative changes over time.

## Current source inventory

| Source | Type | Trust tier | Retrieved | Confidence | Contribution | Usage constraints | Notes |
|---|---|---|---|---|---|---|---|
| `SKILL.md` | local canonical | canonical | 2026-05-01 | high | Baseline orchestration, path model, and runtime contract | local active skill root | Primary source of current behavior |
| `references/**/*.md` | local canonical | canonical | 2026-05-01 | high | Detailed path guidance, examples, routed leaf references, and validation requirements | local active skill root | Includes shape, synthesis, iteration, evaluation, provider-specific guidance, and lookup-oriented subfolders |
| `SPEC.md` | local canonical | canonical | 2026-05-01 | high | Canonical maintenance contract for intent, scope, evidence model, evaluation, and limitations | local active skill root | Updated to treat `skill-writer` as a meta-router |
| `https://agentskills.io/specification` | external canonical spec | canonical | 2026-05-01 | high | Portable skill structure, frontmatter, progressive disclosure, optional directories, and file-reference rules | spec-level constraints take precedence over local preferences | Cross-agent compatibility baseline |
| `https://agentskills.io/skill-creation/best-practices` | external official docs | canonical | 2026-05-01 | high | Coherent unit design, moderate detail, progressive disclosure, defaults over menus, validation loops, plan-validate-execute | skill-authoring guidance, not provider-specific runtime semantics | Informed shape-selection and workflow guidance |
| `https://agentskills.io/skill-creation/using-scripts` | external official docs | canonical | 2026-05-01 | high | Script bundling, non-interactive requirements, `--help`, structured output, and safe script interfaces | script examples are illustrative, adapt to local tooling | Informed script-backed workflow requirements |
| `https://code.claude.com/docs/en/skills` | external official docs | canonical | 2026-05-01 | high | Current Claude Code skill lifecycle, frontmatter fields, argument features, `context: fork`, `allowed-tools`, and hooks-in-skills support | provider-specific; do not generalize to portable Agent Skills behavior | Replaced stale local assumptions about Claude-specific fields |
| `https://code.claude.com/docs/en/sub-agents` | external official docs | canonical | 2026-05-01 | high | Automatic delegation, focused subagents, explicit invocation modes, and subagent lifecycle integration | provider-specific | Informed `subagent-fork` shape guidance |
| `https://code.claude.com/docs/en/hooks` | external official docs | canonical | 2026-05-01 | high | Hook lifecycle, hooks in skills and agents, async constraints, and security requirements | provider-specific and security-sensitive | Informed `hook-backed` shape guidance and safety notes |
| `https://www.anthropic.com/engineering/building-effective-agents` | external official engineering guidance | canonical | 2026-05-01 | high | Simplicity-first design and workflow taxonomy: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer | conceptual guidance; adapt to skill authoring rather than full app orchestration | Core source for execution-shape taxonomy |
| `https://developers.openai.com/api/docs/guides/reasoning-best-practices` | external official docs | canonical | 2026-05-01 | high | Planner/doer distinction, reasoning-vs-GPT model tradeoffs, and avoiding explicit chain-of-thought prompting | provider-specific model guidance; use only as general orchestration input unless exact product syntax matters | Informed reasoning-model and evaluator-loop notes |
| `https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/` | external official guidance | canonical | 2026-05-01 | high | Maximize a single agent first, use multi-agent only when needed, manager-vs-handoff split, layered guardrails | product-level guidance, not a skills standard | Informed simplicity rule and advanced-shape escalation criteria |
| `https://openai.github.io/openai-agents-python/agents/` | external official SDK docs | canonical | 2026-05-01 | medium | Manager-vs-handoff distinction and structured-output support | SDK-specific implementation details | Informed router/orchestrator language and contract expectations |
| `https://openai.github.io/openai-agents-python/handoffs/` | external official SDK docs | canonical | 2026-05-01 | medium | Handoff metadata, input filters, and receiving-agent history control | SDK-specific implementation details | Informed route/handoff contract guidance |
| `https://huggingface.co/docs/hub/model-cards` | external documentation pattern | secondary | 2026-04-26 | high | Model-card sections for intended use, data, evaluation, limitations, and reproducibility | adapted as documentation prior art, not a skill standard | Inspired `SPEC.md` maintenance contract shape |
| `https://huggingface.co/docs/hub/en/model-card-annotated` | external documentation pattern | secondary | 2026-04-26 | high | Annotated intended-use, out-of-scope, risks, limitations, and evaluation sections | adapted as documentation prior art, not a skill standard | Informed SPEC scope and limitations sections |
| `https://cacm.acm.org/research/datasheets-for-datasets/` | research/documentation pattern | secondary | 2026-04-26 | high | Data provenance, collection, composition, intended use, and maintenance transparency | adapted from dataset documentation to skill evidence documentation | Informed source/evidence model and privacy rules |
| `https://diataxis.fr/` | documentation framework | secondary | 2026-04-26 | high | User-need-centered documentation types: tutorial, how-to, reference, explanation | adapted as information architecture prior art, not a skill standard | Informed reference files as lookup needs rather than topic buckets |
| `https://dita-lang.org/` | documentation standard | secondary | 2026-04-26 | high | Topic-oriented technical content patterns: task, concept, reference, troubleshooting | adapted as documentation architecture prior art | Informed reference type table and troubleshooting matrix guidance |
| `https://www.writethedocs.org/guide/writing/docs-principles/` | documentation guidance | secondary | 2026-04-26 | medium | Documentation should be structured for findability, reuse, and user participation | general writing guidance | Cross-check for reference architecture usability |
| `AGENTS.md` | repo convention | canonical | 2026-05-01 | high | Repository-specific workflow requirements and registration checklist | repository-local policy | Registration + validator expectations |
| `README.md` | repo convention | canonical | 2026-05-01 | high | Skill table format and authoring conventions | repository-local policy | Registration and discoverability source |

## Decisions

1. `skill-writer` is a meta-router: it must choose both a skill class and an execution shape before authoring.
2. Default to the simplest adequate shape. Advanced mechanics require evidence and an explicit reason simpler shapes were rejected.
3. Skill class and execution shape are independent axes. Class drives coverage requirements; shape drives runtime mechanics and artifact layout.
4. `SKILL.md` remains the orchestration/index layer; references, scripts, assets, hooks, and subagents are leaves selected by that router.
5. Provider-specific Claude Code features are valuable but not default. Use them only when justified and record portability implications.
6. Claude-specific frontmatter guidance should track the current `code.claude.com/docs/en/skills` fields, including `when_to_use`, `arguments`, `effort`, `paths`, `shell`, `context`, `agent`, and `hooks`.
7. Router, parallel/orchestrator, evaluator-loop, subagent-fork, and hook-backed shapes each require explicit contracts, not just prose.
8. Hooks are deterministic enforcement and need narrow scope plus security notes because command hooks run with full user permissions.
9. Multi-agent guidance should distinguish manager/orchestrator, handoff, and isolated subagent execution instead of collapsing them into one pattern.
10. Reasoning-model guidance is a design option, not a universal default: planner/doer splits are useful when complexity warrants them.
11. Validation should check architectural choices qualitatively, not only file structure and prose depth.
12. Reference files remain split by lookup need rather than topic buckets, even as the set of supported shapes expands.
13. Subfolders inside `references/` are acceptable when they create clearer lookup leaves, but every bundled reference should still be directly discoverable from `SKILL.md`.
14. The validator should enforce durable structural guarantees and required fields, but should not hardcode provider-specific optional frontmatter keys.

## Coverage matrix

| Dimension | Coverage status | Evidence |
|---|---|---|
| SKILL.md vs references placement | complete | Agent Skills spec, local reference architecture |
| Reference splitting heuristics | complete | Agent Skills best practices, Diataxis, DITA, local reference architecture and artifact-layout guidance |
| Long reference navigation | complete | local design principles |
| Source discovery beyond docs | complete | local synthesis depth gates, repository history practices |
| Commit log as source material | complete | local source-discovery guidance |
| Positive/negative evidence storage | complete | local iteration path, prior eval guidance |
| Skill maintenance specification | complete | model cards, datasheets, local `SPEC.md` reference implementation |
| Shape-selection framework | complete | Anthropic effective agents, OpenAI practical guide, local execution-shapes guidance |
| Router/orchestrator/evaluator patterns | complete | Anthropic effective agents, OpenAI agent guides, local workflow-mechanics guidance |
| Current Claude skill frontmatter and lifecycle mechanics | complete | Claude Code skills docs |
| Subagent-fork guidance | complete | Claude Code skills docs, subagents docs |
| Hook-backed guidance and security constraints | complete | Claude Code hooks docs |
| Script-backed workflow design | complete | Agent Skills using scripts guide |
| Planner/doer reasoning guidance | complete | OpenAI reasoning best practices |
| Lookup-oriented reference architecture | complete | Diataxis user needs, DITA topic types, local reference architecture |

## Open gaps

1. The validator still only partially checks advanced-shape contracts; deeper automated checks may be worth adding.
2. This repository still has few real shipped examples using `hooks`, `context: fork`, `when_to_use`, `arguments`, `paths`, or `effort`.
3. Public repo docs outside `skill-writer` may need follow-up updates to fully reflect the current Claude-specific skill fields.

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
- 2026-05-01: Reworked `skill-writer` around explicit execution-shape routing, added shape-specific example profiles, refreshed Claude Code provider mechanics from current official docs, and added eval/source guidance for routing, delegation, hooks, and evaluator loops.
- 2026-05-01: Replaced generic pattern bucket references with routed leaf files under `references/artifact-layouts/`, `references/workflow-mechanics/`, and `references/claude-code/`; made `SKILL.md` enumerate every bundled reference file with a direct open-when reason.
- 2026-05-01: Removed the validator's hardcoded optional frontmatter allowlist so provider-specific field drift does not create noisy false warnings.
