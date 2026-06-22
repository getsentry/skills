# Create Kafka Topic Specification

## Intent

The `create-kafka-topic` skill provisions a brand-new Kafka topic across the four repos that must all agree for a Sentry topic to exist and deploy: `sentry-kafka-schemas` (schema + ownership), `ops` (deployment/partition/region config), `sentry` (topic enum + cluster mapping), and `getsentry` (cell-silo cluster mapping).

Its main job is to turn a topic name and a few deployment choices into one correct, reviewable PR per repo, matching the conventions of the topics that already exist, and to hand the user the resulting PR links.

## Scope

In scope:

- Prompting for the topic name, default partition count, owning team, and per-region enablement/partitions/cluster.
- Creating the schema file and CODEOWNERS entry in `sentry-kafka-schemas`.
- Creating the default partition file, per-region override files, and `all_topics.yaml` entry in `ops`, plus the `sentry-kafka-schemas` requirement bump.
- Adding the `Topic` enum entry and `KAFKA_TOPIC_TO_CLUSTER` entry in `sentry`, plus the `sentry-kafka-schemas` dependency bump.
- Adding the topic→cluster entry in `getsentry`'s `cellsilo.py`.
- Opening one PR per repo and reporting all four URLs.

Out of scope:

- Editing generated/materialized config (CI regenerates ops `_materialized_configs/`, `k8s/`, and topicctl manifests via `make materialize`).
- Publishing the `sentry-kafka-schemas` release that the dependency bumps depend on.
- Writing producer/consumer application code or schema definitions themselves.
- Modifying or migrating existing topics.

## Users And Trigger Context

- Primary users: Sentry engineers (and coding agents) standing up a new Kafka topic.
- Common requests: "create a new Kafka topic", "add a Kafka topic", "register a Kafka topic", "set up a new Kafka topic".
- Should not trigger for: changing an existing topic's partitions/clusters, debugging consumers, or general Kafka questions.

## Runtime Contract

- Required first actions: prompt for topic name, default partitions, and owning team; locate all four repos; verify the topic name is not already taken in `sentry-kafka-schemas/topics/`.
- Per-repo precondition: a clean working tree on an updated default branch before creating the topic branch.
- Required outputs: four pull requests (one per repo) plus the four URLs returned to the user.
- Non-negotiable constraints:
  - Do not edit generated/materialized files in `ops`.
  - Per-region override contents follow the exact rules: `disabled: true` when not enabled; `cluster:` only when enabled and partitions equal the default; `cluster:` + `partitions:` when they differ.
  - The `getsentry` cluster value is a real cluster name (e.g. `kafka-small`), never `"default"`, and may differ from the ops cluster name.
  - Insert enum / `all_topics.yaml` entries next to sibling topics (grouped by family), not alphabetically.
  - Confirm the generated schema file with the user before opening the first PR.
- Sequencing: the schemas PR gates the dependency bumps in `sentry`/`ops`, which reference the released schema version; these may need to follow the schemas release.
- Expected bundled files loaded at runtime: only `SKILL.md`.

## Evaluation

A run is correct when:

- All four PRs are opened, each containing only the source-of-truth changes for its repo (no generated files).
- The schema YAML, region overrides, enum entry, and cluster mappings match the conventions of comparable existing topics.
- The user receives four working PR links.

Reference example: the `taskworker-ingest-push` topic was created via getsentry/sentry-kafka-schemas#484, getsentry/ops#20917, getsentry/sentry#117135, and getsentry/getsentry#20495 — the skill should reproduce that same change set for an equivalent topic.

## Limitations

- Cannot determine the released `sentry-kafka-schemas` version until that release is published; the dependency bumps may be deferred.
- Relies on a sibling topic to infer the correct region set and good field values; an entirely novel topic shape may need extra user input.
- Does not run repo test suites or CI; reviewers/CI validate the generated config.

## Maintenance

- If the four-repo wiring changes (new repo, renamed config dict, new required file), update the corresponding step and this spec.
- If `ops` changes how regions or clusters are configured, update Steps 2–3.
- Keep the reference example current if the canonical topic-creation PR set changes.
