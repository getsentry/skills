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

Classify the target skill before synthesis. This determines required coverage dimensions and artifacts.

| Skill class | Typical request shape | Required dimensions |
|-------------|-----------------------|---------------------|
| `workflow-process` | repeatable operations, CI/task orchestration | preconditions, ordered flow, failure handling, safety boundaries |
| `integration-documentation` | library/framework integration, SDK usage, API correctness | API surface, config/runtime options, common use cases, known issues/workarounds, version/migration variance |
| `security-review` | vulnerability finding, exploitability review | vulnerability classes, exploit paths, false-positive controls, remediations |
| `skill-authoring` | creating/updating/evaluating other skills | source provenance, depth gates, transformed examples, registration/validation |
| `generic` | does not match above | explicit dimensions chosen and justified in synthesis |

When the class is ambiguous, ask one direct clarification question before synthesis.

## Required outputs by path

- `synthesis`: source inventory, decisions, coverage matrix, gaps.
- `synthesis`: selected class and selected example profile path(s), including profile-requirement coverage.
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
