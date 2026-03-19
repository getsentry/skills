# Python Exemplars

Use these examples to calibrate what strong interface clarity, small public surfaces, and concise contract documentation look like.

## requests

What makes this a good example:

- obvious verbs like `get`, `post`, and `request`
- very small amount of surface area for the common case
- examples that teach by showing straightforward calls first

What to avoid:

- hiding basic behavior behind wrappers that are less obvious than the original call
- adding helper layers that rename standard HTTP concepts without a good reason

## HTTPX

What makes this a good example:

- requests-like usability with explicit modern details such as clients, timeouts, and async variants
- parallel sync and async APIs that stay recognizable
- names that tell the caller exactly what they are configuring

What to avoid:

- exposing transport knobs before callers need them
- letting configuration objects replace simple function arguments when the common case is small

## pluggy

What makes this a good example:

- extremely small extension vocabulary
- clear separation between hook definition and hook implementation
- names like `hookspec`, `hookimpl`, and `PluginManager` that explain the role directly

What to avoid:

- plugin systems with hidden registration rules
- too many lifecycle concepts before the caller has even used one hook

## Click

What makes this a good example:

- command functions that read like normal Python
- decorators and docstrings that map directly to CLI help
- clear option and argument names

What to avoid:

- burying the command contract in decorator noise
- using short option names when the long name is the one users actually understand

## pathlib

What makes this a good example:

- one coherent object model
- names that map closely to real filesystem concepts
- methods that usually mean exactly what they say

What to avoid:

- wrapping a simple domain in many helper classes
- generic methods that combine unrelated file operations

## Python Heuristics

If you are rewriting a Python API, prefer this order of choices:

1. named function with a short docstring
2. small module of related functions
3. object with real state and several meaningful methods

Reach for classes, decorators, or registries only when the public contract stays clearer because of them.
