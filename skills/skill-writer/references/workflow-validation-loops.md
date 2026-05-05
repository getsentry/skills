# Validation Loops

Use this workflow when a validator can reliably catch mistakes before the skill should claim completion.

## Choose this workflow when

- a script, schema, test, or parser can catch important failures
- the agent should fix issues immediately after each change
- the main risk is silent drift or invalid output

## Required contract

1. The validator or check to run.
2. When it runs in the workflow.
3. What to fix before retrying.
4. What counts as a passing state.

## Example

```markdown
1. Make the change
2. Validate immediately
3. If validation fails, fix the issue
4. Re-run validation
5. Only proceed when validation passes
```
