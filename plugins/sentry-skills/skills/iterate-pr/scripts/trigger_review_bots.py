#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""
Detect and trigger review bots on draft PRs.

Usage:
    python trigger_review_bots.py [--pr PR_NUMBER]

Detects which review bots are active on the repo by scanning review/comment
authors on the last 10 merged PRs, then posts trigger comments for each
detected bot. Only triggers on draft PRs — exits early otherwise.

Before posting a new trigger comment, minimizes (hides) any previous trigger
comments we posted for the same bot to keep the PR conversation clean.

Example:
    python trigger_review_bots.py
    python trigger_review_bots.py --pr 123
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any

# Maps bot usernames to their trigger commands.
# Add new bots here as they're discovered.
TRIGGER_MAP: dict[str, str] = {
    "cursor": "@cursor review",
    "sentry": "@sentry review",
}

# All possible trigger command bodies (lowercased) for matching old comments
TRIGGER_BODIES: set[str] = {cmd.lower() for cmd in TRIGGER_MAP.values()}


def run_gh(args: list[str]) -> dict[str, Any] | list[Any] | None:
    """Run a gh CLI command and return parsed JSON output."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout) if result.stdout.strip() else None
    except subprocess.CalledProcessError as e:
        print(f"Error running gh {' '.join(args)}: {e.stderr}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        return None


def minimize_comment(node_id: str) -> bool:
    """Minimize (hide) a comment using the GraphQL API."""
    query = """
    mutation($id: ID!) {
      minimizeComment(input: {subjectId: $id, classifier: OUTDATED}) {
        clientMutationId
      }
    }
    """
    return run_gh(["api", "graphql", "-f", f"query={query}", "-F", f"id={node_id}"]) is not None


def detect_and_trigger(pr_number: int | None = None) -> dict[str, Any]:
    """Detect review bots and trigger them on draft PRs.

    Uses a single GraphQL query to fetch:
    - Current PR's draft status, number, and existing comments
    - Review/comment authors from the last 10 merged PRs (for bot detection)
    """
    # Get repo info
    repo_info = run_gh(["repo", "view", "--json", "owner,name"])
    if not repo_info:
        return {"error": "Could not determine repository"}
    owner = repo_info.get("owner", {}).get("login", "")
    repo = repo_info.get("name", "")

    # Get current PR number if not provided
    if pr_number is None:
        pr_info = run_gh(["pr", "view", "--json", "number"])
        if not pr_info:
            return {"error": "No PR found for current branch"}
        pr_number = pr_info["number"]

    # Single GraphQL query: current PR info + recent PR review/comment authors
    query = """
    query($owner: String!, $repo: String!, $pr: Int!) {
      repository(owner: $owner, name: $repo) {
        pullRequest(number: $pr) {
          isDraft
          number
          comments(first: 100) {
            nodes {
              id
              body
              isMinimized
            }
          }
        }
        pullRequests(states: MERGED, last: 10) {
          nodes {
            reviews(first: 20) {
              nodes {
                author { login }
              }
            }
            comments(first: 50) {
              nodes {
                author { login }
              }
            }
          }
        }
      }
    }
    """

    data = run_gh([
        "api", "graphql",
        "-f", f"query={query}",
        "-F", f"owner={owner}",
        "-F", f"repo={repo}",
        "-F", f"pr={pr_number}",
    ])
    if not data:
        return {"error": "GraphQL query failed"}

    repo_data = data.get("data", {}).get("repository", {})
    pr_data = repo_data.get("pullRequest", {})
    is_draft = pr_data.get("isDraft", False)

    if not is_draft:
        return {"is_draft": False, "triggered": []}

    # Collect unique authors from reviews and comments on recent merged PRs
    authors: set[str] = set()
    for pr_node in repo_data.get("pullRequests", {}).get("nodes", []):
        for review in pr_node.get("reviews", {}).get("nodes", []):
            login = (review.get("author") or {}).get("login", "")
            if login:
                authors.add(login.lower())
        for comment in pr_node.get("comments", {}).get("nodes", []):
            login = (comment.get("author") or {}).get("login", "")
            if login:
                authors.add(login.lower())

    # Find which bots to trigger
    bots_to_trigger = {
        username: cmd
        for username, cmd in TRIGGER_MAP.items()
        if username.lower() in authors
    }

    if not bots_to_trigger:
        return {"is_draft": True, "triggered": [], "no_bots_found": True}

    # Minimize previous trigger comments (hide as outdated)
    minimized = 0
    for comment in pr_data.get("comments", {}).get("nodes", []):
        body = (comment.get("body") or "").strip().lower()
        if not comment.get("isMinimized") and body in TRIGGER_BODIES:
            if minimize_comment(comment["id"]):
                minimized += 1

    # Post new trigger comments
    triggered = []
    for bot_username, trigger_command in bots_to_trigger.items():
        result = run_gh([
            "api",
            f"repos/{owner}/{repo}/issues/{pr_number}/comments",
            "-f", f"body={trigger_command}",
        ])
        if result is not None:
            triggered.append(trigger_command)

    output: dict[str, Any] = {"is_draft": True, "triggered": triggered}
    if minimized:
        output["minimized_previous"] = minimized
    return output


def main():
    parser = argparse.ArgumentParser(
        description="Detect and trigger review bots on draft PRs"
    )
    parser.add_argument(
        "--pr", type=int, help="PR number (defaults to current branch PR)"
    )
    args = parser.parse_args()

    result = detect_and_trigger(args.pr)
    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
