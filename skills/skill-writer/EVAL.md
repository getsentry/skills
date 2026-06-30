# Skill Writer Evaluation

Use this file to evaluate changes to `skill-writer` itself. This is a maintainer eval, not a runtime reference: do not link it from `SKILL.md`.

## Framework Choice

Use AXIS as the skill-eval harness.

| Requirement | AXIS Fit |
|-------------|----------|
| open source | `@netlify/axis` is MIT licensed |
| must use Codex | AXIS has a built-in `codex` adapter |
| must use Codex harness | the adapter runs `codex exec --json` |
| isolated workspaces | each scenario runs in a temp workspace with isolated `HOME` and `CODEX_HOME` |
| LLM-as-judge | scenario `judge` checks grade the full transcript and workspace |
| debugging | reports include transcripts, scores, artifacts, and raw agent output |
| regressions | baselines support score comparison and CI gates |

Do not add custom `run-codex.*` scripts. Add a small AXIS scenario, fixture, or artifact pattern instead.

## Quick Run

Run the working set:

```bash
npx @netlify/axis run --config skills/skill-writer/evals/axis.config.json
```

Run one case:

```bash
npx @netlify/axis run \
  --config skills/skill-writer/evals/axis.config.json \
  --scenario small-inline-workflow
```

Inspect results:

```bash
npx @netlify/axis reports latest --config skills/skill-writer/evals/axis.config.json
npx @netlify/axis reports latest --config skills/skill-writer/evals/axis.config.json --html
```

Compare to a stored baseline:

```bash
npx @netlify/axis run \
  --config skills/skill-writer/evals/axis.config.json \
  --compare-baseline
```

Set or refresh a baseline only after reviewing the report:

```bash
npx @netlify/axis baseline set --config skills/skill-writer/evals/axis.config.json
```

## Evaluation Principles

Use these principles when adding or changing `skill-writer` evals:

1. Start with 2-3 realistic cases before expanding the suite.
2. Compare candidate output against a baseline instead of trusting one-off scores.
3. Write observable judge checks: files created, forbidden files absent, validation mentioned, generated instructions concise.
4. Use LLM-as-judge for open-ended quality: concision, routed structure, source coverage, progressive disclosure, and overfitting risk.
5. Require concrete evidence in judge checks and manual review: paths, artifacts, diffs, transcript snippets, or validation output.
6. Track timing, token use, and interaction waste from AXIS reports.
7. Review transcripts when a run fails or is slow; wasted steps usually point to bloated or ambiguous skill instructions.
8. Use blind old-vs-new comparison for qualitative regressions when scores are close.

## Case Set

AXIS scenarios live in `evals/scenarios/`.

| Case | Purpose |
|------|---------|
| `small-inline-workflow` | catches over-splitting and invented source requirements |
| `reference-backed-integration` | catches bloated `SKILL.md` and hidden optional depth |
| `iteration-from-bad-output` | catches failure to improve from concrete negative evidence |

Add provider-specific cases only when changed rules affect provider-specific mechanics.

## What To Test

| Layer | Purpose | Evidence |
|-------|---------|----------|
| trigger | `skill-writer` is invoked for intended requests and skipped for unrelated requests | AXIS transcript and skill-use behavior |
| structure | generated files obey Agent Skills format and repo registration rules | artifacts, diff, final message, validator transcript |
| quality | generated runtime instructions are concise, routed, sourced, and actionable | AXIS judge checks and manual artifact review |
| regression | candidate output is better than or equal to the baseline on held-out cases | AXIS baseline comparison |

## AXIS Setup

`evals/axis.config.json` configures:

1. `agents: [{"agent": "codex"}]` so Codex is the agent under test.
2. `skills: ["./.."]` so AXIS installs this local `skill-writer` skill for the run.
3. scenario limits so a stuck generation fails quickly enough to debug.

Each scenario configures artifacts for generated skill files, registration files, and validator output when present.

Each scenario copies the repository into AXIS's isolated workspace before Codex starts. That gives `skill-writer` the same repo conventions it sees in normal use without polluting this checkout.

## Rubric

Score each dimension `pass`, `warn`, or `fail` during manual review. AXIS supplies the transcript, artifacts, and judge scores; this rubric decides whether to adopt the change.

| Dimension | Pass | Fail |
|-----------|------|------|
| trigger precision | description fits should-trigger and should-not-trigger requests | overbroad or misses obvious requests |
| artifact minimality | every file has a clear runtime, validation, source, or maintenance role | extra docs, duplicate refs, or catch-all files |
| runtime concision | `SKILL.md` is a router when needed and added lines change decisions/actions/checks | prose repeats rationale or generic background |
| source coverage | decisions cite enough local, official, or example evidence | important behavior depends on unsupported assumptions |
| progressive disclosure | optional depth is routed from `SKILL.md` with clear open-when reasons | required instructions are hidden or always-loaded detail is bloated |
| validation | structural validator runs and manual checks match the skill class/shape | validation missing, irrelevant, or treated as semantic proof |
| portability | provider-specific mechanics are labeled and justified | provider-specific behavior leaks into portable defaults |

Critical dimensions: trigger precision, artifact minimality, runtime concision, progressive disclosure, and validation.

## Adoption Gate

Adopt a `skill-writer` change only when:

1. AXIS runs complete for the working set.
2. no critical dimension regresses on holdout cases.
3. at least one target dimension improves on the case that motivated the change.
4. structural validation passes for generated skills or the transcript explains a legitimate blocker.
5. runtime `SKILL.md` remains a router and does not link to eval files.
6. source and maintenance notes are updated only when the skill contract changes.

## Result Template

```markdown
## Eval Summary
- Baseline:
- Candidate:
- AXIS report:
- Cases run:
- Critical regressions:
- Decision: adopt | revise | reject

## Case Results
| Case | Score | Structure | Quality | Regression | Notes |
|------|-------|-----------|---------|------------|-------|

## Required Fixes
- ...

## Evidence
- AXIS report:
- generated artifacts:
- validator output:
- transcript notes:
```
