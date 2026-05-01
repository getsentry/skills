---
name: skill-writer
description: Create, synthesize, and iteratively improve agent skills following the Agent Skills specification. Use when asked to "create a skill", "write a skill", "synthesize sources into a skill", "improve a skill from positive/negative examples", "update a skill", or "maintain skill docs and registration". Handles source capture, depth gates, authoring, registration, and validation.
---

# Skill Writer

Use this as the single canonical workflow for skill creation and improvement.
Primary success condition: maximize high-value input coverage before authoring so the resulting skill has minimal blind spots.

Load only the path(s) required for the task. `SKILL.md` is the primary router: every bundled reference file should have a direct "open when..." reason here.

## Core Workflow References

| Open when you need to... | Read |
|--------------------------|------|
| choose the minimum workflow path for create, update, iterate, or research-first work | `references/mode-selection.md` |
| choose the simplest adequate execution shape before deciding files | `references/execution-shapes.md` |
| apply writing constraints for depth, concision, and portability | `references/design-principles.md` |
| decide what belongs in `SKILL.md`, `references/`, `SPEC.md`, or subfolders | `references/reference-architecture.md` |
| create or update the maintenance contract for a skill | `references/spec-template.md` |
| find missing high-signal sources, including history and regressions | `references/source-discovery.md` |
| run the full synthesis pass with depth gates and source capture | `references/synthesis-path.md` |
| author or update `SKILL.md`, `SPEC.md`, and supporting files | `references/authoring-path.md` |
| improve trigger language and false-positive/false-negative behavior | `references/description-optimization.md` |
| iterate from positive, negative, or fix examples | `references/iteration-path.md` |
| store persistent working and holdout examples for future revisions | `references/iteration-evidence.md` |
| choose a response template, schema, or output contract | `references/output-contracts.md` |
| troubleshoot overloaded layouts, hidden refs, or other structure failures | `references/structure-troubleshooting.md` |
| evaluate whether the new skill structure and behavior are actually better | `references/evaluation-path.md` |
| register the skill and run final validation checks | `references/registration-validation.md` |

## Artifact Layout References

| Open when you need to... | Read |
|--------------------------|------|
| keep the whole skill inline in one coherent `SKILL.md` | `references/artifact-layouts/inline-skill-layout.md` |
| split optional deep knowledge into focused routed references | `references/artifact-layouts/reference-backed-skill-layout.md` |
| add scripts for deterministic automation or validation | `references/artifact-layouts/script-backed-skill-layout.md` |
| define a skill that is usually invoked with explicit arguments | `references/artifact-layouts/argument-driven-skill-layout.md` |
| ship reusable templates, schemas, or other static assets | `references/artifact-layouts/asset-template-skill-layout.md` |

## Workflow Mechanic References

| Open when you need to... | Read |
|--------------------------|------|
| break a task into fixed ordered steps | `references/workflow-mechanics/prompt-chaining.md` |
| classify requests and route them to different downstream paths | `references/workflow-mechanics/routing-workflows.md` |
| split independent work into parallel units or votes | `references/workflow-mechanics/parallel-workflows.md` |
| discover work units dynamically and coordinate worker outputs | `references/workflow-mechanics/orchestrator-workers.md` |
| critique and revise output against a rubric | `references/workflow-mechanics/evaluator-loops.md` |
| run validate-fix-repeat checks during authoring or execution | `references/workflow-mechanics/validation-loops.md` |
| validate a plan before executing a risky action | `references/workflow-mechanics/plan-validate-execute.md` |

## Claude Code References

| Open when you need to... | Read |
|--------------------------|------|
| use Claude-specific frontmatter or invocation controls | `references/claude-code/frontmatter-and-invocation.md` |
| use Claude argument fields or substitution variables | `references/claude-code/argument-substitutions.md` |
| build a skill that runs in isolated `context: fork` | `references/claude-code/subagent-fork-skills.md` |
| build a skill that uses Claude hooks for deterministic enforcement | `references/claude-code/hook-backed-skills.md` |
| use Claude shell preprocessing for dynamic context injection | `references/claude-code/dynamic-context.md` |

## Example Profiles

| Open when you need to... | Read |
|--------------------------|------|
| see the expected depth for a documentation-heavy skill | `references/examples/documentation-skill.md` |
| see the expected depth for a security-review skill | `references/examples/security-review-skill.md` |
| see the expected depth for a workflow-process skill | `references/examples/workflow-process-skill.md` |
| see what a good routed skill looks like | `references/examples/router-skill.md` |
| see what a good evaluator-loop skill looks like | `references/examples/evaluator-loop-skill.md` |
| see what a good subagent-fork skill looks like | `references/examples/subagent-fork-skill.md` |
| see what a good hook-backed skill looks like | `references/examples/hook-backed-skill.md` |

## Step 1: Resolve target, path, and shape

1. Resolve target skill root and intended operation (`create`, `update`, `synthesize`, `iterate`).
2. Inspect workspace prior art before choosing where the skill belongs:
   - existing skill directories and neighboring skills
   - repository docs such as `AGENTS.md`, `README.md`, and `CONTRIBUTING.md`
   - plugin manifests or other layout-defining files when present
3. Choose the target skill root from observed conventions:
   - default to `.agents/skills/<name>/`
   - if the workspace clearly uses another established layout, follow that layout instead
   - common established alternatives include `skills/<name>/` when the workspace uses a canonical root skill tree, `.claude/skills/<name>/`, `plugins/<plugin>/skills/<name>/`, or another repo-managed skill root with clear prior art
4. If multiple plausible locations exist and the canonical one is still unclear after inspection, ask the user where the skill should go before editing files.
5. Distinguish skill-internal paths from repo registration paths:
   - inside a skill, reference bundled files relative to that skill root (for example `references/foo.md`, `scripts/check.py`)
   - for repository registration edits, use the repository's actual canonical files/locations after inspecting the workspace
6. Read `references/mode-selection.md` and `references/execution-shapes.md`.
7. Classify the skill on two axes:
   - skill class (`workflow-process`, `integration-documentation`, `security-review`, `skill-authoring`, `generic`)
   - execution shape (`inline-guidance`, `reference-backed-expert`, `script-backed-workflow`, `argument-driven`, `router`, `parallelization`, `orchestrator-workers`, `evaluator-optimizer`, `subagent-fork`, `hook-backed`, `asset-template`, or `hybrid`)
8. Default to the simplest adequate execution shape. If selecting a more complex shape, record why simpler shapes were rejected.
9. After choosing the shape, load only the specific artifact-layout, workflow-mechanic, and Claude-specific leaf files that match that shape. Do not bulk-load whole subtrees.
10. If the selected shape or artifact plan uses Claude Code-only mechanics, record portability implications before authoring.
11. Ask one direct question if class, shape, target location, or depth requirements are ambiguous; otherwise state explicit assumptions.

## Step 2: Run synthesis when needed

Read `references/synthesis-path.md`.

1. Collect and score relevant sources with provenance.
2. Read `references/source-discovery.md` when source material is thin, stale, or ambiguous.
3. Apply trust and safety rules when ingesting external content.
4. Produce source-backed decisions and coverage/gap status, including the class and execution-shape choice.
5. Load one or more profiles from `references/examples/*.md` when the skill is hybrid or when the selected shape is nontrivial.
6. If the skill uses provider-specific mechanics, include current official provider docs in the source pack and capture usage constraints.
7. Enforce baseline source pack for skill-authoring workflows.
8. Enforce depth gates before moving to authoring.

## Step 3: Run iteration first when improving from outcomes/examples

Read `references/iteration-path.md` first when selected path includes `iteration` (for example operation `iterate`).

1. Capture and anonymize examples with provenance.
2. Read `references/iteration-evidence.md` when examples should persist beyond the current turn.
3. Re-evaluate skill behavior against working and holdout slices.
4. Propose improvements from positive/negative/fix evidence.
5. Carry concrete behavior deltas into authoring.

Skip this step when selected path does not include `iteration`.

## Step 4: Author or update skill artifacts

Read `references/authoring-path.md`.

1. Write or update `SKILL.md` in imperative voice with trigger-rich description.
2. Read `references/reference-architecture.md` before adding bulk instructions or new reference files.
3. Create or update `SPEC.md` using `references/spec-template.md` when creating a new skill or materially changing an existing skill's intent, sources, evaluation, or maintenance model.
4. Create focused reference files, subfolders, scripts, and assets only when each one has a clear "open when..." reason.
5. If you add a bundled reference file, add a direct routing entry for it in this `SKILL.md`.
6. Follow only the specific artifact-layout, workflow-mechanic, Claude-specific, and output-contract references selected for this skill.
7. For advanced execution shapes, add the required routing, delegation, evaluation, or safety contracts before considering the skill complete.
8. For authoring/generator skills, include transformed examples in references:
   - happy-path
   - secure/robust variant
   - anti-pattern + corrected version

## Step 5: Optimize description quality

Read `references/description-optimization.md`.

1. Validate should-trigger and should-not-trigger query sets.
2. Reduce false positives and false negatives with targeted description edits.
3. Keep trigger language generic across providers unless the skill is intentionally provider-specific.

## Step 6: Evaluate outcomes

Read `references/evaluation-path.md`.

1. Run a lightweight qualitative check by default (recommended).
2. For integration/documentation and skill-authoring skills, include the concise depth rubric from `references/evaluation-path.md`.
3. For material skill changes, verify that the selected execution shape was appropriate, that any advanced mechanics were justified, and that every bundled reference remains directly routable from `SKILL.md`.
4. Run deeper eval playbook and quantitative baseline-vs-with-skill only when requested or risk warrants it.
5. Record outcomes and unresolved risks.

## Step 7: Register and validate

Read `references/registration-validation.md`.

1. Apply repository registration steps for the active layout you verified in the workspace.
2. Run quick validation with strict depth gates.
3. Reject shallow outputs that fail depth gates or required artifact checks.

## Output format

Return:

1. `Summary`
2. `Changes Made`
3. `Validation Results`
4. `Open Gaps`
