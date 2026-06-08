---
name: pr-writer
description: Create, refresh, and rewrite PR titles and descriptions following Sentry conventions. Use when opening a PR, writing or updating a PR title/body/description, refreshing an existing PR after material changes, or preparing branch changes for review.
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

Write a reviewer-facing cover note, not a generated changelog.

Default to 1-2 short paragraphs:

```markdown
<What changed and what effect it has.>

<Why this approach, tradeoff, risk, or review focus matters, if it is not obvious from the diff.>
```

Write enough context that a reviewer can predict the shape and intent of the diff before opening it. The body should answer the questions that code alone will not: why the change exists, what behavior changes, what tradeoff was chosen, and what deserves careful review.

Use structure only when the change needs it:

| Change shape | Useful body shape |
|--------------|-------------------|
| Small obvious change | one concise paragraph; no headings |
| Bug fix | problem/root cause/fix in prose; headings only if the body would be confusing without them |
| API, schema, payload, config, permissions, or CLI change | before/after fenced blocks when direct comparison is clearer than prose |
| Performance or reliability change | include measured impact or expected tradeoff when known; do not invent numbers |
| Broad, generated, or cross-cutting change | explain the organizing principle and where reviewers should start |
| Review feedback update | rewrite the whole body around the current final diff; do not append a progress log |

Rules:
- Lead with changed behavior or effect, then implementation detail only when useful.
- Prefer paragraphs over headings and bullets.
- Use bullets only to guide review order, list genuine alternatives/tradeoffs, or compare independent contract changes.
- When verification matters, fold it into the relevant prose instead of adding a separate checklist.
- Include issue references only when the exact ID or URL is present in user input, branch name, commits, or verified tracker output; omit the line entirely otherwise.
- Keep links self-contained by summarizing the relevant context in the body.
- Prefer synthesized reviewer context over file-by-file narration, copied commit logs, generic headings like "Summary" or "Changes", and stale template scaffolding.

Hard constraints:
- Customer data — customer/org names, user emails, support ticket contents, or PII. Describe the technical symptom, not who hit it, and use the Issue References syntax below only when a verified ticket is available. PRs are typically public on open-source repos.
- Never invent issue references or leave placeholders like `XXXXX`, `<issue>`, or `TODO`.
- Generate reviewer prose only. Do not add new agent trace links, "action taken on behalf" lines, or tool attribution. When refreshing an existing PR, preserve an existing integration-owned footer only if it appears intentional and the user did not ask to remove it.

When updating, rewrite the body as one coherent description of the current PR.

### Step 6: Create or Update the PR

For a new PR, create a draft with the rewritten title and body:

```bash
gh pr create --draft --title "<type>(<scope>): <description>" --body "$(cat <<'EOF'
<description body here>
EOF
)"
```

Before running the create or update command, strip any issue reference not backed by known context. Never emit placeholder IDs (`XXXXX`, `<issue>`, `TODO`).

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
The AI Customizations section in the sessions sidebar now starts collapsed so
it does not consume space before users need it. Expanding the section keeps the
same persisted preference behavior as before.
```

### Feature PR

```markdown
Alert updates and resolves now reply to the original Slack message instead of
creating a new channel message. This keeps the notification timeline grouped in
one thread and reduces channel noise.
```

### Bug Fix PR

```markdown
Inactive authenticated users now go to account reactivation before the login
view honors a `next` URL.

The GET login path could previously bounce an inactive user between
`/auth/login/` and a protected view because it redirected authenticated users
without checking `is_active`. The POST path already handled this case, so this
applies the same guard to the GET redirect and covers the loop with a regression
test.
```

### Schema Change PR

````markdown
Run logs now write one versioned record per analyzed chunk instead of one
large skill-level record. This lets `warden runs follow` show findings as
chunks complete while preserving durable run reconstruction at finalization.

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

````

### Refactor PR

````markdown
Duplicate validation code from the alerts, issues, and projects endpoints now
lives in a shared validator class without changing endpoint behavior.
Future validation rules can now be added in one place instead of being copied
across each endpoint.
````

### Broad Review PR

```markdown
The admin layout now holds together at narrow viewport widths: the shared
header, details grid, result table, and sidebar wrap, collapse, or scroll
instead of overflowing the viewport. The changes are intentionally limited to
responsive layout behavior; table column prioritization is left out because it
needs product judgment.

Review the shared layout and table wrappers first, then check individual
component breakpoints for regressions.
```

## Issue References

Reference issues in the PR body:

| Syntax | Effect |
|--------|--------|
| `Fixes #1234` | Closes GitHub issue on merge |
| `Fixes SENTRY-1234` | Closes Sentry issue |
| `Refs GH-1234` | Links without closing |
| `Refs LINEAR-ABC-123` | Links Linear issue |

These are syntax examples — do not copy example IDs into a real PR body.

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
