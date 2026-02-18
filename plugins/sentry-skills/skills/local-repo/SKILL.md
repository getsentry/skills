---
name: local-repo
description: Investigate, compare, and modify files in other local git repositories. Use when asked to "check another repo", "look at other repo", "compare repos", "local-repo", "cross-repo", "what does sentry-python do", or work with a repository outside the current working directory.
argument-hint: "<repo-name> [file-pattern-or-query]"
---

# Local Repository

Load another local git repository into the conversation for investigation, comparison, or modification.

## Arguments

- `repo-name` — name of a repository folder within configured repo directories (e.g., `sentry-python`)
- `file-pattern-or-query` (optional) — specific files, glob patterns, or a description of what to look for

## Examples

```
/local-repo sentry-python
/local-repo sentry-python src/sentry_sdk/hub.py
/local-repo sentry-python "how is the SDK initialized"
/local-repo sentry-cocoa **/*Scope*
```

## Step 1: Read the Config

Determine the user's home directory (run `echo $HOME` via Bash if needed), then read `$HOME/.claude/repos.local.json` using the Read tool. This file already exists — do not recreate or overwrite it.

The config contains a `repoDirs` array of directories where repositories are stored:

```json
{
  "repoDirs": [
    "/path/to/repos",
    "/another/path/to/repos"
  ]
}
```

## Step 2: List Available Repositories

Run the list script to show available repos:

```bash
bash ${CLAUDE_SKILL_ROOT}/scripts/list-repos.sh
```

If the requested repo is not in the list, inform the user.

## Step 3: Resolve the Repository Path

For each directory in `repoDirs`, check if the repo exists by running a **separate** Bash call for each:

```bash
test -d <repoDir>/<repo-name>/.git
```

Use the first match as `<repo-path>` for all subsequent steps. Do not assume the repo is in the first `repoDir` — check each one.

**IMPORTANT — Simple commands only:** Every Bash command in this skill MUST be a single, simple command. Do NOT chain commands with `&&`, `||`, or pipes (`|`). Do NOT use shell redirects (`2>/dev/null`, `2>&1`). These break user permission patterns. Run each command as its own separate Bash tool call instead.

### If Not Found Locally

1. Check GitHub: use WebFetch on `https://github.com/orgs/getsentry/repositories?type=source&q=<repo-name>` and look for a matching repository
2. If a match exists on GitHub:
   - Tell the user the repo exists on GitHub but is not cloned locally
   - Ask (using AskUserQuestion) whether to clone it with `devenv fetch getsentry/<repo-name>`
   - If the user agrees, run the clone command, then resolve the path again from `repoDirs`
   - If the user declines, stop
3. If not found on GitHub either, inform the user the repo was not found locally or on GitHub under the getsentry org

**IMPORTANT:** Never attempt to answer the user's query by fetching repository content from GitHub. Steps 4–6 (freshness check, investigation, presenting findings) MUST only operate on locally cloned repositories. If the repo is not available locally, report that and stop — do not browse or fetch code from GitHub as a substitute.

## Step 4: Check Repository Freshness

Do this once per repo, the first time it is used in a conversation. Run each command as a **separate** Bash tool call (no chaining, no redirects).

1. Determine the default branch:
   ```bash
   git -C <repo-path> symbolic-ref refs/remotes/origin/HEAD --short
   ```
   Strip the `origin/` prefix from the output. If this command fails, try `main` then `master`.

2. Check the current branch:
   ```bash
   git -C <repo-path> branch --show-current
   ```

3. Fetch latest remote refs:
   ```bash
   git -C <repo-path> fetch origin --quiet
   ```

4. Count commits behind remote:
   ```bash
   git -C <repo-path> rev-list <default-branch>..origin/<default-branch> --count
   ```

5. Check for local changes:
   ```bash
   git -C <repo-path> status --porcelain
   ```

6. Report status before presenting any content using GitHub-flavored markdown alerts:

   | Condition | Format |
   |---|---|
   | Not on default branch | `> [!WARNING]` "repo-name is on branch 'current-branch' (default is 'default-branch')" |
   | Behind remote | `> [!NOTE]` "repo-name is N commit(s) behind origin/default-branch" |
   | Local changes | `> [!WARNING]` "repo-name has local changes" |
   | Not cloned locally | `> [!CAUTION]` "repo-name is not cloned locally" |
   | All OK | No notice needed |

Do not switch branches or pull automatically — just inform the user.

## Step 5: Handle the Request

| Input Type | Detection | Action |
|---|---|---|
| No file/query provided | No second argument | Give an overview: check for README.md/CLAUDE.md, list top-level directory structure, identify main source directories |
| File pattern | Contains `/`, `*`, or `.` | Use Glob to find matching files in `<repo-path>`, then read them |
| Query or question | Free text | Use the Explore agent (Task tool with `subagent_type=Explore`) to search the repository for relevant code |

## Step 6: Present Findings

Note which repository each piece of information comes from. When comparing across repos:

- Look for similar class/function names
- Check for common patterns (Options classes, transport layers, scope management)
- Note language-specific idioms that achieve the same goal
- Reference both repos clearly

## Config File

The config lives at `$HOME/.claude/repos.local.json`. Only modify it if the user explicitly asks to add or remove a repo directory. Never overwrite or recreate it.
