# Synthesis Path

Use this path when creating or materially changing a skill.

## Output Style

- Keep synthesis notes terse.
- Prefer tables, status lists, and gap lists over narrative summaries.
- Record decisions as `adopted`, `rejected`, or `deferred`.

## Step 0: Classify

Record the parts that affect the skill's behavior or maintenance:

1. skill class
2. primary execution shape
3. secondary shapes, if any
4. why simpler shapes were not enough

For `integration-documentation`, cover:

1. API surface and behavior contracts
2. config/runtime options
3. downstream use cases
4. issues/failure modes with workarounds
5. version or migration variance

## Step 1: Collect Sources

Collect from:

1. Agent Skills spec and best practices
2. similar in-repo skills
3. upstream implementations and orchestration docs
4. domain or library docs
5. repo conventions and validators
6. tests, fixtures, changelogs, and issue or PR history
7. commit history and blame for regressions or edge cases
8. prior `SPEC.md`, `SOURCES.md`, and `references/evidence/`

If the shape uses provider-specific mechanics, include current provider docs.

## Step 1.2: Adapt Source Material When Needed

Read `references/source-adaptation.md` when the primary input is an upstream prompt, workflow, rubric, benchmark, guide, or docs set.

Record:

1. source intent
2. local target behavior
3. fidelity boundary
4. local replacements
5. omitted material
6. license, notice, attribution, or excerpt constraints

## Baseline Source Pack For Skill-Authoring

Require at minimum:

1. local `skill-writer` runtime files
2. Agent Skills spec and repo conventions
3. provider docs for any provider-specific mechanic being recommended

## Step 1.5: Load Example Profiles

Load only the flat example profile files you need from the reference index in `SKILL.md`.

## Step 1.6: Expand Coverage

Run targeted passes for:

| Pass | Retrieve |
|------|----------|
| core behavior | happy path and main workflow |
| edge behavior | failures, retries, permissions, cleanup |
| negative behavior | false positives, reviewer concerns, bad outputs |
| repair patterns | fixes and corrected outputs |
| version variance | platform or release differences |
| shape mechanics | routing, delegation, loop stops, hook constraints |

Extra retrieval for advanced shapes:

1. route or delegation criteria
2. worker or handoff contracts
3. loop stopping rules
4. provider-specific lifecycle or security constraints

## Step 2: Capture Provenance

For each source, record:

- source URL or path
- trust tier
- confidence
- contribution
- usage constraints

Store provenance in `SOURCES.md`, not long runtime prose.

## Step 3: Synthesize Decisions

Map each major decision to source evidence, including:

- class choice
- shape choice
- provider-specific mechanics
- deferred gaps

## Step 4: Check Synthesis Completeness

Address these before authoring, or report the unresolved item as an explicit gap:

1. no missing high-impact coverage dimensions
2. partial dimensions have explicit next retrieval actions
3. authoring or generator skills include transformed examples
4. selected profile requirements are satisfied
5. coverage passes are reflected in the coverage matrix
6. stopping rationale is explicit
7. supporting refs stay focused and directly discoverable from `SKILL.md`
8. `SPEC.md` exists or is updated when the contract changed
9. advanced mechanics include required contracts and justification
10. provider-specific mechanics include portability notes

## Required Output

- synthesis summary
- source inventory in `SOURCES.md`
- decisions and rationale
- coverage matrix
- gaps and next retrieval actions
- selected class and shape
- source-adaptation notes when an upstream source materially shapes the skill
- `SPEC.md` update summary when applicable
