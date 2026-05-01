# Script-Backed Skill Layout

Use this layout when parsing, validation, APIs, or repeatable transformations are fragile in plain shell or prose alone.

## Choose this layout when

- the skill benefits from deterministic automation
- repeated shell snippets would be brittle
- validation or data extraction should be reusable

## File layout

```text
my-skill/
├── SKILL.md
└── scripts/
    ├── fetch.py
    └── validate.py
```

## Required contract

1. Every script is named in `SKILL.md` with arguments, outputs, and fallback behavior.
2. Scripts are non-interactive.
3. Standard output is structured when practical.
4. The skill explains what to do if a script fails or is unavailable.

## Avoid this layout when

- one simple shell command is enough
- the "script" would only wrap trivial shell for no reliability gain
