# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""
Quick validation script for Agent Skills.

Validates SKILL.md frontmatter, naming conventions, and required file structure.
Depth and quality checks are advisory warnings.

Usage:
    uv run quick_validate.py <skill_directory> [--skill-class <class>]

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
REFERENCE_LINE_WARNING = 150

SKILL_CLASSES = {
    "auto",
    "workflow-process",
    "integration-documentation",
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

SPEC_REQUIRED_HEADINGS = (
    "Intent",
    "Scope",
    "Users And Trigger Context",
    "Runtime Contract",
    "Source And Evidence Model",
    "Reference Architecture",
    "Validation",
    "Known Limitations",
    "Maintenance Notes",
)

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

SKILL_WRITER_ROUTING_EXCEPTIONS = {
    "references/evidence/findings-log.md",
    "references/evidence/holdout-set.md",
    "references/evidence/working-set.md",
}

MACHINE_SPECIFIC_PATH_PATTERNS = (
    re.compile(r"/Users/[^/\s`\"'<>)](?:[^\s`\"'<>)]*)"),
    re.compile(r"/home/[^/\s`\"'<>)](?:[^\s`\"'<>)]*)"),
    re.compile(r"/var/folders/[^/\s`\"'<>)](?:[^\s`\"'<>)]*)"),
    re.compile(r"/private/var/folders/[^/\s`\"'<>)](?:[^\s`\"'<>)]*)"),
    re.compile(r"[A-Za-z]:\\Users\\[^\s`\"'<>)](?:[^\s`\"'<>)]*)"),
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate agent skill structure and report advisory quality warnings.",
    )
    parser.add_argument("skill_directory")
    parser.add_argument("--skill-class", choices=sorted(SKILL_CLASSES), default="auto")
    return parser.parse_args(argv)


def infer_skill_class(description: str, content: str) -> str:
    text = f"{description}\n{content}".lower()

    if has_any_term(text, ("create a skill", "write a skill", "skill-writer", "maintain skill docs")):
        return "skill-authoring"
    if has_any_term(text, ("integrate", "sdk", "library", "api surface", "public api", "api contract")) and has_any_term(
        text, ("use when", "downstream", "consumer", "abstraction")
    ):
        return "integration-documentation"
    if has_any_term(text, ("workflow", "ci", "branch", "checklist", "runbook", "triage")):
        return "workflow-process"
    return "generic"


def has_any_term(text: str, terms: tuple[str, ...]) -> bool:
    for term in terms:
        if " " in term:
            if term in text:
                return True
            continue
        if re.search(rf"\b{re.escape(term)}\b", text):
            return True
    return False


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


def find_machine_specific_paths(text: str) -> list[str]:
    matches: list[str] = []
    for pattern in MACHINE_SPECIFIC_PATH_PATTERNS:
        for match in pattern.finditer(text):
            matched = match.group(0)
            if matched not in matches:
                matches.append(matched)
    return matches


def validate_portable_paths(
    skill_path: Path,
    skill_content: str,
    warnings: list[str],
) -> None:
    portability_hits: list[str] = []

    skill_hits = find_machine_specific_paths(skill_content)
    if skill_hits:
        portability_hits.append(f"SKILL.md: {', '.join(skill_hits[:3])}")

    refs_dir = skill_path / "references"
    if refs_dir.exists():
        for ref_path in sorted(refs_dir.rglob("*.md")):
            ref_hits = find_machine_specific_paths(ref_path.read_text())
            if ref_hits:
                portability_hits.append(
                    f"{ref_path.relative_to(skill_path)}: {', '.join(ref_hits[:3])}"
                )

    if portability_hits:
        warnings.append(
            "Machine-specific absolute filesystem paths detected. Use portable placeholders like "
            "`<repo-root>/...` or `<skill-dir>/...`. Offenders: " + "; ".join(portability_hits)
        )


def validate_reference_lengths(skill_path: Path, warnings: list[str]) -> None:
    refs_dir = skill_path / "references"
    if not refs_dir.exists():
        return

    long_refs: list[str] = []
    for ref_path in sorted(refs_dir.rglob("*.md")):
        line_count = len(ref_path.read_text().splitlines())
        if line_count > REFERENCE_LINE_WARNING:
            long_refs.append(f"{ref_path.relative_to(skill_path)} ({line_count} lines)")

    if long_refs:
        warnings.append(
            "Long reference file(s) detected. Consider splitting by lookup need or adding navigation: "
            + "; ".join(long_refs)
        )


def validate_skill_writer_reference_routing(
    skill_path: Path,
    skill_content: str,
    warnings: list[str],
) -> None:
    if skill_path.name != "skill-writer":
        return

    refs_dir = skill_path / "references"
    if not refs_dir.exists():
        return

    all_refs: list[str] = []
    for ref_path in sorted(refs_dir.rglob("*.md")):
        rel_path = ref_path.relative_to(skill_path).as_posix()
        if rel_path in SKILL_WRITER_ROUTING_EXCEPTIONS:
            continue
        all_refs.append(rel_path)

    missing = [rel_path for rel_path in all_refs if rel_path not in skill_content]
    if not missing:
        return

    warnings.append(
        "skill-writer references should be directly discoverable from SKILL.md. "
        "Missing routing entries for: " + ", ".join(missing)
    )


def validate_spec_md(
    skill_path: Path,
    warnings: list[str],
) -> None:
    spec_md = skill_path / "SPEC.md"
    if not spec_md.exists():
        return

    spec_content = spec_md.read_text()
    missing_headings = [
        heading
        for heading in SPEC_REQUIRED_HEADINGS
        if not re.search(rf"^##\s+{re.escape(heading)}\s*$", spec_content, re.MULTILINE)
    ]
    if missing_headings:
        warnings.append("SPEC.md is missing expected heading(s): " + ", ".join(missing_headings))

    spec_hits = find_machine_specific_paths(spec_content)
    if spec_hits:
        warnings.append(
            "SPEC.md contains machine-specific absolute filesystem paths. "
            "Use portable placeholders like `<repo-root>/...` or `<skill-dir>/...`. "
            "Offenders: " + ", ".join(spec_hits[:3])
        )


def validate_integration_depth(
    skill_path: Path,
    warnings: list[str],
) -> None:
    sources_md = skill_path / "SOURCES.md"

    if not sources_md.exists():
        warnings.append(
            "Integration/documentation skill usually should include SOURCES.md with a coverage matrix and open gaps section"
        )
        return

    sources_content = sources_md.read_text()
    coverage_rows = parse_coverage_rows(sources_content)
    if not coverage_rows:
        warnings.append("SOURCES.md is missing a parseable `## Coverage matrix` table")
    else:
        missing_dimensions: list[str] = []
        for label, tokens in INTEGRATION_REQUIRED_DIMENSIONS:
            if not any(any(token in dim for token in tokens) for dim, _status in coverage_rows):
                missing_dimensions.append(label)
        if missing_dimensions:
            warnings.append(
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
                warnings.append(
                    "Coverage matrix has partial/missing dimensions but `## Open gaps` lacks actionable next retrieval steps"
                )


def validate_skill(
    skill_path: Path,
    selected_skill_class: str = "auto",
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

    # Validate frontmatter keys without hardcoding provider-specific optional fields.
    invalid_keys = [key for key in frontmatter.keys() if not isinstance(key, str) or not key.strip()]
    if invalid_keys:
        errors.append("Frontmatter keys must be non-empty strings")

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
                warnings.append(f"description is long ({len(description)} chars, recommended max {MAX_DESCRIPTION_LENGTH})")
            if "<" in description or ">" in description:
                warnings.append("description should avoid angle brackets (< or >)")

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

    validate_skill_writer_reference_routing(skill_path, content, warnings)

    resolved_skill_class = (
        selected_skill_class
        if selected_skill_class != "auto"
        else infer_skill_class(description, "\n".join(body_lines))
    )

    if resolved_skill_class == "integration-documentation":
        validate_integration_depth(skill_path, warnings)
    validate_portable_paths(skill_path, content, warnings)
    validate_reference_lengths(skill_path, warnings)
    validate_spec_md(skill_path, warnings)

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
    )
    result = {
        "valid": valid,
        "skill_class": resolved_skill_class,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, indent=2))
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
