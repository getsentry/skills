---
name: prompt-optimizer
description: Create, optimize, and iteratively refine agent prompts and system prompts. Use when asked to "improve a prompt", "optimize a system prompt", "rewrite an agent prompt", "tune prompt wording", "make this prompt more reliable", "adapt a prompt for OpenAI, Claude, or Gemini", "design tool policy for an agent prompt", "how should I expose tools in a prompt", or "how should I disclose skills in an agent". Handles model-specific prompt guidance, prompt markers/tags, tool disclosure and tool-call narration, skill disclosure and routing, layered platform/deployer prompts, eval design, and meta optimization loops.
---

# Prompt Optimizer

Optimize prompts for agents, system/developer instructions, and reusable prompt templates.
Treat prompt work as an eval-driven workflow, not wordsmithing.

Load only the references you need:

| Task | Read |
|------|------|
| Create a new agent prompt | `references/core-patterns.md`, `references/model-family-notes.md`, `references/transformed-examples.md` |
| Refine an existing prompt | `references/meta-optimization-loop.md`, `references/core-patterns.md`, `references/model-family-notes.md`, `references/transformed-examples.md` |
| Shape tool disclosure, tool policy, or tool-call narration | `references/tools.md`, `references/core-patterns.md` |
| Shape skill disclosure, invocation, or routing between skills | `references/skills.md`, `references/core-patterns.md` |
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

Read `references/core-patterns.md`. When the prompt surface includes tools or a skill layer, also read `references/tools.md` or `references/skills.md`. Reach for `references/transformed-examples.md` when the task is under-specified or the first draft is weak.

Apply, in order:

1. Layer the prompt — stable behavior in `system`/`developer`, task-local context in templated user sections, examples as a third layer.
2. Place directives in canonical rules sections (`<behavior>`, `<tool_policy>`, `<constraints>`, `<workflow>`), not buried inside descriptive markers.
3. Keep one authoritative owner per rule. Collapse duplicates.
4. Cross-check the symptom-to-fix table in `core-patterns.md` before adding new instructions.

## Step 4: Run the meta optimization loop

Read `references/meta-optimization-loop.md`.

Baseline on a representative slice → cluster failures → write critiques as concrete edits → generate a small candidate beam (minimal-diff repair, structure-first rewrite, example-or-tool-rule variant) → compare on the same slice → keep the best → validate on a holdout → stop when scores plateau, edits oscillate, or cost rises without gain.

Record what you remove as well as what you add.

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

## Output standard

The final prompt package should be reusable by another engineer without rediscovering:

- what the prompt is for
- which model family it targets
- how success is measured
- what changed during optimization
- which risks remain open
