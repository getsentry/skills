# Inline Skill Layout

Use this layout when one coherent policy, checklist, or procedure fits directly in `SKILL.md`.

## Choose this layout when

- the skill has one dominant path
- every invocation needs roughly the same instructions
- deep optional knowledge is not the main problem

## File layout

```text
my-skill/
└── SKILL.md
```

## Required contract

1. Keep the body small enough to scan in one read.
2. Put all universal steps in `SKILL.md`.
3. Add references only if a real branch or lookup need appears.

## Avoid this layout when

- most invocations need only a subset of a large knowledge base
- scripts or validators carry important runtime behavior
- routing or iterative validation is central to the skill
