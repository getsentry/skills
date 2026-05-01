# Plan-Validate-Execute

Use this workflow when a destructive or high-stakes action should be preceded by a machine-checkable plan.

## Choose this workflow when

- validating the plan is safer than validating the final action
- the task changes many files or records
- rollback would be expensive

## Required contract

1. The plan artifact and schema.
2. The validation step and source of truth.
3. Rework rules when validation fails.
4. Final execution and verification steps.

## Example

```markdown
1. Analyze the input and generate `changes.json`
2. Validate the plan against source of truth
3. Revise until validation passes
4. Execute the plan
5. Verify the result
```
