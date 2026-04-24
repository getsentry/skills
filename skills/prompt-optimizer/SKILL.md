---
name: prompt-optimizer
description: Create, optimize, and iteratively refine agent prompts and system prompts. Use when asked to "improve a prompt", "optimize a system prompt", "rewrite an agent prompt", "tune prompt wording", "make this prompt more reliable", or "adapt a prompt for OpenAI, Claude, or Gemini". Handles model-specific prompt guidance, prompt markers/tags, eval design, and meta optimization loops for new and existing prompts.
---

# Prompt Optimizer

Optimize prompts for agents, system/developer instructions, and reusable prompt templates.
Treat prompt work as an eval-driven workflow, not wordsmithing.

Load only the references you need:

| Task | Read |
|------|------|
| Create a new agent prompt | `references/core-patterns.md`, `references/model-family-notes.md`, `references/transformed-examples.md` |
| Refine an existing prompt | `references/meta-optimization-loop.md`, `references/core-patterns.md`, `references/model-family-notes.md`, `references/transformed-examples.md` |
| Port a prompt between model families | `references/model-family-notes.md`, `references/core-patterns.md` |
| Diagnose repeated prompt failures | `references/meta-optimization-loop.md`, `references/core-patterns.md` |
| Explain the provenance behind this workflow | `SOURCES.md` |

## Step 1: Define the prompt contract

1. Determine whether the task is:
- creating a new prompt
- refining an existing prompt
- porting a prompt between model families
- debugging prompt failures

2. Capture the contract before rewriting anything:
- target model family and snapshot if known
- prompt surface: `system`, `developer`, `user`, tool descriptions, examples, schemas
- task objective and non-goals
- inputs, context, and tools available to the agent
- required output shape
- success criteria
- known failures
- hard constraints: latency, verbosity, safety, budget, tool use, style

3. If the user does not provide success criteria or examples, build a small eval set before editing the prompt.

4. If the real bottleneck is model choice, missing retrieval, weak tool schemas, or a missing eval harness, say so. Do not keep rewriting prompt text when the failure is elsewhere.

## Step 2: Choose the model strategy

Read `references/model-family-notes.md`.

1. If the target family is known, optimize specifically for that family.
2. If the target family is unknown, write:
- a portable base prompt
- short adapter notes for the likely target families
3. Do not pretend one prompt is universal when the behavior clearly depends on model family.
4. Pin model snapshots when the surrounding system supports it.

## Step 3: Shape the prompt deliberately

Read `references/core-patterns.md`.

1. Separate durable behavior from task-local context:
- stable policy and behavioral defaults belong in `system` or `developer`
- variable inputs, retrieved context, and task instances belong in templated user-facing sections
- when the system prompt is assembled at runtime from a platform layer and a deployer-authored persona layer (e.g., `SOUL.md`, `CLAUDE.md`, `AGENTS.md`), see "Layered prompts with multiple owners" in `references/core-patterns.md` — platform behavior rules must not depend on what the deployer layer contains

2. Keep one authoritative instruction per behavior:
- if a rule appears in more than one layer, choose one owner for it
- stable cross-task rules belong in `system` or `developer`
- examples should teach format, edge-case handling, or tool behavior, not restate the whole policy
- user payloads should carry task-local facts, not durable policy

3. Use markers only when they reduce ambiguity:
- use markdown headings or XML-style tags to separate instructions, context, examples, tool rules, and output contracts
- keep tag names descriptive and consistent
- do not wrap every sentence in markup

4. Make the prompt easy to execute:
- put one high-value behavior per bullet or line when the task is fragile
- prefer positive instructions over "do not do X" lists
- place tool-use rules, escalation boundaries, and stop conditions in explicit sections
- keep persona light unless it changes behavior in a useful way
- use the shortest wording that preserves the intended behavioral constraint
- cut motivational filler, repeated reminders, and examples that do not improve evals
- for long-context prompts, place evidence before the final query and keep the actual ask in a clear terminal section
- keep instructions, evidence, and schemas in distinct blocks so the model does not have to infer what is policy versus data

5. Treat examples as first-class prompt assets:
- start simple before adding examples
- add examples only when they improve format control, edge-case handling, or tool behavior
- keep examples structurally consistent
- prefer positive demonstrations over anti-pattern-only demonstrations

## Step 4: Run the meta optimization loop

Read `references/meta-optimization-loop.md`.

1. Start with the current prompt or a simple first draft.
2. Score it on a representative slice:
- at least one happy-path case
- at least one failure replay
- at least one ambiguous case
- at least one edge case
- at least one "should refuse", "should ask", or "should defer" case when relevant

3. Turn failures into explicit criticisms:
- identify what the prompt under-specified, over-specified, or contradicted
- write critiques as actionable edits, not vague complaints

4. Generate a small beam of candidate prompts:
- one minimal-diff repair
- one structure-first rewrite
- one example- or tool-rule-centered variant when that is the likely bottleneck
- one provider-specific adapter when cross-model behavior is the issue

5. Compare candidates on the same eval slice.
6. Keep the best candidate and log what changed and why.
7. Preserve the evidence for each round:
- prompt version
- eval case
- model output
- failure reason
- relevant scores

8. Test the winner on a holdout slice before finalizing.
9. Stop when scores plateau, edits oscillate, cost rises without quality gain, or the remaining issue is outside prompt control.

Keep edits minimal and causal. Record what you removed as well as what you added. If you change everything at once, you learn nothing about what actually helped.

## Step 5: Produce a reusable deliverable

Return:

1. `Target`
2. `Success Criteria`
3. `Optimized Prompt`
4. `Adapter Notes`
5. `Eval Set`
6. `Optimization Log`
7. `Residual Risks`

If the user supplied an existing prompt, include a concise diff-style explanation of the biggest behavioral changes.

## Step 6: Guard against common failure modes

Read `references/transformed-examples.md` when the task is ambiguous or the first draft is weak.

Do not:

- optimize wording before defining the eval target
- mix instructions, examples, and raw context without boundaries
- keep the same rule in multiple layers unless there is a proven reason
- let stable rules drift into the user payload just because the current prompt template makes it convenient
- ask reasoning models to reveal chain-of-thought just because the task is hard
- keep contradictory legacy instructions in the same prompt
- overfit to one or two examples
- keep examples that do not improve measured behavior
- solve tool-use failures only in the system prompt when the real problem is the tool description or schema
- add markers everywhere and mistake structure for clarity
- use a bloated persona as a substitute for concrete behavior rules

## Output standard

The final prompt package should be reusable by another engineer without rediscovering:

- what the prompt is for
- which model family it targets
- how success is measured
- what changed during optimization
- which risks remain open
