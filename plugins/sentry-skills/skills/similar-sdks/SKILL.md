---
name: similar-sdks
description: Investigate how other Sentry SDKs in the same category implement a concept. Use when asked to "check other SDKs", "how do other SDKs do X", "similar SDKs", "cross-sdk comparison", "compare SDK implementations", "what do sibling SDKs do", or investigate a feature across backend, mobile, or frontend SDK groups.
argument-hint: "[category:] <query>"
---

# Similar SDKs

Investigate how other Sentry SDKs in the same category implement a concept, then compile a cross-SDK comparison.

## Arguments

- `query` — a question or topic to investigate across sibling SDKs (e.g., "what are typical options for metrics")
- `category` (optional prefix) — one of `backend`, `mobile`, or `frontend`; restricts the search to that category only

## Examples

```
/similar-sdks what are typical options for metrics
/similar-sdks how is session replay implemented
/similar-sdks backend: how are breadcrumbs captured
/similar-sdks frontend: how is error boundary handled
```

## Step 1: Detect the Current Repo

Run this command via Bash to get the repo root path:

```bash
git rev-parse --show-toplevel
```

Extract the repo name from the last path component of the output (e.g., `/Users/me/repos/sentry-java` → `sentry-java`).

## Step 2: Load SDK Groups

Read `${CLAUDE_SKILL_ROOT}/references/sdk-groups.md` to load the category-to-SDK mapping.

## Step 3: Parse the Argument

Check if the argument starts with a category prefix:

| Pattern | Category | Query |
|---------|----------|-------|
| `backend: how are breadcrumbs captured` | `backend` | `how are breadcrumbs captured` |
| `mobile: scope management` | `mobile` | `scope management` |
| `how is replay implemented` | _(none)_ | `how is replay implemented` |

The category must be one of: `backend`, `mobile`, `frontend`.

## Step 4: Determine Target SDKs

**If a category was specified:**
1. Use only the SDKs listed under that category
2. Remove the current repo from the list

**If no category was specified:**
1. Find ALL categories that contain the current repo
2. Collect all SDKs from those categories into a single list
3. Deduplicate — each SDK appears only once
4. Remove the current repo from the list

**Examples (from `sentry-java`, which is in `backend` + `mobile`):**
- No prefix → targets: `sentry-python`, `sentry-ruby`, `sentry-go`, `sentry-dotnet`, `sentry-php`, `sentry-elixir`, `sentry-cocoa`, `sentry-dart`, `sentry-react-native`
- `backend:` prefix → targets: `sentry-python`, `sentry-ruby`, `sentry-go`, `sentry-dotnet`, `sentry-php`, `sentry-elixir`

## Step 5: Investigate Each Target SDK

For each SDK in the target list, invoke `/local-repo` using the Skill tool:

```
/local-repo <sdk-name> <query>
```

- Launch all invocations in parallel using the Task tool (one Task per SDK, `subagent_type` of `general-purpose`)
- Each Task should use the Skill tool to call `/local-repo <sdk-name> <query>`
- Never invoke `/local-repo` for the same SDK more than once
- If `/local-repo` reports that a repo is not available locally, do NOT fall back to GitHub or any remote queries. Instead, report "`<sdk-name>` is not cloned locally — skipped." in the final summary.
- **Relay warnings:** `/local-repo` may report that a repo is not on its default branch, is behind the remote, or has local changes. Each Task MUST include these warnings in its result so they can be surfaced in the final summary.

## Step 6: Compile Cross-SDK Comparison

After all investigations complete, present a structured summary:

1. **Repo notices** — list any warnings from `/local-repo` about repos that were skipped (not cloned locally), not on their default branch, behind the remote, or having local changes. Omit this section if there are no notices.
2. **Overview** — one-paragraph summary of how the concept is handled across SDKs
3. **Per-SDK findings** — for each SDK investigated:
   - What it does (brief description)
   - Key file paths
   - Notable implementation details
4. **Common patterns** — what most SDKs share
5. **Notable differences** — where SDKs diverge and why (language idioms, platform constraints, etc.)
6. **Recommendations** (if applicable) — insights relevant to the current repo based on what sibling SDKs do
