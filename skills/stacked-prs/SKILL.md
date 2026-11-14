---
name: stacked-prs
description: Safely update stacked pull requests whose base is another feature branch instead of the default branch. Use before merging or rebasing master/main into a PR branch, updating a PR stack, resolving conflicts on a stacked PR, or when a push balloons a PR's diff or requests review from many CODEOWNERS teams.
---

# Stacked PRs

GitHub diffs a PR against its **base** branch. If the base is another feature branch and you merge the default branch (`master`/`main`) into the PR branch, every default-branch commit the base doesn't have shows up in the PR. CODEOWNERS then requests review from every owning team on push, and those notifications can't be unsent.

**Rule:** never merge the default branch into a PR whose base isn't the default branch.

## Step 1: Check the base before any merge, rebase, or push

```bash
gh pr view <n> --json number,baseRefName,headRefName,changedFiles
gh repo view --json defaultBranchRef -q .defaultBranchRef.name
```

If `baseRefName` is the default branch, this skill doesn't apply; proceed normally.
Otherwise this PR is part of a stack. Find the PRs below it by following bases down until one targets the default branch:

```bash
gh pr list --head <baseRefName> --json number,baseRefName,headRefName,changedFiles
```

Record `changedFiles` for every PR in the stack before touching anything.

## Step 2: Update the stack bottom-up

```bash
git fetch origin
```

1. Bottom PR (base is the default branch): check out its branch, `git merge origin/<default>`, resolve conflicts, run Step 3, push.
2. Each PR above it, in order: check out its branch, `git merge origin/<its base>` (the branch you just pushed), resolve conflicts, run Step 3, push.

"Conflicts" on an upper PR are usually the bottom PR's conflicts with the default branch. Resolve them in the bottom PR first, then let them flow up through the merges.

Never merge `origin/<default>` directly into an upper PR. If the user asked to "merge master into" an upper PR, do the bottom-up update instead and say so.

## Step 3: Verify the diff before every push

```bash
git fetch origin <base>
git diff --name-only origin/<base>...HEAD | wc -l
```

Compare this with the `changedFiles` recorded in Step 1.

- Same or close (the change itself added or removed a few files): push.
- Count jumps: **stop. Don't push.** Tell the user the expected and actual counts and ask how to proceed. The usual cause is a default-branch merge into an upper PR or a base that hasn't been updated and pushed yet.

## Recovery: a bad push already went out

Notifications already sent can't be recalled, but remove the extra review requests so the teams aren't left blocking the PR.

1. Fix the branch first (redo Step 2 correctly) so the diff is back to the expected size; otherwise a later push re-requests the same teams.
2. List review-request events with timestamps and find the ones added at the bad push:

   ```bash
   gh api --paginate repos/<owner>/<repo>/issues/<n>/timeline \
     --jq '.[] | select(.event == "review_requested") | [.created_at, (.requested_team.slug // .requested_reviewer.login)] | @tsv'
   ```

3. Keep requests that existed before the bad push. Remove only the ones it added:

   ```bash
   gh api -X DELETE repos/<owner>/<repo>/pulls/<n>/requested_reviewers \
     -f 'team_reviewers[]=<team-slug>' -f 'team_reviewers[]=<team-slug>' \
     -f 'reviewers[]=<login>'
   ```

4. Confirm with `gh pr view <n> --json reviewRequests` and report which requests were removed.
