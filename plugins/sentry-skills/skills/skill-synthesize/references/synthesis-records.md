# `SYNTHESIS.md` Record Management

Maintain `<target-skill-dir>/SYNTHESIS.md` as the persistent synthesis ledger. Keep it outside the references directory.

## Required structure

```markdown
# Synthesis Record

## Source Inventory
| Source | Type | Trust Tier | Accessed | Confidence | Contribution | Status | License/Terms | Storage Mode |
|--------|------|------------|----------|------------|--------------|--------|---------------|--------------|

## Synthesis Decisions
- Decision: ...
  - Sources: [...]
  - Rationale: ...
  - Status: adopted | rejected | deferred

## Coverage Gaps
- Gap: ...
  - Impact: ...
  - Next retrieval step: ...

## Coverage Matrix
| Dimension | Status | Notes |
|-----------|--------|-------|
| API/feature surface | covered | ... |
| Happy-path examples | covered | ... |
| Failure behavior | partial | ... |
| Edge cases | partial | ... |
| Migrations/deprecations | covered | ... |
| Detection TP/FP/fixes (if applicable) | covered | ... |

## Replay Results
- Corpus replay date: YYYY-MM-DD
- Checked sets: working-corpus | holdout-corpus
- Outcome: improved | unchanged | regressed
- PII check completed: yes | no
- Notes: ...

## Changelog
- YYYY-MM-DD: Initial synthesis for <skill-name>.
- YYYY-MM-DD: Updated from new positive/negative examples.
```

## Update rules

1. Add or update source inventory rows before adding decisions.
2. Link every major decision to source entries.
3. Keep rejected and deferred decisions so future iterations preserve context.
4. Add one dated changelog entry per synthesis pass.
5. Keep language concise and implementation-relevant.
6. Keep `Coverage Matrix` and `Replay Results` current on every iteration.
7. Keep `Storage Mode` as `summary` by default unless verbatim storage is necessary and permitted.
