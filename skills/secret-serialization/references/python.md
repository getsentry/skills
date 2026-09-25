# Python Secret Serialization Notes

Use this when reviewing Python code. These notes refine the core skill; they do not add reporting scope.

## Generated Serialization Paths

| Type | Paths that include every field by default | Field-level exclusion |
|------|-------------------------------------------|-----------------------|
| `@dataclasses.dataclass` | `__repr__` (so `str()`, f-strings, `%s`, `%r`), `dataclasses.asdict`, `dataclasses.astuple`, `dataclasses.fields`, `__eq__` | `field(repr=False)` covers repr only. Nothing excludes a field from `asdict`; keep the value off the instance or wrap it. |
| `attrs` `@define` / `@attr.s` | `__repr__`, `attrs.asdict`, `attrs.astuple` | `field(repr=False)`; `asdict(filter=...)` only at call sites. |
| `pydantic.BaseModel` | `__repr__`, `__str__`, `model_dump`, `model_dump_json`, `.dict()`, `.json()`, FastAPI response serialization | `SecretStr` / `SecretBytes` (render as `**********`), `Field(exclude=True)`, `Field(repr=False)`. |
| `pydantic_settings.BaseSettings` | Same as `BaseModel`; often logged wholesale at startup | `SecretStr` for every credential setting. |
| `typing.NamedTuple` | `__repr__`, `_asdict`, iteration and unpacking | None. Do not hold credentials on a NamedTuple. |
| `TypedDict` / `dict` | `repr`, `json.dumps`, iteration | None. Redact at the sink. |
| `msgspec.Struct` | `__repr__`, `msgspec.to_builtins`, encoders | `field(repr=False)` on newer versions; otherwise none. |
| Plain class | `vars(obj)`, `obj.__dict__`, `pickle`, Sentry local-variable capture | A hand-written `__repr__` covers repr only. `__dict__` sinks still see the value. |

`dataclass(init=False)` with a hand-written `__init__` still generates `__repr__` and still registers annotated fields with `asdict`. A custom constructor is not an exclusion.

`functools.cached_property` stores its result in `instance.__dict__`. A `cached_property` that returns a secret leaks through `vars(obj)` and Sentry local-variable capture after first access, even when the declared field has `repr=False`.

## High-Signal Sinks

| Sink | Why it leaks | Safe form |
|------|--------------|-----------|
| `safe_kwargs[key] = str(value)` over `**kwargs` | Stringifies client and config objects passed as tool or task arguments | Allowlist scalar keys; record `type(value).__name__` for objects; redact keys matching credential names |
| `span.set_data(key, obj)`, `span.set_attribute(key, obj)`, `set_context(name, obj)`, `set_extra` | Sentry and OpenTelemetry serialize objects by `repr` or a `__dict__` walk | Pass explicit scalar fields only |
| `logger.info("... %s", obj)`, `{obj}` in f-strings, `logger.exception(...)` | Interpolates `__repr__`; Sentry `include_local_variables=True` (the default) captures frame locals by repr on exceptions | Log identifiers, not objects; exclude credential fields from repr |
| `json.dumps(obj, default=str)`, `default=repr`, `default=vars` | Falls back to repr or `__dict__` for unknown objects | An explicit `to_dict()` with an allowlist |
| `dataclasses.asdict(obj)` / `model.model_dump()` into a response, cache, or queue | Includes every field regardless of `repr=False` | `exclude={...}` or a separate public DTO |
| `pickle.dumps(obj)` into Redis or a task queue | Serializes `__dict__`, including cached properties | Rebuild clients from config at the consumer |
| `pprint`, `rich.inspect`, `print(obj)` in shipped code | repr | Remove, or log identifiers |

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

**Do not report: pydantic `SecretStr`**

```python
class Settings(BaseSettings):
    database_password: SecretStr
```

`repr`, `str`, and `model_dump` render `**********`. Report only if a changed call site passes `get_secret_value()` to a sink.

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
