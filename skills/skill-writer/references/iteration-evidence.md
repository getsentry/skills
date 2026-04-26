# Iteration Evidence

Use this guide when improving a skill from positive examples, negative examples, review feedback, eval results, or observed agent behavior.

## Storage Layout

Store persistent improvement evidence under:

```text
references/evidence/
├── findings-log.md
├── working-set.md
└── holdout-set.md
```

Use this directory only when examples should outlive the current task. For a one-off small fix, summarize the examples in `SOURCES.md` instead.

## File Roles

`references/evidence/findings-log.md` records interpreted findings:

- repeated failure patterns
- preserved success patterns
- suspected root causes
- instruction changes made in response
- unresolved risks

`references/evidence/working-set.md` stores examples used while editing the skill.

`references/evidence/holdout-set.md` stores examples reserved for validation after edits. Do not tune directly against holdout examples unless the user explicitly moves them into the working set.

## Example Record Schema

Use one record per example:

```markdown
## EX-001: Short label

- Label: positive | negative
- Kind: true-positive | false-positive | false-negative | fix | regression | edge-case
- Origin: human-verified | mixed | synthetic
- Source: issue/PR/commit/log/user note/local eval pointer
- Status: working | holdout | resolved | deferred
- Expected behavior: concise statement
- Observed behavior: concise statement
- Skill delta: instruction, reference, description, or eval change
- Anonymization: what was removed or generalized

### Content

Summarized or redacted example content.
```

Keep records concise. Preserve enough detail to reproduce the behavior, but redact secrets, customer data, private URLs, and unnecessary user content.

## Positive And Negative Findings

Positive findings are not just success stories. Use them to protect behaviors that must not regress.

Negative findings should identify the smallest failing decision:

- wrong trigger behavior
- missing source type
- skipped reference file
- overloaded or hidden instruction
- weak output contract
- missing validation step
- unsafe or non-portable path assumption

Each negative finding should map to a concrete skill delta or an explicit deferred reason.

## Promotion Rules

Promote evidence into the skill artifacts only when it changes future behavior:

- Put universal behavioral rules in `SKILL.md`.
- Put domain-specific examples in a focused reference.
- Put source provenance and decisions in `SOURCES.md`.
- Put reusable eval prompts in `EVAL.md`.
- Keep raw or semi-raw examples in `references/evidence/`.

Do not turn `references/evidence/` into a changelog. The changelog belongs in `SOURCES.md`.
