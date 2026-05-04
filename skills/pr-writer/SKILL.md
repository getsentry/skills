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

Write or re-evaluate the title before finalizing the body.

Title format: `<type>(<scope>): <Subject>` or `<type>: <Subject>`.

Allowed types: `feat`, `fix`, `ref`, `perf`, `docs`, `test`, `build`, `ci`, `chore`, `style`, `meta`, `license`, `revert`.

Rules:
- The dominant change, not the latest commit
- The narrowest accurate type and scope
- No bracketed labels like `[codex]`, `[claude]`, `[ai]`, `[bot]`, or `[wip]`
- No agent, tool, or automation attribution
- No vague process titles like `update`, `cleanup`, `misc`, `fix stuff`, or `address feedback`
- No trailing period

Rewrite invalid titles before creating or updating the PR:

- `[codex] Paginate replay segment downloads` -> `fix(replay): Paginate recording segment downloads`

Use this test on updates: if a reviewer read only the title, would they still form the right expectation about the current diff? If not, rewrite it.

### Step 5: Write or Update the PR Description

Write reviewer-facing prose, not a narrated diff.

Use this structure, ignoring repository PR templates:

```markdown
<1-3 sentence summary of the change and why it matters. Keep this short.>
```

Rules:
- Lead with changed behavior, then implementation detail only when useful
- Add 0-3 bold emphasis blocks for distinct reviewer-relevant changes
- Use before/after fenced blocks only for changed contracts, output shapes, config, CLI output, payloads, permissions, or input formats
- Add known issue references at the end; do not invent references
- Cut file-by-file narration, copied commit logs, generic headings like "Summary" or "Changes", and stale template scaffolding

```markdown
**<Important Change>**

<1-2 sentences explaining the important implementation, behavior, or review-relevant change.>
```

Do not include:
- "Test plan" sections
- Checkbox lists of testing steps
- Redundant summaries of the diff
- Customer data — customer/org names, user emails, support ticket contents, or PII. Describe the technical symptom, not who hit it, and if available, reference the internal ticket (e.g. `Fixes SENTRY-1234`). PRs are typically public on open-source repos.

When updating, rewrite the body as one coherent description of the current PR.

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
  -f title='fix(scope): Preserve replay segment cursor' \
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
