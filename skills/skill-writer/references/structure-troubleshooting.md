# Structure Troubleshooting

Load this when the skill layout is unclear, overloaded, or drifting away from focused routing.

## Over-long SKILL.md

Problem: `SKILL.md` exceeds 500 lines and becomes a second encyclopedia.

Fix: extract detailed material into focused `references/` files and keep `SKILL.md` as the router.

## Additive Drift

Problem: each update adds another rule, section, or reference without removing or tightening the old one.

Fix: run the precision pass before editing and again after skill artifacts change. Replace, narrow, move, or delete existing guidance before adding new guidance.

## Missing Trigger Keywords

Problem: the description is too vague to match user language.

Fix: include the phrases users actually say.

## Trigger Info In Body Instead Of Description

Problem: "when to use" guidance appears only in the body, after triggering has already happened.

Fix: move trigger language into `description`.

## Duplicating CLAUDE.md Or AGENTS.md

Problem: the skill repeats repo-wide conventions instead of adding net-new value.

Fix: reference existing project docs and keep the skill focused on domain-specific behavior.

## Unconditional Reference Loading

Problem: the skill tells the agent to read every reference up front.

Fix: add a decision table so references load only when needed.

## Large References Without Navigation

Problem: long reference files are hard to preview and easy to misuse.

Fix: add a table of contents or split by lookup need.

## Extraneous Files

Problem: the skill directory accumulates user-facing docs or miscellaneous notes that do not help runtime, validation, or maintenance.

Fix: keep only `SKILL.md`, `SPEC.md`, `SOURCES.md`, `references/`, `scripts/`, `assets/`, and `LICENSE` when needed.

## Scripts Without Documentation

Problem: `SKILL.md` names a script but does not document arguments, output, or fallback behavior.

Fix: document the script interface and expected output shape in `SKILL.md`.

## Hardcoded Paths

Problem: the skill embeds host-specific or repo-hardcoded paths.

Fix: use skill-root-relative paths or established portable placeholders.

## First/Second Person Descriptions

Problem: the description says "I can..." or "You can use this..."

Fix: write in third person so skill discovery stays consistent.

## Time-Sensitive Information

Problem: the skill bakes in dates or transitional logic that will quietly rot.

Fix: move legacy behavior into a clearly labeled deprecated section or remove it.

## Advanced Mechanics Without Justification

Problem: the skill uses routing, `context: fork`, or hooks because they seem sophisticated.

Fix: name the shape, explain why simpler shapes were rejected, and add portability/safety notes.

## Router Without Fallback

Problem: the skill has multiple downstream paths but no default route or clarification step.

Fix: add a fallback branch that asks one clarifying question or picks a documented safe default.

## Evaluator Loop Without Stop Condition

Problem: the skill says "iterate until good" with no rubric or cap.

Fix: add a rubric plus a max-loop or plateau rule.

## Passive Guidance In Forked Context

Problem: `context: fork` is used for conventions or reference material instead of a concrete delegated task.

Fix: keep passive guidance inline; use forked execution only for actionable isolated tasks.

## Hook-Backed Enforcement Without Safety Notes

Problem: the skill uses hooks but does not explain event scope, fallback behavior, or shell risk.

Fix: add hook event scope, fallback path, and explicit security notes.

## Hidden Reference File

Problem: a bundled reference exists, but `SKILL.md` never tells the agent when to open it.

Fix: add the file to the main router with a one-line "open when..." reason, or remove/split the file if no clear reason exists.

## Generic Bucket Reference

Problem: a file groups unrelated techniques under a vague name such as "patterns", "notes", or "context".

Fix: split the file by lookup need and rename each leaf so the filename predicts why it should be opened.
