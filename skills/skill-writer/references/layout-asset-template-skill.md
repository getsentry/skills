# Asset-Template Skill Layout

Use this layout when reusable templates, schemas, or static artifacts carry most of the skill's value.

## Choose this layout when

- the skill fills in or adapts reusable artifacts
- the runtime procedure is small compared to the bundled assets
- output quality depends on stable templates or schemas

## File layout

```text
my-skill/
├── SKILL.md
└── assets/
    ├── template.md
    └── schema.json
```

## Required contract

1. `SKILL.md` tells the agent when to load each asset.
2. The skill explains how to adapt placeholders or fields.
3. Add a validation checklist when filled-in output can silently drift.

## Avoid this layout when

- the template is small enough to stay inline
- the asset is just an attachment with no routing or reuse value
