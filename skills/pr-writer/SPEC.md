# PR Writer Specification

## Intent

The `pr-writer` skill creates and updates pull requests with concise, review-oriented titles and descriptions that match Sentry conventions.

Its main job is to turn branch changes into a reviewer-facing cover note that explains what changed, why it changed, and the few details reviewers need before reading the diff. The output should adapt to the size, risk, and shape of the change: simple PRs should stay terse, while broad, risky, breaking, API/schema, migration, generated, or workflow-heavy PRs should include only the extra structure that makes review easier.

The skill should offer the agent a small menu of optional reviewer aids, such as before/after examples, schemas, interfaces, Mermaid diagrams, screenshots, rollout notes, migration notes, review order, or risk callouts. These are decision tools, not required sections. The agent should choose them with simple heuristics and its own judgment, then omit anything that does not materially improve reviewer understanding.

## Scope

In scope:

- Creating draft pull requests from committed feature branches.
- Updating existing PRs by re-evaluating both title and body against the full branch diff against the base branch.
- Producing natural PR bodies that default to short paragraphs and use structure only when the change shape needs it.
- Choosing optional reviewer aids based on the actual diff shape, including code snippets, payload examples, schemas/interfaces, diagrams, screenshots, review-order notes, rollout notes, migration notes, or risk/tradeoff callouts.
- Producing titles that accurately describe the dominant change in the PR.
- Rejecting bracketed agent, bot, or tool prefixes in PR titles.
- Including issue references, breaking-change context, and review focus when useful and supported by known evidence.

Out of scope:

- Writing commits or deciding commit history policy.
- Running full CI or iterating on failing checks.
- Producing release notes, changelogs, or customer-facing announcements.
- Including mechanical test-plan checklists in PR bodies.
- Mirroring repository PR templates, including empty headings, placeholder checklists, rote "Summary / Test Plan" sections, or validation logs that do not help reviewers understand the change.
- Creating decorative diagrams, exhaustive file-by-file walkthroughs, or copied diffs that make the body longer without reducing reviewer effort.

## Users And Trigger Context

- Primary users: engineers and coding agents preparing Sentry pull requests.
- Common user requests: open a PR, update a PR, refresh a PR after scope changes, address review feedback after follow-up commits, prepare changes for review.
- Should not trigger for: code review requests, commit-only requests, CI-fix loops, or generic documentation writing.

## Runtime Contract

- Required first actions: verify the current branch, committed state, base branch, and diff scope before writing or updating a PR; when updating, use the PR's `baseRefName` as the base branch and inspect the current PR title and body before deciding what to keep.
- Required outputs: a conventional PR title and a concise, natural PR body suitable for `gh pr create` or GitHub API update commands; on updates, include an explicit keep-or-rewrite decision for the title.
- Required body-shape decision: decide whether the change is small/obvious, bug fix, feature, refactor, API/schema/payload/config/CLI change, breaking change, migration, performance/reliability change, broad/generated/cross-cutting change, UI change, workflow/architecture change, or review-feedback update. Use the decision to select the minimum useful structure.
- Required update behavior: if an open PR exists and follow-up commits materially change reviewer expectations, refresh the PR even when the user did not explicitly ask for a PR edit.
- Optional reviewer aids: use before/after blocks for contract or behavior comparisons; schemas or interface snippets for API, payload, type, config, event, or storage changes; Mermaid sequence/flow/state diagrams for async flows, queues, state transitions, lifecycle changes, or multi-component interactions; screenshots or recordings for UI behavior; review-order notes for broad or generated PRs; rollout, migration, compatibility, feature-flag, or deprecation notes for changes that affect adopters or operations.
- Hard negatives: do not add a `Test Plan` section by default, do not paste command transcripts, do not list routine validation as its own heading unless it changes risk assessment, do not add empty template headings, do not narrate every file, do not include Mermaid when prose is clearer, and do not include schemas or examples that merely duplicate obvious code.
- Non-negotiable constraints: never include customer data or PII, never use bracketed agent/tool labels such as `[codex]` in PR titles, never invent issue references, generate reviewer prose rather than tool attribution, ignore repository PR templates, and prefer draft PRs for newly opened pull requests.
- Expected bundled files loaded at runtime: only `SKILL.md`.

## Source And Evidence Model

Authoritative sources:

- Sentry engineering practices for code review.
- Sentry commit message conventions.
- Repository-level agent instructions.
- Google Engineering Practices guidance for CL descriptions.
- Git and Linux kernel patch submission guidance.
- GitHub pull request reviewability guidance.
- GitHub and GitLab Markdown support for Mermaid diagrams in PR/MR descriptions.
- GitLab merge request template prior art for before/after visual comparisons and local validation only when useful.
- Atlassian pull request guidance on using descriptions, reviewer navigation, and visuals to reduce reviewer reconstruction work.
- Conventional Commits and changelog guidance for identifying and communicating breaking changes.
- Observed user rejection of programmatic PR descriptions and preference for concise reviewer context.
- `getsentry/warden#265` as a formatting exemplar for before/after examples on schema and output-shape changes, only when direct comparison is warranted.

Useful improvement sources:

- positive examples: PR descriptions that read like a human cover note and give reviewers the missing context.
- positive examples: PR descriptions that use optional artifacts sparingly, such as a compact schema/interface, before/after payload, Mermaid flow, screenshot, rollout note, or review-order note when that artifact makes the diff easier to review.
- positive examples: PR descriptions that use concrete behavior and reviewer impact instead of meta phrases like "decision model", "expanded contract", or "runtime guidance".
- positive examples: PR titles that stay specific after follow-up commits.
- negative examples: PR bodies that read like essays, repeat the diff, overuse headings, mirror a template, or leak internal agent process.
- negative examples: PR bodies with rote `Test Plan` headings, pasted command output, generic validation details, decorative diagrams, oversized Mermaid blocks, unnecessary schemas, empty headings, or file-by-file narration.
- negative examples: PR bodies that read like release notes for the prompt rather than a human cover note for the change.
- negative examples: PR titles that are vague, process-oriented, or stale after scope changes.
- negative examples: PR titles that use bracketed agent/tool labels instead of conventional commit types, such as `[codex] Paginate replay segment downloads`.
- negative examples: branches with material follow-up commits where the agent pushed changes but left the PR title/body stale.
- commit logs/changelogs: only as source context, not as body text to paste.
- issue or PR feedback: reviewer comments about missing context or excessive detail.
- eval results: prompt-based checks for title accuracy, natural reviewer prose, justified structure, verified references, and privacy boundaries.

Data that must not be stored:

- secrets
- customer data
- private customer, organization, or user identifiers
- support ticket contents not needed for a public PR

## Reference Architecture

- `SKILL.md` contains runtime workflow, command patterns, conditional PR body guidance, examples, and safety constraints.
- `references/` contains no files currently; add focused style or evidence examples only if the runtime file becomes too long or repeated regressions show the examples need more room.
- `references/evidence/` contains no files currently; use it for durable positive and negative PR body examples if iteration data accumulates.
- `scripts/` contains no files currently.
- `assets/` contains no files currently.

## Evaluation

- Lightweight validation: compare generated titles and PR bodies against representative feature, bug-fix, schema-change, breaking-change, migration, UI, performance/reliability, broad-review, generated-change, workflow-diagram, and refactor prompts for brevity, clarity, justified structure, issue references, update-path title handling, and privacy handling.
- Deeper evaluation: maintain a small prompt set with expected body shapes if regressions recur.
- Holdout examples: include at least one simple PR that should be one paragraph, one bug fix that should explain root cause without file bullets, one PR with no known issue reference, and one API or input-format change that should use separate before/after fenced blocks.
- Holdout examples: include at least one breaking contract change that should identify affected consumers and migration guidance, one workflow-heavy PR that should use a compact Mermaid diagram, one UI PR that should mention screenshots or visual evidence only if available, one broad generated PR that should explain generation/review order, and one small PR that must not grow a `Test Plan` or template headings.
- Holdout examples: include at least one PR update where the old title no longer matches the whole PR diff and must be rewritten.
- Holdout examples: include at least one review-feedback or follow-up-commit scenario where the skill should refresh an open PR without an explicit PR-update request.
- Acceptance gates: output title uses an allowed Sentry conventional commit type, uses `!` when the dominant change is breaking, contains no bracketed agent/tool prefix, matches the dominant change, update flows explicitly re-evaluate whether the existing title still fits, material follow-up commits to an open PR trigger a refresh even without an explicit PR-update request, output reads like natural reviewer-facing prose, default body uses paragraphs instead of generic headings, structure is present only when justified by the change shape, optional artifacts are used only when they reduce reviewer effort, body language describes concrete behavior and reviewer impact instead of internal process, breaking changes include affected surface and migration/compatibility context when known, before/after examples appear only when direct comparison is the clearest explanation, unknown issue references are omitted instead of invented, routine validation is omitted unless it changes reviewer risk assessment or explains coverage for changed behavior, generated tool attribution is absent, and customer data is excluded.

## Known Limitations

- The skill cannot guarantee that issue references are correct unless the branch, commits, or user provide them. It must omit references rather than invent placeholders.
- It relies on the agent's judgment to decide when a heading, bullet list, or before/after block helps reviewers more than plain paragraphs.
- It relies on the agent's judgment to decide whether optional reviewer aids, such as schemas, diagrams, screenshots, migration notes, or review-order notes, reduce reviewer effort enough to justify their length.
- Mermaid rendering support and syntax differ by platform/version, so diagrams must stay simple and should be omitted when uncertain or not essential.
- It relies on the agent's judgment to decide when a title is still accurate enough to keep versus rewrite.
- Very large PRs may still need more context than the default body shape encourages.

## Maintenance Notes

- Update `SKILL.md` when PR creation workflow, title rules, body template, examples, or safety constraints change.
- Update `SPEC.md` when intent, scope, evaluation gates, or evidence policy changes.
- Add focused reference files only when examples or guidance would make `SKILL.md` noisy.
- Keep public inventories pointed at the canonical `skills/pr-writer` skill, not mirrors.
