# Reference-Backed Skill Layout

Use this layout when the skill needs deep knowledge, but most runs only need one branch or subset of that knowledge.

## Choose this layout when

- `SKILL.md` can act as a router
- bundled references can stay focused by lookup need
- the complexity is optional knowledge, not heavy automation

## File layout

```text
my-skill/
├── SKILL.md
└── references/
    ├── focused-topic-a.md
    ├── focused-topic-b.md
    └── troubleshooting.md
```

Keep reference files as direct children of `references/`. For related variant-specific leaves, use a shared filename prefix and list each file directly from `SKILL.md`.

## Required contract

1. `SKILL.md` tells the agent exactly when to open each reference.
2. Reference filenames predict their contents.
3. No reference mixes routing, troubleshooting, examples, and source notes without a clear reason.
4. Large references include navigation or are split further.
5. Runtime references stay flat unless there is a non-runtime evidence or asset reason to use a subfolder.

## Avoid this layout when

- the skill is small enough to stay inline
- scripts or validators are central to execution
- the references would only exist as vague topic buckets
