# PR Screenshots Specification

## Intent

Turn a UI change into screenshot evidence in a PR description. It is separate
from `commit` and `pr-writer`, so attaching images is not part of committing
and the table conventions can change without widening the PR prose guidance.

## Out of Scope

- PR titles and prose bodies (`pr-writer`).
- Commit messages (`commit`).
- Product-specific setup for running a local app, logging in, or seeding data.
- Browser automation tool setup.

## Should Not Trigger For

- PRs without visual changes.
- Screenshots for bug reports outside a PR or issue body.
- Design mockups.

## Acceptance Gates

- No synthetic stories or injected styles used as evidence.
- One row per location and state, never grouped.
- Pixel-identical pairs move to the Unchanged table.
- `Location` first-column header, and no "What changed" column.
- New pages get "after" screenshots only.

## Known Limitations

- Pixel diffs need an image tool in the environment. Without one, the agent
  falls back to an eye check and should say so.
- Capturing the base branch may require rebuilding the app, which the skill
  does not automate.
