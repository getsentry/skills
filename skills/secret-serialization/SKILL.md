---
name: secret-serialization
description: 'Finds secrets, tokens, passwords, and API keys that can leak through generated serialization: Python dataclass repr and asdict, attrs, pydantic model_dump, NamedTuple, JavaScript JSON.stringify and util.inspect, structured logs, tracing spans, and error reports. Use when asked to "check for secret serialization", "credential in repr", "repr=False audit", "secret in spans", "token in logs", or when a change adds a credential field to a dataclass, model, or config object, or adds code that stringifies whole objects or every kwarg into telemetry.'
allowed-tools: Read Grep Glob
---

# Secret Serialization Review

Find credentials that can leak because a type serializes itself and something upstream serializes whole objects.

A leak usually needs two changes that each look safe alone:

1. **Holder**: a credential is stored as a field on a type with generated `repr`, `str`, `asdict`, `model_dump`, `toJSON`, or property enumeration.
2. **Sink**: logging, tracing, error reporting, caching, or a response serializes whole objects or every kwarg (`str(value)`, `span.set_data(key, obj)`, `logger.info("%s", obj)`, `JSON.stringify(args)`).

The two sides are often written months apart by different authors. Report either side on its own. Always search the existing tree for the other side, because it is frequently already on the default branch and absent from the diff.

## Boundary

- This skill covers indirect leaks through generated serialization and wholesale sinks.
- Direct leaks, such as interpolating a token into a log message, belong to `security-review`. Report them here only when they come from a changed wholesale sink.
- Hardcoded secret literals and committed `.env` files are out of scope.

## References

| Reference | Read When |
|-----------|-----------|
| `references/python.md` | Reviewing Python dataclasses, attrs, pydantic, NamedTuple, msgspec, logging, Sentry SDK, or OpenTelemetry code |
| `references/javascript-typescript.md` | Reviewing JavaScript or TypeScript classes, config objects, `JSON.stringify`, `util.inspect`, pino or winston, or Sentry and OpenTelemetry spans |

## Credential Fields

Treat a field as credential-bearing when its name, type, or source says so:

- Names containing `secret`, `token`, `password`, `passwd`, `pwd`, `api_key`, `apikey`, `access_key`, `private_key`, `signing_key`, `client_secret`, `bearer`, `credential`, `authorization`, `auth_header`, `cookie`, `session_key`, `dsn`, `connection_string`, `webhook_secret`, `hmac`, or `refresh_token`.
- Types such as `SecretStr`, `SecretBytes`, or wrappers around them.
- Values assigned from environment variables, a secrets manager, or a constructor argument named like the above.

## Explicit Exclusion

Separate two kinds of path:

- **Generated paths** are produced by the type itself: `__repr__` and `__str__`, `asdict`, `model_dump`, `toJSON`, and own-enumerable-property walks (`JSON.stringify`, `util.inspect`, spread). They are the holder's responsibility.
- **Raw attribute access** reads the stored value directly: `vars(obj)`, `obj.__dict__`, `pickle`, `json.dumps(obj, default=vars)`. Every stored attribute is exposed this way, whatever flags the field has. Treat these only as sinks: report them when a sink in the repository applies one to a credential-bearing instance.

A field is fully excluded when every generated path its type has is blocked, whether by one mechanism or several together. A field is partially excluded when at least one generated path still includes it. No field-level mechanism defeats raw attribute access. Only not storing the value does, so fix raw attribute findings at the sink.

| Mechanism | Blocks | Still includes the field |
|-----------|--------|---------------------------|
| `dataclasses.field(repr=False)`, `attrs.field(repr=False)` | `__repr__`, `__str__` | `asdict`, `astuple`, raw access |
| Pydantic `Field(repr=False)` | `__repr__`, `__str__` | `model_dump`, `model_dump_json`, response serialization, raw access |
| Pydantic `Field(exclude=True)` | `model_dump`, `model_dump_json`, response serialization | `__repr__`, `__str__`, raw access |
| Pydantic `Field(repr=False, exclude=True)` | Every generated path | Raw access |
| JavaScript `#private` field | Every generated path | Nothing outside the class body |
| `Object.defineProperty(..., { enumerable: false })` | Every generated path | Explicit property reads, `Object.getOwnPropertyNames` |
| Hand-written `__repr__`, `__str__`, `toJSON`, or `[util.inspect.custom]` that omits the field | Only the path it overrides (a `__repr__` also serves `str()` when there is no `__str__`) | Every other generated path, raw access |
| Redacting wrapper: `SecretStr`, `SecretBytes`, a project `Redacted[T]` | Every generated path | `pickle` and recursive `__dict__` walks such as `default=vars`, which reach the value stored inside the wrapper |
| Not stored on the object: read inside the method, or held in a closure | Everything | Nothing |

Do not treat underscore naming, TypeScript `private`, `__slots__`, type annotations, comments, `dataclass(init=False)`, or a custom `__init__` that still assigns the field as blocking any path.

## Investigation Process

1. Read the changed hunk. Find new or modified credential fields on auto-serializing types, and new or modified code that serializes objects or kwargs into logs, spans, error context, caches, queues, or responses.
2. For each credential field, read the full class, decorators, base classes, and model config. List every generated path and check which ones the field's mechanisms block, using the table above.
3. Grep for where instances are constructed and passed. Instances handed to decorators, `**kwargs`, tool call arguments, task payloads, or middleware reach generic sinks.
4. Grep the whole repository for sinks that can see those instances, not only the diff. Useful patterns: `str(value)`, `repr(`, `asdict(`, `model_dump(`, `set_data(`, `set_attribute(`, `set_context(`, `set_extra(`, `JSON.stringify(`, `util.inspect(`, loggers called with objects, and raw attribute access (`vars(`, `__dict__`, `pickle.dumps(`, `default=vars`).
5. For each changed sink, check for a key allowlist, redaction keyed on credential names, or a filter that replaces objects with their type name. Then grep for callers that pass credential-bearing objects into it.
6. Look at tests only to see whether one asserts the credential is absent from the serialized form. A missing test is fix guidance, not a finding.
7. Confirm the code ships. Skip fixtures, examples, generated code, and test-only helpers.

## What To Report

| Category | Report When |
|----------|-------------|
| Unexcluded credential field | A credential field is added or moved onto a type with generated serialization, and no mechanism blocks any of its generated paths. |
| Partial exclusion | At least one generated path still includes the field, and a sink in the repository uses that path on instances of the type. |
| Raw attribute sink | A sink applies `vars`, `__dict__`, `pickle`, or `default=vars` to an instance that stores a credential, even if the field is fully excluded or wrapped. |
| Credential moved onto a holder | A refactor moves a credential from a lazy read or closure onto an object field. |
| Wholesale serialization sink | New or changed telemetry, logging, error-context, cache, or response code serializes every kwarg, every attribute, or whole objects without an allowlist or redaction. |
| Sink loses its filter | A change removes or weakens redaction, an allowlist, or object-to-type-name replacement in an existing sink. |
| Object passed to telemetry | A client, config, or settings object is passed to a span, log, or error-context call that stringifies it. |

## Severity

| Level | Use For |
|-------|---------|
| high | The credential reaches a sink anywhere in the repository: log line, span attribute, error event, cache entry, persisted row, queue payload, or API response. The other side may predate the diff. Also a new wholesale sink whose existing callers pass credential-bearing objects. |
| medium | An unexcluded credential field whose instances leave the constructing module, after a repository search found no sink. Also a wholesale sink with no allowlist and no traced credential-bearing caller. |
| low | An unexcluded credential field whose instances never leave the constructing scope. |

- Do not downgrade because the sink or the holder is outside the diff. That is the normal shape of this bug.
- Choose the lower severity when reachability depends on unproven preconditions.

## What Not To Report

- Fully excluded fields, unless a raw attribute sink receives the instance.
- Partial exclusions when no sink in the repository uses the unblocked path.
- Credentials read inside a method and never stored on the instance.
- Placeholder or fake values in tests, fixtures, or examples.
- Types with no generated serialization and no `__dict__` or enumeration sink.
- Sinks that already allowlist scalar keys, redact by credential name, or replace objects with a type name.
- Pre-existing fields and sinks the diff does not touch, unless the diff connects them.
- Style, naming, or missing-test-only observations.

## Fix Guidance

Include one concrete fix per finding:

- Holder: block every generated path, wrap the value in a redacting type, or stop storing it on the object.
- Raw attribute sink: serialize an explicit allowlisted dict instead of the instance, or stop storing the credential on it. A field flag or wrapper does not fix it.
- Sink: allowlist scalar keys, redact keys matching credential names, and record `type(value).__name__` instead of `str(value)` for non-scalar values.
- Regression test: serialize an instance with the same serializer the sink uses (for example `sentry_sdk.serializer.serialize`, `json.dumps(asdict(obj))`, `JSON.stringify(obj)`, `util.inspect(obj)`) and assert the credential string is absent.

## Finding Format

- Title: name the field or sink and the leak path, for example "`_shared_secret` included in `RpcClient` dataclass repr".
- Description: one or two sentences naming the generated path that exposes the credential, where instances travel, and the fix.
- Evidence: 2 to 5 bullets naming the class, decorator, generated paths checked, the exclusion looked for, and every sink or caller traced, including those outside the diff.
