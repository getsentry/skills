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
- `<tool_policy>`
- `<workflow>`
- `<constraints>`
- `<output_format>`

Do not add markup around every sentence. Markers are useful when they carve the prompt into distinct blocks, not when they add noise.

If the target stack or model family responds better to plain markdown, use headings and bullets instead of XML-style tags. The structure matters more than the syntax.

### Where rules live

Markers signal to the model what kind of content a block carries. Descriptive
or state markers (`<context>`, `<state>`, `<turn-state>`, `<environment>`,
`<artifact-state>`) read as facts about the situation — data, not policy.
Canonical rules markers (`<behavior>`, `<constraints>`, `<tool_policy>`,
`<workflow>`) read as directives the model should follow.

A directive buried in a descriptive block can underperform the same directive
placed in a rules block, especially for state-conditional rules. Observed in
the field: a resume-notice instruction placed inside `<turn-state>resumed</turn-state>`
scored 0.5 on the relevant eval; the identical sentence moved into
`<behavior>` passed at ≥0.75 with no other change.

Rules of thumb:

- keep descriptive markers descriptive — put facts about the situation there,
  not directives
- directives live in a canonical rules section
- for state-conditional rules, phrase them in the rules section and reference
  the state by name: "When `<turn-state>` is `resumed`, post a brief
  continuation notice, then answer."

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

### Layered prompts with multiple owners

The layers above assume a single author owns the whole system prompt. Many
runtimes concatenate the system prompt from multiple layers with different
owners at request time:

- a **platform layer** owned by the product or framework team (harness rules,
  tool-use policy, output contract, safety boundaries)
- a **deployer or persona layer** authored by the downstream user or customer
  (voice, tone, identity files such as `SOUL.md`, `CLAUDE.md`, `AGENTS.md`)

When this is the case, treat the deployer layer as **voice-only**:

- every platform behavior rule — evidence gathering, tool-use policy, narration
  rules, output contract, escalation boundaries — must live in the
  platform-owned layer and must still fire if the deployer layer is empty,
  five lines of voice, or customized in unexpected ways
- do not delete a platform bullet on the assumption that a persona file
  "probably covers it"; deployers ship sparse persona files in practice
- if a rule is load-bearing, it belongs in the platform layer by default;
  the deployer layer gets voice and domain framing, not policy

Hermes Agent, OpenClaw, and similar SOUL.md-style frameworks use this split
explicitly: platform behavior is code-level, SOUL.md carries identity and
tone, and the platform falls back to a built-in default identity if SOUL.md
is absent or sparse. Mirror that invariant whenever a prompt is assembled
from more than one authorship layer.

## Portable agent prompt skeleton

Use this as a starting point and adapt it.

Tool schemas are disclosed to the model by the provider-native tools parameter
(Anthropic `tools`, OpenAI `tools`, Gemini `tools`). On Anthropic this is
explicit — the API constructs a special system prompt that injects the tool
definitions from the `tools` parameter alongside the user-authored system
prompt. Well-tuned harnesses (Codex CLI, pi-agent-core) pass tools natively
and keep the prompt text free of schema restatements.

The prompt text should carry tool *policy* — when to call tools, when to avoid
them, what evidence to gather before acting — not a restated list of tool
names or argument schemas. Naming a specific tool in a policy rule ("prefer
`Read` over a `Bash` cat") is fine; re-enumerating the tool inventory or its
schemas is not.

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

<tool_policy>
When to use tools:
When to avoid tools:
Evidence to gather before acting:
</tool_policy>

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
- Place directives in canonical rules sections (`<behavior>`, `<constraints>`, `<tool_policy>`, `<workflow>`), not buried inside descriptive markers like `<context>`, `<state>`, or `<turn-state>`.

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
