# Prompt Learnings

Use this file when you want the optimization workflow to explicitly apply the learnings from current prompt guidance rather than implicitly relying on them.

## Why this matters

Prompt quality is not only about adding better instructions. It is also about removing low-value tokens, reducing duplication, and ordering context so the model can reliably distinguish policy from evidence.

Treat the prompt as a scarce budget:

- every token competes with task context and conversation state
- every duplicate instruction increases the chance of drift or contradiction
- every unnecessary example increases cost and can overfit the prompt
- every mixed block of instructions and evidence makes the model do avoidable parsing work

## Core rules

### 1. Keep prompts concise on purpose

Use the shortest wording that preserves the behavioral constraint.

Cut:

- motivational filler
- repeated reminders
- redundant persona text
- generic explanations the model already knows
- examples that do not improve evals

Keep:

- task-specific rules
- hard constraints
- output contracts
- tool-use triggers
- escalation boundaries

### 2. Keep one authoritative instruction per behavior

If a rule exists in more than one layer, choose one owner:

- `system` or `developer` for durable behavior
- example set for format and edge-case demonstrations
- user/template variables for task-local facts

Do not repeat the same rule in all three unless evals show the duplication is necessary.

Typical duplicates to collapse:

- verbosity rules
- "check before guessing"
- ask-first versus act-now behavior
- output format rules
- refusal and escalation boundaries

### 3. Separate policy from evidence

Use distinct sections for:

- instructions
- retrieved documents
- examples
- tool rules
- output schema

The model should not have to infer which text is binding instruction and which text is background material.

### 4. Order long context deliberately

For long-context prompts:

- place long documents and raw evidence before the final query
- keep the actual ask in a terminal section
- keep supporting metadata attached to the evidence it describes

If the prompt is short and direct, do not cargo-cult long-context ordering. Use it when there is enough context for placement to matter.

### 5. Start simple before adding examples

Especially for reasoning-oriented models:

- try zero-shot first
- add few-shot examples only when output shape, boundary behavior, or edge cases remain unstable

When examples are needed:

- keep them structurally consistent
- prefer positive demonstrations
- remove examples that no longer move the score

### 6. Use markers as tools, not decoration

Markers help when they:

- separate content types
- label boundaries clearly
- reduce instruction/context mixing

Markers hurt when they:

- wrap every sentence
- duplicate information already conveyed by headings
- add naming complexity without improving clarity

### 7. Optimize by deletion too

A prompt often improves when you remove:

- obsolete constraints
- contradictory legacy language
- duplicate instructions
- overgrown example blocks
- unused placeholders

Do not measure progress only by what you added.

## Compaction checklist

Run this checklist before finalizing:

1. Can I point to one owner for each major behavior rule?
2. Can I remove any sentence without changing behavior?
3. Are there examples that are only restating the instructions?
4. Are instructions and evidence in clearly separate blocks?
5. For long context, is the actual query in a terminal section?
6. Are tags or headings earning their token cost?
7. Did the compacted version keep or improve the eval score?

If the answer to 7 is no, restore only the smallest amount of removed text needed to recover behavior.

## Symptom to likely cause

| Symptom | Likely cause | Typical fix |
|---------|--------------|-------------|
| Prompt feels long but still unstable | duplicated or contradictory rules | collapse to one authoritative owner per rule |
| Output style varies despite many reminders | format rules spread across layers | move them into one explicit output contract plus one strong example if needed |
| Model confuses instructions with source docs | policy and evidence mixed together | split sections and label them clearly |
| Long-context performance is poor | query placement and context order are weak | move long evidence earlier and the final ask to the end |
| Cost rises with no quality gain | too many examples or decorative markers | prune examples and remove low-value tags |
