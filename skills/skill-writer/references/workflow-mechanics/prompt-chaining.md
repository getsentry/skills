# Prompt Chaining

Use this workflow when the task should move through fixed ordered steps and each step makes the next one easier.

## Choose this workflow when

- the decomposition is known in advance
- step order matters
- validation between steps improves quality

## Required contract

1. Step order.
2. Inputs and outputs for each step.
3. Validation or gate points between steps.

## Example

```markdown
1. Summarize the current state
2. Propose the target state
3. Validate the proposal against constraints
4. Write the final document
```
