# Sources

This file tracks the material synthesized into `prompt-optimizer`.

## Selected profile

- `skills/skill-writer/references/examples/workflow-process-skill.md`

Why: this skill is a repeatable prompt-optimization workflow with explicit preconditions, ordered execution, validation, and failure handling.

## Current source inventory

| Source | Type | Trust tier | Retrieved | Confidence | Contribution | Usage constraints | Notes |
|---|---|---|---|---|---|---|---|
| `skills/skill-writer/SKILL.md` | local canonical | canonical | 2026-04-19 | high | Baseline synthesis, authoring, and registration workflow | local repository authority | Primary workflow source |
| `skills/skill-writer/references/*.md` | local canonical | canonical | 2026-04-19 | high | Structure, depth gates, transformed example requirements, validation expectations | local repository authority | Includes authoring and workflow patterns |
| `README.md` | repo convention | canonical | 2026-04-18 | high | Skill template, naming, registration conventions | repository-local policy | Canonical public skill inventory |
| `CONTRIBUTING.md` | repo convention | canonical | 2026-04-18 | high | Local testing and registration checklist | repository-local policy | Confirms registration steps |
| `AGENTS.md` | repo convention | canonical | 2026-04-18 | high | Mandatory use of `skill-writer`, registration checklist, portability conventions | repository-local policy | Highest-priority local instruction source |
| `https://developers.openai.com/api/docs/guides/reasoning-best-practices` | official docs | canonical | 2026-04-18 | high | Reasoning-model prompting differences, simplicity, delimiters, no explicit CoT | verify product syntax if exact API behavior matters | Used for OpenAI family notes |
| `https://developers.openai.com/api/docs/guides/prompt-optimizer` | official docs | canonical | 2026-04-18 | high | Evals, graders, annotations, critique-driven prompt iteration | verify current product surface if depending on dashboard workflow | Supports eval-first workflow |
| `https://developers.openai.com/api/docs/guides/prompting` | official docs | canonical | 2026-04-18 | high | Prompt versioning, reuse, prompt objects, eval linkage | product-specific features may evolve | Supports reusable prompt packaging |
| `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview` | official docs | canonical | 2026-04-18 | high | Success-criteria-first prompting and reminder that not every failure is a prompt problem | product syntax may evolve | Supports precondition checks |
| `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices` | official docs | canonical | 2026-04-18 | high | XML tags, role prompting, examples, long-context ordering, output control | provider-specific behavior | Used for Claude family notes and marker guidance |
| `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools` | official docs | canonical | 2026-04-18 | medium | Prompt improver inputs: prompt, failure feedback, ideal examples | console workflow may change | Reinforces critique-plus-example loop |
| `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices` | official docs | canonical | 2026-04-18 | high | Concision as a context-budget discipline; "context window is a public good" framing | skill-oriented source, generalized carefully to prompt authoring | Supports prompt compaction guidance |
| `https://ai.google.dev/gemini-api/docs/prompting-strategies` | official docs | canonical | 2026-04-18 | high | Clear instructions, example consistency, positive patterns, prompt iteration | provider-specific behavior | Used for Gemini family notes |
| `https://ai.google.dev/gemini-api/docs/text-generation` | official docs | canonical | 2026-04-18 | high | System instruction surface for Gemini | product syntax may evolve | Confirms system-instruction layer |
| `https://ai.google.dev/gemini-api/docs/thinking` | official docs | canonical | 2026-04-18 | high | Dynamic thinking defaults and controllable reasoning settings | product syntax may evolve | Used for Gemini adapter notes |
| `https://ai.google.dev/gemini-api/docs/long-context` | official docs | canonical | 2026-04-18 | high | Many-shot in-context learning and long-context prompt placement notes | provider-specific behavior | Supports many-shot adapter note |
| `https://arxiv.org/abs/2309.03409` | research paper | canonical | 2026-04-18 | high | OPRO candidate search loop and score-driven prompt optimization | research result, not product guarantee | Supports candidate beam design |
| `https://arxiv.org/abs/2305.03495` | research paper | canonical | 2026-04-18 | high | Textual gradients, minibatch critiques, beam search | research result, not product guarantee | Supports critique-driven edits |
| `https://arxiv.org/abs/2303.17651` | research paper | canonical | 2026-04-18 | high | FEEDBACK -> REFINE loop and test-time improvement | research result, not product guarantee | Supports iterative refinement loop |
| `https://arxiv.org/abs/2303.11366` | research paper | canonical | 2026-04-18 | high | Reflection memory across trials for agents | research result, not product guarantee | Supports optimization log and reflection memory |
| `https://dspy.ai/` | official project docs | canonical | 2026-04-18 | high | Current prompt optimizers such as GEPA and MIPROv2; score-driven instruction search; composable optimization | framework-specific guidance | Supports modern optimizer framing |
| `https://platform.claude.com/docs/en/api/messages` | official docs | canonical | 2026-04-24 | high | Native `tools` parameter mechanics on Anthropic Messages; system-prompt auto-injection of tool definitions | provider-specific | Used in `tools.md` |
| `https://modelcontextprotocol.io/specification/2025-11-25` | standards spec | canonical | 2026-04-24 | high | MCP tool/capability/prompt disclosure; `tools/list` and `tools/list_changed` notifications | spec version-sensitive | Used in `tools.md` and `skills.md` for capability-negotiation pattern |
| `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview` | official docs | canonical | 2026-04-24 | high | Agent Skills primitive, `SKILL.md` format, frontmatter fields, progressive disclosure | product surface may evolve | Used in `skills.md` |
| `https://agentskills.io/specification` | standards spec | canonical | 2026-04-24 | high | Cross-framework SKILL.md specification, frontmatter schema, portability contract | early-stage spec | Used in `skills.md` |
| `https://code.claude.com/docs/en/skills` | official docs | canonical | 2026-04-24 | medium | Claude Code skill-tool pattern and deferred tool mechanism (`ToolSearch`) | product surface may evolve | Used in `tools.md` and `skills.md` for deferred-disclosure pattern |
| `https://learn.microsoft.com/en-us/semantic-kernel/concepts/plugins/` | official docs | canonical | 2026-04-24 | medium | Plugin/skill primitive; function-calling-native disclosure; plugin-per-folder structure | provider-specific | Used in `skills.md` |
| `https://developers.openai.com/docs/guides/function-calling` | official docs | canonical | 2026-04-24 | high | OpenAI native tool-array disclosure, parallel tool calls, tool search for large suites | product surface may evolve | Used in `tools.md` |
| `https://ai.google.dev/docs/function_calling` | official docs | canonical | 2026-04-24 | high | Gemini native function declarations and tool-array disclosure | product surface may evolve | Used in `tools.md` |
| `https://langchain-ai.github.io/langgraphjs/reference/classes/langgraph_prebuilt.ToolNode.html` | official docs | canonical | 2026-04-24 | medium | LangGraph ToolNode concurrent tool execution; tools-first binding pattern | framework-specific | Used in `tools.md` |
| `https://arxiv.org/abs/2601.04748` | research paper | canonical | 2026-04-24 | medium | Skills-based routing at scale; semantic confusability dominates library-size effects | research result, not product guarantee | Used in `skills.md` for routing guidance |

## Decisions

1. Use an eval-first workflow before prompt edits.
   Status: adopted
   Why: Anthropic explicitly recommends success criteria, tests, and a first draft before prompt engineering, and OpenAI's prompt optimizer centers graders and annotations.

2. Keep a provider-agnostic base prompt plus model-family adapters.
   Status: adopted
   Why: OpenAI, Anthropic, and Gemini each recommend materially different prompting strategies around reasoning, XML tags, examples, and thinking controls.

3. Use markers and tags selectively, not automatically.
   Status: adopted
   Why: OpenAI and Anthropic both recommend delimiters for clarity, but over-structuring adds noise and reduces readability.

4. Use a candidate-based optimization loop instead of one linear rewrite.
   Status: adopted
   Why: OPRO, ProTeGi, and DSPy all support score-driven search across multiple prompt variants.

5. Keep an explicit optimization log and reflective memory across rounds.
   Status: adopted
   Why: Self-Refine and Reflexion both show the value of critique and retained reflection across iterations.

6. Optimize examples, tool rules, and output contracts together with the core prompt.
   Status: adopted
   Why: Provider docs and DSPy both treat examples and instructions as first-class levers, not optional decoration.

7. Make prompt compaction and de-duplication a first-class optimization step.
   Status: adopted
   Why: OpenAI recommends simple, direct prompts; Gemini explicitly says to avoid passing tokens you do not need; Anthropic frames concision as a context-budget issue.

8. Make context ordering explicit rather than implicit.
   Status: adopted
   Why: Gemini and Anthropic both document that long-context prompts perform better when evidence comes before the final query.

9. Treat tool schemas as disclosed by the provider-native tool array; keep the prompt free of tool-schema restatement.
   Status: adopted
   Why: Anthropic, OpenAI, Gemini, Semantic Kernel, LangGraph, and MCP all expose tools via a native parameter or protocol handshake. Restating schemas in the system prompt is redundant and costs tokens every turn.

10. Document progressive and deferred tool disclosure as the scaling pattern beyond ~20 tools.
    Status: adopted
    Why: Claude Code (`ToolSearch`) and MCP (`tools/list` + `list_changed`) converge on deferred/progressive disclosure as the scaling strategy. Prompt-level enumeration degrades routing and context budget.

11. Require explicit handling of layered prompts where part of the system prompt is deployer-authored.
    Status: adopted
    Why: `SOUL.md`/`WORLD.md`-style layered runtimes risk platform rules drifting into deployer-authored files that may be sparse or absent. Platform behavior must survive independent of the deployer layer.

12. Treat skills as a distinct prompt surface from tools, with their own disclosure, invocation, and lifecycle decisions.
    Status: adopted
    Why: Skills carry procedural instructions that must reach the model at the right time; tools do not. Disclosure (eager vs lazy vs hybrid), invocation (slash vs meta-tool vs description-match vs implicit), and resumability (does a loaded skill survive a pause?) are all distinct design axes not covered by tool guidance.

## Coverage matrix

| Dimension | Coverage status | Evidence |
|---|---|---|
| Preconditions and eval inputs | complete | Anthropic overview, OpenAI prompt optimizer, repo authoring guidance |
| Ordered optimization flow | complete | workflow-process example, OPRO, ProTeGi, Self-Refine, DSPy |
| Failure handling and stop conditions | complete | Anthropic overview, Self-Refine, Reflexion, DSPy |
| Model-family variance | complete | OpenAI, Anthropic, Gemini docs |
| Prompt compaction and deduplication | complete | OpenAI reasoning best practices, Anthropic skill best practices, Gemini long-context guidance |
| Context ordering and query placement | complete | Anthropic prompting docs, Gemini long-context guidance |
| Safety and escalation boundaries | complete | provider docs plus repo workflow conventions |
| Output and acceptance checks | complete | OpenAI prompting and optimizer docs, skill-writer output patterns |
| Transformed example artifacts | complete | `references/transformed-examples.md` |
| Tool disclosure and policy | complete | `references/tools.md` |
| Skill disclosure, invocation, and lifecycle | complete | `references/skills.md` |
| Future-family coverage beyond OpenAI/Claude/Gemini | partial | currently deferred until there is a concrete repo need |

## Description QA

### Should trigger

- "Improve this system prompt for our coding agent."
- "Optimize an agent prompt for Claude."
- "Rewrite this OpenAI developer prompt."
- "Port this prompt from GPT to Gemini."
- "Make this tool-using prompt more reliable."
- "Tune this prompt wording with a proper eval loop."
- "How should I expose tools in my agent's system prompt?"
- "Design tool policy for our harness prompt."
- "Stop the model from narrating 'let me check' before tool calls."
- "How should I disclose skills in the system prompt — eager or lazy?"
- "Route between two adjacent skills that keep mis-matching."
- "Split platform rules out of our customer-authored persona file."

### Should not trigger

- "Write a new skill."
- "Review my pull request."
- "Fix this bug in the repository."
- "Summarize this document."
- "Design a new model architecture."
- "Tune only the temperature and top-p settings."
- "Implement a new MCP server." (this is a tool/server authoring task, not a prompt task)
- "Write the SKILL.md body for a new skill." (this is a skill-authoring task — use `skill-writer`)

## Open gaps

1. Add provider notes for additional families only when the repository has a real downstream need.
2. If this skill starts getting heavy use, add an optional script or eval template for capturing prompt scores across rounds.
3. Re-check provider docs when major model-family updates land, especially around tool use and reasoning defaults.

## Stopping rationale

Further retrieval is currently low-yield for this first version. The source pack already covers:

- official prompt guidance from the three major model families most likely to matter in practice
- current optimizer framing from a live prompt-programming framework
- foundational prompt-optimization research for candidate search, critique loops, and reflection memory
- local repository conventions for canonical skill authoring and registration

## Changelog

- 2026-04-18: Created the initial `prompt-optimizer` skill, references, and provenance record.
- 2026-04-18: Added an explicit prompt learnings pass covering compaction, deduplication, and context ordering.
- 2026-04-18: Folded the prompt learnings back into the core shaping and iteration guidance to keep the workflow compact.
- 2026-04-24: Added `references/tools.md` (tool disclosure, policy, deferred/progressive disclosure, tool-count ceilings, narration, error policy) and `references/skills.md` (skill vs tool, eager/lazy/hybrid disclosure, invocation conventions, platform-vs-deployer layering, skill-bundled tools, routing, resumable-session lifecycle).
