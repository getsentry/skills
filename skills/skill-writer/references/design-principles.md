# Skill Design Principles

Use this guide to keep skill instructions dense, scannable, and worth their token cost.

## Core Rule

- Every line should help the agent decide, do, or verify something.
- Prefer tables, checklists, templates, and input/output examples over explanatory prose.
- Keep rationale to one short sentence unless the agent is likely to make the wrong choice without it.

## Add Vs Cut

| Keep | Cut |
|------|-----|
| project-specific conventions | generic background the agent already knows |
| non-obvious gotchas | motivational filler |
| exact commands, schemas, and templates | repeated restatements of the same rule |
| branch logic and defaults | long essays where a table would work |
| one strong example | multiple weak examples saying the same thing |

## Match Structure To Fragility

| Fragility | Preferred structure | Avoid |
|-----------|---------------------|-------|
| high | exact steps, strict templates, validation gates | open-ended guidance |
| medium | short checklist plus examples | long rationale-heavy prose |
| low | brief goals and constraints | overspecified playbooks |

## Preferred Instruction Shapes

| Need | Preferred shape |
|------|-----------------|
| choose a path | decision table |
| do a repeatable task | numbered checklist |
| enforce output structure | template or schema |
| show style or tone | input/output examples |
| diagnose failures | symptom/cause/fix matrix |
| communicate exact facts | compact reference table |

## Description Rules

- Keep `description` in third person.
- Put trigger language in `description`, not the body.
- Front-load what the skill does and when to use it.
- Do not spend description space on internals unless they improve triggering.

## Runtime Writing Rules

- Use imperative voice.
- State one default path before mentioning alternatives.
- Use one term per concept; do not rotate synonyms.
- Put universal rules in `SKILL.md`; put optional depth in routed refs.
- If a section is mostly explanation, cut it or replace it with a denser structure.

## Reference Rules

- Reference filenames should predict their contents.
- Each reference should answer one lookup question.
- Subfolders are acceptable only when they make the lookup path clearer.
- Every bundled reference should have a direct "open when..." entry in `SKILL.md`.
- Do not create catch-all files for notes, context, or mixed patterns.

## Independence And Portability

- Do not require another skill by name at runtime.
- Use skill-root-relative paths by default.
- Reuse established repo-specific path variables only when the repo already standardizes on them.
- Label provider-specific mechanics explicitly and add portability notes when they matter.

## Long Files

- Keep `SKILL.md` short enough to scan as a router.
- For references over 100 lines, add `## Contents`.
- If a reference grows because it mixes multiple lookup needs, split it.
