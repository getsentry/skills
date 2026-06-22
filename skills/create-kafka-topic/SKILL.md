---
name: create-kafka-topic
description: Create a new Kafka topic across the Sentry stack — registers it in sentry-kafka-schemas, ops (shared_config/kafka), and sentry, opening one PR per repo. Use when asked to "create a new Kafka topic", "add a Kafka topic", "register a Kafka topic", "set up a new Kafka topic", or provision a topic in sentry-kafka-schemas/ops/sentry.
---

# Create a Kafka Topic

Create and register a new Kafka topic across three repos, opening a PR in each:

1. **sentry-kafka-schemas** — the topic schema definition + CODEOWNERS
2. **ops** — deployment config (default partitions + per-region overrides)
3. **sentry** — the `Topic` enum and cluster mapping

**Requires**: GitHub CLI (`gh`) authenticated, and local checkouts of all three repos.

Run the steps in order. The end deliverable is **three PR links** returned to the user.

> **Not getsentry.** getsentry no longer needs a per-topic change — it loads `KAFKA_TOPIC_TO_CLUSTER` at runtime from the topicctl-generated YAML that ops mounts (getsentry/getsentry#20512, #20661). Do not edit `cellsilo.py`.

## Step 0: Gather inputs and locate repos

1. Prompt the user for:
   - **Topic name** (kebab-case, e.g. `ingest-foo`)
   - **Default number of partitions**
   - **Owning team** (GitHub team handle, e.g. `@getsentry/taskbroker`) — used for the `sentry-kafka-schemas` CODEOWNERS entry and requested as a **reviewer on all three PRs**. For `gh pr create --reviewer`, pass it as the `org/team` slug **without** the leading `@` (e.g. `getsentry/taskbroker`) — referred to as `<owning-team-slug>` below.
2. Locate each repo in the workspace (`sentry-kafka-schemas`, `ops`, `sentry`). If any is not found near the working directory, ask the user for its path. Use `$SCHEMAS`, `$OPS`, `$SENTRY` to refer to them below.
3. **Check for collision**: if `$SCHEMAS/topics/<topic_name>.yaml` already exists, tell the user the topic already exists and ask for a different name. Do not proceed until the name is free.

Before each repo's work, ensure a clean tree on an updated default branch:

```bash
cd "$REPO"
git stash list && git status --porcelain   # must be clean; stop and ask if not
BASE=$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name')
git checkout "$BASE" && git pull --ff-only
git checkout -b add-kafka-topic-<topic_name>
```

## Step 1: sentry-kafka-schemas PR

Create `$SCHEMAS/topics/<topic_name>.yaml`. Read 2–3 existing files in `$SCHEMAS/topics/` that are closest to this topic's purpose to infer good values (pipeline, producer/consumer services, schema type, resource path).

```yaml
pipeline: {pipeline_name}
description: |
  {description}
services:
  producers:
    - {producer_service}
  consumers:
    - {consumer_service}
schemas:
  - version: {version}
    compatibility_mode: none
    type: protobuf
    resource: {resource_name}
    examples:
      - {example_path}
topic_creation_config:
  compression.type: lz4
  message.timestamp.type: LogAppendTime
  max.message.bytes: "10000000"
  retention.ms: "86400000"
```

Field guidance:
- `services` use `getsentry/<repo>` form (e.g. `getsentry/sentry`, `getsentry/relay`).
- `type` is one of `protobuf`, `msgpack`, or `json`. `resource` and `examples` must point at a real schema (e.g. a `sentry_protos` class for protobuf, or a `*.schema.json` for json). If the schema does not exist yet, flag this to the user — the topic file references it.
- Keep the `topic_creation_config` block exactly as above unless the user requests different retention/size.

Also add the topic to `$SCHEMAS/CODEOWNERS`, next to the sibling `topics/*` entries, using the owning team from Step 0:

```
/topics/<topic_name>.yaml                                     <owning_team>
```

**Show the generated files to the user and ask if the values are correct.** If not, prompt for corrections and update the files. Then commit and open the PR:

```bash
git add topics/<topic_name>.yaml CODEOWNERS
git commit -m "feat: add <topic_name> topic schema"
gh pr create --fill --reviewer <owning-team-slug> --title "feat: add <topic_name> topic schema"
```

Capture the PR URL.

> **Release dependency**: the new topic only becomes usable downstream once a new `sentry-kafka-schemas` release is published (after this PR merges, per the repo's release process). The sentry and ops dependency bumps in later steps reference that released version, so they may need to happen after this PR merges and releases.

## Step 2: Choose regions, partitions, and clusters

1. Determine the set of regions that get an override file. Do **not** assume every folder under `regional_overrides/`. Mirror a comparable existing topic — list which regions a sibling topic defines:
   ```bash
   for d in "$OPS"/shared_config/kafka/topics/regional_overrides/*/; do
     [ -f "$d/<sibling_topic>.yaml" ] && basename "$d"
   done
   ```
   The `control` region typically does **not** carry these topics (it only has `taskworker-control*` topics) — exclude it unless the sibling topic includes it.
2. **STOP and ask the user which regions the topic should be enabled in.** This is a required gate — never infer the enabled set from a reference topic, even when the user said "use the same values as `<topic>`" (that covers partitions/cluster/schema defaults, not enablement). Wait for an explicit answer before continuing.
3. For each **enabled** region, prompt for:
   - **Number of partitions** in that region
   - **Cluster** — present the valid choices for that region:
     ```bash
     grep -rh '^cluster:' "$OPS/shared_config/kafka/topics/regional_overrides/<region>/" | sort -u
     ```

Regions not listed as enabled will be written as `disabled: true` in Step 3.

## Step 3: ops PR

In `$OPS`:

1. **Default partitions** — create `shared_config/kafka/topics/<topic_name>.yaml`:
   ```yaml
   partitions: {default_partitions}
   ```
2. **Per-region overrides** — for **each region in the set from Step 2** (not every folder; `control` is normally excluded), create `regional_overrides/<region>/<topic_name>.yaml`:
   - Region **not** enabled by the user → contents are exactly:
     ```yaml
     disabled: true
     ```
   - Region enabled, partitions **differ** from the default:
     ```yaml
     cluster: {cluster_name}
     partitions: {region_partitions}
     ```
   - Region enabled, partitions **equal** the default → omit `partitions`, write only:
     ```yaml
     cluster: {cluster_name}
     ```
3. **Register for deployment** — add `<topic_name>` to the `all_deployed_topics:` list in `shared_config/kafka/topics/defaults/all_topics.yaml`. The list is grouped by topic family, not strictly alphabetical — insert it next to its sibling topics (e.g. right after `<sibling_topic>`).
4. **Bump the schemas dependency** — update the `sentry-kafka-schemas==` pin in `python/requirements.txt` to the version that includes the new topic (see the release dependency note in Step 1).

> **Do not edit generated/materialized files.** CI regenerates `shared_config/_materialized_configs/`, `k8s/clusters/*/_topicctl_generated.yaml`, `k8s/materialized_manifests/`, and topicctl job manifests via `make materialize`. Only edit the source files above.

Commit and open the PR:

```bash
git add shared_config/kafka/topics/ python/requirements.txt
git commit -m "feat: deploy <topic_name> topic"
gh pr create --fill --reviewer <owning-team-slug> --title "feat: deploy <topic_name> topic"
```

Capture the PR URL.

## Step 4: sentry PR

In `$SENTRY`:

1. **`src/sentry/conf/types/kafka_definition.py`** — add an entry to the `class Topic(Enum)`, matching the existing `SCREAMING_SNAKE_CASE = "kebab-name"` convention. Place it next to its sibling topics (the enum is grouped by family, not strictly alphabetical):
   ```python
   TOPIC_NAME = "<topic_name>"
   ```
2. **`src/sentry/conf/server.py`** — add an entry to the `KAFKA_TOPIC_TO_CLUSTER` dict with value `"default"`, next to the sibling entries:
   ```python
   "<topic_name>": "default",
   ```
3. **Bump the schemas dependency** — update `sentry-kafka-schemas>=` in `pyproject.toml` to the released version that includes the new topic, then regenerate the lock so `uv.lock` matches (`uv lock`). See the release dependency note in Step 1.

Commit and open the PR:

```bash
git add src/sentry/conf/types/kafka_definition.py src/sentry/conf/server.py pyproject.toml uv.lock
git commit -m "feat: register <topic_name> kafka topic"
gh pr create --fill --reviewer <owning-team-slug> --title "feat: register <topic_name> kafka topic"
```

Capture the PR URL.

## Step 5: Report

Return all three PR links to the user **and the dependency ordering between them**, so the user knows what must merge first. The schemas PR must merge and publish a release before the dependency-bump PRs can reference the released version.

Output in this shape (annotate each PR with its dependency):

```
Opened 3 PRs for the `<topic_name>` topic:

1. sentry-kafka-schemas: <url>
   └─ Merge + release FIRST. Blocks #2 and #3 (they pin the new schemas version).
2. ops: <url>
   └─ Depends on #1's release (python/requirements.txt bump).
3. sentry: <url>
   └─ Depends on #1's release (pyproject.toml + uv.lock bump).

Merge order: #1 (and its release) → then #2 and #3.
```

If a dependency bump was deferred because the schemas release was not yet published, say so explicitly and note which PR(s) still need the version updated.

## Notes

- For commit messages and PR descriptions, you may use the `commit` and `pr-writer` skills to follow Sentry conventions; the commands above are a self-contained fallback.
- The schemas PR (Step 1) gates the dependency bumps in ops (Step 3) and sentry (Step 4), which reference the released schemas version. If the release is not yet published, open the ops/sentry PRs without the bump and flag it as a follow-up.
