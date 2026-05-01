# Output Contracts

Use this guide when the skill needs a predictable answer shape, template, schema, or reporting format.

## Choose The Contract Shape

| Need | Use this contract |
|------|-------------------|
| exact headings or sections must appear | strict template |
| default structure is helpful but adaptation is allowed | flexible template |
| style is hard to describe but easy to imitate | input/output examples |
| output shape depends on task type | decision table |
| scripts or downstream tools parse the output | structured data schema |

## Strict Template

Use when wrong structure is costly.

```markdown
## Report structure

ALWAYS use this exact template:

# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```

## Flexible Template

Use when consistency helps but the content still needs adaptation.

```markdown
## Report structure

Use this as a sensible default, but adapt based on context:

# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]
```

## Input/Output Examples

Use when examples communicate tone, density, or formatting more clearly than prose.

````markdown
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```
````

## Decision Table

Use when different input classes should produce different response formats.

```markdown
## Output format selection

| Input Type | Output Format | Example |
|-----------|--------------|---------|
| Single file | Inline summary | "Found 3 issues in auth.py: ..." |
| Multiple files | Grouped report | Markdown report with per-file sections |
| Full repository | Executive summary + details | Summary table + expandable sections |
```

## Structured Data Schema

Use when another script, tool, or validator consumes the output.

````markdown
## Output format

Return results as JSON:

```json
{
  "status": "success" | "failure",
  "findings": [
    {
      "severity": "HIGH" | "MEDIUM" | "LOW",
      "file": "path/to/file.py",
      "line": 42,
      "message": "Description of the finding"
    }
  ],
  "summary": "One-line summary of results"
}
```
````
