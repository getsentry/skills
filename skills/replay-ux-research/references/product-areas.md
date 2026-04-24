# Sentry Product Area URL Patterns

Map product areas to URL path patterns for replay filtering. URLs follow the format `https://<org>.sentry.io/<path>`.

This list may not cover newer product areas — the skill should infer patterns from the area name and confirm with the user if unclear.

## Area Mapping

| Product Area  | Primary Pattern          | Notes                                                       |
| ------------- | ------------------------ | ----------------------------------------------------------- |
| issues        | `/issues`                | Issue list, detail views, and user feedback (`/issues/feedback/`) |
| issue-details | `/issues/` + issue ID    | Single issue detail page only                               |
| explore       | `/explore`               | Parent for traces, logs, metrics, discover, profiles, replays, releases, conversations |
| traces        | `/explore/traces`        | Distributed traces                                          |
| logs          | `/explore/logs`          | Log entries                                                 |
| metrics       | `/explore/metrics`       | Metrics explorer                                            |
| discover      | `/explore/discover`      | Saved queries and ad-hoc event exploration                  |
| profiles      | `/explore/profiles`      | Profiling flamegraphs                                       |
| replays       | `/explore/replays`       | Session replay list and detail                              |
| releases      | `/explore/releases`      | Release health and details                                  |
| conversations | `/explore/conversations` | AI conversations                                            |
| dashboards    | `/dashboards`            | Custom and default dashboards                               |
| monitors      | `/monitors`              | All monitor types: errors, metrics, crons, uptime, mobile builds |
| alerts        | `/monitors/alerts`       | Alert rules and alert detail                                |
| settings      | `/settings`              | Org, project, and account settings                          |

## Query Construction

Substitute the product area's primary pattern into this query template:

```
replays from the last 24 hours where url contains "<primary-pattern>" excluding user emails ending in @sentry.io and @getsentry.com, environment prod
```

## Combining Areas

Some research questions span multiple areas. Combine by running separate queries:

- "Issue triage workflow" = issues + alerts + issue-details
- "Performance debugging" = traces + profiles + metrics
- "Release management" = releases + dashboards
- "Monitoring workflows" = monitors + alerts + issues
