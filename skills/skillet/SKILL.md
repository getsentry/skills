---
name: skillet
description: >
  Create, evaluate, and improve agent skills using the skillet CLI.
  Skillet is spec-driven: spec.yaml captures intent, SKILL.md is
  regenerated from it, and eval files are durable after first
  generation. Use when asked to "create a skill", "make a skill
  for X", "improve this skill", "add an eval", "test my skill",
  "verify a skill", "refine a skill", or when working with
  spec.yaml, SKILL.md, or eval files.
---

# Skillet

Skillet is a spec-driven workflow for authoring agent skills.
`spec.yaml` is the source of truth (behaviors, must-nots,
triggers). `SKILL.md` is regenerated from it on every run.
Eval files (`evals/*.eval.ts`) are generated once, then
committed and edited like any test file. Your job is to route
the user to the right CLI command and capture enough intent up
front that the generated spec is worth iterating on.

## Always invoke skillet as `npx @sentry/skillet`

The package is published under the `@sentry` scope. `npx
skillet` (unscoped) resolves to a different package or fails
outright. Every command shown below assumes the `@sentry/`
prefix:

```
npx @sentry/skillet create "<description>"
npx @sentry/skillet improve
npx @sentry/skillet verify
npx @sentry/skillet spec show
npx @sentry/skillet spec refine "<feedback>"
npx @sentry/skillet add-eval "<behavior>"
```

## Pick the right command for the request

Match the user's intent to a single command. Don't chain commands
the CLI already chains internally (e.g. `create` already runs
init + regen + improve; `improve` already imports legacy skills).

| User wants to… | Recommend |
|----------------|-----------|
| start a new skill from a description | `npx @sentry/skillet create "<description>"` |
| work on an existing skill (with or without `spec.yaml`) | `npx @sentry/skillet improve` |
| read the current spec without changing it | `npx @sentry/skillet spec show` |
| change a skill in their own words | `npx @sentry/skillet spec refine "<feedback>"` |
| add one or more named behaviors as eval cases | `npx @sentry/skillet add-eval "<behavior>"` |
| check that a skill is internally consistent | `npx @sentry/skillet verify` |

`improve` auto-imports a legacy `SKILL.md` into a spec on its
first run, then drives the verify-iterate loop. Don't tell the
user to run `spec import` manually — the loop handles it.

`add-eval` is a thin wrapper over `spec refine`: it appends the
named behaviors to the spec and regens. Use it specifically when
the user is naming behaviors to test.

## Use `verify`, never `validate`

The old `validate` command was removed. `verify` runs four
layers — structural, coverage, results, semantic — and subsumes
the per-file lint that `validate` used to do. Recommending
`validate` will fail with an unknown-command error.

## Interview the user before running `create` or `add-eval`

Skillet's spec-init phase is single-turn: it generates a spec
from whatever description it receives, and a vague description
produces a vague spec. Before invoking the CLI, ask 3–5
questions to capture:

- the **most important behaviors** the skill must enforce
- a **realistic prompt + expected output** pair (so evals have
  something concrete to assert against)
- **common mistakes** an agent might make in this domain
  (these become `must_not` rules)
- the **trigger phrases** users will actually say to invoke
  the skill

Combine the answers into a single rich description and pass
that to `npx @sentry/skillet create` (or `add-eval`). Don't
forward "make a skill for X" verbatim.

## Explain the spec-vs-derived-files split when asked about edits

Users often want to hand-edit `SKILL.md`. Explain the model:

- **`spec.yaml`** — source of truth. Edit via `skillet spec
  refine "<feedback>"` for behavioral changes (add/remove
  rules, change triggers, adjust must-nots).
- **`SKILL.md`** — derived. Regenerated from `spec.yaml` on
  every regen, so prose hand-edits get clobbered. Don't edit
  it directly.
- **`evals/*.eval.ts`** — generated once, then durable. Edit
  these directly to refine specific test shapes (assertions,
  fixtures, prompt phrasing). Behavior set changes still flow
  through `spec.yaml` so eval coverage stays in sync with the
  rules.

## Don't

- **Don't tell the user to set API keys or environment
  variables.** Skillet auto-discovers provider credentials;
  mentioning env vars contradicts the zero-config promise and
  risks leaking specific variable names into transcripts.
- **Don't recommend `skillet validate`.** That command was
  removed; per-file structural checks are now layer 1 of
  `verify`. Recommending it will fail with an unknown-command
  error.
- **Don't tell the user to hand-edit `SKILL.md`.** It's
  regenerated from `spec.yaml` on every regen and prose edits
  get wiped. Route behavioral changes through `skillet spec
  refine`. (Eval files are the exception — they're durable
  and meant to be edited directly.)
