# Python Secret Serialization Notes

Use this when reviewing Python code. These notes refine the core skill; they do not add reporting scope. "Generated paths" and "raw attribute access" have the meanings defined in `SKILL.md` under Explicit Exclusion.

## Generated Serialization Paths

| Type | Generated paths that include every field by default | What blocks them |
|------|------------------------------------------------------|------------------|
| `@dataclasses.dataclass` | `__repr__` (so `str()`, f-strings, `%s`, `%r`), `dataclasses.asdict`, `dataclasses.astuple` | `field(repr=False)` blocks repr only. Nothing blocks `asdict`; wrap the value or keep it off the instance. |
| `attrs` `@define` / `@attr.s` | `__repr__`, `attrs.asdict`, `attrs.astuple` | `field(repr=False)` blocks repr only. `asdict` still includes the field unless the call passes `filter=`. |
| `pydantic.BaseModel` | `__repr__`, `__str__`, `model_dump`, `model_dump_json`, `.dict()`, `.json()`, FastAPI response serialization | `SecretStr` / `SecretBytes` redact all of these (`**********`). `Field(repr=False)` blocks `__repr__` and `__str__`. `Field(exclude=True)` blocks dump, JSON, and response serialization. A plain field is fully excluded only with both flags. |
| `pydantic_settings.BaseSettings` | Same as `BaseModel`; often logged wholesale at startup | `SecretStr` for every credential setting. Plain fields follow the `BaseModel` flag rules. |
| `typing.NamedTuple` | `__repr__`, `_asdict`, iteration and unpacking | None. Do not hold credentials on a NamedTuple. |
| `TypedDict` / `dict` | `repr`, `json.dumps`, iteration | None. Redact at the sink. |
| `msgspec.Struct` | `__repr__`, `msgspec.to_builtins`, encoders | `field(repr=False)` on newer versions blocks repr only. |
| Plain class | None. The default repr is `<Class object at 0x...>`. | Nothing to block. A hand-written `__repr__` that prints fields creates a generated path. |

Every stored attribute on these types, including one with `repr=False`, `exclude=True`, or both, is still visible through raw attribute access. `SecretStr` hides the value from `repr`-based rendering of `vars(obj)`, but `pickle` and a recursive `default=vars` walk still reach the raw string stored inside the wrapper.

`dataclass(init=False)` with a hand-written `__init__` still generates `__repr__` and still registers annotated fields with `asdict`. A custom constructor blocks nothing.

`functools.cached_property` stores its result in `instance.__dict__` after first access. It does not appear in the generated `__repr__` or in `asdict`, so it matters only when a raw attribute sink receives the instance.

The Sentry SDK serializer, used for span data, `set_context`, `set_extra`, and exception frame locals, renders unknown objects with `repr()`. It does not walk `__dict__`. A fully excluded field does not reach Sentry through that serializer.

## High-Signal Sinks

| Sink | Why it leaks | Safe form |
|------|--------------|-----------|
| `safe_kwargs[key] = str(value)` over `**kwargs` | Stringifies client and config objects passed as tool or task arguments | Allowlist scalar keys; record `type(value).__name__` for objects; redact keys matching credential names |
| `span.set_data(key, obj)`, `set_context(name, obj)`, `set_extra` | The Sentry serializer renders objects with `repr()` | Pass explicit scalar fields only |
| `span.set_attribute(key, str(obj))` in OpenTelemetry | OpenTelemetry drops non-primitive values, so callers stringify with `str()` or `json.dumps` first | Pass explicit scalar fields only |
| `logger.info("... %s", obj)`, `{obj}` in f-strings, `logger.exception(...)` | Interpolates `__repr__`; Sentry `include_local_variables=True` (the default) captures frame locals by repr on exceptions | Log identifiers, not objects; exclude credential fields from repr |
| `json.dumps(obj, default=str)`, `default=repr` | Falls back to repr for unknown objects | An explicit `to_dict()` with an allowlist |
| `json.dumps(obj, default=vars)`, `vars(obj)`, `obj.__dict__` into a log, span, or payload | Raw attribute access, including fully excluded fields, cached properties, and the value inside a `SecretStr` when the walk recurses | An explicit `to_dict()` with an allowlist |
| `dataclasses.asdict(obj)` / `model.model_dump()` into a response, cache, or queue | Includes every field regardless of `repr=False` | `exclude={...}` or a separate public DTO |
| `pickle.dumps(obj)` into Redis or a task queue | Raw attribute access: serializes `__dict__`, including fully excluded fields and cached properties | Rebuild clients from config at the consumer |
| `pprint`, `print(obj)` in shipped code | repr | Remove, or log identifiers |
| `rich.inspect(obj)` in shipped code | Raw attribute access: lists attribute values | Remove |

## Examples

**Report (high): credential field added to a dataclass that existing instrumentation stringifies**

```python
@dataclasses.dataclass(init=False)
class RpcClient:
    referrer: str
    _base_url: str | None
    _shared_secret: str | None   # new field, no repr=False

    def __init__(self, referrer, *, base_url=None, shared_secret=None):
        self.referrer = referrer
        self._base_url = base_url
        self._shared_secret = shared_secret
```

```python
# tracing.py, already on the default branch, not in this diff
for key, value in kwargs.items():
    safe_kwargs[key] = str(value)          # rpc_client=RpcClient(...) lands here
span.set_data("gen_ai.tool.call.arguments", safe_kwargs)
```

Evidence: `str(rpc_client)` renders `RpcClient(referrer=..., _base_url=..., _shared_secret='...')`. The tool-tracing decorator passes every kwarg through `str()` into a span attribute, and tools receive `rpc_client` as a kwarg. Fix: `_shared_secret: str | None = dataclasses.field(repr=False)`, and have the sink record `type(value).__name__` for non-scalar values.

**Report (medium): unexcluded field, instances travel, no sink found**

```python
@dataclass
class WebhookConfig:
    url: str
    signing_secret: str

def register(config: WebhookConfig) -> None:
    dispatcher.enqueue("register_webhook", config=config)
```

Evidence: `WebhookConfig.__repr__` includes `signing_secret`, and instances are enqueued as task kwargs. A repository search found no task instrumentation that serializes kwargs. Fix: `signing_secret: str = field(repr=False)`, or pass `config.url` and read the secret inside the task.

**Report (high): partial exclusion with a sink on the unblocked path**

```python
@dataclass
class Settings:
    api_key: str = field(repr=False)

cache.set("settings", json.dumps(asdict(settings)))
```

Evidence: `repr=False` does not affect `asdict`, and the cache write serializes the key. Fix: build an explicit dict of non-secret fields for the cache.

**Report (medium): new wholesale sink with no filter**

```python
def trace_call(func):
    def wrapper(*args, **kwargs):
        with start_span() as span:
            span.set_data("call.kwargs", {k: str(v) for k, v in kwargs.items()})
            return func(*args, **kwargs)
    return wrapper
```

Evidence: every kwarg is stringified into span data with no allowlist or type filter, and no credential-bearing caller was traced yet. Fix: record `int`, `float`, `bool`, and short `str` values; record `type(v).__name__` for everything else; redact keys matching credential names.

**Do not report: credential never stored on the instance**

```python
@dataclass
class RpcClient:
    referrer: str

    @property
    def shared_secret(self) -> str:
        return os.environ["RPC_SHARED_SECRET"]
```

A plain `property` is not a dataclass field and does not write to `__dict__`. Switching it to `cached_property` would make `vars(obj)` leak after first access.

**Report (high): `Field(exclude=True)` with a `str()` sink**

```python
class Settings(BaseModel):
    service: str
    api_key: str = Field(exclude=True)

span.set_data("settings", str(settings))
```

Evidence: `exclude=True` omits `api_key` from `model_dump` and response serialization. `str(settings)` and `repr(settings)` still contain the raw key, and the span records `str(settings)`. Fix: `api_key: str = Field(repr=False, exclude=True)`, or use `SecretStr`. `repr=False` alone still leaks through `model_dump`.

**Report (high): fully excluded field with a raw attribute sink**

```python
class Settings(BaseModel):
    service: str
    api_key: str = Field(repr=False, exclude=True)

redis.set("settings", pickle.dumps(settings))
```

Evidence: both flags block every generated path, but `pickle` serializes `__dict__`, which holds the raw key, into a cache entry. `SecretStr` would not help, because it pickles its raw value. Fix: cache `settings.model_dump()` and read the key from the secret source at the consumer.

**Do not report: fully excluded field with only generated-path sinks**

```python
class Settings(BaseModel):
    service: str
    api_key: str = Field(repr=False, exclude=True)

logger.info("loaded %s", settings)
return settings.model_dump()
```

`repr`, `str`, and `model_dump` all omit `api_key`, and no sink reads `__dict__`.

**Do not report: pydantic `SecretStr`**

```python
class Settings(BaseSettings):
    database_password: SecretStr
```

`repr`, `str`, and `model_dump` render `**********`. Report only if a changed call site passes `get_secret_value()` to a sink, or a raw attribute sink such as `pickle` receives the instance.

**Do not report: sink already filters**

```python
SCALARS = (str, int, float, bool, type(None))
safe_kwargs = {
    k: (v if isinstance(v, SCALARS) and not is_credential_key(k) else type(v).__name__)
    for k, v in kwargs.items()
}
```

## Regression Test Shape

```python
from sentry_sdk.serializer import serialize

def test_client_serialization_excludes_secret():
    client = RpcClient(referrer="test", shared_secret="shared-secret-value")
    assert "shared-secret-value" not in json.dumps(serialize({"client": client}))
    assert "shared-secret-value" not in repr(client)
```

Use the serializer the real sink uses. A `repr` check alone misses the `asdict` and `__dict__` paths.
