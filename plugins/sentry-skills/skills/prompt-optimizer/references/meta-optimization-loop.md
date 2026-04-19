# Meta Optimization Loop

Use this file when refining an existing prompt or when a first draft needs disciplined iteration.

## Inputs

Collect these before iterating:

- current prompt or first draft
- target model family
- optimizer model, if different from the deployment model
- representative eval cases
- scoring rubric
- known failures
- hard constraints

## Optimization loop

### 1. Baseline

Run the current prompt on a representative slice.

Score at least:

- instruction following
- output shape
- tool behavior
- refusal and escalation correctness
- brevity or verbosity
- robustness on ambiguous inputs
- cost, latency, or tool-call efficiency when those matter

Preserve a structured evidence pack for each run:

- prompt version
- eval case
- model output
- relevant trace or tool behavior
- failure reason
- scores

### 2. Failure clustering

Group failures before editing:

- ambiguity
- missing constraints
- conflicting rules
- bad example fit
- weak tool instructions
- weak stop conditions
- provider mismatch
- prompt bloat or duplicated rules

Do not patch each failing case independently if the same root cause appears in multiple places.

### 3. Textual gradients

Write criticisms as concrete directional edits:

- "Clarify when to ask before acting."
- "Separate retrieved context from instructions."
- "Move tool rules into an explicit section."
- "Replace anti-pattern examples with positive demonstrations."

Avoid vague critiques like "make it better" or "be clearer."

### 4. Candidate beam

Generate two to four candidates:

- minimal-diff repair
- structure-first rewrite
- examples-first or tool-rule-centered variant
- provider-specific adapter when needed

Keep one low-risk candidate in the beam so you can tell whether a larger rewrite actually helped.

### 5. Compare on the same slice

Use the same eval cases for the candidate round.

Do not compare candidates on different inputs and assume the scores are comparable.

### 6. Reflective memory

Keep a short log:

| Round | Hypothesis | Edit | Result | Keep? |
|-------|------------|------|--------|-------|
| 1 | Tool-use rules are too vague | Added explicit tool criteria | Better tool selection, same formatting | Yes |

This prevents looping back into edits that already failed.
Record deletions and compaction edits, not just additions.

### 7. Holdout validation

Before finalizing:

- test the winner on holdout cases
- replay the original failure cases
- verify the fix did not regress happy-path behavior

### 8. Stop conditions

Stop prompt editing when:

- scores plateau across rounds
- edits oscillate between two behaviors
- the remaining failures are caused by model or tool limitations
- you are clearly overfitting to the eval slice
- cost rises without enough quality gain to justify the extra prompt complexity

## Practical defaults

- Use five to ten cases for a quick pass.
- Keep at least one holdout case.
- Edit one or two causal dimensions per round.
- Optimize examples, tool descriptions, and output contracts alongside the core prompt.
- For repeated optimization, keep fixed train, validation, and holdout slices so before/after comparisons stay meaningful.
- When budget allows, consider using a stronger optimizer pass than the eventual deployment model.

## What this loop is borrowing from

- score-driven candidate search rather than one linear rewrite
- explicit critique before revision
- lightweight reflection memory across rounds
- holdout validation to resist overfitting
- structured evidence capture so revisions are grounded in actual outputs and scores

Use the loop pragmatically. The point is to learn which edits change behavior, not to imitate a paper mechanically.
