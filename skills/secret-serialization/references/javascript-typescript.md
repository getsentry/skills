# JavaScript and TypeScript Secret Serialization Notes

Use this when reviewing JavaScript or TypeScript code. These notes refine the core skill; they do not add reporting scope.

## Generated Serialization Paths

| Shape | Paths that include every own enumerable property | Exclusion |
|-------|--------------------------------------------------|-----------|
| Plain object or class instance | `JSON.stringify`, `util.inspect` / `console.log`, spread `{...obj}`, `Object.entries`, `structuredClone` | `#private` fields (excluded from all of these), `Object.defineProperty(obj, k, { enumerable: false })`, a `toJSON()` returning an allowlisted object, `[util.inspect.custom]()` for inspect only |
| Class with TypeScript `private` or `protected` | Same as a plain class. The modifier is compile-time only. | Not an exclusion. Use `#private`. |
| Zod or Valibot parsed config object | Plain object; `JSON.stringify` and loggers see every key | Split secrets into a separate object, or redact at the sink |
| Value held in a closure | Not reachable by serialization | Preferred for client credentials |
| `WeakMap` keyed by instance | Not reachable by `JSON.stringify` or `util.inspect` of the instance | Acceptable for credentials attached to instances |

A `toJSON()` covers `JSON.stringify` only. `console.log`, `util.inspect`, pino, and the Sentry normalizer walk own enumerable properties and ignore `toJSON`. Treat a `toJSON`-only block as partial when an inspect or logger sink exists.

## High-Signal Sinks

| Sink | Why it leaks | Safe form |
|------|--------------|-----------|
| `logger.info({ ...config })`, `logger.info('msg', client)` in pino, winston, or bunyan | Serializes own enumerable properties | Log identifiers. Logger `redact` paths are defense in depth, not the fix. |
| `console.log(obj)` / `util.inspect(obj)` in shipped code | Walks properties, including TypeScript `private` ones | Remove, or log a summary |
| `Sentry.setContext('client', obj)`, `setExtra`, `captureException(err, { extra: { client } })` | The normalizer walks properties | Pass explicit scalar fields |
| `span.setAttribute(key, JSON.stringify(obj))`, `span.setAttributes(obj)` | Stringifies whole objects | Allowlist scalar attributes |
| Logging an HTTP client error with its request config (for example axios `error.config.headers`) | The attached request carries `Authorization` | Strip headers before logging |
| `res.json(obj)`, `Response.json(obj)`, a Server Action return value | Serializes a config or client object into a response | Return a DTO |
| `for (const [k, v] of Object.entries(args)) attrs[k] = String(v)` | Stringifies arbitrary argument objects into telemetry | Allowlist keys; record `v.constructor.name` for objects; redact credential-named keys |

## Examples

**Report (high): token property on a client that instrumentation serializes**

```ts
export class ApiClient {
  constructor(
    public readonly baseUrl: string,
    private readonly token: string,   // compile-time private only
  ) {}
}
```

```ts
// instrumentation.ts, already on the default branch
span.setAttribute('tool.args', JSON.stringify(args)); // args.client is an ApiClient
```

Evidence: `private` does not affect `JSON.stringify`, so `args.client` serializes with `token`. Fix: `readonly #token: string` or a closure, and have the sink skip object values.

**Report (medium): unexcluded credential on a shared config object**

```ts
export const config = {
  region: process.env.REGION,
  webhookSecret: process.env.WEBHOOK_SECRET,
};

export function createHandler(cfg: typeof config) { ... }
```

Evidence: `config` is exported and passed into handler factories. A repository search found no logger or Sentry context call on it yet. Fix: split into `config` and `secrets`, or read the secret inside the function that signs.

**Report (medium): new wholesale sink**

```ts
export function traced<T extends (...a: any[]) => any>(fn: T) {
  return (...args: Parameters<T>) =>
    Sentry.startSpan({ name: fn.name, attributes: { args: JSON.stringify(args) } }, () => fn(...args));
}
```

Evidence: every argument is stringified into span attributes with no filter. Fix: record primitive arguments and a type name for objects.

**Do not report: `#private` field**

```ts
export class ApiClient {
  readonly #token: string;
  constructor(readonly baseUrl: string, token: string) { this.#token = token; }
}
```

`#private` fields are not own enumerable properties. `JSON.stringify`, `util.inspect`, spread, and the Sentry normalizer do not see them.

**Do not report: allowlisted `toJSON` with no inspect or logger sink**

```ts
toJSON() { return { baseUrl: this.baseUrl }; }
```

This is enough when the only sinks are `JSON.stringify` or `res.json`. It becomes a partial exclusion if the instance is also passed to `console.log` or a logger.

## Regression Test Shape

```ts
it('does not serialize the token', () => {
  const client = new ApiClient('https://example.invalid', 'token-value');
  expect(JSON.stringify(client)).not.toContain('token-value');
  expect(util.inspect(client)).not.toContain('token-value');
});
```

Assert against every serializer a sink in the repository uses.
