---
name: pr-writer
description: ALWAYS use this skill when creating or updating pull requests — never create or edit a PR directly without it. Follows Sentry conventions for PR titles, descriptions, and issue references. Trigger on any create PR, open PR, submit PR, make PR, update PR title, update PR description, edit PR, push and create PR, prepare changes for review task, or request for a PR writer.
---

# PR Writer

Create pull requests following Sentry's engineering practices.

**Requires**: GitHub CLI (`gh`) authenticated and available.

## Prerequisites

Before creating a PR, ensure all changes are committed **to a feature branch**, not to the default branch.

```bash
# Check current branch and for uncommitted changes
git branch --show-current
git status --porcelain
```

If on `main` or `master`, create a feature branch and move any uncommitted changes onto it before committing — a PR cannot be opened from the default branch against itself. If there are uncommitted changes, commit them on the feature branch before proceeding.

## Process

### Step 1: Verify Branch State

```bash
# Detect the default branch — note the output for use in subsequent commands
gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'
```

```bash
# Check current branch and status (substitute the detected branch name above for BASE)
git status
git log BASE..HEAD --oneline
```

Ensure:
- All changes are committed
- Branch is up to date with remote
- Changes are rebased on the base branch if needed

### Step 2: Analyze Changes

Review what will be included in the PR:

```bash
# See all commits that will be in the PR (substitute detected branch name for BASE)
git log BASE..HEAD

# See the full diff
git diff BASE...HEAD
```

Understand the scope and purpose of all changes before writing the description.

### Step 3: Write the PR Description

Use this structure for PR descriptions, ignoring any repository PR templates:

```markdown
<1-3 sentence summary of the change and why it matters. Keep this short.>
```

When there is a known issue, ticket, or related PR, add references at the end. Do not invent one.

When the PR has distinct changes reviewers should scan, add 0-3 bold emphasis blocks after the opening summary:

```markdown
**<Important Change>**

<1-2 sentences explaining the important implementation, behavior, or review-relevant change.>
```

When direct comparison is the clearest explanation, add a before/after block under the relevant paragraph or emphasis block:

````markdown
Before, <old shape or behavior in one sentence>:

```<format-or-pseudocode>
...
```

After, <new shape or behavior in one sentence>:

```<format-or-pseudocode>
...
```
````

Treat the bold sections as optional emphasis blocks, not mandatory headings. Use them when the PR has one or more distinct changes that reviewers should scan quickly. Omit them for simple PRs where the opening summary is enough.

Use before/after examples only when that is the clearest way to explain the changeset. They are usually useful for changed contracts or output shapes, such as JSON responses, schemas, config, CLI output, event payloads, permissions, or input formats. Omit them when prose is clearer.

Prefer:
- A concise opening summary, usually 1-3 sentences
- 0-3 bold emphasis blocks for the parts that matter most
- Before/after examples only for changes that benefit from direct comparison, with separate fenced blocks for the old and new forms
- Known issue references at the end, when available

Avoid:
- Essays, exhaustive file-by-file walkthroughs, or copied commit logs
- Generic headings like "Summary" or "Changes"
- A bold block for every touched file
- Inline before/after snippets that are hard to compare
- Placeholder issue references when no issue is known
- Repeating details that are obvious from the diff

**Do NOT include:**
- "Test plan" sections
- Checkbox lists of testing steps
- Redundant summaries of the diff
- Customer data — customer/org names, user emails, support ticket contents, or PII. Describe the technical symptom, not who hit it, and if available, reference the internal ticket (e.g. `Fixes SENTRY-1234`). PRs are typically public on open-source repos.

**Do include:**
- Clear explanation of what changed and why it matters
- Links to relevant issues or tickets, when known
- Context that isn't obvious from the code
- Specific review notes when a part of the diff needs extra attention

### Step 4: Create the PR

```bash
gh pr create --draft --title "<type>(<scope>): <description>" --body "$(cat <<'EOF'
<description body here>
EOF
)"
```

**Title format** follows commit conventions:
- `feat(scope): Add new feature`
- `fix(scope): Fix the bug`
- `ref: Refactor something`

## PR Description Examples

### Simple PR

```markdown
Collapse the AI Customizations section by default in the sessions sidebar.

The section now starts hidden so it does not consume space before users need
it. Users who expand it keep the same persisted preference behavior as before.
```

### Feature PR

```markdown
Add Slack thread replies for alert notifications

When an alert is updated or resolved, we now post a reply to the original
Slack thread instead of creating a new message. This keeps related
notifications grouped and reduces channel noise.

**Notification Threading**

Resolved and updated alerts now reply to the original Slack message instead
of creating a new channel message.

Refs SENTRY-1234
```

### Schema Change PR

````markdown
Switch run logs to chunk-level JSONL records

Run logs now write one versioned record per analyzed chunk instead of one
large skill-level record. This lets `warden runs follow` show findings as
chunks complete while preserving durable run reconstruction at finalization.

**JSONL Shape**

Before, each line represented a full skill result:

```jsonc
{
  "run": {...},
  "skill": "security-review",
  "summary": "Found 2 issues",
  "findings": [...],
  "files": [...]
}
```

After, each line represents one chunk result:

```jsonc
{
  "schemaVersion": 1,
  "run": {...},
  "skill": "security-review",
  "chunk": {
    "file": "src/api/auth.ts",
    "index": 1,
    "total": 2,
    "lineRange": "42-45"
  },
  "status": "ok",
  "findings": [...]
}
```

Refs WARDEN-123
````

### Refactor PR

````markdown
Extract validation logic to shared module

Moves duplicate validation code from the alerts, issues, and projects
endpoints into a shared validator class. No behavior change.

**Shared Validator**

The shared class keeps the existing endpoint behavior but gives future
validation rules one place to live.

Refs SENTRY-9999
````

## Issue References

Reference issues in the PR body:

| Syntax | Effect |
|--------|--------|
| `Fixes #1234` | Closes GitHub issue on merge |
| `Fixes SENTRY-1234` | Closes Sentry issue |
| `Refs GH-1234` | Links without closing |
| `Refs LINEAR-ABC-123` | Links Linear issue |

## Guidelines

- **One PR per feature/fix** - Don't bundle unrelated changes
- **Keep PRs reviewable** - Smaller PRs get faster, better reviews
- **Explain the why** - Code shows what; description explains why
- **Mark WIP early** - Use draft PRs for early feedback

## Editing Existing PRs

If you need to update a PR after creation, use `gh api` instead of `gh pr edit`:

```bash
# Update PR description
gh api -X PATCH repos/{owner}/{repo}/pulls/PR_NUMBER -f body="$(cat <<'EOF'
Updated description here
EOF
)"

# Update PR title
gh api -X PATCH repos/{owner}/{repo}/pulls/PR_NUMBER -f title='new: Title here'

# Update both
gh api -X PATCH repos/{owner}/{repo}/pulls/PR_NUMBER \
  -f title='new: Title' \
  -f body='New description'
```

Note: `gh pr edit` is currently broken due to GitHub's Projects (classic) deprecation.

## References

- [Sentry Code Review Guidelines](https://develop.sentry.dev/engineering-practices/code-review/)
- [Sentry Commit Messages](https://develop.sentry.dev/engineering-practices/commit-messages/)
