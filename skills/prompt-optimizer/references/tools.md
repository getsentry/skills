# Tools

Use this file when designing how an agent prompt refers to tools, when to suppress tool enumeration, and how to write tool policy. Covers what belongs in the prompt vs. the provider-native tool array, progressive and deferred disclosure, tool-count ceilings, and tool-call narration.

## Contents

- Where tools are actually disclosed
- What the prompt should say about tools
- Progressive and deferred disclosure
- Tool count and context budget
- Tool-call narration
- Parallel and sequential tool calls
- Tool-call error policy
- Skill-bundled and runtime-gated tools
- Anti-patterns

## Where tools are actually disclosed

Modern provider APIs (Anthropic Messages, OpenAI Responses and Chat Completions, Gemini function calling, Bedrock Converse) transmit tool schemas to the model via a native `tools` parameter on the request. Each entry carries the tool's name, description, and a JSON Schema for arguments. The provider presents these to the model as first-class callable functions; no system-prompt text is needed to make a tool visible.

On Anthropic, the API assembles a system prompt that automatically injects the definitions from `tools` alongside the caller's system text. Pi-agent-core, Codex CLI, and other well-tuned harnesses pass tools natively and leave schema restatement out of the prompt body.

Two consequences:

1. Re-listing tool names or descriptions inside the system prompt is redundant and costs tokens every turn.
2. The `description` field in the native schema is the primary place to shape when the model reaches for each tool. Prose about a tool in the system prompt is a second-order effect on top of the description.

Exceptions where prompt-level tool mention is warranted:

- **Deferred tools**. The tool name appears in a short index (often a system reminder), but the schema loads only when the model calls a meta-tool such as `ToolSearch`. The prompt must surface both the fact that deferred tools exist and the fetch mechanism; otherwise the model will never call it.
- **Just-activated tools**. When the native tool array changes mid-session (skill load, auth completion), a one-line "these tools are now registered" reminder may be justified. Skip it when the change is already obvious from conversation history.

## What the prompt should say about tools

Reserve prompt-level text for behavior the tool `description` cannot encode:

- Ordering and preconditions: "Run `searchIndex` before `editFile`."
- Cross-tool policy: "Gather evidence with tools before answering factual questions."
- Negative rules: "Never call side-effecting tools when the user asked only for analysis."
- Escalation: "When a destructive tool returns an ambiguous result, ask before retrying."

Do not put in the prompt:

- Tool names, signatures, or argument schemas.
- Generic "use tools when appropriate" without a real trigger.
- "When to use tool X" — that belongs in tool X's `description`.

If the same rule applies to every tool, write it once as a general behavior rule. If the rule is tool-specific, push it into the tool's native `description`.

## Progressive and deferred disclosure

When a runtime can expose more than ~20 tools, per-turn token cost and routing reliability both degrade. Two patterns scale better:

1. **Lazy schema via meta-tool.** Tool names appear in a short index (often delivered as a system reminder), but full schemas load only on request. Claude Code's `ToolSearch` is the reference implementation: a deferred tool is visible by name, and calling the meta-tool fetches its schema as a callable tool for the rest of the session. The prompt must explicitly say that deferred tools exist and how to fetch them.

2. **Capability negotiation.** MCP clients list available tools at connection time via `tools/list`, and servers advertise changes via `notifications/tools/list_changed`. The harness can filter which tools are exposed per turn (by skill, scope, or auth state). The prompt does not need to re-describe the inventory.

Do not combine both mechanisms for the same tool surface in one prompt. Pick one model and state it. Progressive disclosure with deferred fetch only helps when the model knows to fetch; if the prompt implies all tools are already loaded, the model will never call the meta-tool.

## Tool count and context budget

No provider publishes a hard ceiling; plan for your model family and measure. Rough shape:

- ≤10 tools: routing is reliable without extra structure.
- 10–20 tools: ensure descriptions are high-signal (not just names) and disambiguate overlap.
- Above ~20: expect routing noise. Use deferred disclosure, scope tools per skill, or gate by auth state.
- Per-tool schema overhead: ~100 tokens. 100 tools eagerly disclosed ≈ ~10k tokens of prompt budget repeated every turn.

When a user reports "the model picked the wrong tool," the fix is almost always in the description of the intended tool and the competitors, not in the system prompt.

## Tool-call narration

Streaming, assistant-status, and Slack-style UIs surface tool-call events as UI. Narration in the assistant's text reply restates what the UI already shows and pushes the first useful message later. Even without streaming UI, narration inflates output tokens and hurts judged output quality.

Write these rules in the canonical behavior section:

- Do not narrate in advance ("Let me check...", "Fetching...", "Looking this up...").
- Do not restate what the tool is about to do.
- Send an interim reply only when blocked or waiting on user input.

Placement matters. A "no narration" rule buried inside a descriptive marker (`<context>`, `<turn-state>`, `<environment>`) is reliably weaker than the same rule in `<behavior>` or `<tool_policy>`. See `core-patterns.md` / "Where rules live."

## Parallel and sequential tool calls

Parallel tool use is a provider capability, not a prompt feature. Anthropic defaults to parallel and exposes `disable_parallel_tool_use`; OpenAI auto-parallels unless `parallel_tool_calls: false`; LangGraph's `ToolNode` runs concurrent calls. The prompt cannot enable or disable parallelism; it can only influence choice.

When the tool flow is order-dependent, say so explicitly:

- "Run `readFile` for every referenced path before writing `edit`."
- "Do not call `postMessage` until the analysis tools have resolved."

When parallelism is safe and desired, do not write any rule about it. Providers default to parallel; silent defaults are cheaper than restating them.

## Tool-call error policy

Tool errors fall into a small set, each handled in a different place:

- **Transient** (network, rate limit, timeout) — the runtime retries; the prompt should not tell the model to retry.
- **Auth / permission** — usually a pause-and-resume handled by the runtime; the prompt may state how the model should behave after auth completes.
- **Malformed input** — the model produced bad arguments; it should re-attempt with corrected input, not narrate the retry.
- **Real failure** — external state disallows the action; the model should report plainly and not pretend success.

Write one cross-cutting rule that protects against hallucinated outcomes:

> Do not claim a tool call succeeded unless the tool returned a success result this turn. When it did and the tool returned a link or identifier, include it.

This is more robust than enumerating error codes. It also doubles as a honesty rule around attachments, canvases, and channel posts.

## Skill-bundled and runtime-gated tools

Skills often bundle their own tools (MCP sub-servers, skill-specific shell commands, provider SDKs). Two clarity requirements:

1. **Registration timing.** Skill-bundled tools should reach the native tool array only after the skill loads. Pre-loading every skill's tools inflates the tool inventory and breaks whatever routing ceiling you were planning for.
2. **Namespacing.** Skill-bundled tools should be namespaced (e.g., `mcp__sentry__search_issues`) so the model can distinguish skill-tools from platform-tools at a glance.

For broader guidance on how skills disclose themselves and persist across resumable turns, see `references/skills.md`.

## Anti-patterns

| Symptom | Fix |
|---------|-----|
| System prompt re-lists tool names and descriptions that already appear in the native tool array | Delete the listing; promote any tool-selection hints into the tool's `description` field |
| "Use tool X when Y" appears in both prompt and tool description | Keep the rule in the `description`; remove it from the prompt |
| Prompt has a rule about a specific tool that no longer exists | Delete it; tool-specific rules drift silently when tools are renamed |
| Model narrates tool calls despite a "no narration" rule | Check placement — the rule must live in the rules section, not inside a context or state block |
| Model never discovers a deferred tool | The prompt is missing the "deferred tools exist; fetch via `<meta-tool>`" disclosure |
| 50+ tools, slow or confused routing | Scope tools per skill, per auth state, or gate behind a meta-tool; do not flatten everything into one array |
| Assistant claims an attachment or canvas succeeded when the tool failed | Add the cross-cutting success-only rule under Tool-call error policy above |
| Tool flow needs strict ordering but runs in parallel | State the ordering explicitly in the rules section; do not rely on provider defaults |
