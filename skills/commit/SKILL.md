---
name: commit
description: Use for every request to commit changes or draft a commit message. Creates Sentry-style conventional commits with issue references, and covers attaching screenshots to the pull request with gh.
---

# Sentry Commit Messages

## Before Committing

```bash
git branch --show-current
```

If the branch is `main` or `master`, create a feature branch unless the user
explicitly requested a direct commit. Re-check the branch and stop if it is
still `main` or `master`.

Commit one coherent, independently reviewable change at a time.

## Message Rules

Use:

```text
<type>(<scope>): <subject>

<optional body>

<optional footer>
```

- Scope is optional. Add `!` before `:` for a breaking change.
- Write the subject in imperative, present tense; capitalize it, omit the
  trailing period, and keep it at 70 characters or fewer.
- Keep every line under 100 characters.
- Use the body only when useful. Explain what changed and why, including
  previous behavior or motivation when it helps.
- Never include customer or organization names, user emails, support ticket
  contents, secrets, or PII. Describe the technical symptom instead.

Allowed types: `feat`, `fix`, `ref`, `perf`, `docs`, `test`, `build`,
`ci`, `chore`, `style`, `meta`, `license`, and `revert`.

Use `ref` for refactoring without behavior changes, `style` for formatting
without logic changes, and `meta` for repository metadata.

## Footers

- `Fixes <issue>` closes an issue when merged.
- `Refs <issue>` links an issue without closing it.
- For breaking changes, add `BREAKING CHANGE: <impact>`.

## Creating the Commit

Use separate `-m` arguments for paragraphs and footers. Never put literal
`\n` sequences in a commit message or open an interactive editor.

```bash
git commit -m "fix(api): Handle null response in user endpoint" \
  -m "Return 404 when the user API finds a deleted account." \
  -m "Fixes SENTRY-5678"
```

## Attaching Images to the Pull Request

Since gh 2.99.0, `gh pr create` and `gh pr edit` upload images and videos with
`--attach '<path>#<alt text>'`, so attach screenshots directly rather than
asking the user to drag them in. If `gh` rejects `--attach` as an unknown flag,
ask the user to upgrade `gh`. A body reference to the local path, such as
`![Before](./before.png)`, is rewritten to the uploaded asset; without one,
the attachment is appended to the body.

```bash
gh pr edit --attach './before.png#Before' --attach './after.png#After' \
  --body "... ![Before](./before.png) ![After](./after.png)"
```

Without a body flag, `gh pr edit --attach` keeps the existing body.
