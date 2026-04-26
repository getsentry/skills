# Reference Architecture

Use this guide before adding bulk instructions to `SKILL.md` or creating bundled files.

Good reference files answer a concrete lookup need: "I need to decide X", "I need to execute Y", or "I need to diagnose Z". Avoid files that are only buckets of related facts.

## Contents

- Placement Rule
- Design The Lookup First
- Reference Types
- Put In SKILL.md
- Put In References
- Put In SPEC.md
- Split Heuristics
- Naming Pattern
- Progressive Disclosure Checks

## Placement Rule

`SKILL.md` is the router. It should tell the agent what path to take, when to load a reference, what outputs are required, and what gates must pass before completion.

Reference files are lookup modules. They should be opened only when the current task needs that module's decision logic, procedure, facts, examples, or diagnostic matrix.

`SPEC.md` is the maintenance contract. It describes intent, scope, source/evidence model, evaluation expectations, known limitations, and update rules for future skill authors.

## Design The Lookup First

Before creating a reference file, write the sentence that would make an agent open it:

- "I need to classify the requested skill, so read `references/mode-selection.md`."
- "I need to choose the right output contract, so read `references/output-patterns.md`."
- "I need to diagnose why the generated skill failed validation, so read `references/validation-failures.md`."
- "I need examples of before/after prompt transformations, so read `references/transformed-examples.md`."

If the sentence sounds like "I need common use cases" or "I need context", the file is probably too vague. Reframe it around the decision or action:

- "I need to decide whether this API behavior needs a workaround."
- "I need to select the safest integration pattern for streaming responses."
- "I need to map a user request to the right workflow path."

## Reference Types

Use these types as a starting point, adapted from task/concept/reference/troubleshooting documentation patterns:

| Need | Use This Shape | Contains | Avoid |
|------|----------------|----------|-------|
| Decide which path to take | Decision guide | criteria, branch table, examples, hard stops | broad background |
| Perform a repeatable procedure | Task guide | ordered steps, preconditions, validation, failure handling | conceptual essays |
| Look up exact facts | Reference table | API fields, commands, schemas, options, limits | narrative explanation |
| Understand a concept | Concept note | definitions, mental model, why it matters, boundaries | step-by-step workflows |
| Diagnose a failure | Troubleshooting matrix | symptom, likely cause, remedy, escalation | generic "known issues" lists |
| Imitate quality | Example set | representative inputs/outputs, anti-patterns, corrected versions | isolated toy snippets |
| Judge completeness | Evaluation rubric | pass/fail criteria, scoring, holdout prompts, acceptance gates | implementation details |

## Put In SKILL.md

- Required first steps and branch points.
- A compact reference map keyed by task need.
- Non-negotiable constraints that apply to every run.
- Output sections and completion gates.
- Short examples only when they prevent frequent misexecution.
- Script names, arguments, and expected output shape when scripts are part of the workflow.

## Put In References

- Decision guides that are too detailed for the main workflow.
- Task guides for conditional procedures.
- Reference tables for exact lookup data.
- Troubleshooting matrices with symptom/cause/remedy structure.
- Example sets large enough to crowd `SKILL.md`.
- Evaluation rubrics and holdout prompts.

## Put In SPEC.md

- Why the skill exists and what problem it solves.
- In-scope and out-of-scope behavior.
- Expected users and trigger contexts.
- Source categories used to create or improve the skill.
- Evidence storage policy for positive and negative examples.
- Evaluation expectations and acceptance gates.
- Known limitations and maintenance rules.

Do not put runtime step-by-step instructions in `SPEC.md`; keep those in `SKILL.md`.
Do not put full source inventories in `SPEC.md`; keep those in `SOURCES.md`.

## Split Heuristics

Create a new reference file when any of these are true:

- The content is only needed after a specific branch decision.
- The file has a clear "open when..." sentence.
- The content has one dominant type: decision, task, fact lookup, concept, troubleshooting, examples, or evaluation.
- The section would make `SKILL.md` harder to scan as a router.
- The same file would otherwise mix procedures, facts, examples, and evaluation results.
- The file is approaching 100 lines and contains multiple lookup needs.

Keep content in `SKILL.md` when all of these are true:

- Every invocation needs it.
- It is short enough to remain visible in one read.
- Moving it out would force the agent to open another file before doing basic work.

## Naming Pattern

Name references for the action or question they answer:

- `references/mode-selection.md`
- `references/source-discovery.md`
- `references/validation-failures.md`
- `references/output-contracts.md`
- `references/streaming-integration-patterns.md`
- `references/transformed-examples.md`
- `references/evaluation-rubric.md`

Avoid bucket names that do not explain why the agent should open them:

- `references/notes.md`
- `references/everything.md`
- `references/context.md`
- `references/research.md`
- `references/common-use-cases.md`

For references over 100 lines, add a `## Contents` section near the top.
For very large source-derived material, split by task or lookup path instead of adding a table of contents to an overloaded file.

## Progressive Disclosure Checks

Before finalizing, verify:

1. Every reference has an "open when..." reason in `SKILL.md`, `SPEC.md`, or the adjacent workflow reference.
2. Every reference mostly matches one type from the reference type table.
3. The agent can decide whether to open each reference from its filename and one-line description.
4. No required instruction is hidden only inside a reference that may not be loaded.
5. No reference file has become a second `SKILL.md` with broad orchestration plus unrelated details.
6. Repeatedly accessed reference content is promoted to `SKILL.md` only if it is small and truly universal.
