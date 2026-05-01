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
5. Only then consider routing, worker delegation, evaluator loops, subagent execution, hooks, or templates.

Do not jump to advanced mechanics because they sound powerful.

## Shape Decision Table

| Shape | Use when | Open next | Portability notes |
|-------|----------|-----------|-------------------|
| `inline-guidance` | one coherent policy, checklist, or procedure is enough | `references/artifact-layouts/inline-skill-layout.md` | most portable default |
| `reference-backed-expert` | optional deep knowledge is the main complexity | `references/artifact-layouts/reference-backed-skill-layout.md` | portable if file references stay relative |
| `script-backed-workflow` | repeated parsing, validation, APIs, or transformations are fragile in plain shell | `references/artifact-layouts/script-backed-skill-layout.md` | portable if dependencies are explicit |
| `argument-driven` | the skill is usually invoked with issue numbers, paths, targets, or modes | `references/artifact-layouts/argument-driven-skill-layout.md` | often provider-specific beyond basic manual invocation |
| `router` | distinct categories need different downstream prompts, tools, or references | `references/workflow-mechanics/routing-workflows.md` | portable if routing stays in prompt logic |
| `parallelization` | independent subtasks or multiple votes improve speed or confidence | `references/workflow-mechanics/parallel-workflows.md` | often implemented with tools or agents |
| `orchestrator-workers` | the number or type of subtasks is discovered at runtime | `references/workflow-mechanics/orchestrator-workers.md` | usually higher-latency and provider-sensitive |
| `evaluator-optimizer` | critique-and-revise loops improve output quality materially | `references/workflow-mechanics/evaluator-loops.md` | portable in concept; costly if overused |
| `subagent-fork` | the skill needs isolated context, tools, or model defaults | `references/claude-code/subagent-fork-skills.md` | Claude Code-specific |
| `hook-backed` | deterministic enforcement is required beyond prompt guidance | `references/claude-code/hook-backed-skills.md` | highly provider-specific and security-sensitive |
| `asset-template` | reusable templates, schemas, or static artifacts carry most of the value | `references/artifact-layouts/asset-template-skill-layout.md` | portable if assets are generic files |

If the chosen shape also uses explicit arguments, Claude-specific frontmatter, or shell preprocessing, load the matching file from `references/claude-code/`.

## Secondary Workflow Mechanics

These are not usually primary execution shapes, but they often refine one:

- fixed ordered steps -> `references/workflow-mechanics/prompt-chaining.md`
- validate-fix-repeat loops -> `references/workflow-mechanics/validation-loops.md`
- plan-before-execute flows -> `references/workflow-mechanics/plan-validate-execute.md`

## Hybrid Shapes

Use a hybrid only when one primary shape is insufficient.

1. Declare one primary shape.
2. Add only the minimum secondary shapes needed.
3. Keep each secondary shape scoped to one concrete need.
4. Avoid stacking multiple advanced shapes without a clear base path.

## Advanced-Shape Hard Stops

Do not finalize a skill when any of these are true:

1. The chosen shape is implied but not named.
2. A simpler shape was not considered.
3. A router has no fallback or default path.
4. An evaluator loop has no stopping rule.
5. A subagent-fork skill contains only passive guidance.
6. A hook-backed skill lacks a security note or fallback behavior.
7. Provider-specific mechanics are used without portability notes.
