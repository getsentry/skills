# Secret Serialization Skill Sources

## Source Inventory

| Source | Trust tier | Confidence | Usage constraints | Decisions |
|--------|------------|------------|-------------------|-----------|
| Internal Sentry incident: an RPC client's shared secret reached tracing spans | Internal incident | High | Mechanism only. No repository names, PR links, secrets, or span data in this public repo. | Two-sided threat model; report each side alone; search the repository for the other side; require exclusion on every generated path; recommend a serializer-based regression test. |
| Python `dataclasses`, `attrs`, `pydantic`, and `functools.cached_property` documentation, checked against Pydantic 2.11 | Official docs and runtime | High | Summarize as tables. | `repr=False` covers repr only; `asdict` has no field exclusion; `cached_property` writes to `__dict__`; `SecretStr` redacts repr, str, and `model_dump`, but `pickle` and a recursive `default=vars` walk reach its raw value. Pydantic `Field(exclude=True)` leaves the raw value in `__repr__` and `__str__`. `Field(repr=False)` leaves it in `model_dump`. Both flags together block every generated path and still leave the value in `__dict__` and `pickle`. |
| Sentry Python SDK serializer and `include_local_variables` behavior | Official docs and SDK source | High | Treat as a sink, not an SDK bug. | Exception frames are a sink for any credential holder in scope. The serializer renders unknown objects with `safe_repr`, not a `__dict__` walk, so it follows generated repr exclusions. |
| Node `util.inspect`, `JSON.stringify`, and `#private` field semantics | Official docs | High | Summarize as tables. | TypeScript `private` is not an exclusion; `#private` is; `toJSON` alone is partial when inspect or logger sinks exist. |
| `security-review` skill in this repo | Local prior art | High | Avoid overlap. | Direct secret logging stays in `security-review`; this skill covers generated serialization and wholesale sinks. |

## Incident Mechanism

1. A tool-tracing decorator recorded every tool kwarg with `str(value)` into a span attribute. It was harmless while no kwarg object held a secret.
2. Much later, a refactor moved the shared secret from a lazy environment read onto a dataclass field of the RPC client, without `field(repr=False)`. The client was passed to tools as a kwarg.
3. The generated `__repr__` included the secret, and the decorator wrote it into spans.
4. The fix added `field(repr=False)` to the credential fields and a test that runs `sentry_sdk.serializer.serialize` over the client and asserts the secret is absent.

Neither change looked dangerous in its own diff, and the sink was already on the default branch when the field was added.

## Source-Backed Decisions

1. Report the holder without a proven sink.
   - Reason: the sink predated the field and lived in another module.
   - Decision: an unexcluded credential field is medium when instances leave the module and no sink is found, and high when a sink is found anywhere in the repository.
2. Report the sink without a proven credential input.
   - Reason: the wholesale `str(value)` sink was harmless until an unrelated change.
   - Decision: a wholesale sink without an allowlist is medium on its own.
3. Search beyond the diff and do not downgrade for it.
   - Reason: diff-only review marked each half safe, and consumers commonly publish only high findings.
   - Decision: the investigation greps the repository for the other side, and severity follows what it finds.
4. Treat partial exclusion as a finding.
   - Reason: `repr=False` is the reflexive fix and does not cover `asdict`, `__dict__`, or pickle.
   - Decision: severity follows the unblocked path.
5. Name the sink's serializer in the regression test.
   - Reason: a `repr` check alone misses `__dict__`-based serializers.
6. Do not treat a single Pydantic field flag as exclusion.
   - Reason: a review treated `Field(exclude=True)` as complete. On Pydantic 2.11, `str(model)` and `repr(model)` still contain that field, which is the span path this skill targets. `Field(repr=False)` still appears in `model_dump`. Setting both flags covers those paths and does not clear `__dict__`.
   - Decision: accept `Field(repr=False, exclude=True)` together, or `SecretStr` / `SecretBytes`, as fully excluding generated paths. Report either flag alone at the severity of the unblocked path.
7. Treat raw attribute access as a sink, not as a generated path.
   - Reason: a follow-up review found the skill both accepted `Field(repr=False, exclude=True)` and called a leftover `__dict__` path partial. Every stored attribute is in `__dict__`, so counting it as a generated path would make every field-level mechanism, including the incident's `repr=False` fix, fail.
   - Decision: judge holders by generated paths only. Report `vars`, `__dict__`, `pickle`, and `default=vars` as a raw attribute sink finding when they receive a credential-bearing instance, whatever its field flags or wrapper.
8. Report a partial exclusion only when a sink uses the unblocked path.
   - Reason: the report table required a sink while the severity table also listed a sinkless low partial exclusion. The incident eval expects no findings for `repr=False` fields with only a repr-based sink.
   - Decision: drop the sinkless low case.

## Evaluation Runs

Warden `pi` runtime, `openrouter/x-ai/grok-4.5`, effort `high`, against the original internal repository.

| Case | Expected | Result |
|------|----------|--------|
| Incident diff: two credential fields added to dataclass RPC clients, `str(value)` kwarg sink already on the default branch | High findings naming both fields and the sink | Pass, twice. 3 and 4 high findings; every finding traced tool kwarg, tracing decorator, `str(value)`, span attribute. |
| Same diff with `field(repr=False)` on both fields | No findings | Pass. No findings. |
| Unrelated diff adding seven `*_tokens` usage-count fields to an LLM proxy model | No findings | Pass. No findings across 22 hunks. |

Observations:

1. With comma-delimited `allowed-tools`, the same incident run produced only 2 medium findings: the agent had no `read` or `grep`, so it could not trace the sink. Fixed by switching to space-delimited tools.
2. Call-site hunks that pass a credential into the constructor produce extra findings for the same field. Warden analyzes hunks independently, so a per-hunk dedupe instruction did not help and was removed. These are duplicates, not false positives.
3. Substring name matching did not cause false positives on LLM token counters in this run, so the name list was left unchanged.

## Open Gaps

- Sample size is one positive and two negative cases on one model. Add more negative diffs, such as OAuth request models that legitimately serialize a token into an outbound request body, before relying on precision.
- Not yet run on Claude models.
- Add Go, Java, or Rust references only if findings in those languages recur.
