# Output Contracts

Use this guide when the skill needs a predictable response shape.

## Choose The Contract

| Need | Use |
|------|-----|
| exact sections or headings | strict template |
| default structure with adaptation | flexible template |
| style is easier to imitate than describe | input/output examples |
| format depends on task type | decision table |
| scripts or tools parse the output | structured schema |

## Strict Template

```markdown
# [Title]

## Summary
[Required summary]

## Findings
- ...
```

## Flexible Template

```markdown
# [Title]

## Summary
[Default summary section; adapt if needed]

## Findings
[Adapt based on context]
```

## Input/Output Example

````markdown
Input: fix date formatting bug
Output:
```text
fix(reports): correct timezone date formatting
```
````

## Decision Table

```markdown
| Input Type | Output Format |
|------------|---------------|
| single file | inline summary |
| many files | grouped report |
```

## Structured Schema

````markdown
```json
{
  "status": "success",
  "summary": "One-line result",
  "findings": []
}
```
````
