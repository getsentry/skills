# Sentry Skills

> [!NOTE]
> For skills to help set up Sentry in your project or debug production issues, see https://github.com/getsentry/sentry-for-ai

Agent skills for Sentry employees, following the [Agent Skills](https://agentskills.io) open format.

## Installation

### Claude Code

```bash
claude plugin marketplace add getsentry/skills
claude plugin install sentry-skills@sentry-skills
```

Restart Claude Code after installation. Skills activate automatically when relevant.

**Update:**

```bash
claude plugin marketplace update
claude plugin update sentry-skills@sentry-skills
```

Or run `/plugin` to open the plugin manager.

### Skills Package (skills.sh)

For agents supporting the [skills.sh](https://skills.sh) ecosystem:

```bash
npx skills add getsentry/skills
```

Works with Claude Code, Cursor, Cline, GitHub Copilot, and other compatible agents.

## Available Skills

| Skill | Description |
|-------|-------------|
| [agents-md](plugins/sentry-skills/skills/agents-md/SKILL.md) | This skill should be used when the user asks to "create AGENTS.md", "update AGENTS.md", "maintain agent docs", "set up CLAUDE.md", or needs to keep agent instructions concise. |
| [blog-writing-guide](plugins/sentry-skills/skills/blog-writing-guide/SKILL.md) | Write, review, and improve blog posts for the Sentry engineering blog following Sentry's specific writing standards, voice, and quality bar. |
| [brand-guidelines](plugins/sentry-skills/skills/brand-guidelines/SKILL.md) | Write copy following Sentry brand guidelines. |
| [claude-settings-audit](plugins/sentry-skills/skills/claude-settings-audit/SKILL.md) | Analyze a repository to generate recommended Claude Code settings.json permissions. |
| [code-review](plugins/sentry-skills/skills/code-review/SKILL.md) | Perform code reviews following Sentry engineering practices. |
| [code-simplifier](plugins/sentry-skills/skills/code-simplifier/SKILL.md) | Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality. |
| [commit](plugins/sentry-skills/skills/commit/SKILL.md) | ALWAYS use this skill when committing code changes — never commit directly without it. |
| [create-branch](plugins/sentry-skills/skills/create-branch/SKILL.md) | Create git branches following Sentry naming conventions. |
| [django-access-review](plugins/sentry-skills/skills/django-access-review/SKILL.md) | Django access control and IDOR security review. |
| [django-perf-review](plugins/sentry-skills/skills/django-perf-review/SKILL.md) | Django performance code review. |
| [doc-coauthoring](plugins/sentry-skills/skills/doc-coauthoring/SKILL.md) | Guide users through a structured workflow for co-authoring documentation. |
| [find-bugs](plugins/sentry-skills/skills/find-bugs/SKILL.md) | Find bugs, security vulnerabilities, and code quality issues in local branch changes. |
| [gh-review-requests](plugins/sentry-skills/skills/gh-review-requests/SKILL.md) | Fetch unread GitHub notifications for open PRs where review is requested from a specified team or opened by a team member. |
| [gha-security-review](plugins/sentry-skills/skills/gha-security-review/SKILL.md) | GitHub Actions security review for workflow exploitation vulnerabilities. |
| [iterate-pr](plugins/sentry-skills/skills/iterate-pr/SKILL.md) | Iterate on a PR until CI passes. |
| [pr-writer](plugins/sentry-skills/skills/pr-writer/SKILL.md) | Canonical workflow to create and update pull requests following Sentry conventions. |
| [security-review](plugins/sentry-skills/skills/security-review/SKILL.md) | Security code review for vulnerabilities. |
| [skill-scanner](plugins/sentry-skills/skills/skill-scanner/SKILL.md) | Scan agent skills for security issues. |
| [skill-writer](plugins/sentry-skills/skills/skill-writer/SKILL.md) | Canonical workflow to synthesize, create, and iteratively improve agent skills for this repository. |
| [sred-project-organizer](plugins/sentry-skills/skills/sred-project-organizer/SKILL.md) | Take a list of projects and their related documentation, and organize them into the SRED format for submission. |
| [sred-work-summary](plugins/sentry-skills/skills/sred-work-summary/SKILL.md) | Go back through the previous year of work and create a Notion doc that groups relevant links into projects that can then be documented as SRED projects. |

## Available Subagents

| Subagent | Description |
|----------|-------------|
| [code-simplifier](plugins/sentry-skills/agents/code-simplifier.md) | Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality |
| [senpai](plugins/sentry-skills/agents/senpai.md) | Senior engineer and technical mentor for new Sentry hires. Explains infrastructure, architecture, and engineering concepts step-by-step with references |

## Contributing

### Local Development

```bash
# SSH
git clone git@github.com:getsentry/skills.git ~/sentry-skills
# or HTTPS
git clone https://github.com/getsentry/skills.git ~/sentry-skills

claude plugin marketplace add ~/sentry-skills
claude plugin install sentry-skills@sentry-skills
```

### Repository Structure

```
sentry-skills/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace manifest
├── plugins/
│   └── sentry-skills/
│       ├── .claude-plugin/
│       │   └── plugin.json   # Plugin manifest
│       ├── agents/
│       │   └── code-simplifier.md
│       └── skills/
│           ├── code-review/
│           │   └── SKILL.md
│           └── commit/
│               └── SKILL.md
├── AGENTS.md                 # Agent-facing documentation
├── CLAUDE.md                 # Symlink to AGENTS.md
└── README.md                 # This file
```

### Creating New Skills

Skills follow the [Agent Skills specification](https://agentskills.io/specification). Each skill requires a `SKILL.md` file with YAML frontmatter.

For repeatable `skill-writer` evaluation prompts, see [plugins/sentry-skills/skills/skill-writer/EVAL.md](plugins/sentry-skills/skills/skill-writer/EVAL.md).

#### Skill Template

Create a new directory under `plugins/sentry-skills/skills/`:

```
plugins/sentry-skills/skills/my-skill/
└── SKILL.md
```

**SKILL.md format:**

```yaml
---
name: my-skill
description: A clear description of what this skill does and when to use it. Include keywords that help agents identify when this skill is relevant.
---

# My Skill Name

## Instructions

Step-by-step guidance for the agent.

## Examples

Concrete examples showing expected input/output.

## Guidelines

- Specific rules to follow
- Edge cases to handle
```

#### Naming Conventions

- **name**: 1-64 characters, lowercase alphanumeric with hyphens only
- **description**: Up to 1024 characters, include trigger keywords
- Keep SKILL.md under 500 lines; split longer content into reference files

#### Optional Fields

| Field | Description |
|-------|-------------|
| `license` | License name or path to license file |
| `compatibility` | Environment requirements (max 500 chars) |
| `allowed-tools` | Comma-separated list of tools the skill can use |
| `metadata` | Arbitrary key-value pairs for additional properties |

```yaml
---
name: my-skill
description: What this skill does
license: Apache-2.0
allowed-tools: Read, Grep, Glob
---
```

### Where Skills Belong

Skills should live in the appropriate location based on their scope:

| Scope | Location | Example |
|-------|----------|---------|
| **Global** - Used across Sentry | `sentry-skills` plugin | `commit`, `code-review`, `pr-writer` |
| **Domain-specific** - Used by a team or domain | Dedicated plugin in this repo (e.g., `infra-skills`) | `gcp-logs`, `terraform-review` |
| **Repo-specific** - Only relevant to one repo | The repository itself (`.claude/skills/`) | Project-specific workflows |

When deciding where to place a skill:
- If most Sentry engineers would benefit, add it to `sentry-skills`
- If only a specific team needs it, create or use a domain-specific plugin
- If it only makes sense in one repo, keep it in that repo

#### Marketplace Structure

This repository is a Claude Code **marketplace** - a collection of plugins that can be installed independently. The marketplace manifest (`.claude-plugin/marketplace.json`) lists all available plugins:

```json
{
  "plugins": [
    { "name": "sentry-skills", "source": "./plugins/sentry-skills" },
    { "name": "infra-skills", "source": "./plugins/infra-skills" }
  ]
}
```

Each plugin lives in its own directory under `plugins/` with its own `plugin.json` manifest. Users can install individual plugins:

```bash
# Install just the global skills
claude plugin install sentry-skills@sentry-skills

# Install domain-specific skills
claude plugin install infra-skills@sentry-skills
```

To add a new domain-specific plugin:

1. Create `plugins/<plugin-name>/.claude-plugin/plugin.json`
2. Add skills under `plugins/<plugin-name>/skills/`
3. Register the plugin in `.claude-plugin/marketplace.json`

### Vendoring Skills

We vendor (copy) skills and agents that we use regularly into this repository rather than depending on external sources at runtime. This approach:

- **Ensures consistency** - Everyone on the team uses the same version of each skill
- **Enables customization** - We can adapt skills to Sentry-specific conventions
- **Improves reliability** - No external dependencies that could change or disappear

#### Attribution

When vendoring a skill or agent from an external source, retain proper attribution:

1. **Add a comment** at the top of the file referencing the original source:
   ```markdown
   <!--
   Based on [Original Name] by [Author/Org]:
   https://github.com/example/original-source
   -->
   ```

2. **Include a LICENSE file** in the skill directory if the original has specific licensing requirements:
   ```
   plugins/sentry-skills/skills/vendored-skill/
   ├── SKILL.md
   └── LICENSE      # Original license text
   ```

#### Example: code-simplifier

The `code-simplifier` agent is vendored from [Anthropic's official plugins](https://github.com/anthropics/claude-plugins-official). See the attribution comment at the top of the agent file.

## References

- [Agent Skills Specification](https://agentskills.io/specification)
- [Sentry Engineering Practices](https://develop.sentry.dev/engineering-practices/)

## License

Apache-2.0
