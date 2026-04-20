---
name: iterate-pr
description: Iterate on a PR until CI passes. Use when you need to fix CI failures, address review feedback, or continuously push fixes until all checks are green. Automates the feedback-fix-push-wait cycle.
---

# Iterate on PR Until CI Passes

Continuously iterate on the current branch until all CI checks pass and review feedback is addressed.

**Requires**: GitHub CLI (`gh`) authenticated.

**Requires**: The `uv` CLI for python package management, install guide at https://docs.astral.sh/uv/getting-started/installation/

**Important**: All scripts must be run from the repository root directory (where `.git` is located), not from the skill directory. Use the full path to the script via `${CLAUDE_SKILL_ROOT}`.

## Bundled Scripts

### `scripts/fetch_pr_checks.py`

Fetches CI check status and extracts failure snippets from logs.

```bash
uv run ${CLAUDE_SKILL_ROOT}/scripts/fetch_pr_checks.py [--pr NUMBER]
```

Returns JSON:
```json
{
  "pr": {"number": 123, "branch": "feat/foo"},
  "summary": {"total": 5, "passed": 3, "failed": 2, "pending": 0},
  "checks": [
    {"name": "tests", "status": "fail", "log_snippet": "...", "run_id": 123},
    {"name": "lint", "status": "pass"}
  ]
}
```

### `scripts/fetch_pr_feedback.py`

Fetches and categorizes PR review feedback using the [LOGAF scale](https://develop.sentry.dev/engineering-practices/code-review/#logaf-scale).

```bash
uv run ${CLAUDE_SKILL_ROOT}/scripts/fetch_pr_feedback.py [--pr NUMBER]
```

Returns JSON with feedback categorized as:
- `high` - Must address before merge (`h:`, blocker, changes requested)
- `medium` - Should address (`m:`, standard feedback)
- `low` - Optional (`l:`, nit, style, suggestion)
- `bot` - Informational automated comments (Codecov, Dependabot, etc.)
- `resolved` - Already resolved threads

Review bot feedback (from Sentry, Warden, Cursor, Bugbot, CodeQL, etc.) appears in `high`/`medium`/`low` with `review_bot: true` — it is NOT placed in the `bot` bucket.

### `scripts/monitor_pr_checks.py`

Monitors PR checks until they all reach a terminal state. Retries transient `gh` failures, treats `skipping` and `cancel` as terminal states, and waits for checks to register after a fresh push instead of exiting early.

```bash
uv run ${CLAUDE_SKILL_ROOT}/scripts/monitor_pr_checks.py [--pr NUMBER]
```

Prints one terminal marker followed by a tab-separated check summary:
- `ALL_CHECKS_PASSED`
- `CHECKS_DONE_WITH_FAILURES`

## Workflow

### 1. Identify PR

```bash
gh pr view --json number,url,headRefName
```

Stop if no PR exists for the current branch.

### 2. Gather Review Feedback

Run `${CLAUDE_SKILL_ROOT}/scripts/fetch_pr_feedback.py` to get categorized feedback already posted on the PR.

### 3. Handle Feedback by LOGAF Priority

**Auto-fix (no prompt):**
- `high` - must address (blockers, security, changes requested)
- `medium` - should address (standard feedback)

When fixing feedback:
- Understand the root cause, not just the surface symptom
- Check for similar issues in nearby code or related files
- Fix all instances, not just the one mentioned

This includes review bot feedback (items with `review_bot: true`). Treat it the same as human feedback:
- Real issue found → fix it
- False positive → skip, but explain why
- Never silently ignore review bot feedback — always verify the finding

**Prompt user for selection:**
- `low` - present numbered list and ask which to address:

```
Found 3 low-priority suggestions:
1. [l] "Consider renaming this variable" - @reviewer in api.py:42
2. [nit] "Could use a list comprehension" - @reviewer in utils.py:18
3. [style] "Add a docstring" - @reviewer in models.py:55

Which would you like to address? (e.g., "1,3" or "all" or "none")
```

**Skip silently:**
- `resolved` threads
- `bot` comments (informational only — Codecov, Dependabot, etc.)

### 4. Check CI Status

Run `${CLAUDE_SKILL_ROOT}/scripts/fetch_pr_checks.py` to get structured failure data.

**Wait if pending:** If review bot checks (sentry, warden, cursor, bugbot, seer, codeql) are still running, wait before proceeding—they post actionable feedback that must be evaluated. Informational bots (codecov) are not worth waiting for.

### 5. Fix CI Failures

**Investigation is mandatory before any fix.** Do not guess, assume, or infer the cause from the check name or a surface-level reading of the error. You must trace the failure to its root cause in the actual code.

For each failure:

1. **Read the full log, not just the snippet.** Use `gh run view <run-id> --log-failed` if the snippet is truncated or ambiguous. Identify the exact failing assertion, exception, or lint rule.
2. **Trace backwards from the failure to the cause.** Follow the stack trace or error message into the source code. Read the relevant functions, types, and call sites — not just the line flagged. Do not stop at the first plausible explanation.
3. **Verify your understanding before touching code.** You should be able to state: "This fails because X, which was introduced/affected by Y." If you cannot state that clearly, keep investigating.
4. **Do not assume the feedback is wrong.** If a check flags something that seems incorrect, investigate fully before concluding it's a false positive. Most apparent false positives turn out to be real issues on closer inspection.
5. **Check for related instances.** If a type error, import issue, or logic bug exists at one call site, search for the same pattern in nearby code and related files. Fix all instances.
6. **Fix the root cause with minimal, targeted changes.** Do not paper over the symptom with a workaround.
7. **Extend tests when needed.** If the fix introduces behavior not covered by existing tests, add a test case (not a whole new test file).

### 6. Verify Locally, Then Commit and Push

Before committing, verify your fixes locally:
- If you fixed a test failure: re-run that specific test locally
- If you fixed a lint/type error: re-run the linter or type checker on affected files
- For any code fix: run existing tests covering the changed code

If local verification fails, fix before proceeding — do not push known-broken code.

```bash
git add <files>
git commit -m "fix: <descriptive message>"
git push
```

### 7. Monitor CI and Address Feedback

Keep monitoring CI status and review feedback in a loop instead of blocking:

1. Run `uv run ${CLAUDE_SKILL_ROOT}/scripts/fetch_pr_checks.py` to get current CI status
2. If all checks passed, proceed to exit conditions
3. If any checks failed (none pending), return to step 5
4. If checks are still pending:
   a. Run `uv run ${CLAUDE_SKILL_ROOT}/scripts/fetch_pr_feedback.py` for new review feedback
   b. Address any new high/medium feedback immediately (same as step 3)
   c. If changes were needed, commit and push (this restarts CI), then continue monitoring from the refreshed branch state
   d. Sleep 30 seconds (don't increase on subsequent iterations), then repeat from sub-step 1
5. After all checks pass, wait 10 seconds for late-arriving review bot comments, then run `uv run ${CLAUDE_SKILL_ROOT}/scripts/fetch_pr_feedback.py`. Address any new high/medium feedback — if changes are needed, return to step 6.

If you're in Claude Code, you can replace the sleep-based wait above with `MonitorTool` so the polling happens in the background instead of consuming context. This is a Claude-only optimization, not the default workflow for other agents.

Run the bundled monitor script through `MonitorTool` with `persistent: false`:

```bash
uv run ${CLAUDE_SKILL_ROOT}/scripts/monitor_pr_checks.py
```

Set `timeout_ms` to match the repository's normal CI duration instead of hardcoding a 15-minute timeout.

After `MonitorTool` reports completion, re-run `uv run ${CLAUDE_SKILL_ROOT}/scripts/fetch_pr_checks.py`:
- If any checks failed, return to step 5.
- If all checks passed, continue to sub-step 5 above.

If you pushed new changes while monitoring, start a fresh monitor so it watches the new set of CI runs.

### 8. Repeat

If step 7 required code changes (from new feedback after CI passed), return to step 2 for a fresh cycle. CI failures during monitoring are already handled within step 7's polling loop.

## Exit Conditions

**Success:** All checks pass, post-CI feedback re-check is clean (no new unaddressed high/medium feedback including review bot findings), user has decided on low-priority items.

**Ask for help:** Same failure after 2 attempts, feedback needs clarification, infrastructure issues.

**Stop:** No PR exists, branch needs rebase.

## Fallback

If scripts fail, use `gh` CLI directly:
- `gh pr checks name,state,bucket,link`
- `gh run view <run-id> --log-failed`
- `gh api repos/{owner}/{repo}/pulls/{number}/comments`
