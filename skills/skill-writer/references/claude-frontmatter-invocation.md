# Claude Frontmatter And Invocation

Load this when the skill needs Claude Code-specific frontmatter or invocation control.

## Use this file for

- extra trigger metadata
- invocation visibility rules
- skill-scoped model or effort overrides
- path or shell activation controls

## Relevant fields

| Field | Purpose | Notes |
|-------|---------|-------|
| `when_to_use` | extra trigger context for Claude | additive only; keep trigger-rich language in `description` |
| `disable-model-invocation` | only the user can invoke | good for side-effect-heavy workflows |
| `user-invocable` | hide from `/` menu and let Claude invoke | good for passive background knowledge |
| `allowed-tools` | pre-approve tools while skill is active | provider-specific |
| `model` | skill-scoped model override | provider-specific |
| `effort` | skill-scoped effort override | provider-specific |
| `paths` | glob-based activation limits | provider-specific |
| `shell` | shell for `!` preprocessing | provider-specific |

## Invocation rules

1. If Claude should not decide when to run the skill, set `disable-model-invocation: true`.
2. If deliberate metadata should document that Claude may select the skill, set `disable-model-invocation: false`.
3. If the skill is not a meaningful command for humans, consider `user-invocable: false`.
4. Keep trigger-rich language in `description` even if `when_to_use` is present.

## Cross-provider parity

For Codex, add `agents/openai.yaml` under the skill root. Match Claude's behavior with `policy.allow_implicit_invocation`: use `false` when `disable-model-invocation` is `true`, and `true` when it is `false`. The same file may include `interface.display_name`, `interface.short_description`, and an explicit `interface.default_prompt` that references the skill as `$skill-name`.

## Portability rule

When using Claude or Codex-specific fields, say why they are necessary and note that they are not portable Agent Skills behavior.
