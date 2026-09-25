# Secret Serialization Skill Sources

## Source Inventory

| Source | Trust tier | Confidence | Usage constraints | Decisions |
|--------|------------|------------|-------------------|-----------|
| Internal Sentry incident: an RPC client's shared secret reached tracing spans | Internal incident | High | Mechanism only. No repository names, PR links, secrets, or span data in this public repo. | Two-sided threat model; report each side alone; search the repository for the other side; require exclusion on every generated path; recommend a serializer-based regression test. |
| Python `dataclasses`, `attrs`, `pydantic`, and `functools.cached_property` documentation | Official docs | High | Summarize as tables. | `repr=False` covers repr only; `asdict` has no field exclusion; `cached_property` writes to `__dict__`; `SecretStr` is an accepted exclusion. |
| Sentry Python SDK serializer and `include_local_variables` behavior | Official docs and SDK source | High | Treat as a sink, not an SDK bug. | Exception frames are a sink for any credential holder in scope. |
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

## Open Gaps

- No recorded runs yet against real repositories. Capture sanitized positive and negative examples before adding `references/evidence/`.
- Add Go, Java, or Rust references only if findings in those languages recur.
