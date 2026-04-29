# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
"""
GoCD read-only deployment API client for Sentry.

Auth:
    - IAP token: minted via service account impersonation (gcloud)
    - GoCD token: from GOCD_ACCESS_TOKEN env var, else GCP Secret Manager

Commands: pipelines, status, history, stage, job-log
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

import requests

GOCD_HOST = os.environ.get("GOCD_HOST", "https://deploy.getsentry.net")
IAP_CLIENT_ID = os.environ.get(
    "GOCD_IAP_CLIENT_ID",
    "610575311308-9bsjtgqg4jm01mt058rncpopujgk3627.apps.googleusercontent.com",
)
IAP_SERVICE_ACCOUNT = os.environ.get(
    "GOCD_IAP_SERVICE_ACCOUNT",
    "incident-scout-bot@incident-scout-bot.iam.gserviceaccount.com",
)


def get_iap_token() -> str | None:
    """Mint an IAP identity token by impersonating a service account via gcloud."""
    try:
        result = subprocess.run(
            [
                "gcloud", "auth", "print-identity-token",
                f"--impersonate-service-account={IAP_SERVICE_ACCOUNT}",
                f"--audiences={IAP_CLIENT_ID}",
                "--include-email",
            ],
            capture_output=True, text=True, check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Warning: could not get IAP token: {e}", file=sys.stderr)
        return None


def get_gocd_token() -> str:
    """Fetch GoCD API token from env var, else GCP Secret Manager."""
    if env_token := os.environ.get("GOCD_ACCESS_TOKEN", "").strip():
        return env_token
    try:
        result = subprocess.run(
            [
                "gcloud", "secrets", "versions", "access", "latest",
                "--secret=gocd-access-token",
                "--project=dicd-team-devinfra-cd",
            ],
            capture_output=True, text=True, check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(
            f"Error: could not retrieve GoCD token: {e}\nSet GOCD_ACCESS_TOKEN"
            + " to a personal token, or run `gcloud auth login` and ensure access"
            + " to project dicd-team-devinfra-cd.",
            file=sys.stderr,
        )
        sys.exit(1)


def build_session() -> requests.Session:
    session = requests.Session()
    session.headers["Authorization"] = f"bearer {get_gocd_token()}"
    if iap_token := get_iap_token():
        session.headers["Proxy-Authorization"] = f"Bearer {iap_token}"
    return session


def api_get(session: requests.Session, path: str, version: int = 1) -> dict:
    """GET a GoCD API endpoint, return parsed JSON."""
    resp = session.get(
        f"{GOCD_HOST}{path}",
        headers={"Accept": f"application/vnd.go.cd.v{version}+json"},
    )
    if not resp.ok:
        print(json.dumps({"error": f"HTTP {resp.status_code}", "message": resp.text[:500]}, indent=2))
        sys.exit(1)
    return resp.json()


def api_get_text(session: requests.Session, path: str) -> str:
    """GET a GoCD endpoint, return raw text (for console logs)."""
    resp = session.get(f"{GOCD_HOST}{path}")
    if not resp.ok:
        print(json.dumps({"error": f"HTTP {resp.status_code}", "message": resp.text[:500]}, indent=2))
        sys.exit(1)
    return resp.text


def fmt_timestamp(ms: int | None) -> str | None:
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()


def fmt_stage(stage: dict) -> dict:
    return {
        "name": stage.get("name"),
        "counter": stage.get("counter"),
        "status": stage.get("result") or stage.get("status", "Unknown"),
        "jobs": [
            {
                "name": j.get("name"),
                "state": j.get("state"),
                "result": j.get("result"),
                "scheduled": fmt_timestamp(j.get("scheduled_date")),
            }
            for j in stage.get("jobs", [])
        ],
    }


def fmt_materials(build_cause: dict) -> list[dict]:
    out = []
    for rev in build_cause.get("material_revisions", []):
        mat = rev.get("material", {})
        mods = rev.get("modifications", [])
        latest = mods[0] if mods else {}
        out.append({
            "name": mat.get("name"),
            "type": mat.get("type"),
            "revision": latest.get("revision"),
            "user": latest.get("user_name"),
            "comment": (latest.get("comment") or "")[:120],
        })
    return out


def fmt_pipeline_run(run: dict) -> dict:
    return {
        "name": run.get("name"),
        "counter": run.get("counter"),
        "scheduled": fmt_timestamp(run.get("scheduled_date")),
        "materials": fmt_materials(run.get("build_cause", {})),
        "stages": [fmt_stage(s) for s in run.get("stages", [])],
    }


def fetch_pipeline_groups(session: requests.Session) -> dict[str, list[str]]:
    """Map of group name -> pipeline names."""
    data = api_get(session, "/go/api/admin/pipeline_groups")
    return {
        g.get("name"): [p.get("name") for p in g.get("pipelines", [])]
        for g in data.get("_embedded", {}).get("groups", [])
    }


def resolve_pipelines(session: requests.Session, name: str) -> list[str]:
    """If name is a group, return its pipelines. Otherwise return [name]."""
    groups = fetch_pipeline_groups(session)
    return groups[name] if name in groups else [name]


def cmd_pipelines(session: requests.Session, args: argparse.Namespace) -> None:
    output = [
        {"group": name, "pipelines": pipelines}
        for name, pipelines in fetch_pipeline_groups(session).items()
        if pipelines
    ]
    print(json.dumps(output, indent=2))


def _pipeline_status(session: requests.Session, name: str) -> dict:
    status = api_get(session, f"/go/api/pipelines/{name}/status")
    history = api_get(session, f"/go/api/pipelines/{name}/history?page_size=10")
    runs = history.get("pipelines", [])
    return {
        "pipeline": name,
        "paused": status.get("paused", False),
        "paused_cause": status.get("paused_cause"),
        "paused_by": status.get("paused_by"),
        "locked": status.get("locked", False),
        "schedulable": status.get("schedulable", True),
        "latest_run": fmt_pipeline_run(runs[0]) if runs else None,
    }


def cmd_status(session: requests.Session, args: argparse.Namespace) -> None:
    pipelines = resolve_pipelines(session, args.pipeline)
    if len(pipelines) == 1:
        print(json.dumps(_pipeline_status(session, pipelines[0]), indent=2))
    else:
        results = [_pipeline_status(session, p) for p in pipelines]
        print(json.dumps({"group": args.pipeline, "pipelines": results}, indent=2))


def cmd_history(session: requests.Session, args: argparse.Namespace) -> None:
    data = api_get(session, f"/go/api/pipelines/{args.pipeline}/history?page_size={args.count}")
    runs = [fmt_pipeline_run(r) for r in data.get("pipelines", [])]
    print(json.dumps({"pipeline": args.pipeline, "total": len(runs), "runs": runs}, indent=2))


def cmd_stage(session: requests.Session, args: argparse.Namespace) -> None:
    data = api_get(
        session,
        f"/go/api/stages/{args.pipeline}/{args.pipeline_counter}/{args.stage}/{args.stage_counter}",
        version=3,
    )
    jobs = []
    for j in data.get("jobs", []):
        transitions = {t["state"]: t.get("state_change_time") for t in j.get("job_state_transitions", [])}
        jobs.append({
            "name": j.get("name"),
            "state": j.get("state"),
            "result": j.get("result"),
            "agent_uuid": j.get("agent_uuid"),
            "scheduled": fmt_timestamp(j.get("scheduled_date")),
            "assigned": transitions.get("Assigned"),
            "preparing": transitions.get("Preparing"),
            "building": transitions.get("Building"),
            "completing": transitions.get("Completing"),
            "completed": transitions.get("Completed"),
        })
    print(json.dumps({
        "pipeline": data.get("pipeline_name"),
        "pipeline_counter": data.get("pipeline_counter"),
        "stage": data.get("name"),
        "stage_counter": data.get("counter"),
        "result": data.get("result"),
        "jobs": jobs,
    }, indent=2))


def cmd_job_log(session: requests.Session, args: argparse.Namespace) -> None:
    path = (
        f"/go/files/{args.pipeline}/{args.pipeline_counter}"
        f"/{args.stage}/{args.stage_counter}"
        f"/{args.job}/cruise-output/console.log"
    )
    lines = api_get_text(session, path).splitlines()
    total = len(lines)
    truncated = bool(args.tail) and total > args.tail
    if truncated:
        lines = lines[-args.tail:]
    print(json.dumps({
        "pipeline": args.pipeline,
        "pipeline_counter": args.pipeline_counter,
        "stage": args.stage,
        "stage_counter": args.stage_counter,
        "job": args.job,
        "total_lines": total,
        "showing_lines": len(lines),
        "truncated": truncated,
        "log": "\n".join(lines),
    }, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GoCD read-only deployment API client for Sentry")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("pipelines", help="List all pipeline groups and pipelines")

    p = sub.add_parser("status", help="Current status of a pipeline or group")
    p.add_argument("pipeline")

    p = sub.add_parser("history", help="Recent pipeline runs")
    p.add_argument("pipeline")
    p.add_argument("--count", type=int, default=5)

    p = sub.add_parser("stage", help="Stage instance details")
    p.add_argument("pipeline")
    p.add_argument("pipeline_counter")
    p.add_argument("stage")
    p.add_argument("stage_counter")

    p = sub.add_parser("job-log", help="Console log for a job")
    p.add_argument("pipeline")
    p.add_argument("pipeline_counter")
    p.add_argument("stage")
    p.add_argument("stage_counter")
    p.add_argument("job")
    p.add_argument("--tail", type=int, default=200)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    session = build_session()
    {
        "pipelines": cmd_pipelines,
        "status": cmd_status,
        "history": cmd_history,
        "stage": cmd_stage,
        "job-log": cmd_job_log,
    }[args.command](session, args)


if __name__ == "__main__":
    main()
