# Mode Selection

Choose the minimal set of paths needed for the request.
Regardless of path, prioritize input quality and coverage depth before finalizing outputs.

## Path mapping

| Request shape | Required paths |
|---------------|----------------|
| New skill from scratch | synthesis + authoring + description optimization + registration/validation |
| Update existing skill wording/structure | authoring + description optimization + registration/validation |
| Improve skill from outcomes/examples | iteration + authoring + description optimization + registration/validation |
| Research-first skill planning | synthesis only, then authoring if requested |

## Skill class selection

Classify the target skill before synthesis. This determines the coverage dimensions that must be represented in sources, references, and validation.

| Skill class | Typical request shape | Required dimensions |
|-------------|-----------------------|---------------------|
| `workflow-process` | repeatable operations, CI/task orchestration | preconditions, ordered flow, failure handling, safety boundaries |
| `integration-documentation` | library/framework integration, SDK usage, API correctness | API surface, config/runtime options, common use cases, known issues/workarounds, version/migration variance |
| `skill-authoring` | creating/updating/reviewing other skills | source provenance, precision pass, transformed examples, registration/validation |
| `generic` | does not match above | explicit dimensions chosen and justified in synthesis |

When the class is ambiguous, ask one direct clarification question before synthesis.

## Execution shape selection

Choose the skill's primary execution shape separately from the skill class.
Class answers "what domain/problem is this skill for?"
Shape answers "how should this skill run?"

Use `references/execution-shapes.md` for the full decision table and the next leaf reference to load.

Record:

1. primary execution shape
2. simpler-shape rejection when the chosen shape is advanced
3. exact leaf references opened because of that choice

## Required outputs by path

- `synthesis`: source inventory, decisions, coverage matrix, gaps.
- `synthesis`: selected class, selected execution shape, and selected example profile path(s), including profile-requirement coverage.
- `synthesis`: simplicity rationale showing why the chosen shape is necessary and which simpler shapes were rejected.
- `synthesis`: portability note when provider-specific mechanics are used.
- `synthesis`: explicit retrieval stopping rationale showing why further collection is currently low-yield.
- `authoring`: updated `SKILL.md` and required supporting files.
- `description optimization`: should/should-not trigger sets and final description.
- `iteration`: example intake summary and behavior deltas.
- `registration/validation`: registration edits and validator results.

## Completion Checks

Do not claim completion when any required path output is missing.

For authoring/generator skills, report missing transformed examples, selected-profile requirements, required class dimensions, or execution-shape choices as open gaps instead of hiding them.
When advanced mechanics are used, include justification and portability notes or report the missing decision as an open gap.
