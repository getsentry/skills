# Execution Shapes

Use this guide to choose the runtime shape of a skill before you decide its files.
Default rule: choose the simplest adequate shape, then add complexity only when it clearly improves outcomes.
Once you pick a shape, load only the concrete leaf references it needs.

## Defaulting To The Simplest Shape

Start from these questions, in order:

1. Can one coherent set of instructions handle most requests?
   If yes, prefer `inline-guidance`.
2. Is the main complexity optional knowledge rather than control flow?
   If yes, prefer `reference-backed-expert`.
3. Is the hard part data extraction, validation, or repeatable automation?
   If yes, prefer `script-backed-workflow`.
4. Does the user usually invoke the skill with explicit parameters?
   If yes, add `argument-driven`.
5. Only then consider routing, worker delegation, subagent execution, hooks, or templates.

Do not jump to advanced mechanics because they sound powerful.

## Complexity Budget

Adding shape complexity should usually replace ambiguity, not add ceremony.

| Addition | Require |
|----------|---------|
| new reference | a routed lookup need that existing files cannot satisfy precisely |
| new script | a repeated operation that is fragile or error-prone in plain instructions |
| new route | distinct inputs that require different tools, references, or output contracts |
| provider-specific mechanic | a capability that portable prompt guidance cannot provide |

If the benefit is only "more thorough", keep the simpler shape and tighten the existing instructions.

## Shape Decision Table

| Shape | Use when | Open next | Portability notes |
|-------|----------|-----------|-------------------|
| `inline-guidance` | one coherent policy, checklist, or procedure is enough | `references/layout-inline-skill.md` | most portable default |
| `reference-backed-expert` | optional deep knowledge is the main complexity | `references/layout-reference-backed-skill.md` | portable if file references stay relative |
| `script-backed-workflow` | repeated parsing, validation, APIs, or transformations are fragile in plain shell | `references/layout-script-backed-workflow.md` | portable if dependencies are explicit |
| `argument-driven` | the skill is usually invoked with issue numbers, paths, targets, or modes | `references/layout-argument-driven-skill.md` | often provider-specific beyond basic manual invocation |
| `router` | distinct categories need different downstream prompts, tools, or references | `references/workflow-routing.md` | portable if routing stays in prompt logic |
| `parallelization` | independent subtasks or multiple votes improve speed or confidence | `references/workflow-parallel.md` | often implemented with tools or agents |
| `orchestrator-workers` | the number or type of subtasks is discovered at runtime | `references/workflow-orchestrator-workers.md` | usually higher-latency and provider-sensitive |
| `subagent-fork` | the skill needs isolated context, tools, or model defaults | `references/claude-subagent-fork.md` | Claude Code-specific |
| `hook-backed` | deterministic enforcement is required beyond prompt guidance | `references/claude-hook-backed.md` | highly provider-specific and security-sensitive |
| `asset-template` | reusable templates, schemas, or static artifacts carry most of the value | `references/layout-asset-template-skill.md` | portable if assets are generic files |

If the chosen shape also uses explicit arguments, Claude-specific frontmatter, or shell preprocessing, load the matching flat `references/claude-*` file listed in `SKILL.md`.

## Secondary Workflow Mechanics

These are not usually primary execution shapes, but they often refine one:

- fixed ordered steps -> `references/workflow-prompt-chaining.md`
- validate-fix-repeat loops -> `references/workflow-validation-loops.md`
- plan-before-execute flows -> `references/workflow-plan-validate-execute.md`

## Hybrid Shapes

Use a hybrid only when one primary shape is insufficient.

1. Declare one primary shape.
2. Add only the minimum secondary shapes needed.
3. Keep each secondary shape scoped to one concrete need.
4. Remove or narrow any older shape guidance that the secondary shape replaces.
5. Avoid stacking multiple advanced shapes without a clear base path.

## Advanced-Shape Hard Stops

Do not finalize a skill when any of these are true:

1. The chosen shape is implied but not named.
2. A simpler shape was not considered.
3. A router has no fallback or default path.
4. A subagent-fork skill contains only passive guidance.
5. A hook-backed skill lacks a security note or fallback behavior.
6. Provider-specific mechanics are used without portability notes.
