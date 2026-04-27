# PR Writer Specification

## Intent

The `pr-writer` skill creates and updates pull requests with concise, review-oriented titles and descriptions that match Sentry conventions.

Its main job is to turn branch changes into a readable PR body that explains what changed, why it changed, and the few details reviewers need before reading the diff. It should avoid long essays and mechanical diff summaries.

## Scope

In scope:

- Creating draft pull requests from committed feature branches.
- Updating existing PR titles or descriptions.
- Producing compact PR bodies with optional bold emphasis sections.
- Including issue references and review context when useful.

Out of scope:

- Writing commits or deciding commit history policy.
- Running full CI or iterating on failing checks.
- Producing release notes, changelogs, or customer-facing announcements.
- Including test-plan checklists in PR bodies.

## Users And Trigger Context

- Primary users: engineers and coding agents preparing Sentry pull requests.
- Common user requests: create a PR, open a PR, update a PR body, edit a PR title, prepare changes for review.
- Should not trigger for: code review requests, commit-only requests, CI-fix loops, or generic documentation writing.

## Runtime Contract

- Required first actions: verify the current branch, committed state, base branch, and diff scope before writing or updating a PR.
- Required outputs: a conventional PR title and a concise PR body suitable for `gh pr create` or GitHub API update commands.
- Non-negotiable constraints: never include customer data or PII, ignore repository PR templates, omit test-plan sections, and prefer draft PRs for newly opened pull requests.
- Expected bundled files loaded at runtime: only `SKILL.md`.

## Source And Evidence Model

Authoritative sources:

- Sentry engineering practices for code review.
- Sentry commit message conventions.
- Repository-level agent instructions.
- Observed user preference for short PR bodies with optional bold emphasis sections.
- `getsentry/warden#265` as a formatting exemplar for before/after examples on schema and output-shape changes.

Useful improvement sources:

- positive examples: PR descriptions that reviewers can scan quickly.
- negative examples: PR bodies that read like essays, repeat the diff, or overuse headings.
- commit logs/changelogs: only as source context, not as body text to paste.
- issue or PR feedback: reviewer comments about missing context or excessive detail.
- eval results: prompt-based checks for concise summaries, optional sections, and privacy boundaries.

Data that must not be stored:

- secrets
- customer data
- private customer, organization, or user identifiers
- support ticket contents not needed for a public PR

## Reference Architecture

- `SKILL.md` contains runtime workflow, command patterns, PR body template, examples, and safety constraints.
- `references/` contains no files currently; add focused style or evidence examples only if the runtime file becomes too long or repeated regressions show the examples need more room.
- `references/evidence/` contains no files currently; use it for durable positive and negative PR body examples if iteration data accumulates.
- `scripts/` contains no files currently.
- `assets/` contains no files currently.

## Evaluation

- Lightweight validation: compare generated PR bodies against representative feature, schema-change, and refactor prompts for brevity, clarity, optional-section use, issue references, and privacy handling.
- Deeper evaluation: maintain a small prompt set with expected body shapes if regressions recur.
- Holdout examples: include at least one simple PR that should have no bold section, one PR with no known issue reference, and one API or input-format change that should use separate before/after fenced blocks.
- Acceptance gates: output begins with a 1-3 sentence summary, uses no required generic headings, includes at most a few bold emphasis blocks, uses before/after examples only when direct comparison is the clearest explanation, omits unknown issue references instead of inventing placeholders, avoids test-plan sections, and does not include customer data.

## Known Limitations

- The skill cannot guarantee that issue references are correct unless the branch, commits, or user provide them, and should omit references rather than invent placeholders.
- It relies on the agent's judgment to decide whether a bold emphasis block is useful.
- Very large PRs may still need more context than the default body shape encourages.

## Maintenance Notes

- Update `SKILL.md` when PR creation workflow, title rules, body template, examples, or safety constraints change.
- Update `SPEC.md` when intent, scope, evaluation gates, or evidence policy changes.
- Add focused reference files only when examples or guidance would make `SKILL.md` noisy.
- Keep public inventories pointed at the canonical `skills/pr-writer` skill, not mirrors.
