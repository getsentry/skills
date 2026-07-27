---
name: pr-writer
description: Write a PR title and body as a cover note for reviewers. Use when opening a PR or refreshing an existing one's title or body.
---

# PR Writer

A PR body is a cover note for reviewers: what changed, what it affects, and
where to look.

## Inspect the Change

Requires authenticated `gh`. Inspect the current branch, working tree, PR,
base branch, commits, and full diff:

```bash
git branch --show-current
git status --porcelain
gh pr view --json number,title,body,url,baseRefName,headRefName
gh repo view --json defaultBranchRef
```

If `gh pr view` reports that no PR exists, continue with first-time PR
creation. For an existing PR, use its `baseRefName`; otherwise use the
repository default branch. Set `BASE`, then inspect:

```bash
git log "$BASE"..HEAD --oneline
git diff --stat "$BASE"...HEAD
git diff "$BASE"...HEAD
```

If on `main` or `master`, create a feature branch first. Commit the intended
changes, then read the whole branch diff. The `--stat` total is the budget the
cover note is written against.

## Core Rules

- Lead with concrete changed behavior, affected surfaces, and reviewer impact;
  implementation detail comes after, if at all.
- Use the smallest structure that makes the change easier to review.
- Match length to the diff: a body that takes longer to read than the diff
  takes to review has failed. Every paragraph carries something the diff does
  not show — root cause, rationale, risk, migration, or where to start. Cut
  the ones that restate what the reviewer is about to read.
- Write each body paragraph as one long line, with a blank line between
  paragraphs. GitHub renders an intra-paragraph newline as a line break, so a
  hard-wrapped body breaks raggedly at the source column. Fenced code blocks
  keep their newlines.
- Replace internal prompt or process terminology with specific behavior.
- When refreshing, rewrite around the current full diff: the cover note
  describes the PR as it now stands, not the revisions that got it there.

## Titles

Use `<type>(<scope>): <subject>` or `<type>: <subject>`.

Allowed types: `feat`, `fix`, `ref`, `perf`, `docs`, `test`, `build`,
`ci`, `chore`, `style`, `meta`, `license`, and `revert`.

- Describe the dominant full-branch change with the narrowest accurate type
  and scope.
- Use `!` only when the change breaks an external contract, and explain the
  affected surface in the body.
- Name the specific behavior that changed in the subject, with no trailing
  period.
- Keep an existing title only when it still describes the whole diff.

## Body Shape

Choose the minimum useful shape:

| Change | Include |
|--------|---------|
| Small or obvious | One concise paragraph without headings. |
| Feature, bug fix, or refactor | Changed behavior and effect; add root cause, unchanged behavior, or non-obvious approach when relevant. |
| Contract or breaking change | Affected API, schema, payload, config, permission, storage, or CLI surface; include compatibility and migration guidance. |
| Operational, visual, or workflow change | User/operator effect, measured impact, failure modes, or flow when useful. |
| Broad, generated, or cross-cutting change | Organizing principle, why the breadth is necessary, and where review should start. |

Default:

```markdown
<What changed and what effect it has.>

<Why the approach, risk, migration, or review focus matters, if not obvious.>
```

## Reviewer Aids

Use an aid only when it reduces reviewer reconstruction work:

- A compact before/after or interface example for changed contracts.
- A small Mermaid diagram for async flows or state transitions.
- A screenshot or recording note when visual evidence exists.
- A rollout, compatibility, risk, or review-order note when reviewers or
  adopters need it.

Introduce an artifact with one sentence explaining what reviewers should
notice.

## Boundaries

- The cover note carries prose plus, when earned, one aid. Command output, CI
  logs, commit logs, placeholders, and file lists stay out; include validation
  only when it changes risk assessment or shows meaningful regression coverage.
- Write the body from the diff, ignoring any repository PR template, and skip
  default `Summary`, `Changes`, and `Test Plan` headings.
- Never include customer or organization names, user emails, support ticket
  contents, secrets, or PII.
- Use issue references only when verified from user input, branch names,
  commits, PR discussion, or tracker output. `Fixes <issue>` closes;
  `Refs <issue>` only links.

## Create or Update

Create new PRs as drafts. Write the body to a temporary Markdown file, then run:

```bash
gh pr create --draft --title '<title>' --body-file /tmp/pr-body.md
```

Update existing PRs with `gh api`:

```bash
gh api -X PATCH repos/{owner}/{repo}/pulls/PR_NUMBER \
  -f title='<title>' \
  -F body=@/tmp/pr-body.md
```

Refresh the title and body when follow-up commits materially change scope,
approach, breaking behavior, risk, migration, or review expectations. Skip
typo-only, formatting-only, and rename-only follow-ups.

## Examples

Small change:

```markdown
The AI Customizations section now starts collapsed so it does not consume sidebar space before users need it. Expanding it preserves the existing saved preference behavior.
```

Breaking contract:

````markdown
Run logs now emit chunk-level records instead of one skill-level record. Consumers that read top-level `findings` must iterate over `chunk.findings` for each record.

Before:

```json
{"skill": "security-review", "findings": [...]}
```

After:

```json
{"schemaVersion": 1, "chunk": {"index": 1, "findings": [...]}}
```
````
