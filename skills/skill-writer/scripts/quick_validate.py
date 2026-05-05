# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""
Quick structural validation for Agent Skills.

Validates that SKILL.md exists, has valid frontmatter, declares the required
fields, and references bundled files that exist. Size checks are advisory
warnings.

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

MAX_SKILL_CHARS = 20000

LOCAL_FILE_REFERENCE_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])"
    r"((?:references|scripts|assets)/[A-Za-z0-9][A-Za-z0-9._/-]*\.[A-Za-z0-9]+|"
    r"(?:SPEC|SOURCES)\.md)"
    r"(?![A-Za-z0-9_./-])"
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the structural requirements for an agent skill.",
    )
    parser.add_argument("skill_directory")
    return parser.parse_args(argv)


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

    if len(content) > MAX_SKILL_CHARS:
        warnings.append(
            f"SKILL.md is {len(content)} characters (recommended max {MAX_SKILL_CHARS}). "
            "Consider moving optional detail to references/."
        )

    validate_local_file_references(skill_path, content, errors)

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
