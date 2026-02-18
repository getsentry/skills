---
name: rust-development
description: Review Rust code for Sentry conventions and best practices. Use when finishing a Rust PR, validating Rust changes, "review Rust code", "check Rust conventions", or ensuring Rust code follows Sentry style guidelines. Covers error handling, naming, iterators, async patterns, imports, documentation, and versioning.
allowed-tools: Read, Grep, Glob, Bash, Task
---

<!--
Based on Sentry Rust Development Practices:
https://develop.sentry.dev/engineering-practices/rust.md
-->

# Rust Development Review

Review Rust code changes against Sentry's Rust conventions. Focus on the diff — only flag issues in changed code.

## Step 1: Gather Context

1. Run `git diff main...HEAD -- '*.rs' 'Cargo.toml'` to identify changed Rust files
2. If no Rust files changed, stop and report "No Rust files in this PR"
3. Read the changed files to understand the full context around each diff hunk

## Step 2: Review Error Handling

These patterns cause panics in production. Flag every occurrence in changed code.

| Pattern | Issue | Fix |
|---------|-------|-----|
| `.unwrap()` | Panics on None/Err | Use `?`, `.unwrap_or()`, `.unwrap_or_default()`, or match |
| `array[index]` on slices | Panics on out-of-bounds | Use `.get(index)` |
| `a - b` on unsigned integers | Panics on overflow in debug, wraps in release | Use `checked_sub()` or `saturating_sub()` |
| Unchecked arithmetic on user input | Overflow/underflow | Use `checked_add()`, `checked_mul()`, etc. |

**Exception:** `.unwrap()` is acceptable in tests and when immediately preceded by a guard that guarantees `Some`/`Ok` (e.g., `.is_some()` check).

## Step 3: Review Iterator Patterns

Check iterator usage in public interfaces.

**Public API iterators:**
- Use an explicit named iterator type, not `impl Iterator` (which prevents naming the return type)
- Name custom iterator types with `Iter` suffix (e.g., `EventIter`)
- Implement `FusedIterator` by default
- Implement `ExactSizeIterator` when size is known upfront
- Consider `DoubleEndedIterator` for reverse iteration support

**For complex cases:** wrap a boxed iterator in a newtype struct rather than returning `Box<dyn Iterator>`.

Only flag iterator issues in **public** functions and types. Internal iterators using `impl Iterator` are fine.

## Step 4: Review Async Code

- Prefer native `async fn` in traits (Rust 1.75+) over the `async-trait` crate
- Returned futures must be `Send` when used in multi-threaded runtimes — flag `async fn` in traits that don't add a `Send` bound when the crate uses `tokio::spawn` or similar multi-threaded executors
- The `async-trait` crate is acceptable as a fallback for compatibility with older Rust versions

## Step 5: Review Field Visibility

Default to private struct fields. Only flag `pub` fields when they don't fit these exceptions:

| Acceptable `pub` fields | Reason |
|--------------------------|--------|
| Newtype wrappers (`pub struct Foo(pub Bar)`) | Direct inner-type access is the point |
| Stable schema/protocol types | Part of a defined wire format |

For all other structs, provide accessor methods instead of `pub` fields:
- `fn foo(&self) -> &T` — getter
- `fn foo_mut(&mut self) -> &mut T` — mutable access
- `fn set_foo(&mut self, val: T)` — setter

## Step 6: Review Import Organization

Imports must be organized in three groups separated by blank lines:

```rust
// 1. Standard library
use std::collections::HashMap;
use std::fmt;

// 2. External and workspace dependencies
use serde::Deserialize;
use tokio::sync::Mutex;

// 3. Crate-local modules
use crate::config::Config;
use super::utils;
```

Flag imports that mix these groups without blank line separators.

## Step 7: Review Naming Conventions

| Convention | Correct | Incorrect |
|-----------|---------|-----------|
| Getters | `fn foo(&self)` | `fn get_foo(&self)` |
| Borrowed conversion | `fn as_foo(&self) -> &Foo` | `fn to_foo(&self) -> &Foo` |
| Owned conversion | `fn to_foo(&self) -> Foo` | `fn as_foo(&self) -> Foo` (if cloning) |
| Consuming conversion | `fn into_foo(self) -> Foo` | `fn to_foo(self) -> Foo` |
| Constructors | `fn new(...) -> Self` | `fn create(...)`, `fn build(...)` |
| Iterator types | `FooIter` | `FooIterator` |
| Fallible constructors | `fn new(...) -> Result<Self, E>` or `fn try_new(...)` | — |

Also check for redundant prefixes — e.g., `Event::event_type` should be `Event::kind` or `Event::ty`.

## Step 8: Review Documentation

Check that **public** items have doc comments following these conventions:

- Start with a single-line summary in third person: `/// Returns the event timestamp.`
- Use American English spelling
- Cross-reference related types with `[`backtick links`]`
- Include doctests for public utility functions and SDK methods
- Unit test names should be descriptive: `tests::parse_empty_input` not `tests::test1`

Only flag missing docs on new public items introduced in the PR. Do not flag pre-existing undocumented items.

## Step 9: Review Declaration Order

Within each file, the expected order is:

1. Module-level doc comment
2. Imports (organized per Step 6)
3. Re-exports (`pub use`)
4. Module declarations (`mod`)
5. Constants and statics
6. Error types
7. Main types (structs, enums) and their impls
8. Free functions
9. Tests (`#[cfg(test)]`)

Within a type's implementation:

1. Struct/enum definition
2. Inherent `impl` blocks
3. Standard library trait impls (`Display`, `From`, etc.)
4. Custom/external trait impls

Flag significant ordering violations in new code. Don't flag minor reordering in existing files.

## Step 10: Review Versioning (if Cargo.toml changed)

If `Cargo.toml` version was bumped, verify it follows these rules:

| Crate Version | Breaking change | New feature | Bug fix |
|--------------|-----------------|-------------|---------|
| **1.0+** (post-1.0) | Major bump | Minor bump | Patch bump |
| **0.x** (pre-1.0) | Minor bump | Patch bump | Patch bump |

The pre-1.0 convention aligns with Cargo's caret requirement behavior where `0.x.y` treats minor as the compatibility version.

## Output Format

```markdown
## Rust Review: [Summary]

### Findings

#### [RUST-001] Category (Severity)
**Location:** `file.rs:42`
**Issue:** Description of what's wrong
**Fix:**
\```rust
// suggested fix
\```

### Summary
- X issues found (Y high, Z medium)
```

**Severity levels:**
- **High** — will panic in production, violates public API contract, or breaks semver
- **Medium** — convention violation, naming issue, or missing documentation
- **Low** — minor style issue, ordering preference

If no issues found: "No Rust convention issues found in the changed files."

## What NOT to Flag

- Pre-existing code not modified in this PR
- Test files (unless public test utilities)
- `.unwrap()` in tests
- Generated code or build scripts
- One-time setup concerns (lint configuration, Clippy settings, IDE setup)
- Formatting issues (rely on `rustfmt` for this)
