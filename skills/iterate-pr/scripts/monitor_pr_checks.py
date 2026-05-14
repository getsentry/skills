#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""
Monitor PR checks until they reach a terminal state.

Usage:
    uv run monitor_pr_checks.py [--pr PR_NUMBER]

If --pr is not specified, uses the PR for the current branch.

Output:
    - Prints `ALL_CHECKS_PASSED` when all checks finish without failures
    - Prints `CHECKS_DONE_WITH_FAILURES` when checks finish with failures
    - Prints a tab-separated check summary after the terminal marker

The script stays quiet while polling so background monitor tools do not emit
unnecessary notifications on every iteration. Transient `gh` failures are
retried instead of terminating the monitor.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from typing import Any


def run_gh_json(
    args: list[str],
    allowed_returncodes: tuple[int, ...] = (0,),
) -> list[dict[str, Any]] | dict[str, Any] | None:
    """Run a gh command that returns JSON."""
    result = subprocess.run(
        ["gh"] + args,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode not in allowed_returncodes:
        return None

    if not result.stdout.strip():
        return None

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def get_pr_number(pr_number: int | None) -> int | None:
    """Resolve the PR number to monitor."""
    if pr_number is not None:
        return pr_number

    pr_info = run_gh_json(["pr", "view", "--json", "number"])
    if not isinstance(pr_info, dict):
        return None

    number = pr_info.get("number")
    return number if isinstance(number, int) else None


def get_checks(pr_number: int) -> list[dict[str, Any]] | None:
    """Fetch the current check list for a PR."""
    checks = run_gh_json([
        "pr",
        "checks",
        str(pr_number),
        "--json",
        "name,bucket,link",
    ], allowed_returncodes=(0, 1, 8))
    return checks if isinstance(checks, list) else None


def print_check_summary(checks: list[dict[str, Any]], max_lines: int = 20) -> None:
    """Print a concise tab-separated check summary."""
    for check in checks[:max_lines]:
        name = str(check.get("name", "unknown"))
        bucket = str(check.get("bucket", "unknown"))
        link = str(check.get("link", ""))
        print(f"{name}\t{bucket}\t{link}".rstrip(), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Monitor PR checks until they finish")
    parser.add_argument("--pr", type=int, help="PR number (defaults to current branch PR)")
    parser.add_argument(
        "--poll-seconds",
        type=int,
        default=30,
        help="Polling interval while checks are pending or gh is transiently failing",
    )
    parser.add_argument(
        "--no-checks-seconds",
        type=int,
        default=15,
        help="Retry delay when a fresh push has not registered any checks yet",
    )
    args = parser.parse_args()

    pr_number = get_pr_number(args.pr)
    if pr_number is None:
        print("No PR found for current branch", file=sys.stderr)
        return 1

    while True:
        checks = get_checks(pr_number)
        if checks is None:
            time.sleep(args.poll_seconds)
            continue

        if not checks:
            time.sleep(args.no_checks_seconds)
            continue

        pending = sum(1 for check in checks if check.get("bucket") == "pending")
        if pending:
            time.sleep(args.poll_seconds)
            continue

        failed = sum(1 for check in checks if check.get("bucket") == "fail")
        if failed:
            print("CHECKS_DONE_WITH_FAILURES", flush=True)
        else:
            print("ALL_CHECKS_PASSED", flush=True)

        print_check_summary(checks)
        return 0


if __name__ == "__main__":
    sys.exit(main())
