#!/usr/bin/env python3
"""
Fetch and categorize PR review feedback.

Usage:
    python fetch_pr_feedback.py [--pr PR_NUMBER]

If --pr is not specified, uses the PR for the current branch.

Output: JSON to stdout with categorized feedback.

Categories:
- blocking: Changes requested, must address
- suggestion: Comments, nitpicks, style suggestions
- bot: Automated comments (Codecov, Sentry bot, etc.)
- resolved: Already resolved threads
"""

import argparse
import json
import re
import subprocess
import sys
from typing import Any


# Known bot usernames and patterns
BOT_PATTERNS = [
    r"(?i)bot$",
    r"(?i)^codecov",
    r"(?i)^sentry",
    r"(?i)^dependabot",
    r"(?i)^renovate",
    r"(?i)^github-actions",
    r"(?i)^mergify",
    r"(?i)^semantic-release",
    r"(?i)^sonarcloud",
    r"(?i)^snyk",
    r"(?i)^cursor",
    r"(?i)^bugbot",
    r"(?i)^seer",
    r"(?i)^copilot",
    r"(?i)\[bot\]$",
]


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


def get_repo_info() -> tuple[str, str] | None:
    """Get owner and repo name from current directory."""
    result = run_gh(["repo", "view", "--json", "owner,name"])
    if result:
        return result.get("owner", {}).get("login"), result.get("name")
    return None


def get_pr_info(pr_number: int | None = None) -> dict[str, Any] | None:
    """Get PR info, optionally by number or for current branch."""
    args = ["pr", "view", "--json", "number,url,headRefName,author,reviews,reviewDecision"]
    if pr_number:
        args.insert(2, str(pr_number))
    return run_gh(args)


def is_bot(username: str) -> bool:
    """Check if username matches known bot patterns."""
    for pattern in BOT_PATTERNS:
        if re.search(pattern, username):
            return True
    return False


def get_review_comments(owner: str, repo: str, pr_number: int) -> list[dict[str, Any]]:
    """Get inline code review comments via API."""
    result = run_gh([
        "api",
        f"repos/{owner}/{repo}/pulls/{pr_number}/comments",
        "--paginate",
    ])
    return result if isinstance(result, list) else []


def get_issue_comments(owner: str, repo: str, pr_number: int) -> list[dict[str, Any]]:
    """Get PR conversation comments (includes bot comments)."""
    result = run_gh([
        "api",
        f"repos/{owner}/{repo}/issues/{pr_number}/comments",
        "--paginate",
    ])
    return result if isinstance(result, list) else []


def get_review_threads(owner: str, repo: str, pr_number: int) -> list[dict[str, Any]]:
    """Get review threads with resolution status via GraphQL."""
    query = """
    query($owner: String!, $repo: String!, $pr: Int!) {
      repository(owner: $owner, name: $repo) {
        pullRequest(number: $pr) {
          reviewThreads(first: 100) {
            nodes {
              id
              isResolved
              isOutdated
              path
              line
              comments(first: 10) {
                nodes {
                  id
                  body
                  author {
                    login
                  }
                  createdAt
                }
              }
            }
          }
        }
      }
    }
    """
    try:
        result = subprocess.run(
            [
                "gh", "api", "graphql",
                "-f", f"query={query}",
                "-F", f"owner={owner}",
                "-F", f"repo={repo}",
                "-F", f"pr={pr_number}",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(result.stdout)
        threads = data.get("data", {}).get("repository", {}).get("pullRequest", {}).get("reviewThreads", {}).get("nodes", [])
        return threads
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return []


def categorize_comment(comment: dict[str, Any], body: str) -> str:
    """Categorize a comment based on content and author."""
    author = comment.get("author", {}).get("login", "") or comment.get("user", {}).get("login", "")

    if is_bot(author):
        return "bot"

    # Look for blocking indicators
    body_lower = body.lower()
    blocking_patterns = [
        r"(?i)must\s+(fix|change|update|address)",
        r"(?i)please\s+(fix|change|update|address)",
        r"(?i)this\s+(is\s+)?(wrong|incorrect|broken|buggy)",
        r"(?i)security\s+(issue|vulnerability|concern)",
        r"(?i)will\s+(break|cause|fail)",
        r"(?i)critical",
        r"(?i)blocker",
    ]

    for pattern in blocking_patterns:
        if re.search(pattern, body):
            return "blocking"

    # Look for suggestion indicators
    suggestion_patterns = [
        r"(?i)nit[:\s]",
        r"(?i)nitpick",
        r"(?i)suggestion[:\s]",
        r"(?i)consider\s+",
        r"(?i)could\s+(also\s+)?",
        r"(?i)might\s+(want\s+to|be\s+better)",
        r"(?i)optional[:\s]",
        r"(?i)minor[:\s]",
        r"(?i)style[:\s]",
        r"(?i)prefer\s+",
        r"(?i)what\s+do\s+you\s+think",
        r"(?i)up\s+to\s+you",
        r"(?i)take\s+it\s+or\s+leave",
        r"(?i)fwiw",
    ]

    for pattern in suggestion_patterns:
        if re.search(pattern, body):
            return "suggestion"

    # Default to suggestion for non-bot comments without strong indicators
    return "suggestion"


def extract_feedback_item(
    body: str,
    author: str,
    path: str | None = None,
    line: int | None = None,
    url: str | None = None,
    is_resolved: bool = False,
    is_outdated: bool = False,
) -> dict[str, Any]:
    """Create a standardized feedback item."""
    # Truncate long bodies for summary
    summary = body[:200] + "..." if len(body) > 200 else body
    summary = summary.replace("\n", " ").strip()

    item = {
        "author": author,
        "body": summary,
        "full_body": body,
    }

    if path:
        item["path"] = path
    if line:
        item["line"] = line
    if url:
        item["url"] = url
    if is_resolved:
        item["resolved"] = True
    if is_outdated:
        item["outdated"] = True

    return item


def main():
    parser = argparse.ArgumentParser(description="Fetch and categorize PR feedback")
    parser.add_argument("--pr", type=int, help="PR number (defaults to current branch PR)")
    args = parser.parse_args()

    # Get repo info
    repo_info = get_repo_info()
    if not repo_info:
        print(json.dumps({"error": "Could not determine repository"}))
        sys.exit(1)
    owner, repo = repo_info

    # Get PR info
    pr_info = get_pr_info(args.pr)
    if not pr_info:
        print(json.dumps({"error": "No PR found for current branch"}))
        sys.exit(1)

    pr_number = pr_info["number"]
    pr_author = pr_info.get("author", {}).get("login", "")

    # Get review decision
    review_decision = pr_info.get("reviewDecision", "")

    # Categorized feedback
    feedback = {
        "blocking": [],
        "suggestion": [],
        "bot": [],
        "resolved": [],
    }

    # Process reviews for overall status
    reviews = pr_info.get("reviews", [])
    for review in reviews:
        if review.get("state") == "CHANGES_REQUESTED":
            author = review.get("author", {}).get("login", "")
            body = review.get("body", "")
            if body and author != pr_author:
                item = extract_feedback_item(body, author)
                item["type"] = "changes_requested"
                feedback["blocking"].append(item)

    # Get review threads (inline comments with resolution status)
    threads = get_review_threads(owner, repo, pr_number)
    seen_thread_ids = set()

    for thread in threads:
        if not thread.get("comments", {}).get("nodes"):
            continue

        first_comment = thread["comments"]["nodes"][0]
        author = first_comment.get("author", {}).get("login", "")
        body = first_comment.get("body", "")

        # Skip if author is PR author (self-comments)
        if author == pr_author:
            continue

        # Skip empty or very short comments
        if not body or len(body.strip()) < 3:
            continue

        is_resolved = thread.get("isResolved", False)
        is_outdated = thread.get("isOutdated", False)

        item = extract_feedback_item(
            body=body,
            author=author,
            path=thread.get("path"),
            line=thread.get("line"),
            is_resolved=is_resolved,
            is_outdated=is_outdated,
        )

        thread_id = thread.get("id")
        if thread_id:
            seen_thread_ids.add(thread_id)

        if is_resolved:
            feedback["resolved"].append(item)
        elif is_bot(author):
            feedback["bot"].append(item)
        else:
            category = categorize_comment(first_comment, body)
            feedback[category].append(item)

    # Get issue comments (general PR conversation)
    issue_comments = get_issue_comments(owner, repo, pr_number)

    for comment in issue_comments:
        author = comment.get("user", {}).get("login", "")
        body = comment.get("body", "")

        # Skip if author is PR author
        if author == pr_author:
            continue

        # Skip empty comments
        if not body or len(body.strip()) < 3:
            continue

        item = extract_feedback_item(
            body=body,
            author=author,
            url=comment.get("html_url"),
        )

        if is_bot(author):
            feedback["bot"].append(item)
        else:
            category = categorize_comment(comment, body)
            feedback[category].append(item)

    # Build output
    output = {
        "pr": {
            "number": pr_number,
            "url": pr_info.get("url", ""),
            "author": pr_author,
            "review_decision": review_decision,
        },
        "summary": {
            "blocking": len(feedback["blocking"]),
            "suggestions": len(feedback["suggestion"]),
            "bot_comments": len(feedback["bot"]),
            "resolved": len(feedback["resolved"]),
            "needs_attention": len(feedback["blocking"]) + len(feedback["suggestion"]),
        },
        "feedback": feedback,
    }

    # Add actionable summary
    if feedback["blocking"]:
        output["action_required"] = "Address blocking feedback before merge"
    elif feedback["suggestion"]:
        output["action_required"] = "Review suggestions - ask user which to address"
    else:
        output["action_required"] = None

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
