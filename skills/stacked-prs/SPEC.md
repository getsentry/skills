# Stacked PRs Specification

## Intent

Prevent agents from merging the default branch into a stacked PR (one whose base is another feature branch). That mistake floods the PR diff with unrelated commits and makes CODEOWNERS request review from dozens of teams, which can't be unsent.

This lives as an on-demand skill instead of always-on `CLAUDE.md`/`AGENTS.md` context so it only costs tokens when an agent is actually updating a PR branch.

## Scope

In scope:
- Detecting whether a PR is part of a stack before merge, rebase, or push.
- Updating a stack bottom-up from the default branch.
- Pre-push diff-size check against the PR's recorded `changedFiles`.
- Cleaning up review requests added by a bad push.

Out of scope:
- Creating stacks or choosing a stacking tool (Graphite, ghstack, git-town, etc.).
- Rebase-based stack workflows; the runtime flow assumes merge-based updates.
- Iterating on CI or review feedback (use `iterate-pr`).

## Users And Trigger Context

- Primary users: engineers and coding agents updating existing PR branches.
- Invocation: model-invocable, so it triggers before an agent merges or rebases the default branch into a PR branch.
- Common user requests: merge master into this PR, update my stack, fix conflicts on this stacked PR, why did my PR request review from every team.
- Should not trigger for: PRs that target the default branch, creating new PRs, writing PR descriptions.

## Runtime Contract

- Required first actions: read the PR's `baseRefName` and `changedFiles`, and the repo's default branch.
- Required outputs: stack updated bottom-up, or a stop-and-ask report when the diff size jumps.
- Non-negotiable constraints: never merge the default branch into a non-bottom stacked PR; never push when the file count jumps without user confirmation; only remove review requests the bad push added.
- Expected bundled files loaded at runtime: `SKILL.md` only.

## Source And Evidence Model

Authoritative sources:
- GitHub PR comparison semantics (diff against base) and CODEOWNERS auto-request behavior.
- GitHub REST endpoints: issue timeline (`review_requested` events) and `DELETE /pulls/{n}/requested_reviewers`.
- Original guidance: an engineer's `CLAUDE.md` rule written after an agent merged master into a stacked PR in `getsentry/sentry` and requested review from ~20 CODEOWNERS teams.

Useful improvement sources:
- negative examples: pushes that triggered mass CODEOWNERS requests.
- positive examples: stacks updated bottom-up without diff growth.

Data that must not be stored:
- secrets
- customer data
- private URLs or identifiers not needed for reproduction

## Reference Architecture

- `SKILL.md` contains the full runtime workflow.
- `references/`, `scripts/`, `assets/`: none.

## Validation

- Lightweight validation: `uv run skills/skill-writer/scripts/quick_validate.py skills/stacked-prs`.
- Acceptance gates: validator passes; workflow refuses a direct default-branch merge into an upper stacked PR; pre-push check stops on a file-count jump.

## Known Limitations

- `changedFiles` comparison is a heuristic; legitimate large changes can trip it, which is why it asks instead of failing.
- Stack discovery via `gh pr list --head` assumes one open PR per head branch.

## Maintenance Notes

- Update `SKILL.md` if GitHub changes timeline event shapes or the requested-reviewers API.
- Revisit whether the skill is still needed as models stop making this mistake unprompted.
