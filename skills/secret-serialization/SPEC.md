# Secret Serialization Skill Specification

## Intent

`secret-serialization` catches credentials that leak through generated serialization. The leak needs a holder (a credential field on a type with generated `repr`, `asdict`, `model_dump`, or property enumeration) and a sink (code that serializes whole objects or every kwarg into logs, spans, errors, caches, or responses). The two sides are usually added separately, and each looks safe in its own diff.

The skill reports either side alone and searches the whole repository for the other side, so a leak is caught whichever half lands second.

## Scope

In scope:

- Credential fields on auto-serializing types in Python and JavaScript/TypeScript.
- Partial exclusions, where one generated path is blocked and another is not.
- New or changed wholesale serialization sinks and weakened sink filters.

Out of scope:

- Direct interpolation of a secret into a log or response. `security-review` covers that.
- Hardcoded secret literals and committed `.env` files. Secret scanners cover those.
- Secrets-manager architecture advice with no changed field or sink.
- Missing tests as a standalone finding.

## Users And Trigger Context

- Primary users: Warden runs in repositories that keep credentials on client, config, or settings objects, added with `remote = "getsentry/skills"`, and engineers reviewing such changes locally.
- Should trigger for: "secret serialization", "credential in repr", "repr=False", "SecretStr", "token in logs", "secret in spans", "dataclass secret field", "kwargs stringified into telemetry", "asdict leaks", "JSON.stringify config".
- Should not trigger for: general security review, hardcoded-secret scanning, or dataclass refactors with no credential fields.

This is opt-in and specialized. It reports an unexcluded credential field before a sink is proven, which is too noisy for a default review of every repository.

## Runtime Contract

- Required first actions: find changed credential fields and changed sinks in the diff, then read the full class or sink and enumerate generated paths.
- Required evidence per finding: the field or sink, the generated path or serialization call, the exclusion looked for, and where instances travel or what the sink receives, including code outside the diff.
- Constraints:
  - Keep `allowed-tools` space-delimited (`Read Grep Glob`). Warden drops comma-suffixed tokens such as `Read,`, which leaves the agent with only `find` and `ls` and caps every finding at medium because no sink can be traced.
  - Do not downgrade because the other side predates the diff.
  - Judge holders by generated paths only (`__repr__`, `asdict`, `model_dump`, `toJSON`, enumeration). A field is fully excluded when its mechanisms together block all of them.
  - Treat raw attribute access (`vars`, `__dict__`, `pickle`, `default=vars`) as a sink category. No field flag or wrapper defeats it, so it never makes a fully excluded holder partial.
  - Do not treat underscore naming, TypeScript `private`, `__slots__`, or a custom `__init__` as blocking any path. Pydantic `Field(exclude=True)` or `Field(repr=False)` alone is partial.
  - Keep language-specific tables and examples in `references/`.

## Source And Evidence Model

See `SOURCES.md`. Do not store secrets, customer data, span payloads, or internal repository identifiers in this skill.

## Reference Architecture

- `SKILL.md`: threat model, boundary with `security-review`, credential heuristics, exclusion rules, investigation steps, report table, severity, exclusions, fix guidance, finding format.
- `references/python.md`: generated paths and exclusions per Python type, sink table, report and do-not-report examples, regression test shape.
- `references/javascript-typescript.md`: the same for JavaScript and TypeScript.

## Validation

- Run `uv run scripts/quick_validate.py ../secret-serialization` from `skills/skill-writer`.
- Manual check against the incident shape: a diff that adds an unexcluded credential field to a dataclass, with a pre-existing `str(value)` kwarg sink elsewhere in the repository, should produce a high finding naming both.
- Precision checks: `SecretStr`, `#private`, a lazily read `property`, a filtered sink, and `Field(repr=False, exclude=True)` with only repr or `model_dump` sinks should produce no finding.
- Recall checks: `Field(exclude=True)` alone on a model passed to `str()` should produce a partial-exclusion finding. Any credential-bearing instance, including a fully excluded or `SecretStr` one, passed to `pickle` or `default=vars` should produce a raw attribute sink finding.

## Known Limitations

- Credential detection depends on names, types, and sources. Oddly named credential fields are missed unless their source is an obvious secret read.
- Behavior of third-party serializers is limited to what the references document.
- Go, Java, and Rust are not covered by references. The core contract still applies.

## Maintenance Notes

- Update `SKILL.md` when exclusion rules, severity, or the report table change.
- Update `references/` when a new serializer or sink causes a real leak or a repeated false positive.
- Record each incident or review outcome that changes a decision in `SOURCES.md`.
