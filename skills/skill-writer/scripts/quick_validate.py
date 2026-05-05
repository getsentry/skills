# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""
Quick structural validation for Agent Skills.

Validates that SKILL.md exists, has valid frontmatter, declares the required
fields, and references bundled files that exist. Size and portability checks are
advisory warnings.

Usage:
    uv run quick_validate.py <skill_directory>

Returns exit code 0 on success, 1 on failure. Outputs JSON with validation
results.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

MAX_NAME_LENGTH = 64
MAX_SKILL_LINES = 500

LOCAL_FILE_REFERENCE_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])"
    r"((?:references|scripts|assets)/[A-Za-z0-9][A-Za-z0-9._/-]*\.[A-Za-z0-9]+|"
    r"(?:SPEC|SOURCES)\.md)"
    r"(?![A-Za-z0-9_./-])"
)

MACHINE_SPECIFIC_PATH_PATTERNS = (
    re.compile(r"/Users/[^/\s`\"'<>)](?:[^\s`\"'<>)]*)"),
    re.compile(r"/home/[^/\s`\"'<>)](?:[^\s`\"'<>)]*)"),
    re.compile(r"/var/folders/[^/\s`\"'<>)](?:[^\s`\"'<>)]*)"),
    re.compile(r"/private/var/folders/[^/\s`\"'<>)](?:[^\s`\"'<>)]*)"),
    re.compile(r"[A-Za-z]:\\Users\\[^\s`\"'<>)](?:[^\s`\"'<>)]*)"),
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the structural requirements for an agent skill.",
    )
    parser.add_argument("skill_directory")
    return parser.parse_args(argv)


def find_machine_specific_paths(text: str) -> list[str]:
    matches: list[str] = []
    for pattern in MACHINE_SPECIFIC_PATH_PATTERNS:
        for match in pattern.finditer(text):
            matched = match.group(0)
            if matched not in matches:
                matches.append(matched)
    return matches


def find_local_file_references(text: str) -> list[str]:
    refs: list[str] = []
    for match in LOCAL_FILE_REFERENCE_RE.finditer(text):
        ref = match.group(1)
        if ref not in refs:
            refs.append(ref)
    return refs


def validate_local_file_references(
    skill_path: Path,
    skill_content: str,
    errors: list[str],
) -> None:
    for rel_path in find_local_file_references(skill_content):
        target = skill_path / rel_path
        if not target.exists():
            errors.append(f"Referenced file not found: {rel_path}")
        elif not target.is_file():
            errors.append(f"Referenced path is not a file: {rel_path}")


def validate_portable_paths(
    skill_path: Path,
    skill_content: str,
    warnings: list[str],
) -> None:
    portability_hits: list[str] = []

    skill_hits = find_machine_specific_paths(skill_content)
    if skill_hits:
        portability_hits.append(f"SKILL.md: {', '.join(skill_hits[:3])}")

    for filename in ("SPEC.md", "SOURCES.md"):
        file_path = skill_path / filename
        if not file_path.exists():
            continue
        file_hits = find_machine_specific_paths(file_path.read_text())
        if file_hits:
            portability_hits.append(f"{filename}: {', '.join(file_hits[:3])}")

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


def validate_skill(
    skill_path: Path,
) -> tuple[bool, list[str], list[str]]:
    """Validate a skill directory. Returns (valid, errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, ["SKILL.md not found"], []

    content = skill_md.read_text()

    if not content.startswith("---"):
        errors.append("No YAML frontmatter found (file must start with ---)")
        return False, errors, warnings

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        errors.append("Invalid frontmatter format (missing closing ---)")
        return False, errors, warnings

    frontmatter_text = match.group(1)
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            errors.append("Frontmatter must be a YAML mapping")
            return False, errors, warnings
    except yaml.YAMLError as exc:
        errors.append(f"Invalid YAML in frontmatter: {exc}")
        return False, errors, warnings

    invalid_keys = [key for key in frontmatter.keys() if not isinstance(key, str) or not key.strip()]
    if invalid_keys:
        errors.append("Frontmatter keys must be non-empty strings")

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

    if "description" not in frontmatter:
        errors.append("Missing required field: description")
    else:
        description = frontmatter["description"]
        if not isinstance(description, str):
            errors.append(f"description must be a string, got {type(description).__name__}")
        elif not description.strip():
            errors.append("description must not be empty")

    body_lines = content[match.end() :].strip().splitlines()
    if len(body_lines) > MAX_SKILL_LINES:
        warnings.append(
            f"SKILL.md body is {len(body_lines)} lines (recommended max {MAX_SKILL_LINES}). "
            "Consider moving optional detail to references/."
        )

    validate_local_file_references(skill_path, content, errors)
    validate_portable_paths(skill_path, content, warnings)

    return len(errors) == 0, errors, warnings


def main() -> None:
    args = parse_args(sys.argv[1:])
    skill_path = Path(args.skill_directory).resolve()
    if not skill_path.is_dir():
        print(json.dumps({"valid": False, "errors": [f"Not a directory: {skill_path}"]}))
        sys.exit(1)

    valid, errors, warnings = validate_skill(skill_path)
    result = {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, indent=2))
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
