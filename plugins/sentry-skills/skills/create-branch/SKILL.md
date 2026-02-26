---
name: create-branch
description: Create a git branch following Sentry naming conventions. Use when asked to "create a branch", "new branch", "start a branch", "make a branch", "switch to a new branch", or when starting new work on the default branch.
argument-hint: '[optional description of the work]'
---

# Create Branch

Create a git branch with the correct type prefix and a descriptive name following Sentry conventions.

## Step 1: Get the Username Prefix

Run `git config user.name` and extract the **first name only**, lowercased.

Example: "Priscila Oliveira" becomes `priscila`.

If empty, ask the user for their preferred prefix.

## Step 2: Determine the Branch Description

**If `$ARGUMENTS` is provided**, use it as the description of the work.

**If no arguments**, check for local changes:

```bash
git diff --stat
git diff --cached --stat
git status --short
```

- **Changes exist**: read the diff to understand what the work is about and generate a description.
- **No changes**: ask the user what they are about to work on.

## Step 3: Classify the Type

Pick the type from this table based on the description:

| Type      | Use when                                                              |
| --------- | --------------------------------------------------------------------- |
| `feat`    | New user-facing functionality                                         |
| `fix`     | Broken behavior now works                                             |
| `ref`     | Same behavior, different structure                                    |
| `chore`   | Deps, config, version bumps, updating existing tooling — no new logic |
| `perf`    | Same behavior, faster                                                 |
| `style`   | CSS, formatting, visual-only                                          |
| `docs`    | Documentation only                                                    |
| `test`    | Tests only                                                            |
| `ci`      | CI/CD config                                                          |
| `build`   | Build system                                                          |
| `meta`    | Repo metadata changes                                                 |
| `license` | License changes                                                       |

When unsure: `feat` for new things (including new scripts, skills, or tools), `ref` for restructuring existing things, `chore` only when updating/maintaining something that already exists.

## Step 4: Generate and Propose

Build the branch name as `<username>/<type>/<short-description>`.

Rules for `<short-description>`:

- Kebab-case, lowercase
- 3 to 6 words, concise but clear
- Describe the change, not file names

Present it to the user and ask if they want to use it, modify it, or change the type.

### Examples

| Work description                           | Branch name                                 |
| ------------------------------------------ | ------------------------------------------- |
| Dropdown menu not closing on outside click | `priscila/fix/dropdown-not-closing-on-blur` |
| Adding search to conversations page        | `priscila/feat/add-search-to-conversations` |
| Restructuring drawer components            | `priscila/ref/simplify-drawer-components`   |
| Updating test fixtures                     | `priscila/chore/update-test-fixtures`       |
| Bumping @sentry/react to latest version    | `priscila/chore/bump-sentry-react`          |
| Adding a new agent skill                   | `priscila/feat/add-create-branch-skill`     |

## Step 5: Create the Branch

Once confirmed, first detect the default branch and the current branch:

```bash
# Get current branch
git branch --show-current

# Detect default branch (try in order until one succeeds)
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||'
```

If the above fails (e.g. single-branch clone or remote HEAD not set), run:

```bash
git branch --list main master
```

- If only `main` exists → default is `main`
- If only `master` exists → default is `master`
- If both exist → default is `main`
- If neither exists → ask the user what the default branch is

If `git branch --show-current` returns empty, the repo is in a detached HEAD state. Run `git rev-parse --short HEAD` to get the current commit. Warn the user they are in a detached HEAD state and ask whether to branch from that commit or switch to the default branch first.

Otherwise, if the current branch is not the default branch, warn the user and ask whether to branch from the current branch or switch to the default branch first.

If the user chooses to switch to the default branch first, run:

```bash
git checkout <default-branch>
```

Then create the branch:

```bash
git checkout -b <branch-name>
```

## References

- [Sentry Branch Naming](https://develop.sentry.dev/sdk/getting-started/standards/code-submission/#branch-naming)
