#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""
Reply to PR review threads.

Usage:
    python reply_to_thread.py THREAD_ID BODY [THREAD_ID BODY ...]

Accepts one or more (thread_id, body) pairs as positional arguments.
Batches all replies into a single GraphQL mutation for efficiency.

Example:
    python reply_to_thread.py PRRT_abc "Fixed the issue.\n\n*— Claude Code*"
    python reply_to_thread.py PRRT_abc "Fixed." PRRT_def "Also fixed."
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys


def reply_to_threads(pairs: list[tuple[str, str]]) -> dict[str, bool]:
    """Reply to one or more review threads in a single GraphQL call.

    Returns a dict mapping thread_id -> success.
    """
    # Build aliased mutation
    mutations = []
    for i, (thread_id, body) in enumerate(pairs):
        escaped_body = json.dumps(body)  # handles newlines, quotes
        mutations.append(
            f'  r{i}: addPullRequestReviewThreadReply(input: {{'
            f'pullRequestReviewThreadId: "{thread_id}", '
            f'body: {escaped_body}'
            f'}}) {{ clientMutationId }}'
        )

    query = "mutation {\n" + "\n".join(mutations) + "\n}"

    try:
        result = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={query}"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            print(f"GraphQL error: {result.stderr}", file=sys.stderr)
            return {tid: False for tid, _ in pairs}

        return {tid: True for tid, _ in pairs}
    except subprocess.TimeoutExpired:
        print("Request timed out", file=sys.stderr)
        return {tid: False for tid, _ in pairs}


def main():
    parser = argparse.ArgumentParser(
        description="Reply to PR review threads",
        usage="%(prog)s THREAD_ID BODY [THREAD_ID BODY ...]",
    )
    parser.add_argument(
        "args",
        nargs="+",
        help="Alternating thread_id and body pairs",
    )
    parsed = parser.parse_args()

    if len(parsed.args) % 2 != 0:
        print("Error: arguments must be (thread_id, body) pairs", file=sys.stderr)
        sys.exit(1)

    pairs = []
    for i in range(0, len(parsed.args), 2):
        pairs.append((parsed.args[i], parsed.args[i + 1]))

    results = reply_to_threads(pairs)

    # Output results
    success = all(results.values())
    output = {
        "replied": sum(1 for v in results.values() if v),
        "failed": sum(1 for v in results.values() if not v),
        "threads": {tid: "ok" if ok else "failed" for tid, ok in results.items()},
    }
    print(json.dumps(output, indent=2))

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
