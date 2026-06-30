# PR Writer Evaluation

Use these AXIS evals to check whether `pr-writer` produces concise reviewer-facing PR titles and bodies.

## Quick Run

Run the working set:

```bash
npx @netlify/axis run --config skills/pr-writer/evals/axis.config.json
```

Run one behavior case:

```bash
npx @netlify/axis run \
  --config skills/pr-writer/evals/axis.config.json \
  --scenario concise-docs-pr
```

Inspect results:

```bash
npx @netlify/axis reports latest --config skills/pr-writer/evals/axis.config.json
npx @netlify/axis reports latest --config skills/pr-writer/evals/axis.config.json --html
```

Compare to a stored baseline:

```bash
npx @netlify/axis run \
  --config skills/pr-writer/evals/axis.config.json \
  --compare-baseline
```

## What This Tests

| Layer | Evidence |
|-------|----------|
| structure | AXIS transcript, final message, and judge checks |
| deterministic checks | title format, no default template headings, no validation dump |
| model review | reviewer usefulness and PR-body concision |

## Case Set

| Case | Purpose |
|------|---------|
| `concise-docs-pr` | docs-only skill changes should stay concise and omit template or validation boilerplate |

Add cases for bug fixes, breaking contracts, and broad generated diffs when changing those parts of `SKILL.md`.

## Adoption Gate

Adopt a `pr-writer` change only when:

1. AXIS runs complete.
2. judge checks have no critical failure.
3. output title uses an allowed conventional type.
4. output body avoids default `Summary` / `Test Plan` templates.
5. validation is omitted unless it changes reviewer risk.
