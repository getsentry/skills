# Example Intake and Anonymization

Use examples to improve synthesis decisions over time.

## File layout

Store examples as flat files:

- `<target-skill-dir>/examples/YYYY-MM-DD-<slug>.md`

Aim for a large, diverse corpus. Keep adding examples over time; do not treat examples as one-time inputs.

## Required frontmatter

```yaml
---
id: ex-2026-03-05-001
label: positive
example_kind: true-positive
anonymized: true
evidence_origin: human-verified
date: 2026-03-05
source_type: user-feedback
summary: Short summary of what this example demonstrates.
---
```

Constraints:

- `label` must be `positive` or `negative`.
- `example_kind` should be one of: `true-positive`, `false-positive`, `fix`, `regression`, `edge-case`.
- `anonymized` must be `true` before saving.
- `evidence_origin` should be one of: `human-verified`, `mixed`, `synthetic`.

## Required body sections

1. `## Context`
2. `## Observed Behavior`
3. `## Desired Behavior`
4. `## Explanation`

## Strict anonymization policy

Remove or generalize:

1. Personal names, emails, usernames, and handles.
2. Internal URLs, ticket links, private repo names, and organization identifiers unless technically required.
3. Credentials, tokens, secrets, and environment-specific identifiers.

If a sensitive identifier must remain for technical clarity, justify it in `## Explanation`.

## Iteration loop

When new examples are added:

1. Re-evaluate current synthesis decisions against the full corpus, not only new entries.
2. Run replay checks across two slices:
   - working corpus (examples used during iteration)
   - holdout corpus (examples reserved for final checks)
3. Propose concrete updates to `SKILL.md` and supporting files.
4. Record what improved and what regressed in `SYNTHESIS.md`.
5. Append a dated changelog entry in `SYNTHESIS.md`.
6. Emit an updated `skill-writer` handoff.

## Corpus quality guidance

For detection/review skills, maintain balanced corpus slices:

1. True positives with clear evidence.
2. False positives with clear explanation of why they are incorrect.
3. Fix examples linking issue patterns to successful remediation.

If one slice is weak, mark it in `Coverage Gaps` and prioritize new collection there.

Maintain a small holdout set over time so updates are not judged only on examples used during tuning.
