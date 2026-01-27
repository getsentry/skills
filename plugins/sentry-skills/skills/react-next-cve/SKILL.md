---
name: react-next-cve
description: Scan a GitHub org for repos affected by a React/Next.js CVE. Use when given a CVE blog post URL (Vercel changelog, GitHub advisory) to identify impacted repositories. Extracts affected versions, searches org repos, generates remediation report, and optionally creates PRs.
allowed-tools: WebFetch Bash Grep Read AskUserQuestion
---

# React/Next.js CVE Scanner

Scan a GitHub organization for repositories affected by React or Next.js CVEs.

## Usage

Provide a CVE blog post URL and optionally a GitHub organization:
- URL: Vercel changelog, GitHub advisory, or security blog post
- Org: GitHub organization to scan (defaults to getsentry)

## Process

### Step 1: Extract CVE Details

Fetch the CVE blog post and extract:
- CVE identifier
- Affected packages (next, react, react-dom, react-server-dom-*)
- Affected version ranges (could be any major version, not just React 19)
- Fixed versions for each version line

### Step 2: Search Organization

Search for affected packages in package.json files (includes monorepos with nested packages):

```bash
# Search for Next.js in dependencies - returns ALL package.json files including nested ones
gh search code '"next":' --owner {org} --filename package.json --limit 200

# Search for React (any version that might be affected)
gh search code '"react":' --owner {org} --filename package.json --limit 200

# Search for react-server-dom packages if RSC is affected
gh search code 'react-server-dom' --owner {org} --filename package.json --limit 100
```

**Important**: The search returns the full path including nested directories (e.g., `apps/web/package.json`, `packages/ui/package.json`). Track both the repo AND the path for monorepos.

### Step 3: Filter Results

For each repo/path found:

1. **Check if production dependency** (not devDependencies):
```bash
# For root package.json
gh api repos/{org}/{repo}/contents/package.json --jq '.content' | base64 -d | jq '{
  next: .dependencies.next,
  react: .dependencies.react,
  reactDom: .dependencies["react-dom"]
}'

# For nested package.json (monorepos)
gh api repos/{org}/{repo}/contents/{path}/package.json --jq '.content' | base64 -d | jq '{
  next: .dependencies.next,
  react: .dependencies.react,
  reactDom: .dependencies["react-dom"]
}'
```

2. **Check visibility and activity**:
```bash
gh api repos/{org}/{repo} --jq '{visibility, pushed_at, archived, homepage}'
```

3. **Detect package manager** (check at both root and package path for monorepos):
```bash
# Root level
gh api repos/{org}/{repo}/contents --jq '.[].name' | grep -E "pnpm-lock|yarn.lock|package-lock|bun.lockb"

# For monorepos, also check the package directory
gh api repos/{org}/{repo}/contents/{path} --jq '.[].name' | grep -E "pnpm-lock|yarn.lock|package-lock|bun.lockb"
```

Package manager priority: pnpm-lock.yaml → yarn.lock → package-lock.json → bun.lockb

**Monorepo handling**: If a repo has multiple vulnerable package.json files (e.g., `apps/web/package.json` and `packages/ui/package.json`), list them separately in the report and handle each path during the update process.

### Step 4: Compare Versions

Compare each repo's version against affected/fixed versions:
- Parse semver from package.json (strip ^ or ~ prefixes)
- Determine which version line the repo is on (e.g., 15.4.x, 16.0.x, 19.1.x)
- Check if version is below the fix for that version line
- Mark as VULNERABLE or SAFE

For RSC-specific CVEs, also check if the repo actually uses RSC:
- Has Next.js App Router, OR
- Has react-server-dom-* packages in dependencies

### Step 5: Generate Report

Output a markdown report with:

1. **CVE Summary** - What the vulnerability is
2. **Fixed Versions Table** - All version lines and their minimum fixed versions
3. **Vulnerable Public Repos** - Table with repo, current version, fix needed, package manager, deployment URL if any
4. **Vulnerable Internal Repos** - Separate section
5. **Safe Repos** - Repos already on fixed versions or not affected
6. **Not Affected** - Repos with package in devDependencies only

### Step 6: Create PRs (Optional)

After generating the report, ask the user:

> "Would you like me to create PRs for the vulnerable repos?"

If yes, ask which repos to update (can select all or specific ones).

For each selected repo, follow this workflow:

#### 6a. Clone and Setup

```bash
cd /tmp && rm -rf {repo} && gh repo clone {org}/{repo}
cd /tmp/{repo}
```

Note: For monorepos, stay at the repo root for package manager and git commands.

#### 6b. Check Push Access

```bash
git remote -v
```

If origin points to the org repo (not a fork), test push access:
```bash
git push --dry-run 2>&1
```

If permission denied and repo is public, create/use a fork:
```bash
gh repo fork --remote=true
# This sets origin to fork, upstream to original
```

#### 6c. Update Dependencies

Based on detected package manager and repo structure:

**Single-package repos (package.json at root):**
```bash
# pnpm
pnpm add next@{fixed} react@{fixed} react-dom@{fixed}

# yarn
yarn add next@{fixed} react@{fixed} react-dom@{fixed}

# npm
npm install next@{fixed} react@{fixed} react-dom@{fixed}

# bun
bun add next@{fixed} react@{fixed} react-dom@{fixed}
```

**Monorepos (package.json in subdirectory like apps/web):**
```bash
# pnpm workspaces - run from repo root
pnpm add next@{fixed} react@{fixed} react-dom@{fixed} --filter {package-name}
# Or: pnpm --dir {path} add next@{fixed} react@{fixed} react-dom@{fixed}

# yarn workspaces
yarn workspace {package-name} add next@{fixed} react@{fixed} react-dom@{fixed}

# npm workspaces
npm install next@{fixed} react@{fixed} react-dom@{fixed} -w {path}
```

Always update react and react-dom together to matching versions.

#### 6d. Verify Build

```bash
# Check for build script and run it
grep -q '"build"' package.json && {package_manager} build
```

If build fails, report the error and skip this repo.

#### 6e. Run Tests (if available)

```bash
# Check for test script and run it
grep -q '"test"' package.json && {package_manager} test
```

Report test results but continue even if no tests exist.

#### 6f. Create Branch and Commit

```bash
git checkout -b fix/cve-{cve-id}

# Single-package repos
git add package.json {lockfile}

# Monorepos - add both the subdirectory package.json and root lockfile
git add {path}/package.json {lockfile}
# e.g., git add apps/web/package.json pnpm-lock.yaml

git commit -m "$(cat <<'EOF'
fix: update {packages} for CVE-{cve-id}

Updates:
- {package}: {old} → {new}

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

#### 6g. Push and Create PR

```bash
git push -u origin fix/cve-{cve-id}

# If using fork, create PR to upstream
gh pr create --repo {org}/{repo} --title "fix: update packages for CVE-{cve-id}" --body "$(cat <<'EOF'
## Summary
Updates packages to address CVE-{cve-id}.

### Changes
- `{package}`: {old} → {new}

### Vulnerability Details
{brief description from CVE}

### Verification
- ✅ Build passes
- ✅ Tests pass (or N/A)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

#### 6h. Report Results

After processing all repos, provide a summary:

| Repository | PR | Status |
|------------|-----|--------|
| repo-1 | https://github.com/org/repo-1/pull/123 | ✅ Created |
| repo-2 | - | ❌ Build failed |
| repo-3 | https://github.com/org/repo-3/pull/456 | ✅ Created |

## Example Report Output

### CVE-2026-23864 Impact Assessment

**Vulnerability**: DoS vulnerabilities in React Server Components

#### Fixed Versions

| Package | Line | Fixed Version |
|---------|------|---------------|
| next | 15.4.x | 15.4.11+ |
| next | 15.5.x | 15.5.10+ |
| next | 16.0.x | 16.0.11+ |
| react | 19.1.x | 19.1.5+ |
| react | 19.2.x | 19.2.4+ |

#### Vulnerable Repos

| Repository | Path | Next.js | React | PM | Deployment |
|------------|------|---------|-------|-----|------------|
| sentry-docs | / | 15.1.11 → 15.1.12 | ^19.2.3 → 19.2.4 | yarn | docs.sentry.io |
| abacus | / | 16.1.1 → 16.1.5 | 19.2.3 → 19.2.4 | pnpm | - |
| super-duper-status | apps/web | ^15.4.8 → ^15.4.11 | ^19.1.0 → 19.1.5 | pnpm | - |
| ai-linear-tools | ui | 15.5.7 → 15.5.10 | 19.1.0 → 19.1.5 | pnpm | - |
