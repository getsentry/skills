# Skill Evals

Use this when authoring evals for a skill's behavior or generated outputs.

Do not confuse this with `EVAL.md` for `skill-writer` itself. Runtime skills should not route to their own eval files unless the user explicitly asks to run or maintain evals.

## Placement

| Artifact | Use |
|----------|-----|
| `EVAL.md` | maintainer playbook for running the skill's evals |
| `evals/axis.config.json` or `evals/axis.config.ts` | AXIS configuration for repeatable agent runs |
| `evals/scenarios/*.{json,ts}` | durable AXIS task cases, working examples, and holdouts |
| `evals/fixtures/` | versioned setup files copied into AXIS workspaces |

Keep eval files outside runtime `SKILL.md` routing. Add `SKILL.md` routing only for skills whose purpose is running evals.

## Framework Choice

| Need | Choose |
|------|--------|
| skill eval playbook | `EVAL.md` that points at AXIS |
| repeatable skill evals | AXIS scenarios with `agents: [{"agent": "codex"}]` |
| Codex requirement | AXIS `codex` adapter, which uses `codex exec --json` |
| structured grading | AXIS `judge` checks, reports, and per-run transcripts |
| baseline/regression tracking | AXIS baselines and `--compare-baseline` |
| provider comparison | AXIS agent matrix only when explicitly requested |
| pure prompt/model comparison | out of scope for skill evals unless Codex is not the system under test |

Be prescriptive: default to AXIS for skill evals that must run real coding agents. Do not add custom runner scripts around `codex exec` unless AXIS cannot express the required setup, artifacts, or scoring.

## Case Format

Use AXIS scenario files as the runnable source of truth:

```json
{
  "name": "<human-readable case name>",
  "prompt": "<exact user request>",
  "judge": [
    {"check": "<observable success criterion>", "weight": 0.4},
    {"check": "<quality criterion with evidence>", "weight": 0.4},
    {"check": "<validation or artifact criterion>", "weight": 0.2}
  ],
  "setup": [
    {"action": "copy", "match": "./evals/fixtures/<case>/**", "destination": "."}
  ],
  "artifacts": ["skills/<expected-skill>/**", "README.md"]
}
```

Keep prompts specific enough to make success observable. Put long source fixtures in `evals/fixtures/`, not inside the prompt.

## Minimal Case Set

For authoring/generator skills, start with:

| Case | Purpose |
|------|---------|
| happy path | confirms expected output with normal inputs |
| robust or secure variant | confirms edge cases, safety, or failure handling |
| anti-pattern plus correction | confirms the skill avoids known bad output |

For workflow or documentation skills, use at least one happy path and one failure/edge case. Add holdouts when changing skill behavior repeatedly.

## Assertions And Judges

Start each case with expected output and broad success criteria. After the first real run, add assertions for facts that are observable from the output:

| Check type | Use for |
|------------|---------|
| deterministic assertion | files exist, references resolve, validator passes, required sections are present or absent |
| script check | JSON shape, row counts, image dimensions, schema validity, generated diff shape |
| LLM judge | concision, usefulness, progressive disclosure, overfitting, source coverage, reviewer quality |
| human review | taste, audience fit, surprising omissions, and whether the output solves the actual problem |

LLM judges must cite evidence. Prefer blind old-vs-new comparison for subjective quality so the judge does not know which output is the candidate.

## AXIS Shape

Use AXIS as the harness and configure Codex as the agent under test:

```bash
npx @netlify/axis run --config skills/<skill>/evals/axis.config.json --scenario <case>
npx @netlify/axis reports latest --config skills/<skill>/evals/axis.config.json --html
npx @netlify/axis run --config skills/<skill>/evals/axis.config.json --compare-baseline
```

Minimum AXIS config:

```json
{
  "scenarios": "./scenarios",
  "agents": [{"agent": "codex", "flags": {"full-auto": true}}],
  "skills": ["./.."]
}
```

Put scenario-specific artifact globs in each scenario so reports capture the generated skill, relevant registration files, and validation output without archiving the whole repository.

AXIS provides isolated workspaces, isolated `CODEX_HOME`, Codex JSON transcripts, artifact capture, LLM judge checks, reports, and baselines. Use OpenRouter only when the user explicitly wants an external judge outside Codex/AXIS.

## Rubric

Score `pass`, `warn`, or `fail`.

| Dimension | Pass | Fail |
|-----------|------|------|
| trigger precision | triggers for intended requests and avoids unrelated ones | overbroad or misses obvious requests |
| artifact minimality | every file has a clear role | extra docs, duplicate refs, or catch-all files |
| runtime concision | `SKILL.md` stays compact and behavior-changing | generic or repeated prose |
| source coverage | important decisions have enough evidence | unsupported assumptions drive behavior |
| progressive disclosure | optional depth is routed clearly | required instructions are hidden or always loaded |
| validation | structural checks and manual checks match the skill | validation is missing or treated as semantic proof |

Critical dimensions: trigger precision, artifact minimality, runtime concision, progressive disclosure, and validation.

## Adoption Gate

Adopt a skill change only when:

1. structural validation passes
2. no critical dimension regresses on holdout cases
3. at least one target dimension improves on the case that motivated the change
4. eval artifacts stay out of runtime routing unless the skill's purpose is eval execution
5. AXIS report artifacts show enough evidence to debug failures without rerunning immediately
