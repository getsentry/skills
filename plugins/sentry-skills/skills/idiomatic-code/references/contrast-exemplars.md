# Contrast Exemplars

Use this reference when the user is reacting to an interface that is technically capable but harder to consume than it needs to be.

These are contrast examples, not blanket negative judgments.
Each project below is useful in the right context. The point is to recognize when local code has drifted toward the same failure mode without needing the same power.

## Machinery-Heavy: Container And Provider Systems

### NestJS Custom Providers

What it is good at:

- flexible dependency injection
- swapping implementations for testing and environment-specific behavior
- centralizing wiring in large apps

Why it exceeds this skill's default simplicity bar:

- the consumer vocabulary quickly expands from classes to tokens, `useClass`, `useValue`, `useFactory`, `useExisting`, and `@Inject`
- provider wiring can become more visible than the business operation itself

Local smell to watch for:

- exported code reads like container registration instead of domain behavior
- factories and tokens proliferate before the business interface is even clear

Preferred correction:

- keep DI and provider machinery internal
- expose a plain function, router, or small object with domain names

### InversifyJS

What it is good at:

- container-managed composition in larger modular systems
- binding scopes, container modules, and runtime resolution

Why it exceeds this skill's default simplicity bar:

- the public mental model often shifts from "what does this module do?" to bindings, identifiers, scopes, modules, decorators, and container behavior
- annotation-driven or module-driven registration can make the real interface harder to see

Local smell to watch for:

- many service identifiers, decorators, or container modules before a caller can perform one useful action
- factory and binding vocabulary dominates the exported API

Preferred correction:

- collapse wiring behind a direct module API
- make the consumer call site independent from container terminology

## Concept-Heavy: State And Orchestration DSLs

### XState

What it is good at:

- explicit orchestration of genuinely complex workflows
- predictable state transition modeling

Why it exceeds this skill's default simplicity bar:

- actions, guards, actors, delays, snapshots, setup, and machine configuration can all appear before the reader sees the business operation
- the concept load is high even when the underlying task is small

Local smell to watch for:

- simple UI or workflow code starts reading like a machine definition language
- the reader has to understand orchestration vocabulary before the business action is obvious

Preferred correction:

- use plain functions and narrow state objects for small workflows
- reserve a full state-machine surface for problems that are truly state-machine-shaped

## Abstraction-First: Theory And Algebra Vocabulary

### fp-ts

What it is good at:

- strongly structured functional composition
- reusable abstractions for teams already fluent in typed FP

Why it exceeds this skill's default simplicity bar:

- the docs explicitly assume FP knowledge and center abstractions from Haskell, PureScript, and Scala
- type classes, higher-kinded types, and algebraic vocabulary can dominate the reader experience

Local smell to watch for:

- exported code requires the caller to parse `pipe`, type-class vocabulary, or layered functional abstractions before understanding the domain action
- helper APIs optimize for abstraction reuse more than call-site readability

Preferred correction:

- keep abstraction-heavy helpers internal
- expose domain functions whose names and inputs tell the story directly

## Style-Shift: A Different Programming Model

### Effect

What it is good at:

- coherent error handling, concurrency, retries, dependency management, and composition
- scaling a consistent programming model across large TypeScript systems

Why it is a style-shift contrast:

- the official docs explicitly call out a learning curve, a different programming style, and an extensive API surface
- this is not merely "too complex"; it is a different default way of structuring programs

Local smell to watch for:

- a small module starts adopting framework-wide concepts and runtime vocabulary before the user problem demands them
- the caller has to learn the programming model before the interface becomes obvious

Preferred correction:

- keep the public contract simple even if internals use richer Effect-style composition
- do not force the entire programming model onto small, local interfaces

## Contract-Rich: Explicit But Still Too Busy

### ts-rest

What it is good at:

- explicit contract-first API definitions
- keeping request and response details visible

Why it is a lighter contrast:

- it remains relatively plain, but its surface can accumulate params, headers, metadata, and response maps faster than the common case needs
- the interface can become clear but still noisy

Local smell to watch for:

- a contract is fully explicit, yet the common path is still hard to scan
- transport detail overwhelms the one thing the caller is trying to do

Preferred correction:

- keep the common path tiny
- move advanced contract detail off the main line unless it materially changes how callers use the API

## Convention-Driven With Hidden Mode Boundaries

### Next.js

What it is good at:

- file-based routing and colocated route structure can be clear at the simple end
- some file and route naming conventions make app organization obvious
- layouts, pages, and route-level boundaries can be productive when the hierarchy stays shallow
- at its best, naming conventions give you useful structure without much ceremony

Why it exceeds this skill's default simplicity bar:

- behavior changes across Server Components, Client Components, and Server Actions
- directives like `'use client'` and `'use server'` create mode boundaries that are easy to miss at the call site
- special routing conventions such as route groups, parallel routes, and intercepting routes add behavior through folder names and placement
- the reader often needs framework context to predict where code runs, what can be imported, and which data can cross the boundary
- the directives feel like magic because semantics depend on top-of-file markers instead of the module interface itself

Local smell to watch for:

- a component or module changes behavior depending on file directive or file location
- the interface only makes sense once the reader knows whether it runs on the server, the client, or through a framework action boundary
- route behavior depends on special folders or naming conventions that are no longer obvious from the page or module API
- a simple mutation suddenly depends on form actions, serialization rules, or framework-specific execution context

Preferred correction:

- keep framework-specific mode switches at the edge and expose plain functions or modules underneath
- make server/client and action boundaries explicit in local names and module structure
- use convention-driven routing while it is locally obvious, but treat advanced conventions as a cost that must pay for itself
- avoid APIs whose semantics depend primarily on where the file lives
- keep the naming convention if it helps, but remove directive-driven magic from the local API shape

Positive adjacent reference:

- Remix route file naming is a cleaner example of convention-driven structure because the route shape is carried more by the filename itself than by hidden client/server directives
- use Remix as the positive bar for naming-based organization, and Next.js as the warning sign for conventions that start changing execution semantics

## Decision Rule

When you see one of these failure modes locally, treat the project as a contrast example, not a default bar.
Extract the smallest design lesson:

- machinery-heavy: hide the wiring
- concept-heavy: lower the concept count
- abstraction-first: expose domain language first
- style-shift: keep the public contract simple even if internals are richer
- contract-rich: trim the common path until it reads in one straight line
- convention-driven with hidden mode boundaries: keep conventions helpful, but do not let file context or directives become the main source of behavior
