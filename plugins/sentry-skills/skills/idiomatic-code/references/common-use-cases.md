# Common Use Cases

Use these patterns when the user wants a concrete rewrite path, not just general principles.

1. Rewrite a generic `execute` or `handle` API into a small object of named functions or procedures.
2. Split one function with `mode` or boolean behavior flags into separate functions with domain names.
3. Turn a builder-heavy TypeScript API into an oRPC-like plain object surface with one predictable handler shape.
4. Replace hidden or ad hoc error handling with an explicit return contract or named exceptions.
5. Rewrite a Python helper so required inputs are positional, optional behavior is keyword-only, and the docstring names expected failures.
6. Move transport, schema, or validation details next to the function or procedure they shape instead of hiding them behind framework layers.
7. Rename exported symbols so the call site uses domain words instead of framework or implementation words.
8. Replace comments that narrate implementation with short contract comments that explain return value, side effects, and invariants.
9. Pull server/client or action-specific framework behavior to the edge and expose a plain local module interface underneath.

## Default Rewrite Order

1. Name the actual job.
2. Reduce the number of entry points.
3. Make the input shape obvious.
4. Make failure behavior obvious.
5. Keep framework boundaries and mode switches at the edge.
6. Rewrite comments and docstrings last.
