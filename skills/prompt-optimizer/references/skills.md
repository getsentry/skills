# Skills

Use this file when designing how an agent prompt discloses, invokes, and routes between skills. A skill here means a named capability bundle that carries procedural instructions — not a bare function-calling tool. Examples: Anthropic Agent Skills and SKILL.md files, Semantic Kernel plugins, MCP prompts, CrewAI agent specializations.

## Contents

- Skill vs tool
- Disclosure: eager, lazy, or hybrid
- Invocation conventions
- Platform-authored vs deployer-authored skills
- Skill-bundled tools
- Routing between adjacent skills
- Lifecycle across resumable sessions
- What belongs in a skill vs the core prompt
- Anti-patterns

## Skill vs tool

A tool is a single callable function with a schema. A skill is a named bundle that typically includes:

- a trigger description (used for routing and discovery)
- when-to-use guidance
- procedural steps or reference material
- optionally bundled tools (e.g., an MCP sub-server, per-skill CLI commands)
- optionally declared configuration keys (`uses-config`)
- optionally an `allowed-tools` restriction

If the capability is "call this function with these arguments," it is a tool. If the capability is "run this multi-step procedure, which may involve several tools and references," it is a skill.

For prompt-author decisions the main difference is procedural content: skill bodies must reach the model at the right time. Tools don't carry procedural content — the schema is enough.

## Disclosure: eager, lazy, or hybrid

Three viable disclosure patterns for skills. Each has clear tradeoffs; pick one per product and state it in the prompt.

1. **Eager inline.** Every loaded skill's body is embedded in the system prompt. Best when skill bodies are small, the runtime knows which skills are relevant per turn, and turns may need to resume across pauses (the skill body must survive resumption without additional tool calls).

2. **Lazy index.** The system prompt carries only a short index of available skills (name, description, path). The model calls a meta-tool (`loadSkill`, MCP `prompts/get`, or equivalent) to fetch a body on demand. Best when there are many skills and only a few are relevant per turn.

3. **Hybrid.** An always-emitted `<available-skills>` index of discoverable skills plus an always-emitted `<loaded-skills>` section with the bodies of skills activated this turn. Best when both routing and execution are needed in one prompt, and the runtime can pre-activate skills based on user intent or explicit invocation.

Rule of thumb: if the turn pauses and resumes (OAuth, long-running tool, timeout retry), skill bodies must still be present after the resume. A pure lazy model forces the runtime to re-trigger loading, which is brittle under interruption.

Lazy disclosure saves tokens but costs latency and adds a failure mode (the model may not realize it needs to load). Eager costs tokens but is robust. Hybrid balances both.

Token shape for reference: roughly 100 tokens of metadata per available skill, plus the full body per loaded skill (often 300–2000 tokens).

## Invocation conventions

Four invocation styles, in roughly declining specificity:

- **Slash command** (`/skillname args`). Explicit, easy to parse, unambiguous. Use when users know which skill they want. Junior and Claude Code both recognize this form.
- **Meta-tool by name** (`loadSkill({ name: "..." })`, MCP `prompts/get`). The model has the index and decides based on task description. Good when selection is the model's job.
- **Description matching** (no special syntax; model reads the index and picks by semantic match). Unreliable above a dozen adjacent skills; failure mode is silent mis-routing.
- **Implicit / always-on** (`.cursorrules`, per-directory instruction files, persistent persona). No explicit invocation; applies whenever the scope matches. Cannot be declined by the model.

Pick one primary convention per product. Mixing (`/candidate-brief` and natural-language matching both supported) is fine if the prompt states both. Do not require the user to memorize which skills are slash-triggered and which are natural-language.

## Platform-authored vs deployer-authored skills

Layered runtimes ship two kinds of skill content:

- **Platform skills**, authored by the framework team. Stable contract. Platform behavior rules may depend on these.
- **Deployer skills**, authored by the install owner (per-customer `SKILL.md`, persona files, `WORLD.md`, `SOUL.md`). Content varies across installs.

Platform behavior rules must never depend on deployer skills being present or containing anything specific. A platform rule like "gather evidence before answering" belongs in the platform prompt; do not assume any deployer-authored file covers it. See `core-patterns.md` / "Layered prompts with multiple owners" for the general principle.

Conversely, deployer skills should not encode platform behavior. They are voice, domain context, and organization-specific procedures.

Litmus test: if you replace the deployer layer with a five-line minimal persona, does every platform-level rule still fire? If not, a platform rule has drifted into the deployer layer and needs to move back.

## Skill-bundled tools

Many skills expose their own tools (MCP sub-server functions, shell helpers, auth-gated provider calls). Two requirements for the prompt and the runtime:

1. **Registration timing.** Tools bundled with a skill reach the native tool array only after the skill loads. The prompt must either (a) only disclose those tools after skill activation, or (b) note that the tools exist but are dormant until activation.
2. **Namespacing.** Skill-bundled tools should be namespaced (e.g., `mcp__github__search_issues`) so the model can distinguish skill-tools from platform-tools. Otherwise natural-language references to "the X tool" become ambiguous.

Do not eagerly register every skill's bundled tools at harness startup; that inflates the tool inventory and contradicts whatever disclosure pattern you picked above.

See `references/tools.md` for broader tool-disclosure guidance.

## Routing between adjacent skills

When two skills match a request, the model must pick one. Three routing hints that work:

- **Action-over-noun descriptions.** Skills described by operation route better than skills described by surface-level noun or product. `"Creates pull requests from a branch"` routes better than `"GitHub integration"`.
- **Explicit disambiguation in the prompt.** One bullet, not many: "Pick the skill whose description matches the requested operation, not incidental nouns or product names."
- **Hierarchical categories (for large skill sets).** Partition the index into categories so the model routes category-then-skill rather than picking among dozens of flat entries. Research on skills-based routing shows semantic confusability, not library size, is the bottleneck; flat selection with many similar descriptions degrades before a hierarchy of the same size does.

If adjacent skills routinely mis-route, the fix is usually in the descriptions, not the prompt body.

## Lifecycle across resumable sessions

When a turn pauses (OAuth flow, long-running tool, timeout-and-resume) and later resumes, the prompt is rebuilt from scratch. Three things must hold:

1. Skills loaded before the pause are still listed as loaded after resumption.
2. The model has an explicit "this is a resume" signal — and the rule about how to behave on resume lives in the canonical rules section, not only in a state marker (see `core-patterns.md` / "Where rules live").
3. Skill-bundled tools are re-registered to the native tool array on resume.

Without all three, the model may act as if starting fresh and repeat work, or fail to use a tool that was available pre-pause. No cross-framework standard yet exists for serializing "which skills were loaded" across resumption; each runtime solves this in its checkpoint format.

## What belongs in a skill vs the core prompt

**Belongs in a skill:**

- multi-step procedures with branching logic
- reference material (syntax, schemas, command lists) only needed when the skill is active
- tool restrictions specific to this procedure (`allowed-tools`)
- configuration keys only this skill reads (`uses-config`)
- domain-specific guardrails ("require explicit confirmation before destructive merges")

**Belongs in the core prompt:**

- cross-cutting behavior (evidence first, never claim success without a tool result)
- output contract (format, length, markdown style)
- identity, role, tone (with deployer-authored personality blocks extending but not replacing platform behavior)
- skill routing and disclosure rules themselves
- resumption signals and session-state markers

Test: if you removed a piece of content from every skill, would the platform still be correct? If yes, that content probably belongs in a skill. If no, it belongs in the core prompt.

Meta-skills whose value is their body (prompt-engineering guidelines, style guides, reference atlases) break the lazy disclosure pattern — they need to be read, not called. Some frameworks support an eager flag in frontmatter for exactly this case.

## Anti-patterns

| Symptom | Fix |
|---------|-----|
| Platform prompt relies on a deployer persona file to encode behavior rules | Move the rules into the platform prompt; treat deployer files as voice-only |
| A skill body is copy-pasted into the platform prompt as permanent content | Treat it as a skill; disclose eagerly only when loaded for this turn |
| Two skills match a request; the model picks inconsistently | Tighten descriptions to name the operation, not the noun or domain |
| Resumed turn forgets a skill was loaded | Ensure the skill loader re-runs on resume; surface a turn-state marker *and* the behavior rule about resumes |
| Skill-bundled tools leak into the native tool array before the skill loads | Gate tool registration on skill activation; do not pre-load |
| Model claims to have "used" a skill it never loaded | Add a rule: "Never apply skill-specific behavior unless the skill is in `<loaded-skills>` or `loadSkill` succeeded this turn" |
| Skill index has 50+ entries with similar descriptions | Partition into categories or combine near-duplicates; routing accuracy degrades with confusable descriptions |
| Meta-skill (style guide, glossary) is lazy-loaded and rarely called | Mark it eager or inline it; meta-skills are unusable under pure lazy disclosure |
