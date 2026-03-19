# Sources

This file tracks source material synthesized into `skill-writer`, plus iterative changes over time.

## Current source inventory

| Source | Type | Trust tier | Retrieved | Confidence | Contribution | Usage constraints | Notes |
|---|---|---|---|---|---|---|---|
| `plugins/sentry-skills/skills/skill-writer/SKILL.md` | local canonical | canonical | 2026-03-05 | high | Baseline orchestration, path model, quality gates | local repository authority | Primary source of current behavior |
| `plugins/sentry-skills/skills/skill-writer/references/*.md` | local canonical | canonical | 2026-03-05 | high | Detailed path guidance, examples, validation requirements | local repository authority | Includes synthesis/iteration/evaluation paths |
| `plugins/sentry-skills/skills/skill-creator/SKILL.md` | local compatibility alias | canonical | 2026-03-05 | high | Backward-compatible invocation behavior | local repository authority | Confirms alias delegates to `skill-writer` |
| `.codex/skills/.system/skill-creator/SKILL.md` | local Codex upstream | secondary | 2026-03-05 | medium | Codex-native skill authoring conventions and structure | environment-local snapshot; may diverge from upstream | Used to align cross-agent portability expectations |
| `https://github.com/anthropics/skills/tree/main/skills/skill-creator` | external Claude upstream | canonical | 2026-03-05 | medium | Claude-native prior art and updated guidance | verify periodically against upstream changes | Track for periodic refresh as upstream evolves |
| `https://agentskills.io/specification` | external canonical spec | canonical | 2026-03-05 | high | Portable skill spec requirements | spec-level constraints take precedence over local preferences | Cross-agent compatibility baseline |
| `AGENTS.md` | repo convention | canonical | 2026-03-05 | high | Repository-specific workflow requirements | repository-local policy | Registration + validator expectations |
| `README.md` | repo convention | canonical | 2026-03-05 | high | Skill table format and authoring conventions | repository-local policy | Registration and discoverability source |

## Decisions

1. `skill-writer` is the single canonical workflow; `skill-creator` remains alias-only for compatibility.
2. Source breadth is the primary quality lever; synthesis cannot stop early on limited samples.
3. Provenance is stored in `SOURCES.md`, not SKILL header comments.
4. Case-study style examples are required for deeper, reusable synthesis outcomes.
5. Path guidance in `skill-writer` is agent-generic (no Claude-only root assumptions in workflow docs).

## Open gaps

1. Anthropic upstream source should be periodically re-reviewed for changes and recorded here with new retrieval dates.
2. Add concrete example `SOURCES.md` files in synthesized skills to demonstrate expected depth in practice.

## Changelog

- 2026-03-05: Initialized `SOURCES.md` with baseline source pack (local canonical, Codex upstream, Claude upstream, spec, and repo conventions).
- 2026-03-19: Clarified path-resolution guidance so bundled skill references stay skill-root-relative while registration steps are resolved from the repository's active layout.
- 2026-03-19: Made portability a default authoring rule and disallowed provider-specific path variables in generic skills.
