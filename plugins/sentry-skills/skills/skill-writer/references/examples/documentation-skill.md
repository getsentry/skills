# Case Study: Documentation Skill Synthesis

## Scenario

Goal: create a skill that helps an agent answer and author code for a library without repeatedly re-reading upstream docs.

## Input collection approach

This case used breadth-first source collection and only stopped when new retrieval yielded mostly duplicates:

1. Official docs landing pages and navigation trees.
2. All API/class/module reference pages.
3. Configuration and environment reference pages.
4. Official examples/tutorials.
5. Troubleshooting/error catalog pages.
6. Migration/deprecation/changelog pages.
7. Upstream repo README plus canonical examples.
8. In-repo usage of the library (`rg` on imports and key APIs).

## Coverage matrix used

Required dimensions tracked during synthesis:

1. Setup and installation.
2. Core primitives and API surface.
3. Configuration and runtime options.
4. Normal usage patterns.
5. Edge cases and failure handling.
6. Version-specific differences.
7. Migration and deprecation guidance.
8. Instructional templates/examples for direct reuse.

## Synthesized artifacts produced

The resulting skill references included:

1. Happy-path implementation template.
2. Production-safe variant with defensive defaults.
3. Anti-pattern and corrected implementation.
4. Intent-to-reference routing guide (which section to load for which user request).
5. Gap log with explicit next retrieval steps.

## Source-to-decision trace (sample)

1. Source class: migration/changelog docs.
   Decision: add a version-compatibility checklist section to the skill.
   Why: multiple API signatures existed across versions; without this, answers were inconsistent.
2. Source class: troubleshooting/error catalog.
   Decision: add an error-to-fix lookup table in references.
   Why: user prompts often start from failures, not idealized setup.
3. Source class: in-repo usage scan (`rg`).
   Decision: prioritize examples matching local project patterns.
   Why: produced outputs became directly usable with fewer edits.

## Concrete artifacts (sample)

1. Prompt and output skeleton:
   Prompt: "Configure <library> client for retries and auth in production."
   Output: a production-safe template with retry/backoff, timeout defaults, and auth placeholders.
2. Anti-pattern transformation:
   Before: single inline config with no timeout/error handling.
   After: structured config with explicit timeout, retry policy, and failure handling notes.
3. Reference routing snippet:
   If request mentions "migration" -> load migration/changelog reference first, then API reference.

## What made this high quality

1. Input retrieval was exhaustive across all doc classes, not just top pages.
2. The skill shipped transformed examples, not citation-only notes.
3. Coverage and gaps were explicit, so iteration could continue safely.
