# Core Patterns

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

| Block type | Examples | Content |
|------------|----------|---------|
| descriptive | `<context>`, `<state>`, `<environment>` | facts, inputs, current state |
| rules | `<behavior>`, `<constraints>`, `<tool_policy>`, `<workflow>` | directives |

Rules:

- Keep descriptive markers descriptive.
- Put directives in canonical rules sections.
- For state-conditional rules, write the directive in a rules section and reference the state by name.

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
- tool policy (when/why/whether) in its own labeled section; tool schemas stay in the provider-native tools parameter

For long-context prompts, place long evidence before the final query and keep the actual ask in a terminal section.
Do not cargo-cult this ordering into short prompts that do not need it.

### Layered prompts with multiple owners

When a runtime concatenates prompt layers from different owners:

| Layer | Owns | Must not own |
|-------|------|--------------|
| platform | tool policy, output contract, safety, escalation, workflow | voice-only identity |
| deployer/persona | voice, tone, domain framing, sparse identity files | load-bearing behavior |
| user payload | task facts, variables, current request | durable policy |

Rules:

- Platform behavior must work when `AGENTS.md`, `CLAUDE.md`, or persona files are empty or customized.
- Do not delete platform rules because a deployer layer "probably covers it".
- Put load-bearing rules in the highest stable owner.

## External file inventories

Use path inventories when prompts depend on repo docs, specs, or policies.

```text
<external_files>
- `AGENTS.md` - repo agent rules; loaded
- `docs/api.md` - API contract; reference before endpoint changes
- `SECURITY.md` - security policy; reference for disclosure or auth changes
</external_files>
```

Rules:

- Enumerate exact repo-relative paths.
- Mark each file as `loaded`, `referenced`, or `out of scope`.
- Paste only excerpts needed for the prompt or eval case.
- Prefer `docs/api.md` over "read the docs".
- Keep stable docs outside the prompt when the runtime can retrieve files.

## Tool policy placement

- Tool schemas belong in provider-native tools.
- Prompt text carries tool policy: when, why, whether, evidence, and stop conditions.
- Naming a tool in policy is fine; re-enumerating schemas is not.

## High-value prompt moves

- Tell the agent what to do by default.
- State when it should ask clarifying questions and when it should infer.
- State when it should use tools and what evidence it should gather before acting.
- State what counts as completion.
- State what counts as refusal, escalation, or defer.
- Enumerate external files by path when specs, docs, or policies matter.
- Separate hard constraints from preferences.
- Keep progress-update style explicit if the user should see it.
- Use the shortest wording that preserves the intended behavioral constraint.
- Remove persona, motivation, or reminder text that does not change measured behavior.
- Place directives in canonical rules sections (`<behavior>`, `<constraints>`, `<tool_policy>`, `<workflow>`), not buried inside descriptive markers like `<context>`, `<state>`, or `<turn-state>`.

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
