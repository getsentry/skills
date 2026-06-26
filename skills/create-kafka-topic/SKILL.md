---
name: create-kafka-topic
description: Create a new Kafka topic for Sentry. Public topics (available to self-hosted) get PRs in sentry-kafka-schemas, ops, and sentry; private topics (internal regions only, inheriting settings from a public topic via override_topic) get a single ops PR. Use when asked to "create a new Kafka topic", "add a Kafka topic", "register a Kafka topic", "set up a new Kafka topic", or provision a public or private Kafka topic.
---

# Create a Kafka Topic

First decide whether the topic is **public** or **private** (Step 0 asks). The path differs:

- **Public** — available to self-hosted Sentry. Defined in `sentry-kafka-schemas`, registered in the `sentry` `Topic` enum, and deployed via `ops`. Opens **three PRs**:
  1. **sentry-kafka-schemas** — the topic schema definition + CODEOWNERS
  2. **ops** — deployment config (default partitions + per-region overrides)
  3. **sentry** — the `Topic` enum and cluster mapping
- **Private** — used only in our internal regions; **not** in `sentry-kafka-schemas` or `sentry`. It inherits its `topic_creation_config` from an existing public topic via `override_topic`. Opens **one PR**: just **ops**.

**Requires**: GitHub CLI (`gh`) authenticated, and local checkouts of the repos you'll touch (all three for public; just `ops` for private).

Run the steps in order. For **private** topics, do only Step 0, Step 2, Step 3, and Step 5 — **skip Step 1 (schemas) and Step 4 (sentry)**, which are marked *public only*.

> **Not getsentry.** getsentry no longer needs a per-topic change — it loads `KAFKA_TOPIC_TO_CLUSTER` at runtime from the topicctl-generated YAML that ops mounts (getsentry/getsentry#20512, #20661). Do not edit `cellsilo.py`.

## Step 0: Gather inputs and locate repos

1. **Ask whether the topic is public or private** — this determines the whole path:
   - **Public** — available to self-hosted Sentry. Up to three PRs.
   - **Private** — only used in our internal regions. Single ops PR; inherits settings from a public topic via `override_topic`.
2. Prompt the user for:
   - **Topic name** (kebab-case, e.g. `ingest-foo`)
   - **Default number of partitions**
   - **Reference topic** — the closest existing topic of the same family. It drives region discovery (Step 2) and where the `all_topics.yaml` / `Topic` enum entries go (Steps 3–4). Referred to as `<sibling_topic>` below.
   - **Owning team** (GitHub team handle, e.g. `@getsentry/taskbroker`) — for **public** topics it is the `sentry-kafka-schemas` CODEOWNERS entry; for **all** topics it is requested as a **reviewer on every PR this skill opens**. For `gh pr create --reviewer`, pass it as the `org/team` slug **without** the leading `@` (e.g. `getsentry/taskbroker`) — referred to as `<owning-team-slug>` below.
   - **(private only) Override topic** — the existing **public** topic whose `topic_creation_config` this private topic inherits. It must already exist in `$OPS/shared_config/kafka/topics/defaults/all_topics.yaml` (verify it does); referred to as `<override_topic>` below.
3. **(public only) Confirm a new schema definition is actually needed.** Not every public topic adds a new `sentry-kafka-schemas` entry — ask the user:
   - **taskworker** topics do get their own `topics/<name>.yaml` (reusing the shared `TaskActivation` protobuf) → proceed with Step 1.
   - **outcomes** topics are an exception: they reuse an existing schema and infra-specific variants should **not** be added to `sentry-kafka-schemas`. For an outcomes-style topic, skip Step 1 — confirm the exact handling with the topic owner.
   - If the topic reuses an existing public topic's settings wholesale and adds nothing new to the schema registry, it is really a **private** topic — use `override_topic` (Step 3 only).
4. Locate the repos you'll touch. **Public**: `sentry-kafka-schemas`, `ops`, `sentry`. **Private**: just `ops`. If a needed repo isn't found near the working directory, ask the user for its path. Use `$SCHEMAS`, `$OPS`, `$SENTRY` to refer to them below.
5. **Check for collision in every repo you located** — ask for a different name and do not proceed until it's free:
   - `$OPS/shared_config/kafka/topics/<topic_name>.yaml` and `$OPS/shared_config/kafka/topics/regional_overrides/*/<topic_name>.yaml` (always — covers both private topics and the ops files of deployed public topics).
   - **Public only** (these repos are located only for public): `$SCHEMAS/topics/<topic_name>.yaml`, and the `$SENTRY` `Topic` enum / `KAFKA_TOPIC_TO_CLUSTER` (grep the kebab name in `src/sentry/conf/types/kafka_definition.py` and `src/sentry/conf/server.py`).

Before each repo's work, ensure a clean tree on an updated default branch:

```bash
cd "$REPO"
git stash list && git status --porcelain   # must be clean; stop and ask if not
BASE=$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name')
git checkout "$BASE" && git pull --ff-only
git checkout -b add-kafka-topic-<topic_name>
```

## Step 1: sentry-kafka-schemas PR — *public only*

> **Skip this entire step for private topics.** Private topics are not defined in `sentry-kafka-schemas`.
>
> **Caveat — not every public topic needs a schema entry.** Confirm (Step 0.3) that this topic actually introduces a new schema. **outcomes** topics in particular reuse an existing schema and must not be added to `sentry-kafka-schemas` (infra-specific variants don't belong in the registry that self-hosted consumes). When in doubt, ask the topic owner before creating the file.

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

> **Release dependency**: the new topic only becomes usable downstream once a new `sentry-kafka-schemas` release is published (after this PR merges, per the repo's release process). The ops and sentry PRs still **bump the pin now** to the anticipated next version so the required change is visible in the diff — see Steps 3 and 4.
>
> Compute the anticipated version: take the latest released version and increment the patch (`git -C $SCHEMAS tag --sort=-v:refname | head -1` → e.g. `2.1.35` → `2.1.36`). Releases are manually versioned, so always note in the PR that this is the *anticipated* version and must be confirmed/adjusted to match the actual published release before merge. Call this `<next-version>` below.

## Step 2: Choose regions, partitions, and clusters

1. Build the **candidate region set**. Do **not** assume every folder under `regional_overrides/`. Start from a comparable existing topic — list which regions a sibling topic defines:
   ```bash
   for d in "$OPS"/shared_config/kafka/topics/regional_overrides/*/; do
     [ -f "$d/<sibling_topic>.yaml" ] && basename "$d"
   done
   ```
   The `control` region typically does **not** carry these topics (it only has `taskworker-control*` topics) — exclude it unless the sibling topic includes it.
2. **STOP and ask the user which regions the topic should be enabled in.** This is a required gate — never infer the enabled set from a reference topic, even when the user said "use the same values as `<topic>`" (that covers partitions/cluster/schema defaults, not enablement). Wait for an explicit answer before continuing.
3. The **file set** — regions that get an override file — is the candidate set **plus every region the user enabled** (an enabled region must always get a file, even if the sibling topic did not define it). For each **enabled** region, prompt for:
   - **Number of partitions** in that region
   - **Cluster** — present the valid choices for that region:
     ```bash
     grep -rh '^cluster:' "$OPS/shared_config/kafka/topics/regional_overrides/<region>/" | sort -u
     ```

Every region in the file set that is **not** enabled gets `disabled: true` (Step 3).

## Step 3: ops PR

In `$OPS`:

1. **Default partitions** — create `shared_config/kafka/topics/<topic_name>.yaml`:
   ```yaml
   partitions: {default_partitions}
   ```
2. **Per-region overrides** — for **each region in the file set from Step 2** (not every folder; `control` is normally excluded), create `shared_config/kafka/topics/regional_overrides/<region>/<topic_name>.yaml`:
   - Region **not** enabled by the user → contents are exactly:
     ```yaml
     disabled: true
     ```
   - Region **enabled** → write `cluster:`; for **private** topics also add `override_topic: <override_topic>`; add `partitions:` only when the region's partitions differ from the default.
     - Public, partitions == default → only `cluster: {cluster_name}`
     - Public, partitions differ:
       ```yaml
       cluster: {cluster_name}
       partitions: {region_partitions}
       ```
     - Private, partitions == default:
       ```yaml
       cluster: {cluster_name}
       override_topic: <override_topic>
       ```
     - Private, partitions differ:
       ```yaml
       cluster: {cluster_name}
       override_topic: <override_topic>
       partitions: {region_partitions}
       ```
3. **Cookiecutter region template** — also create the regional override in the new-region template so future regions get the topic: `cookiecutters/cookiecutter-region/shared_config/kafka/topics/regional_overrides/{{region}}/<topic_name>.yaml`. New regions start disabled, so its contents are exactly:
   ```yaml
   disabled: true
   ```
   (Skipping this is flagged by Warden's `cookiecutter-region-backport` check — see the `taskworker-seer-push.yaml` precedent.)
4. **Register for deployment** — *public only*. Add `<topic_name>` to the `all_deployed_topics:` list in `shared_config/kafka/topics/defaults/all_topics.yaml`. The list is grouped by topic family, not strictly alphabetical — insert it next to its sibling topics (e.g. right after `<sibling_topic>`). **Skip for private topics** — they are intentionally not in `all_topics.yaml`.
5. **Bump the schemas dependency** — *only when Step 1 added a new schema* (i.e. a new `sentry-kafka-schemas` release is required). Update the `sentry-kafka-schemas==` pin in `python/requirements.txt` to `<next-version>` (see the release-dependency note in Step 1). The pin lives only in the compiled `requirements.txt`, not `requirements.in`. **Skip the bump** for private topics and for public topics that reuse an existing schema (Step 1 skipped) — no new release is involved.

> **Do not edit generated/materialized files.** CI regenerates `shared_config/_materialized_configs/`, `k8s/clusters/*/_topicctl_generated.yaml`, `k8s/materialized_manifests/`, and topicctl job manifests via `make materialize`. Only edit the source files above.

Commit and open the PR (drop `python/requirements.txt` from the `git add` for private topics):

```bash
git add shared_config/kafka/topics/ cookiecutters/cookiecutter-region/ python/requirements.txt
git commit -m "feat: deploy <topic_name> topic"
gh pr create --fill --reviewer <owning-team-slug> --title "feat: deploy <topic_name> topic"
```

Capture the PR URL.

## Step 4: sentry PR — *public only*

> **Skip this entire step for private topics.** Private topics are not added to the `sentry` `Topic` enum or `KAFKA_TOPIC_TO_CLUSTER`.

In `$SENTRY`:

1. **`src/sentry/conf/types/kafka_definition.py`** — add an entry to the `class Topic(Enum)`. The **member name** is the topic name in `SCREAMING_SNAKE_CASE` (hyphens → underscores, uppercased); the **value** is the kebab-case topic name. Place it next to its sibling topics (the enum is grouped by family, not strictly alphabetical):
   ```python
   # e.g. topic "taskworker-launchpad-push":
   TASKWORKER_LAUNCHPAD_PUSH = "taskworker-launchpad-push"
   ```
2. **`src/sentry/conf/server.py`** — add an entry to the `KAFKA_TOPIC_TO_CLUSTER` dict next to the sibling entries. Use `"default"` (every current entry maps to `"default"`); if a sibling in the same family ever uses a different value, match that instead:
   ```python
   "<topic_name>": "default",
   ```
3. **Bump the schemas dependency** — *only when Step 1 added a new schema* (skip when the topic reuses an existing schema, e.g. outcomes — no new release exists to pin to). Update `sentry-kafka-schemas>=` in `pyproject.toml` to `<next-version>`, and bump the matching `specifier = ">=..."` line for `sentry-kafka-schemas` in `uv.lock` so the two agree. If `<next-version>` is already published, run `uv lock` to fully regenerate. If it is **not** published yet (the usual case when this PR precedes the schemas release), you cannot regenerate `uv.lock`'s resolved version + wheel hash — leave the `[[package]]` `version`/`wheels` block as-is and note in the PR that `uv lock` must be re-run once the release publishes. See the release-dependency note in Step 1.

Commit and open the PR:

```bash
git add src/sentry/conf/types/kafka_definition.py src/sentry/conf/server.py pyproject.toml uv.lock
git commit -m "feat: register <topic_name> kafka topic"
gh pr create --fill --reviewer <owning-team-slug> --title "feat: register <topic_name> kafka topic"
```

Capture the PR URL.

## Step 5: Report

Return the PR link(s) to the user.

**Private topic** — one PR, no cross-PR dependency:

```
Opened 1 PR for the private `<topic_name>` topic:

1. ops: <url>
   └─ Inherits topic_creation_config from public topic `<override_topic>`.
```

**Public topic with a new schema** (Step 1 produced a PR) — three PRs, **with the dependency ordering** so the user knows what must merge first. The schemas PR must merge and publish a release before the dependency-bump PRs can reference the released version:

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

**Public topic that reuses an existing schema** (Step 1 skipped, e.g. outcomes) — two PRs, **no schemas release and no version bump**, so no cross-PR ordering:

```
Opened 2 PRs for the `<topic_name>` topic:

1. ops: <url>
2. sentry: <url>
```

## Notes

- For commit messages and PR descriptions, you may use the `commit` and `pr-writer` skills to follow Sentry conventions; the commands above are a self-contained fallback.
- When Step 1 adds a new schema, its PR gates the dependency bumps in ops (Step 3) and sentry (Step 4). Bump the pins to the anticipated `<next-version>` anyway so reviewers see the required change; flag in each PR body that the version is anticipated (confirm against the actual release) and, for sentry, that `uv.lock` needs `uv lock` once the release publishes. CI on those PRs may stay red until then. When Step 1 is skipped (private, or public reusing an existing schema), there is no release dependency and no version bump.
