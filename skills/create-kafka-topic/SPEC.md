# Create Kafka Topic Specification

## Intent

The `create-kafka-topic` skill provisions a brand-new Kafka topic across the three repos that must all agree for a Sentry topic to exist and deploy: `sentry-kafka-schemas` (schema + ownership), `ops` (deployment/partition/region config), and `sentry` (topic enum + cluster mapping).

`getsentry` is intentionally **not** in scope: it no longer maintains a per-topic cluster map by hand — it loads `KAFKA_TOPIC_TO_CLUSTER` at runtime from the topicctl-generated YAML mounted by ops (getsentry/getsentry#20512, #20661).

Its main job is to turn a topic name and a few deployment choices into one correct, reviewable PR per repo, matching the conventions of the topics that already exist, and to hand the user the resulting PR links.

## Scope

In scope:

- Prompting for the topic name, default partition count, owning team, and per-region enablement/partitions/cluster.
- Creating the schema file and CODEOWNERS entry in `sentry-kafka-schemas`.
- Creating the default partition file, per-region override files, the cookiecutter-region template override (`disabled: true`), and `all_topics.yaml` entry in `ops`, plus the `sentry-kafka-schemas` requirement bump.
- Adding the `Topic` enum entry and `KAFKA_TOPIC_TO_CLUSTER` entry in `sentry`, plus the `sentry-kafka-schemas` dependency bump.
- Opening one PR per repo and reporting all three URLs.

Out of scope:

- Editing `getsentry` config (it derives the cluster map from the ops-generated YAML at runtime; no per-topic change is needed).
- Editing generated/materialized config (CI regenerates ops `_materialized_configs/`, `k8s/`, and topicctl manifests via `make materialize`).
- Publishing the `sentry-kafka-schemas` release that the dependency bumps depend on.
- Writing producer/consumer application code or schema definitions themselves.
- Modifying or migrating existing topics.

## Users And Trigger Context

- Primary users: Sentry engineers (and coding agents) standing up a new Kafka topic.
- Common requests: "create a new Kafka topic", "add a Kafka topic", "register a Kafka topic", "set up a new Kafka topic".
- Should not trigger for: changing an existing topic's partitions/clusters, debugging consumers, or general Kafka questions.

## Runtime Contract

- Required first actions: prompt for topic name, default partitions, and owning team; locate all three repos; verify the topic name is not already taken in `sentry-kafka-schemas/topics/`.
- Per-repo precondition: a clean working tree on an updated default branch before creating the topic branch.
- Required outputs: three pull requests (one per repo), each with the owning team requested as a reviewer, plus the three URLs returned to the user.
- Non-negotiable constraints:
  - Always ask the user which regions to enable; never infer the enabled set from a reference topic, even when told to "use the same values as `<topic>`".
  - Do not edit generated/materialized files in `ops`, and do not edit `getsentry`.
  - Per-region override contents follow the exact rules: `disabled: true` when not enabled; `cluster:` only when enabled and partitions equal the default; `cluster:` + `partitions:` when they differ.
  - Insert enum / `all_topics.yaml` entries next to sibling topics (grouped by family), not alphabetically.
  - Confirm the generated schema file with the user before opening the first PR.
- Sequencing: the schemas PR gates the dependency bumps in `sentry`/`ops`. The ops/sentry PRs still bump the pin to the anticipated next version (latest released patch + 1) so the required change is visible; the PR body must flag it as anticipated and, for sentry, note that `uv.lock` must be regenerated with `uv lock` once the release publishes.
- Expected bundled files loaded at runtime: only `SKILL.md`.

## Evaluation

A run is correct when:

- All three PRs are opened, each containing only the source-of-truth changes for its repo (no generated files).
- The schema YAML, region overrides, enum entry, and cluster mappings match the conventions of comparable existing topics.
- The enabled-region set matches what the user explicitly chose (not a reference topic's set).
- The user receives three working PR links.

Reference examples:
- `taskworker-ingest-push` — getsentry/sentry-kafka-schemas#484, getsentry/ops#20917, getsentry/sentry#117135 (its getsentry/getsentry#20495 predates the loader change and is no longer needed).
- `taskworker-launchpad-push` — getsentry/sentry-kafka-schemas#490, getsentry/ops#21361, getsentry/sentry#118161 (s4s2-only enablement, schemas-release-deferred version bumps).

## Limitations

- The exact published `sentry-kafka-schemas` version is not known until release (versioning is manual); the skill bumps to the anticipated patch increment, which must be confirmed against the actual release. Sentry's `uv.lock` resolved entry + wheel hash cannot be regenerated until the release publishes.
- Relies on a sibling topic to infer the correct region set and good field values; an entirely novel topic shape may need extra user input.
- Does not run repo test suites or CI; reviewers/CI validate the generated config.

## Maintenance

- If the three-repo wiring changes (new repo, renamed config dict, new required file, or getsentry again needing a per-topic edit), update the corresponding step and this spec.
- If `ops` changes how regions or clusters are configured, update Steps 2–3.
- Keep the reference example current if the canonical topic-creation PR set changes.
