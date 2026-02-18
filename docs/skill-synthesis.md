# Skill Synthesis Guide

Skill synthesis is using your AI coding agent to research upstream implementations, specs, and best practices online before creating a skill. Instead of writing from scratch, you have the agent survey what already exists and synthesize the best ideas into your skill.

This pairs with the [skill-creator](../plugins/sentry-skills/skills/skill-creator/SKILL.md) skill — synthesis handles the research phase, skill-creator handles the implementation.

## Key Sources

Point your agent at these when researching:

| Source | What it covers |
|--------|---------------|
| [Agent Skills Specification](https://agentskills.io/specification) | The spec — frontmatter fields, structure, constraints |
| [Anthropic's official skills](https://github.com/anthropics/skills) | Anthropic's reference implementations |
| [OpenAI Codex's skills](https://github.com/openai/skills) | OpenAI's approach to the same problems |
| [Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Claude's guidance on writing effective skills |
| [Claude Code skills docs](https://code.claude.com/docs/en/skills) | How skills integrate with Claude Code |

Not every source is relevant to every skill. If you're creating a code review skill, look for upstream code review skills. If you're creating something novel, focus on the spec and best practices.

## The Workflow

### 1. Research — tell the agent what to look for

Give the agent the concept and ask it to research before writing anything:

```
I want to create a skill for Django performance reviews. Before writing it,
research upstream implementations — check Anthropic's and OpenAI's skill repos
for anything similar, read the Agent Skills spec, and look at the best practices
docs.
```

The agent will fetch sources, cross-reference approaches, and report back what it found.

### 2. Review — understand what the agent found

The agent should show you:
- What patterns it found upstream worth adopting
- What's unique to our context that upstream skills don't cover
- How it recommends structuring the skill

This is your checkpoint. Redirect before writing, not after.

### 3. Create — hand off to skill-creator

Once you agree on the approach, use the skill-creator to build the skill informed by the research:

```
Now use /skill-creator to create the skill, incorporating what you found.
```

The synthesis research stays in context, so the skill-creator produces a better result than it would from a cold start.

## When To Do This

- **Creating any non-trivial skill** — if upstream implementations exist, research them first
- **Porting a skill from another repo** — understand the original before adapting
- **Rebuilding a skill** — when a rewrite is needed, check the current state of the art

## Tips

- **Research before writing.** The whole point is that the agent creates a better skill because it looked at what already exists.
- **Review the research, not just the output.** Understand what the agent pulled from where — some upstream patterns won't fit your context.
- **Check attribution.** If the agent adopts patterns from a specific upstream skill, follow the [vendoring guidelines](../README.md#vendoring-skills).
- **One skill at a time.** Synthesizing multiple skills in one session gets messy.
