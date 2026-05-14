# Prompt Optimizer Specification

## Intent

`prompt-optimizer` improves reusable prompts through a contract-first, eval-backed workflow.

It should produce shorter, more reliable prompt packages with explicit model strategy, external context inventory, eval evidence, and residual risks.

## Scope

In scope:

- New agent, system, developer, and reusable prompt templates.
- Refining existing prompts from failures or examples.
- Porting prompts across OpenAI, Claude, Gemini, or unknown model families.
- Prompt eval set design, candidate comparison, and holdout checks.
- Layering stable policy, task-local context, examples, tool policy, and external file references.

Out of scope:

- Choosing model architecture or fine-tuning strategy except to flag when prompting is not the bottleneck.
- Rewriting product docs, specs, or policies referenced by a prompt.
- Creating reusable agent skills.
- Debugging repository code unrelated to prompt behavior.
- Asking models to reveal hidden reasoning or chain-of-thought.

## Users And Trigger Context

- Primary users: engineers and agents maintaining prompts for coding agents, product agents, eval harnesses, and model integrations.
- Should trigger for: improve a prompt, optimize a system prompt, rewrite an agent prompt, tune prompt wording, make prompts reliable, port prompts across model families, build prompt evals.
- Should not trigger for: normal code review, PR writing, skill authoring, generic documentation editing, or parameter-only tuning.

## Runtime Contract

- Capture the prompt contract before edits: target model, prompt surfaces, layer owners, objective, non-goals, inputs, tools, output shape, success criteria, failures, and hard constraints.
- Build or request a small eval set when success criteria or examples are missing.
- Inventory stable external context by exact repo-relative path.
- Reference docs/specs/policies by path; paste only necessary excerpts.
- Keep one authoritative owner per behavior rule.
- Compare candidates on the same eval slice.
- Validate the selected prompt on holdout cases.
- Return a reusable package with target, success criteria, external context, optimized prompt, adapter notes, eval set, optimization log, and residual risks.

## Source And Evidence Model

Authoritative sources:

- Local `prompt-optimizer` runtime files and references.
- Repository instructions and `skill-writer` authoring rules.
- Official OpenAI, Anthropic, and Gemini prompting and eval guidance.
- Prompt optimization research and framework docs already captured in `SOURCES.md`.

Useful improvement sources:

- positive examples: prompts that meet eval targets with fewer tokens and cleaner layering
- negative examples: prompts with duplicated policy, vague context, stale examples, or weak tool rules
- eval outputs: failure clusters, holdout regressions, candidate scores, and optimization logs
- model changes: provider docs or release notes showing changed behavior, tool APIs, or reasoning defaults

Do not store secrets, customer data, private policy text, or long copyrighted prompt/source excerpts in examples.

## Reference Architecture

- `SKILL.md` contains the runtime workflow and output contract.
- `SPEC.md` contains this maintenance contract.
- `SOURCES.md` stores source inventory, decisions, coverage, gaps, and changelog.
- `references/core-patterns.md` covers prompt structure, layering, markers, external files, tool policy, and symptom fixes.
- `references/meta-optimization-loop.md` covers eval-backed iteration.
- `references/model-family-notes.md` covers provider adapters.
- `references/transformed-examples.md` contains compact examples for new prompts, repairs, and anti-pattern correction.
- `scripts/` and `assets/` are unused unless prompt scoring automation or reusable templates become necessary.

## Evaluation

- Lightweight validation: run representative prompt tasks through the contract checklist and verify the package includes external context, eval cases, and residual risks.
- Candidate validation: compare all candidates on the same working slice and at least one holdout case.
- Trigger QA: confirm prompt optimization requests trigger this skill while skill writing, code review, and parameter-only tuning do not.
- Acceptance gates: prompt is shorter or behaviorally justified, rules have one owner, external files are exact, examples are causal, and residual risks name non-prompt bottlenecks.

## Known Limitations

- Prompt behavior can change across model snapshots; the skill must recommend re-running evals after model changes.
- The skill cannot prove prompt quality without representative eval cases.
- External files referenced by path are useful only when the runtime agent can access them.
- Provider-specific advice can drift; refresh official docs when model or API behavior matters.

## Maintenance Notes

- Update `SKILL.md` when runtime workflow, output package, or failure modes change.
- Update `SPEC.md` when scope, evidence policy, evaluation, or reference architecture changes.
- Update `SOURCES.md` when source inventory, decisions, coverage, gaps, or changelog entries change.
- Keep reference files focused; split any file that mixes unrelated lookup needs.
