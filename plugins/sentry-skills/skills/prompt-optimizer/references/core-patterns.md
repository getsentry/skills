# Core Patterns

Use this file when creating a new prompt or restructuring a weak one.

## When markers help

Use markers when the prompt mixes different content types:

- instructions
- retrieved context
- tool rules
- examples
- input payloads
- output schema

Good section names are concrete and stable:

- `<role>`
- `<goal>`
- `<context>`
- `<tools>`
- `<workflow>`
- `<constraints>`
- `<output_format>`

Do not add markup around every sentence. Markers are useful when they carve the prompt into distinct blocks, not when they add noise.

If the target stack or model family responds better to plain markdown, use headings and bullets instead of XML-style tags. The structure matters more than the syntax.

## Layer the prompt correctly

Keep these layers separate:

1. Stable behavior:
- role
- defaults
- safety boundaries
- tool-use policy
- output contract

2. Task-local context:
- user request
- retrieved documents
- current state
- dynamic variables

3. Examples:
- few-shot examples
- failure replays
- structured output demonstrations

If a rule should apply across tasks, keep it out of the user payload and put it in the stable layer.
Keep one authoritative owner for each major behavior rule instead of repeating it across all layers.

Collapse common duplicates such as:

- verbosity rules
- "check before guessing"
- ask-first versus act-now behavior
- output format rules
- refusal and escalation boundaries

When prompts are long, separate policy from evidence explicitly:

- instructions in one block
- retrieved documents in another
- examples in another
- tool rules and schemas in their own labeled sections

For long-context prompts, place long evidence before the final query and keep the actual ask in a terminal section.
Do not cargo-cult this ordering into short prompts that do not need it.

## Portable agent prompt skeleton

Use this as a starting point and adapt it:

```text
<role>
You are [agent role].
</role>

<goal>
Primary objective:
Secondary objective:
Non-goals:
</goal>

<context>
Available inputs:
Available files or documents:
Known constraints:
</context>

<tools>
Available tools:
When to use them:
When to avoid them:
</tools>

<workflow>
1. Clarify only if required.
2. Gather missing facts with tools instead of guessing.
3. Execute the task.
4. Validate the result.
5. Report outcome and remaining risks.
</workflow>

<constraints>
Hard constraints:
Soft preferences:
Escalation boundaries:
</constraints>

<output_format>
Progress updates:
Final response sections:
</output_format>
```

Use markdown headings instead of tags if that fits the target stack better.

## High-value prompt moves

- Tell the agent what to do by default.
- State when it should ask clarifying questions and when it should infer.
- State when it should use tools and what evidence it should gather before acting.
- State what counts as completion.
- State what counts as refusal, escalation, or defer.
- Separate hard constraints from preferences.
- Keep progress-update style explicit if the user should see it.
- Use the shortest wording that preserves the intended behavioral constraint.
- Remove persona, motivation, or reminder text that does not change measured behavior.

## Examples

Examples help most when they teach one of these:

- output format
- edge-case handling
- tool-use triggers
- the difference between "ask first" and "act now"

Examples hurt when they:

- contradict the instructions
- overfit the model to one narrow phrasing
- use inconsistent structure
- show anti-patterns without a corrected version
- restate rules that are already clear in the instructions
- remain in the prompt after they stop improving evals

## Symptom to fix mapping

| Symptom | Likely fix |
|---------|------------|
| Output format drifts | Add a stronger output contract or a format example |
| The agent guesses instead of checking | Add tool-use criteria and "gather facts before acting" language |
| The agent stays too passive | Add explicit default behavior and action bias |
| The agent is too aggressive | Add ask-first and escalation boundaries |
| Responses are verbose | Tighten output sections and verbosity constraints |
| The prompt is long but still unstable | Remove duplicate rules and choose one owner per behavior |
| Long context causes confusion | Separate context from instructions and move the query to a clear terminal section |
| The prompt works on one provider but not another | Split base prompt from provider-specific adapter notes |
