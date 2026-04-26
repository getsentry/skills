# Skill Writer Specification

## Intent

`skill-writer` is the canonical workflow for creating, updating, synthesizing, and iteratively improving agent skills in this repository.

Its primary purpose is to prevent shallow skill authoring by forcing high-value source coverage, explicit provenance, focused runtime instructions, and validation before completion.

## Scope

In scope:

- New skill creation from local, external, or mixed sources.
- Existing skill updates that affect runtime behavior, structure, trigger precision, references, or validation.
- Research-first synthesis for proposed skills.
- Iteration from positive examples, negative examples, review feedback, eval results, and observed agent behavior.
- Registration and validation for this repository's canonical `skills/<skill-name>/` layout and other discovered layouts.

Out of scope:

- Acting as the runtime instructions for the skills it creates.
- Storing full source inventories, raw examples, or changelog history directly in `SKILL.md`.
- Replacing repository-level instructions in `AGENTS.md`, `README.md`, or `CONTRIBUTING.md`.
- Creating per-skill aliases or symlink skills in this repository.
- Guaranteeing compatibility with provider-specific skill extensions unless they are explicitly scoped and documented.

## Users And Trigger Context

- Primary users: agents and humans authoring or maintaining reusable agent skills.
- Common user requests: "create a skill", "write a skill", "update this skill", "improve from examples", "synthesize a skill from docs", "maintain skill docs", or "validate/register this skill".
- Should not trigger for: ordinary code review, generic documentation edits, PR writing, commit creation, or implementation work that does not create or modify an agent skill.

## Runtime Contract

- Required first actions:
  - Resolve the target skill root and operation.
  - Inspect local repository conventions before deciding where files belong.
  - Classify the skill and select the minimum required workflow paths.
- Required outputs:
  - Summary.
  - Changes Made.
  - Validation Results.
  - Open Gaps.
- Non-negotiable constraints:
  - `SKILL.md` frontmatter is first line and `name` matches the directory.
  - `description` contains realistic trigger language.
  - `SKILL.md` remains an orchestration/index layer for complex skills.
  - Supporting references are focused and loaded conditionally.
  - Source provenance and decisions live in `SOURCES.md`.
  - Durable positive/negative examples live in `references/evidence/`.
  - `SPEC.md` records the maintenance contract for new or materially changed skills.
  - Validation runs before completion.
- Expected bundled files loaded at runtime:
  - `references/mode-selection.md`
  - `references/synthesis-path.md`
  - `references/iteration-path.md`
  - `references/authoring-path.md`
  - `references/reference-architecture.md`
  - `references/spec-template.md`
  - `references/description-optimization.md`
  - `references/evaluation-path.md`
  - `references/registration-validation.md`
  - `scripts/quick_validate.py`

## Source And Evidence Model

Authoritative sources:

- Local `skill-writer` runtime files: `SKILL.md`, `references/*.md`, `scripts/quick_validate.py`.
- Repository policy: `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, plugin manifests, and registration settings.
- Agent Skills specification and official skill authoring guidance.

Useful improvement sources:

- positive examples: successful generated skills, review-approved skill changes, and eval passes that demonstrate desired behavior
- negative examples: shallow generated skills, overloaded `SKILL.md` files, catch-all references, missing provenance, failed validation, false triggers, or review feedback
- commit logs/changelogs: repeated fixes, reversions, migrations, and changes that explain why a rule exists
- issue or PR feedback: reviewer comments about missing coverage, confusing trigger language, poor file placement, or insufficient evaluation
- eval results: fixed prompt sets in `EVAL.md`, qualitative depth checks, and optional baseline-vs-with-skill runs

Data that must not be stored:

- secrets, credentials, or tokens
- raw customer data
- private URLs or identifiers that are not needed for reproduction
- large copied source documents or long copyrighted excerpts
- unredacted personal data from examples, logs, issues, or commits

## Reference Architecture

- `SKILL.md` contains the top-level workflow, path-loading table, branch points, universal constraints, and output contract.
- `SPEC.md` contains this maintenance specification.
- `SOURCES.md` contains source inventory, decisions, coverage matrix, open gaps, and changelog.
- `EVAL.md` contains reusable evaluation prompts and deeper eval runbooks.
- `references/` contains focused workflow guidance, patterns, templates, rubrics, and class-specific authoring requirements.
- `references/evidence/` contains durable positive/negative examples when future iterations need them.
- `scripts/` contains validation automation.
- `assets/` is unused unless a future skill-authoring workflow needs static templates or media.

## Evaluation

- Lightweight validation:
  - Run `uv run skills/skill-writer/scripts/quick_validate.py skills/skill-writer --skill-class skill-authoring --strict-depth`.
  - Inspect changed references for focused scope, direct discoverability, and absence of host-specific paths.
- Deeper evaluation:
  - Use `EVAL.md` when a change affects synthesis depth gates, artifact requirements, or generated skill quality.
  - Compare behavior before and after changes with representative positive and negative prompts.
- Holdout examples:
  - Keep durable holdout examples in `references/evidence/holdout-set.md` when repeated regressions appear.
  - Do not tune directly against holdout examples until they are intentionally moved to the working set.
- Acceptance gates:
  - Validator passes with no errors.
  - New or changed workflow rules are represented in the correct artifact.
  - `SOURCES.md` records source-backed decisions and any remaining gaps.
  - `SPEC.md` is updated when intent, scope, evidence model, evaluation, or maintenance expectations change.

## Known Limitations

- The validator checks structure and selected depth gates; it cannot prove that a generated skill is semantically complete.
- Deeper evals are opt-in unless risk or user request justifies the extra cost.
- Source discovery can still miss private operational knowledge if it is not present in local files, accessible issue/PR history, or supplied context.
- Provider-specific skill extensions may drift; `skill-writer` treats them as compatibility guidance unless a skill is intentionally provider-specific.

## Maintenance Notes

- Update `SKILL.md` when the required runtime workflow, branch conditions, or output contract changes.
- Update `SPEC.md` when intent, scope, user/trigger context, evidence model, evaluation gates, limitations, or maintenance rules change.
- Update `SOURCES.md` when source inventory, decisions, coverage, gaps, or changelog entries change.
- Update `EVAL.md` when reusable evaluation prompts or runbooks change.
- Update `references/evidence/` when preserving examples for future iteration or regression tracking.
