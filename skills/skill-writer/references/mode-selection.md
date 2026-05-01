# Mode Selection

Choose the minimal set of paths needed for the request.
Regardless of path, prioritize input quality and coverage depth before finalizing outputs.

## Path mapping

| Request shape | Required paths |
|---------------|----------------|
| New skill from scratch | synthesis + authoring + description optimization + evaluation + registration/validation |
| Update existing skill wording/structure | authoring + description optimization + evaluation + registration/validation |
| Improve skill from outcomes/examples | iteration + authoring + description optimization + evaluation + registration/validation |
| Research-first skill planning | synthesis only, then authoring if requested |

## Skill class selection

Classify the target skill before synthesis. This determines the coverage dimensions that must be represented in sources, references, and validation.

| Skill class | Typical request shape | Required dimensions |
|-------------|-----------------------|---------------------|
| `workflow-process` | repeatable operations, CI/task orchestration | preconditions, ordered flow, failure handling, safety boundaries |
| `integration-documentation` | library/framework integration, SDK usage, API correctness | API surface, config/runtime options, common use cases, known issues/workarounds, version/migration variance |
| `security-review` | vulnerability finding, exploitability review | vulnerability classes, exploit paths, false-positive controls, remediations |
| `skill-authoring` | creating/updating/evaluating other skills | source provenance, depth gates, transformed examples, registration/validation |
| `generic` | does not match above | explicit dimensions chosen and justified in synthesis |

When the class is ambiguous, ask one direct clarification question before synthesis.

## Execution shape selection

Choose the skill's primary execution shape separately from the skill class.
Class answers "what domain/problem is this skill for?"
Shape answers "how should this skill run?"

Use `references/execution-shapes.md` for the full decision guide and the next leaf reference to load.
After selecting the shape, load only the specific file(s) you need from `references/artifact-layouts/`, `references/workflow-mechanics/`, or `references/claude-code/`.

Common shapes:

| Shape | Use when |
|-------|----------|
| `inline-guidance` | one coherent set of rules is enough |
| `reference-backed-expert` | most complexity is optional deep knowledge |
| `script-backed-workflow` | the skill needs repeatable automation or validation |
| `argument-driven` | the skill is usually invoked with explicit inputs |
| `router` | distinct categories need different downstream paths |
| `parallelization` | known subtasks can run independently |
| `orchestrator-workers` | subtasks are dynamic and must be discovered at runtime |
| `evaluator-optimizer` | quality improves via critique-and-revise loops |
| `subagent-fork` | the work needs isolated context, tools, or model settings |
| `hook-backed` | deterministic enforcement at lifecycle/tool boundaries is required |
| `asset-template` | the main value is reusable templates or assets |
| `hybrid` | more than one shape is required; declare a primary shape |

Default to the simplest adequate shape.
If the selected shape is `router`, `orchestrator-workers`, `evaluator-optimizer`, `subagent-fork`, or `hook-backed`, record why a simpler inline or script-backed shape was not enough.

## Required outputs by path

- `synthesis`: source inventory, decisions, coverage matrix, gaps.
- `synthesis`: selected class, selected execution shape, and selected example profile path(s), including profile-requirement coverage.
- `synthesis`: simplicity rationale showing why the chosen shape is necessary and which simpler shapes were rejected.
- `synthesis`: portability note when provider-specific mechanics are used.
- `synthesis`: explicit retrieval stopping rationale showing why further collection is currently low-yield.
- `authoring`: updated `SKILL.md` and required supporting files.
- `description optimization`: should/should-not trigger sets and final description.
- `iteration`: example intake summary and behavior deltas.
- `evaluation`: qualitative summary (mandatory) and optional quantitative benchmark.
- `registration/validation`: registration edits and validator results.

## Hard stop rules

Do not claim completion when any required path output is missing.

For authoring/generator skills, missing transformed example artifacts is a hard failure.
Missing selected-profile requirements is also a hard failure.
Missing required class dimensions is a hard failure.
Missing an explicit execution-shape choice for a material skill change is a hard failure.
Using advanced mechanics without justification or portability notes is a hard failure.
