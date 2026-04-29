# GoCD REST API Reference (Read-Only)

This reference documents the read endpoints used by the gocd-deploy skill. Mutating
endpoints (schedule, pause, unpause, cancel, run) are intentionally omitted -- this
skill is read-only.

## Authentication

Every request to `deploy.getsentry.net` requires two headers:

```
Authorization: bearer <GOCD_ACCESS_TOKEN>
Proxy-Authorization: Bearer <IAP_ID_TOKEN>
```

## Endpoints

### Pipeline History (paginated)

```
GET /go/api/pipelines/{name}/history?page_size=N&after=CURSOR
Accept: application/vnd.go.cd.v1+json
```

Pagination is cursor-based via `_links.next.href`. Extract the query string from the next href and append to the next call. Absent `_links.next` means last page.

Response fields per pipeline run:

| Field | Type | Description |
|---|---|---|
| `name` | string | Pipeline name |
| `counter` | int | Run number |
| `scheduled_date` | int | Unix timestamp in milliseconds |
| `build_cause.material_revisions[]` | array | Git SHAs, pipeline dependencies |
| `stages[]` | array | Stage name, status, counter, jobs |

Stage `status` values: `Building`, `Passed`, `Failed`, `Unknown`.
Job `state` values: `Scheduled`, `Building`, `Completed`.
Job `result` values: `Passed`, `Failed`.

### Pipeline Instance

```
GET /go/api/pipelines/{name}/{counter}
Accept: application/vnd.go.cd.v1+json
```

Same structure as a single entry in the history response.

### Pipeline Status

```
GET /go/api/pipelines/{name}/status
Accept: application/vnd.go.cd.v1+json
```

```json
{"paused": false, "paused_cause": "", "paused_by": "", "locked": true, "schedulable": false}
```

A pipeline is actively running when `locked: true` and `schedulable: false`.

### Pipeline Groups

```
GET /go/api/config/pipeline_groups
Accept: application/vnd.go.cd.v1+json
```

Returns array of `{name, pipelines: [{name, ...}]}`.

### Stage Instance

```
GET /go/api/stages/{pipeline}/{pipeline_counter}/{stage}/{stage_counter}
Accept: application/vnd.go.cd.v3+json
```

Returns detailed job information including `job_state_transitions` with timestamps for: `Scheduled`, `Assigned`, `Preparing`, `Building`, `Completing`, `Completed`.

### Job Console Log

```
GET /go/files/{pipeline}/{counter}/{stage}/{stage_counter}/{job}/cruise-output/console.log
```

Returns plain text (not JSON). No `Accept` header needed. All path segments are required.

Console logs are stored on the GoCD server's persistent volume. Logs older than 30 days are archived to GCS and deleted from disk.

## Domain Concepts

**Pipeline locator**: `{pipeline}/{counter}/{stage}/{stage_counter}` -- e.g. `deploy-getsentry-backend-us/13954/deploy-primary/1`. Appears in `GO_DEPENDENCY_LOCATOR_*` env vars and in Pipeline-type material revisions.

**Pipeline groups**: Pipelines are organized into groups (e.g., `getsentry-backend`, `sentry-saas`). Config repos in GitHub define the pipeline YAML for each group.
