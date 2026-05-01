---
name: pr-writer
description: Create and update pull requests following Sentry conventions. Use when opening a PR or refreshing an existing PR after material changes.
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

### Step 3: Check Existing PR

If the current branch already has an open PR, inspect the current title and body before rewriting either one:

```bash
gh pr view PR_NUMBER --json number,title,body,url,baseRefName,headRefName
```

Treat the current PR title and body as inputs, not source of truth. Compare them against the current diff, not the diff from when the PR was first opened.

When refreshing a PR:
- Keep the current title only if it still matches the dominant change.
- Rewrite vague or stale titles.
- Rewrite the body as a fresh description of the current diff, not an append-only update log.

If the branch already has an open PR, refresh it after material follow-up changes even if the user did not explicitly ask for a PR edit.

Refresh when follow-up commits change reviewer expectations, such as a scope change, a new implementation approach from review feedback, or new context the current title/body no longer explains. Skip trivial edits like typos or rename-only diffs.

### Step 4: Write or Update the PR Title

Write the title before the body, or re-evaluate it before finalizing the body.

**Title format** follows commit conventions:
- `feat(scope): Add Slack thread replies for alert notifications`
- `fix(scope): Preserve replay segment cursor across pagination`
- `ref(scope): Extract shared project validation helper`

Prefer:
- The dominant change, not the latest commit
- Specific nouns and verbs
- The narrowest accurate type and scope
- One clear change axis a reviewer can scan in a PR list

Avoid:
- Vague words like `update`, `cleanup`, `misc`, `fix stuff`, or `address feedback`
- Titles that describe the process instead of the change
- Titles that no longer match the current branch after follow-up commits
- Trailing periods

Use this test on updates: if a reviewer read only the title, would they still form the right expectation about the current diff? If not, rewrite it.

### Step 5: Write or Update the PR Description

Use this same structure whether you are opening a new PR or updating an existing PR body. When updating, rewrite the final PR body so it still matches this structure instead of appending ad hoc notes or preserving repository template sections.

Write reviewer-facing prose, not a narrated diff.

The opening summary should usually:
- Name the primary change
- Explain the practical effect or behavior change
- Give the why only when it is not already obvious from the change itself

Prefer:
- Concrete nouns and verbs
- The changed behavior before implementation detail
- Short declarative sentences
- Details that help a reviewer understand impact, risk, or why the code is shaped this way

Avoid:
- Throat-clearing like `This PR`, `basically`, `simply`, `just`, `some`, `various`, or `in order to`
- Empty claims like `improves things`, `cleans things up`, or `makes this better` without saying how
- File-by-file narration
- Repeating the diff without adding meaning
- Long setup or project history before the actual change

When a sentence only restates what the diff already makes obvious, delete it.

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

If the existing PR body has stale context, repo-template scaffolding, or a delta-only update note, remove or rewrite it so the final body reads as one coherent description of the current PR.

### Step 6: Create or Update the PR

For a new PR, create a draft with the rewritten title and body:

```bash
gh pr create --draft --title "<type>(<scope>): <description>" --body "$(cat <<'EOF'
<description body here>
EOF
)"
```

For an existing PR, patch the title and body after you have re-evaluated both. If the current title still fits, keep it intentionally rather than skipping title review.

```bash
gh api -X PATCH repos/{owner}/{repo}/pulls/PR_NUMBER \
  -f title='new: Title' \
  -f body="$(cat <<'EOF'
<updated description body here>
EOF
)"
```

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
- **Rewrite, don't append** - Updated PRs should read like a fresh description of the current diff
- **Re-evaluate the title on updates** - Do not assume the existing title still fits after scope changes

Note: `gh pr edit` is currently broken due to GitHub's Projects (classic) deprecation.

## References

- [Sentry Code Review Guidelines](https://develop.sentry.dev/engineering-practices/code-review/)
- [Sentry Commit Messages](https://develop.sentry.dev/engineering-practices/commit-messages/)
