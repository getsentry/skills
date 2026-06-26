# Create Kafka Topic Specification

## Intent

The `create-kafka-topic` skill provisions a brand-new Kafka topic. There are two paths, chosen up front:

- **Public** (available to self-hosted): spans the three repos that must agree for a public topic to exist and deploy — `sentry-kafka-schemas` (schema + ownership), `ops` (deployment/partition/region config), and `sentry` (topic enum + cluster mapping). Three PRs.
- **Private** (internal regions only): defined solely in `ops`, inheriting `topic_creation_config` from an existing public topic via `override_topic`. It is not in `sentry-kafka-schemas`, the `sentry` `Topic` enum, or `all_topics.yaml`. One PR (ops only).

`getsentry` is intentionally **not** in scope for either path: it no longer maintains a per-topic cluster map by hand — it loads `KAFKA_TOPIC_TO_CLUSTER` at runtime from the topicctl-generated YAML mounted by ops (getsentry/getsentry#20512, #20661).

Its main job is to turn a topic name and a few deployment choices into one correct, reviewable PR per touched repo, matching the conventions of the topics that already exist, and to hand the user the resulting PR links.

## Scope

In scope:

- Determining whether the topic is public or private, and for private topics the `override_topic` (an existing public topic).
- Prompting for the topic name, default partition count, owning team, and per-region enablement/partitions/cluster.
- **Public:** schema file + CODEOWNERS entry in `sentry-kafka-schemas`; default partition file, per-region overrides, cookiecutter-region template override, `all_topics.yaml` entry, and `sentry-kafka-schemas` requirement bump in `ops`; `Topic` enum + `KAFKA_TOPIC_TO_CLUSTER` entry + dependency bump in `sentry`. Three PRs.
- **Private:** in `ops` only — per-region overrides carrying `cluster:` + `override_topic:` (+ optional `partitions`), default partition file, and cookiecutter-region template override. No `all_topics.yaml` entry, no schemas/sentry changes, no version bump. One PR.
- Opening one PR per touched repo, each with the owning team as reviewer, and reporting the URLs.

Out of scope:

- Editing `getsentry` config (it derives the cluster map from the ops-generated YAML at runtime; no per-topic change is needed).
- Editing generated/materialized config (CI regenerates ops `_materialized_configs/`, `k8s/`, and topicctl manifests via `make materialize`).
- Publishing the `sentry-kafka-schemas` release that the dependency bumps depend on.
- Writing producer/consumer application code or schema definitions themselves.
- Modifying or migrating existing topics.

## Users And Trigger Context

- Primary users: Sentry engineers (and coding agents) standing up a new Kafka topic.
- Common requests: "create a new Kafka topic", "add a Kafka topic", "register a Kafka topic", "set up a new Kafka topic" (public or private).
- Should not trigger for: changing an existing topic's partitions/clusters, debugging consumers, or general Kafka questions.

## Runtime Contract

- Required first actions: determine public vs private; prompt for topic name, default partitions, a reference/sibling topic, and owning team (and, for private, the `override_topic`); for public, confirm a new schema is actually needed (outcomes topics are an exception); locate the repos for the chosen path; verify the name is free across **all** locations (`sentry-kafka-schemas/topics/`, `ops` default + regional override paths, and the `sentry` `Topic` enum / `KAFKA_TOPIC_TO_CLUSTER`).
- Per-repo precondition: a clean working tree on an updated default branch before creating the topic branch.
- Required outputs: public → three PRs (one per repo); private → one ops PR. Each PR has the owning team requested as a reviewer; return the URL(s).
- Non-negotiable constraints:
  - Always ask the user which regions to enable; never infer the enabled set from a reference topic, even when told to "use the same values as `<topic>`".
  - Do not edit generated/materialized files in `ops`, and do not edit `getsentry`.
  - Per-region override contents: `disabled: true` when not enabled. When enabled, `cluster:` (+ `partitions:` only if it differs from the default); **private topics also include `override_topic: <override_topic>`**.
  - Private topics: ops PR only — no `sentry-kafka-schemas` change, no `sentry` change, no `all_topics.yaml` entry, no version bump. The `override_topic` must be an existing public topic in `all_topics.yaml`.
  - Insert enum / `all_topics.yaml` entries next to sibling topics (grouped by family), not alphabetically.
  - Confirm the generated schema file with the user before opening the first PR (public).
- Sequencing (public only): the schemas PR gates the dependency bumps in `sentry`/`ops`. The ops/sentry PRs still bump the pin to the anticipated next version (latest released patch + 1) so the required change is visible; the PR body must flag it as anticipated and, for sentry, note that `uv.lock` must be regenerated with `uv lock` once the release publishes. Private topics have no such dependency.
- Expected bundled files loaded at runtime: only `SKILL.md`.

## Evaluation

A run is correct when:

- The right PRs are opened for the path (public → three; private → one ops PR), each containing only the source-of-truth changes for its repo (no generated files).
- The schema YAML, region overrides, enum entry, and cluster mappings match the conventions of comparable existing topics; private overrides carry `override_topic` pointing at an existing public topic.
- The enabled-region set matches what the user explicitly chose (not a reference topic's set).
- The user receives the correct PR link(s).

Reference examples:
- Public: `taskworker-ingest-push` — getsentry/sentry-kafka-schemas#484, getsentry/ops#20917, getsentry/sentry#117135 (its getsentry/getsentry#20495 predates the loader change and is no longer needed).
- Public: `taskworker-launchpad-push` — getsentry/sentry-kafka-schemas#490, getsentry/ops#21361, getsentry/sentry#118161 (s4s2-only enablement, schemas-release-deferred version bumps).
- Private (override_topic): `ops` `regional_overrides/us/taskworker-subscriptions-dlq.yaml` (`cluster: kafka-small` + `override_topic: taskworker-dlq`), not present in `all_topics.yaml` or `sentry`.

## Limitations

- The exact published `sentry-kafka-schemas` version is not known until release (versioning is manual); the skill bumps to the anticipated patch increment, which must be confirmed against the actual release. Sentry's `uv.lock` resolved entry + wheel hash cannot be regenerated until the release publishes.
- Relies on a sibling topic to infer the correct region set and good field values; an entirely novel topic shape may need extra user input.
- Does not run repo test suites or CI; reviewers/CI validate the generated config.

## Maintenance

- If the public three-repo wiring changes (new repo, renamed config dict, new required file, or getsentry again needing a per-topic edit), update the corresponding step and this spec.
- If the private-topic mechanism changes (e.g. `override_topic` semantics in `topic_builder.libsonnet`, or private topics start requiring schema/sentry entries), update Steps 0/3 and this spec.
- If `ops` changes how regions or clusters are configured, update Steps 2–3.
- Keep the reference example current if the canonical topic-creation PR set changes.
