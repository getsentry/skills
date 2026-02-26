---
name: create-branch
description: Create a git branch following Sentry naming conventions. Use when asked to "create a branch", "new branch", "start a branch", "make a branch", "switch to a new branch", or when starting new work on the default branch.
argument-hint: '[optional description of the work]'
---

# Create Branch

Create a git branch with the correct type prefix and a descriptive name following Sentry conventions.

## Step 1: Get the Username Prefix

Run `git config user.name`, take the first word, lowercase it, transliterate accented characters to their ASCII equivalents (e.g. é→e, í→i, ñ→n), then remove any remaining characters that are not ASCII letters or digits.

Example: "Priscila Oliveira" → `priscila`, "José García" → `jose`.

If the result is empty, ask the user for their preferred prefix.

## Step 2: Determine the Branch Description

**If `$ARGUMENTS` is provided**, use it as the description of the work.

**If no arguments**, check for local changes:

```bash
git diff
git diff --cached
git status --short
```

- **Changes exist**: read the diff content to understand what the work is about and generate a description.
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
- Only use ASCII letters, digits, and hyphens — no spaces, dots, colons, tildes, or other git-forbidden characters

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

# Detect the primary remote (use "origin" if the output is empty)
git remote | head -1

# Detect default branch using the detected remote (try in order until one succeeds)
# Replace <remote> with the result above (or "origin" if empty)
git symbolic-ref refs/remotes/<remote>/HEAD 2>/dev/null | sed 's|refs/remotes/<remote>/||' | tr -d '[:space:]'
```

If the `symbolic-ref` command above fails (e.g. single-branch clone or remote HEAD not set), run:

```bash
git branch --list main master
```

- If only `main` exists → default is `main`
- If only `master` exists → default is `master`
- If both exist → ask the user which is the default
- If neither exists → ask the user what the default branch is

If `git branch --show-current` returns empty, the repo is in a detached HEAD state. Run `git rev-parse --short HEAD` to get the current commit. Warn the user they are in a detached HEAD state and ask whether to branch from that commit or switch to the default branch first.

Otherwise, if the current branch is not the default branch, warn the user and ask whether to branch from the current branch or switch to the default branch first.

If the user chooses to switch to the default branch first, check for uncommitted changes first:

```bash
git status --short
```

If there are uncommitted changes, warn the user and ask whether to stash them (`git stash`) or abort. If the user chooses to abort, stop here — do not create a branch.

If the user chooses to stash, run `git stash` before switching, then:

```bash
git checkout <default-branch>
```

Before creating the branch, check if a branch with that name already exists locally or on the remote:

```bash
git show-ref --verify --quiet refs/heads/<branch-name>
git show-ref --verify --quiet refs/remotes/<remote>/<branch-name>
```

If either check succeeds, and changes were stashed, restore them first (`git stash pop`), then inform the user the branch name already exists and ask them to choose a different name (return to Step 4).

Otherwise, create the branch:

```bash
git checkout -b <branch-name>
```

If changes were stashed earlier, restore them now:

```bash
git stash pop
```

## References

- [Sentry Branch Naming](https://develop.sentry.dev/sdk/getting-started/standards/code-submission/#branch-naming)
