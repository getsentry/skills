---
name: gocd-deploy-status
description: Read-only access to GoCD deployment pipelines at Sentry. Query pipeline status, fetch deploy logs, view build history, and find which pipeline runs include a given commit SHA. Use when asked about deployments, deploy status, pipeline status, deploy logs, build failures, what's deploying, why did the deploy fail, did my commit ship, gocd, pipeline, canary, stage failed, build broken, or check deploy progress.
---

# GoCD Deploy Status (Read-Only)

This skill is the drill-in tool for GoCD deploy questions -- engineers usually start from a Slack notification (eng-pipes posts "your commit shipped" / "no deploys in 2h" / "consecutive failures") and reach for this skill when they need detail. It cannot trigger, pause, or otherwise modify pipelines; that goes through the GoCD web UI or someone with `role-deploy-operator@sentry.io`.

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
| `job-log <pipeline> <pctr> <stage> <sctr> <job> [--tail N] [--full]` | Console log; smart-deduped by default |
| `find-deploy <sha> <pipeline-or-group> [--count N]` | Find runs containing a commit SHA |
| `failures <pipeline-or-group> [--count N]` | Recent failed runs with failed-job log excerpt |
| `paused [group]` | List currently-paused pipelines; scope to a group or scan all |

The `status`, `find-deploy`, and `failures` commands resolve `<name>` as either a pipeline or a group; group output wraps results from each pipeline in the group.

`job-log` defaults to a smart-truncated view: consecutive lines that differ only in digit fields (timestamps, counters, host indices) are collapsed. Pass `--full` to fetch the entire raw log without dedup or tail.

## Domain Model

- **Pipeline group** ("pipedream"): related pipelines for a deploy target, e.g. `getsentry-backend` contains `deploy-getsentry-backend-us`, `deploy-getsentry-backend-de`, `deploy-getsentry-backend-s4s2`, `rollback-getsentry-backend`. Other common pipedreams: `getsentry-frontend`, `sentry-saas`, `relay`, `snuba`, `seer`, `taskbroker`, `vroom`.
- **Pipeline**: a deploy target with stages (e.g. `checks`, `migrations`, `deploy-canary`, `deploy-primary`, `pipeline-complete`). `pipeline-complete` marks the run finished -- use it when checking "did the deploy actually finish?"
- **Region suffixes** on pipeline names: `-us`, `-de`, `-s4s` / `-s4s2` (single-tenant), `-control`, `-customer-N` (per-customer single tenants), `-st`.
- **Stage**: a step within a pipeline run; contains jobs.
- **Job**: a unit of work with a console log.

## Workflows

**"Did my commit ship?"**

`find-deploy <sha> <group>` -- e.g. `find-deploy 77f89b7e getsentry-backend`. Returns each pipeline run in the search window that includes the SHA, with stage statuses. If no matches, the SHA either hasn't entered the pipeline yet or is older than the search window (`--count` controls window size, default 20 runs per pipeline).

**"What's broken?" / "Why did the deploy fail?"**

`failures <group>` -- one call returns recent failed runs across the group, each with the failed stage, failed jobs, and last 50 lines of the first failed job's console log (deduped). For the full log on a specific job, follow up with `job-log ... --full`.

**"What's paused right now?"**

`paused [group]` -- scope to a group (e.g. `paused getsentry-backend`) or omit to scan everything. Returns each paused pipeline with `paused_by` and `paused_cause`. Sentry's deploy scripts auto-pause pipelines when canary fails (see `getsentry/gocd/templates/bash/backend/rollback-canary-and-pause.sh`), so a paused pipeline often means something broke -- follow up with `failures <pipeline>` to see why.

When `failures` returns `log_status: "archived"`, the run is older than ~30 days and its logs were moved to GCS; for those, fall back to the GoCD web UI.

**"What's deploying right now?"**

1. `status <group>` -- look for `"locked": true` (active run) or stages with `"status": "Building"`.
2. A run that looks "stuck" for a few minutes in `deploy-canary` or `soak-time` is normal -- those stages have intentional 5-minute soak windows.

**"Roll back a deploy"**: not supported here. Use the GoCD web UI or ask someone with `role-deploy-operator@sentry.io`.

## Authentication

Two tokens are needed: a GoCD bearer token and a Google IAP identity token. The IAP token is minted automatically via service account impersonation (no setup needed beyond `gcloud auth login` + `role-deploy-user@sentry.io` membership). For the GoCD token there are two paths:

1. **Default**: fetched from GCP Secret Manager (`gocd-access-token` in `dicd-team-devinfra-cd`). Admin-scoped; anyone with project access can read it. Works out of the box, no setup.
2. **Personal read-only token (preferred)**: mint your own from GoCD's UI. Smaller blast radius (read-only enforced server-side) and produces per-user audit trails on the GoCD side.

### First-time setup with a personal read-only token

1. Open https://deploy.getsentry.net in your browser. Click your avatar (top right) → "Personal Access Tokens".
2. Click "Generate Token". Give it a name like `claude-code-readonly`. Copy the value -- GoCD only shows it once.
3. Make `GOCD_ACCESS_TOKEN` available in the shell where Claude Code runs. Pick whichever fits your workflow:

   **Shell rc file (simplest, persistent):**
   ```bash
   echo 'export GOCD_ACCESS_TOKEN=<your-token>' >> ~/.zshrc
   source ~/.zshrc
   ```

   **Project-local `.env` with `direnv`:**
   ```bash
   echo 'export GOCD_ACCESS_TOKEN=<your-token>' >> .envrc
   direnv allow
   ```

   **Inline for one-off use:**
   ```bash
   GOCD_ACCESS_TOKEN=<your-token> uv run ${CLAUDE_SKILL_ROOT}/scripts/gocd.py status getsentry-backend
   ```

When `GOCD_ACCESS_TOKEN` is set, the skill skips Secret Manager entirely. Tokens don't auto-expire; rotate manually via the same GoCD UI when needed.

See [references/gocd_skill_auth.md](references/gocd_skill_auth.md) for the full auth flow including how IAP impersonation works.

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

Internal Sentry references:
- [Pipedreams in GoCD with Jsonnet](https://www.notion.so/sentry/Pipedreams-in-GoCD-with-Jsonnet-430f46b87fa14650a80adf6708b088d9) -- canonical pipedream model (linked from `getsentry/gocd/templates/backend.jsonnet`)
- [GoCD New Service Quickstart](https://www.notion.so/sentry/GoCD-New-Service-Quickstart-6d8db7a6964049b3b0e78b8a4b52e25d) -- adding a new service to GoCD
