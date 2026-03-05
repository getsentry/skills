# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""
Quick validation script for Agent Skills.

Validates SKILL.md frontmatter, naming conventions, directory structure, and
optional strict depth gates for integration/documentation skills.

Usage:
    uv run quick_validate.py <skill_directory> [--skill-class <class>] [--strict-depth]

Returns exit code 0 on success, 1 on failure. Outputs JSON with validation results.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_SKILL_LINES = 500

SKILL_CLASSES = {
    "auto",
    "workflow-process",
    "integration-documentation",
    "security-review",
    "skill-authoring",
    "generic",
}

INTEGRATION_REQUIRED_DIMENSIONS = [
    ("API surface", ("api surface", "api contract", "public api")),
    ("Config/runtime options", ("config", "runtime option", "configuration", "option")),
    ("Common use cases", ("common use", "usage pattern", "normal usage", "use case")),
    ("Known issues/workarounds", ("known issue", "failure mode", "troubleshooting", "workaround")),
    ("Version/migration variance", ("version", "migration", "deprecation", "variance")),
]

INTEGRATION_REQUIRED_REFERENCES = {
    "references/api-surface.md": None,
    "references/common-use-cases.md": 6,
    "references/troubleshooting-workarounds.md": 8,
}

PARTIAL_STATUS_TOKENS = ("partial", "missing", "incomplete", "todo", "unknown")
ACTION_TOKENS = (
    "add",
    "collect",
    "document",
    "retrieve",
    "validate",
    "test",
    "confirm",
    "expand",
    "review",
    "map",
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate agent skill structure and optional depth gates.",
    )
    parser.add_argument("skill_directory")
    parser.add_argument("--skill-class", choices=sorted(SKILL_CLASSES), default="auto")
    parser.add_argument("--strict-depth", action="store_true")
    return parser.parse_args(argv)


def infer_skill_class(description: str, content: str) -> str:
    text = f"{description}\n{content}".lower()

    if any(tok in text for tok in ("create a skill", "write a skill", "skill-writer", "maintain skill docs")):
        return "skill-authoring"
    if any(tok in text for tok in ("security", "vulnerability", "owasp", "injection", "xss")):
        return "security-review"
    if any(tok in text for tok in ("integrate", "sdk", "library", "api")) and any(
        tok in text for tok in ("use when", "downstream", "consumer", "abstraction")
    ):
        return "integration-documentation"
    if any(tok in text for tok in ("workflow", "ci", "branch", "checklist", "runbook", "triage")):
        return "workflow-process"
    return "generic"


def get_section_lines(markdown: str, heading_name: str) -> list[str]:
    lines = markdown.splitlines()
    heading_index = None
    needle = heading_name.lower()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## ") and needle in stripped.lower():
            heading_index = i
            break

    if heading_index is None:
        return []

    out: list[str] = []
    for line in lines[heading_index + 1 :]:
        if line.strip().startswith("## "):
            break
        out.append(line)
    return out


def parse_coverage_rows(sources_markdown: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    section_lines = get_section_lines(sources_markdown, "coverage matrix")
    for line in section_lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if re.match(r"^\|\s*-+\s*\|", stripped):
            continue
        cols = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cols) < 2:
            continue
        # Skip header row.
        if cols[0].lower() in {"dimension", "coverage status"}:
            continue
        rows.append((cols[0].lower(), cols[1].lower()))
    return rows


def parse_open_gap_lines(sources_markdown: str) -> list[str]:
    raw_lines = get_section_lines(sources_markdown, "open gaps")
    return [ln.strip() for ln in raw_lines if ln.strip()]


def count_list_items(markdown: str) -> int:
    return len(re.findall(r"(?m)^\s*(?:-|\d+\.)\s+", markdown))


def validate_integration_depth(
    skill_path: Path,
    strict_depth: bool,
    errors: list[str],
    warnings: list[str],
) -> None:
    sources_md = skill_path / "SOURCES.md"
    severity = errors if strict_depth else warnings

    if not sources_md.exists():
        severity.append(
            "Integration/documentation skill should include SOURCES.md with a coverage matrix and open gaps section"
        )
        return

    sources_content = sources_md.read_text()
    coverage_rows = parse_coverage_rows(sources_content)
    if not coverage_rows:
        severity.append("SOURCES.md is missing a parseable `## Coverage matrix` table")
    else:
        missing_dimensions: list[str] = []
        for label, tokens in INTEGRATION_REQUIRED_DIMENSIONS:
            if not any(any(token in dim for token in tokens) for dim, _status in coverage_rows):
                missing_dimensions.append(label)
        if missing_dimensions:
            severity.append(
                "Coverage matrix is missing required integration dimensions: " + ", ".join(missing_dimensions)
            )

        partial_rows = [dim for dim, status in coverage_rows if any(tok in status for tok in PARTIAL_STATUS_TOKENS)]
        if partial_rows:
            open_gap_lines = parse_open_gap_lines(sources_content)
            actionable = [
                ln
                for ln in open_gap_lines
                if any(tok in ln.lower() for tok in ACTION_TOKENS)
                and (ln.startswith("-") or re.match(r"^\d+\.", ln))
            ]
            if not actionable:
                severity.append(
                    "Coverage matrix has partial/missing dimensions but `## Open gaps` lacks actionable next retrieval steps"
                )

    for rel_path, min_items in INTEGRATION_REQUIRED_REFERENCES.items():
        ref_path = skill_path / rel_path
        if not ref_path.exists():
            severity.append(f"Missing required reference for integration/documentation skill: {rel_path}")
            continue
        if min_items is not None:
            item_count = count_list_items(ref_path.read_text())
            if item_count < min_items:
                severity.append(
                    f"{rel_path} has {item_count} list items; expected at least {min_items} for sufficient depth"
                )


def validate_skill(
    skill_path: Path,
    selected_skill_class: str = "auto",
    strict_depth: bool = False,
) -> tuple[bool, list[str], list[str], str]:
    """Validate a skill directory. Returns (valid, errors, warnings, resolved_skill_class)."""
    errors: list[str] = []
    warnings: list[str] = []

    # Check SKILL.md exists.
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, ["SKILL.md not found"], [], "generic"

    content = skill_md.read_text()

    # Check frontmatter exists and is first.
    if not content.startswith("---"):
        errors.append("No YAML frontmatter found (file must start with ---)")
        return False, errors, warnings, "generic"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        errors.append("Invalid frontmatter format (missing closing ---)")
        return False, errors, warnings, "generic"

    # Parse frontmatter.
    frontmatter_text = match.group(1)
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            errors.append("Frontmatter must be a YAML mapping")
            return False, errors, warnings, "generic"
    except yaml.YAMLError as exc:
        errors.append(f"Invalid YAML in frontmatter: {exc}")
        return False, errors, warnings, "generic"

    # Validate allowed fields.
    allowed_fields = {
        "name",
        "description",
        "license",
        "compatibility",
        "metadata",
        "allowed-tools",
        # Claude Code extensions.
        "argument-hint",
        "disable-model-invocation",
        "user-invocable",
        "model",
        "context",
        "agent",
        "hooks",
    }
    unexpected = set(frontmatter.keys()) - allowed_fields
    if unexpected:
        warnings.append(
            f"Unexpected frontmatter field(s): {', '.join(sorted(unexpected))}. "
            f"These may be ignored by some tools."
        )

    # Validate name.
    if "name" not in frontmatter:
        errors.append("Missing required field: name")
    else:
        name = frontmatter["name"]
        if not isinstance(name, str):
            errors.append(f"name must be a string, got {type(name).__name__}")
        else:
            name = name.strip()
            if not name:
                errors.append("name must not be empty")
            elif len(name) > MAX_NAME_LENGTH:
                errors.append(f"name is too long ({len(name)} chars, max {MAX_NAME_LENGTH})")
            elif not re.match(r"^[a-z0-9-]+$", name):
                errors.append(f"name '{name}' must contain only lowercase letters, digits, and hyphens")
            elif name.startswith("-") or name.endswith("-"):
                errors.append(f"name '{name}' must not start or end with a hyphen")
            elif "--" in name:
                errors.append(f"name '{name}' must not contain consecutive hyphens")
            elif name != skill_path.name:
                errors.append(f"name '{name}' does not match directory name '{skill_path.name}'")

    # Validate description.
    description = ""
    if "description" not in frontmatter:
        errors.append("Missing required field: description")
    else:
        description = frontmatter["description"]
        if not isinstance(description, str):
            errors.append(f"description must be a string, got {type(description).__name__}")
            description = ""
        else:
            description = description.strip()
            if not description:
                errors.append("description must not be empty")
            elif len(description) > MAX_DESCRIPTION_LENGTH:
                errors.append(f"description is too long ({len(description)} chars, max {MAX_DESCRIPTION_LENGTH})")
            if "<" in description or ">" in description:
                errors.append("description must not contain angle brackets (< or >)")

            lower_desc = description.lower()
            if not any(kw in lower_desc for kw in ["use when", "use for", "use to", "trigger", "invoke"]):
                warnings.append(
                    "description should include trigger phrases "
                    '(e.g., \'Use when asked to "review code"\')'
                )
            if lower_desc.startswith(("i ", "i can", "you ")):
                warnings.append(
                    'description should be in third person ("Processes files..." not "I can process files...")'
                )

    # Check line count.
    body_start = content.index("---", 3) + 3
    body_lines = content[body_start:].strip().splitlines()
    if len(body_lines) > MAX_SKILL_LINES:
        warnings.append(
            f"SKILL.md body is {len(body_lines)} lines (recommended max {MAX_SKILL_LINES}). "
            "Consider moving content to references/."
        )

    # Check for common issues.
    if "references/" in content or "scripts/" in content:
        refs_dir = skill_path / "references"
        scripts_dir = skill_path / "scripts"
        if "references/" in content and not refs_dir.exists():
            errors.append("SKILL.md references 'references/' but directory does not exist")
        if "scripts/" in content and not scripts_dir.exists():
            errors.append("SKILL.md references 'scripts/' but directory does not exist")

    # If SOURCES.md is referenced, ensure it exists and includes provenance schema headers.
    if "SOURCES.md" in content:
        sources_md = skill_path / "SOURCES.md"
        if not sources_md.exists():
            errors.append("SKILL.md references 'SOURCES.md' but file does not exist")
        else:
            sources_content = sources_md.read_text()
            required_headers = ("Trust tier", "Confidence", "Usage constraints")
            missing_headers = [header for header in required_headers if header not in sources_content]
            if missing_headers:
                warnings.append(
                    "SOURCES.md is missing expected provenance columns: " + ", ".join(missing_headers)
                )

    # Check for hardcoded repo paths.
    if re.search(r"(?:plugins|skills)/[a-z-]+/(?:scripts|references|assets)/", content):
        warnings.append(
            "SKILL.md may contain hardcoded paths. "
            "Use skill-local references/... paths and run scripts via <skill-dir>/scripts/..."
        )

    resolved_skill_class = (
        selected_skill_class
        if selected_skill_class != "auto"
        else infer_skill_class(description, "\n".join(body_lines))
    )

    if resolved_skill_class == "integration-documentation":
        validate_integration_depth(skill_path, strict_depth, errors, warnings)

    return len(errors) == 0, errors, warnings, resolved_skill_class


def main() -> None:
    args = parse_args(sys.argv[1:])
    skill_path = Path(args.skill_directory).resolve()
    if not skill_path.is_dir():
        print(json.dumps({"valid": False, "errors": [f"Not a directory: {skill_path}"]}))
        sys.exit(1)

    valid, errors, warnings, resolved_skill_class = validate_skill(
        skill_path,
        selected_skill_class=args.skill_class,
        strict_depth=args.strict_depth,
    )
    result = {
        "valid": valid,
        "skill_class": resolved_skill_class,
        "strict_depth": args.strict_depth,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, indent=2))
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
