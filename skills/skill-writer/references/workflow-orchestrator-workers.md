# Orchestrator-Workers

Use this workflow when the subtasks are not known ahead of time and must be discovered from the input.

## Choose this workflow when

- the orchestrator must discover work units dynamically
- each unit can be delegated to a stable worker contract
- a final synthesis step can merge the results

## Required contract

1. Worker-task schema.
2. Worker output schema.
3. Expansion limit or stopping rule.
4. Final synthesis rule.

## Example

```markdown
1. Inspect the request and identify work units dynamically
2. Assign each work unit to a worker path
3. Collect worker summaries in a fixed schema
4. Synthesize the result
```
