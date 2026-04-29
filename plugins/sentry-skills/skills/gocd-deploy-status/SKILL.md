---
name: gocd-deploy-status
description: >
  Read-only access to GoCD deployment pipelines at Sentry. Query pipeline status,
  fetch deploy logs, and view build history. Use when asked about "deployments",
  "deploy status", "pipeline status", "deploy logs", "build failures", "what's
  deploying", "why did the deploy fail", "gocd", "pipeline", "canary", "stage
  failed", "build broken", "what's deploying right now", or "check deploy progress".
allowed-tools: Read, Bash, Grep
---

# GoCD Deploy Status (Read-Only)

This skill queries GoCD pipelines at Sentry. It cannot trigger, pause, or otherwise modify them -- mutating actions go through the GoCD web UI or someone with `role-deploy-operator@sentry.io`.

## Requirements

- `gcloud` authenticated (`gcloud auth login`) with an account in `role-deploy-user@sentry.io` (same group that gates the GoCD web UI).
- `uv` installed: https://docs.astral.sh/uv/getting-started/installation/

## Commands

Run all commands with `uv run ${CLAUDE_SKILL_ROOT}/scripts/gocd.py <cmd>`:

| Command | What it does |
|---|---|
| `pipelines` | List all pipeline groups |
| `status <name>` | Status of a pipeline or pipeline group |
| `history <pipeline> [--count N]` | Recent runs (default 5) |
| `stage <pipeline> <pctr> <stage> <sctr>` | Stage instance details |
| `job-log <pipeline> <pctr> <stage> <sctr> <job> [--tail N]` | Console log (default last 200 lines) |

The `status` command resolves `<name>` as either a pipeline or a group; group output wraps multiple pipeline statuses.

## Domain Model

- **Pipeline group** ("pipedream"): related pipelines for a deploy target, e.g. `getsentry-backend` contains `deploy-getsentry-backend-us`, `deploy-getsentry-backend-de`, `rollback-getsentry-backend`.
- **Pipeline**: a deploy target with stages (e.g. `migrations`, `deploy-canary`, `deploy-primary`).
- **Stage**: a step within a pipeline run; contains jobs.
- **Job**: a unit of work with a console log.

## Workflows

**"Why did the deploy fail?"**

1. `status <pipeline>` -- find the failed stage
2. `stage <pipeline> <counter> <failed_stage> 1` -- find the failed job
3. `job-log <pipeline> <counter> <failed_stage> 1 <failed_job> --tail 200` -- read the error

**"What's deploying right now?"**

1. `pipelines` to list groups
2. `status <group>` -- look for `"locked": true` (active run) or stages with `"status": "Building"`

**"Roll back a deploy"**: not supported here. Use the GoCD web UI or ask someone with `role-deploy-operator@sentry.io`.

## Authentication

The skill fetches the GoCD token from GCP Secret Manager (`gocd-access-token` in `dicd-team-devinfra-cd`) and mints an IAP identity token via service account impersonation. To use a personal read-only token instead, set `GOCD_ACCESS_TOKEN` -- it takes precedence over the Secret Manager fetch.

See [references/gocd_skill_auth.md](references/gocd_skill_auth.md) for the full auth flow.

## Errors

| Error | Cause | Fix |
|---|---|---|
| `could not get IAP token` | Not in `role-deploy-user@sentry.io` | Get added to the group |
| `HTTP 401` | Invalid GoCD token | Check `GOCD_ACCESS_TOKEN`, or the GCP secret |
| `HTTP 403` | IAP token invalid, or token lacks read permission | `gcloud auth login`; if using personal token, confirm it has the view role |
| `HTTP 404` | Pipeline/stage name typo | Check with `pipelines` |

## Configuration

| Env var | Default | Purpose |
|---|---|---|
| `GOCD_HOST` | `https://deploy.getsentry.net` | GoCD server URL |
| `GOCD_ACCESS_TOKEN` | (unset) | Personal read-only token; overrides Secret Manager |
| `GOCD_IAP_CLIENT_ID` | Sentry's IAP client | IAP audience |
| `GOCD_IAP_SERVICE_ACCOUNT` | Sentry's impersonated SA | SA for IAP token minting |

For curl-based fallback and full API details, see [references/api-surface.md](references/api-surface.md).
