# Troubleshooting And Workarounds

Use this reference when the code still feels confusing after a first simplification pass.

1. Issue: The API uses one generic verb like `execute`, `process`, or `handle`.
   Fix: Split by domain action and rename each entry point for the caller's intent.

2. Issue: One function uses `mode` or boolean flags to switch behavior.
   Fix: Create separate functions or procedures for each meaningfully different job.

3. Issue: Required and optional inputs are mixed into one vague options bag.
   Fix: Make required inputs obvious and group only true optional behavior in named options.

4. Issue: The caller cannot tell whether the function throws, returns `null`, or returns an error object.
   Fix: Pick one visible failure contract and document it in code.

5. Issue: A class exists only to wrap one public method.
   Fix: Replace it with a named function or a small object of related functions unless state is part of the contract.

6. Issue: The code sample needs a long explanation before the API makes sense.
   Fix: Rename the surface and shrink the concept count until the sample is readable without prose.

7. Issue: Comments or docstrings only translate the next line into English.
   Fix: Rewrite them to explain return value, side effects, invariants, and expected failures.

8. Issue: Framework vocabulary has displaced domain vocabulary.
   Fix: Keep framework constructs local, but make exported names describe the business action.

9. Issue: Schema, routing, and business logic are all tangled in one long chain.
   Fix: Keep the public route or function surface small and move non-contract detail down a layer.

10. Issue: The API is technically explicit but still feels noisy.
    Fix: Remove knobs that do not matter to the common case and keep advanced configuration off the main path.

11. Issue: Factories, providers, or tokens dominate the design before the business API is obvious.
    Fix: Treat this as a machinery-heavy smell. Hide the wiring and expose a plain domain interface first.

12. Issue: The code reads like a container configuration system rather than a module with one clear job.
    Fix: Collapse DI vocabulary behind direct functions or a small object of named operations.

13. Issue: A small feature now needs guards, actors, machine setup, or other orchestration concepts just to explain itself.
    Fix: Treat this as a concept-heavy smell. Use a full state-machine surface only when the workflow is genuinely state-machine-shaped.

14. Issue: The interface requires theory-heavy vocabulary before the reader can tell what it does.
    Fix: Treat this as an abstraction-first smell. Keep algebraic or effectful helpers internal and expose domain language first.

15. Issue: A small module now assumes a whole programming style or runtime model.
    Fix: Treat this as a style-shift smell. Keep the public contract simple even if the internals use richer composition.

16. Issue: Behavior changes depending on file directives, file placement, or whether the code runs on the server or client.
    Fix: Treat this as a hidden-boundary smell. Move the mode switch to the edge and expose a plain local contract underneath.

17. Issue: A simple mutation now depends on framework actions, serialization rules, or form wiring that is not obvious at the call site.
    Fix: Define the plain server-side operation first, then wrap it with the framework-specific action interface.

18. Issue: Routing behavior now depends on special folders, slots, route groups, or intercepting conventions that are hard to predict without framework expertise.
    Fix: Treat this as a convention-driven smell. Keep the simple naming conventions, but collapse advanced routing behavior unless it clearly earns its complexity.

19. Issue: A naming convention is helping structure, but top-of-file directives or framework mode switches are carrying too much semantic weight.
    Fix: Keep the naming convention and move the semantic boundary into explicit module or function interfaces instead of directive magic.
