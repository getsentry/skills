# Description Optimization

Use this path to improve skill triggering quality and reduce false matches.

## Trigger quality loop

1. Draft a description with realistic user language and concrete trigger phrases.
2. Build two query sets:
- should-trigger queries
- should-not-trigger queries
3. Evaluate the current description against both sets.
4. Edit description wording to improve precision/recall.
5. Repeat until false positives and false negatives are reduced to acceptable levels.

## Authoring rules

1. Keep the description in third person.
2. Include what the skill does and when to use it.
3. Avoid implementation details that do not help triggering.
4. Avoid provider-specific phrasing unless the skill is intentionally provider-specific.
5. For provider-agnostic skills, avoid naming Claude, Codex, or any provider in ways that would narrow portability expectations.

## Required output

- Final description text
- should-trigger query set
- should-not-trigger query set
- Summary of edits made to improve trigger behavior
