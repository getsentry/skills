# Source Collection and Relevance Scoring

Collect comprehensive context before proposing skill changes.

## Collection mindset

Optimize for corpus quality, not minimum viability. Prefer over-collection with clear filtering over under-collection.
Prioritize maximizing relevant input so synthesis leaves as few gaps as possible.

## Required source categories

Collect broadly across every category below:

1. Agent Skills specification and best-practice docs.
2. Existing in-repo skills with similar purpose or structure.
3. Upstream comparable skills or patterns.
4. Domain/library documentation for the target capability.
5. Repo-local conventions (`AGENTS.md`, `README.md`, validation scripts).

Do not skip categories. If sources in a category are unavailable or blocked, log the gap and retrieval path.

## Task-specific depth rules

### Documentation-heavy skill targets

Treat the documentation set as a corpus, not a sample:

1. Collect all official docs sections relevant to the feature surface.
2. Include versioned pages, migration guides, changelogs, and deprecation notes.
3. Include API references, examples, and troubleshooting/error docs.
4. Record any missing/blocked pages in `Coverage Gaps` with retrieval follow-up.

Do not finalize from only landing pages or overview docs.

### Detection/review skill targets (bug finder, security reviewer, lint-style skills)

Build a mixed example corpus:

1. Confirmed true positives (real issues).
2. Confirmed false positives (incorrect flags).
3. Confirmed fixes/remediations and why they work.
4. Borderline or ambiguous cases that require policy decisions.

Do not rely on only "found bug" examples; include non-findings and counterexamples.

## Source inventory format

For each source, capture:

- `source`: URL or file path
- `type`: spec | docs | repo-skill | upstream-skill | convention | example
- `accessed`: YYYY-MM-DD
- `confidence`: high | medium | low
- `contribution`: one sentence on why it matters
- `status`: adopted | partial | rejected
- `coverage_dimension`: API-surface | examples | edge-cases | failures | migrations | fixes | false-positives

## Relevance and confidence rules

Use these defaults:

- `high`: canonical spec, official docs, or authoritative repository pattern
- `medium`: high-quality secondary source or partial-fit precedent
- `low`: weak authority, stale content, or low applicability

Prefer canonical sources when two sources conflict. If conflict remains unresolved, list both positions in `Coverage Gaps`.

## Coverage matrix

Before finalizing synthesis, build a coverage matrix in `SYNTHESIS.md` showing whether each high-impact dimension has enough evidence:

- API/feature surface
- Happy-path examples
- Failure/error behavior
- Edge-case behavior
- Migration/deprecation behavior
- For detection skills: true positives, false positives, and fixes

Mark each dimension as `covered`, `partial`, or `missing`.

## Coverage stop condition

Stop source collection only when either condition is true:

1. Patterns converge across categories, the coverage matrix has no `missing` high-impact dimensions, and no high-impact ambiguity remains.
2. Remaining ambiguities are explicitly recorded in `Coverage Gaps` with next retrieval actions.

Do not finalize synthesis with unresolved high-impact ambiguity that lacks a retrieval action.
When uncertain, continue collecting additional relevant inputs before finalizing.
