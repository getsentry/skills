# Source Discovery

Use this guide during synthesis when obvious docs are shallow, stale, incomplete, or too polished to reveal real behavior.

## Source Priority

Prefer sources in this order:

1. Local repository authority: `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, manifests, validators, scripts, tests, and existing neighboring skills.
2. Primary upstream material: official specifications, product docs, API references, release notes, changelogs, and source code.
3. Operational evidence: issue threads, PR discussions, CI failures, incident notes, support patterns, and migration notes.
4. Historical evidence: commit logs, blame, reverted changes, and changelog diffs.
5. Secondary summaries: blog posts, tutorials, and community examples.

Treat secondary and generated content as leads, not authority.

## High-Signal Retrieval Passes

Run the passes that match the skill's risk:

- Core behavior: official docs, source exports, public interfaces, happy-path examples.
- Edge behavior: tests, fixtures, error handling, retries, permissions, validation, and cleanup paths.
- Negative behavior: bug fixes, reverted commits, issue reports, support threads, review comments, and skipped tests.
- Usage behavior: in-repo callers, downstream examples, configuration samples, and migration guides.
- Maintenance behavior: changelog entries, release notes, deprecations, and commits touching the same files repeatedly.

## Commit Log Mining

Use commit history when the task depends on lived behavior rather than only intended behavior.

Good candidates:

- Security, access-control, CI, deployment, or migration skills.
- Skills for internal systems with sparse public docs.
- Skills being improved after repeated failures.
- Areas with many regressions, reversions, or subtle edge cases.

Useful commands:

```bash
git log --oneline -- <path>
git log --stat -- <path>
git log -G '<behavior|symbol|error>' -- <path>
git blame <path>
```

Capture findings as source records with commit SHA, date, affected path, observed behavior, and whether the finding is adopted, rejected, or deferred.

Do not copy large commit messages or diffs into `SKILL.md`. Summarize the behavior and keep provenance in `SOURCES.md` or an evidence file.

## Stop Conditions

Stop collecting when:

- Required coverage dimensions are complete or have explicit next retrieval actions.
- New retrieval mostly repeats known facts.
- Remaining unknowns are low impact or require access the agent does not have.
- The source mix includes both intended behavior and observed behavior for high-risk workflows.

Record the stopping rationale in `SOURCES.md`.
