---
name: skill-synthesize
description: Research and synthesize source material to create or improve agent skills with high-context inputs. Use when asked to "synthesize a skill", "collect references for a skill", "improve a skill from examples", "turn docs into a skill", or "prepare skill-writer handoff". Produces a structured handoff for skill-writer and maintains per-skill provenance, gaps, and iteration history.
---

# Skill Synthesize

Collect comprehensive source context for a target skill, synthesize decisions, and produce an implementation-ready handoff for `skill-writer`.

Load deeper guidance on demand:

| Need | Read |
|------|------|
| Source collection and relevance scoring | `${CLAUDE_SKILL_ROOT}/references/source-collection.md` |
| Handoff format for `skill-writer` | `${CLAUDE_SKILL_ROOT}/references/handoff-format.md` |
| `SYNTHESIS.md` structure and update rules | `${CLAUDE_SKILL_ROOT}/references/synthesis-records.md` |
| Example ingestion and anonymization | `${CLAUDE_SKILL_ROOT}/references/example-intake.md` |

## Step 1: Define synthesis target

1. Resolve target skill path (existing or planned).
2. Capture objective, user-trigger phrases, and constraints in one short scope block.
3. State explicit assumptions if scope details are missing.

## Step 2: Collect exhaustive source corpus

Read `${CLAUDE_SKILL_ROOT}/references/source-collection.md`.

1. Gather sources across required categories before drafting conclusions.
2. Prefer canonical docs and authoritative implementations.
3. Maximize relevant input depth for the target type (for example, full relevant official docs for documentation skills; broad TP/FP/fix coverage for detection skills).
4. Record unresolved unknowns in `Coverage Gaps` with concrete next retrieval actions.

## Step 3: Synthesize and decide

1. Derive recommended skill shape (simple, with references, with scripts, full).
2. Map major decisions to source evidence.
3. Mark decisions as `adopted`, `rejected`, or `deferred`.

## Step 4: Produce `skill-writer` handoff

Read `${CLAUDE_SKILL_ROOT}/references/handoff-format.md`.

1. Emit the markdown handoff template exactly as defined.
2. Keep handoff implementation-ready so `skill-writer` can execute without rediscovery.
3. Include assumptions and open gaps when evidence is incomplete.

## Step 5: Update synthesis memory

Read `${CLAUDE_SKILL_ROOT}/references/synthesis-records.md`.

1. Maintain `<target-skill-dir>/SYNTHESIS.md` outside the references directory.
2. Keep every synthesized claim traceable to a source entry.
3. Append dated changelog entries for each synthesis pass.

## Step 6: Ingest examples and improve

Read `${CLAUDE_SKILL_ROOT}/references/example-intake.md`.

1. Store examples in `<target-skill-dir>/examples/YYYY-MM-DD-<slug>.md`.
2. Enforce strict anonymization before storage.
3. Re-evaluate decisions using the full example corpus, not only newly added files.
4. Run replay checks across representative positive, negative, and fix examples.
5. Propose concrete SKILL/support-file updates and append a changelog entry.

## Output format

Return all sections in this order:

1. `Synthesis Summary`
2. `skill-writer Handoff`
3. `SYNTHESIS.md Delta`
4. `Example Intake`
5. `Open Gaps`
