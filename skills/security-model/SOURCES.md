# Security Model Skill Sources

## Source Inventory

| Source | Trust tier | Confidence | Usage constraints | Decisions |
|--------|------------|------------|-------------------|-----------|
| `define-security-policy` skill in [openai/codex-security](https://github.com/openai/codex-security/tree/main/plugins/codex-security/skills/define-security-policy), plugin 0.1.95, commit `2b74623e` | Upstream skill | High | Apache-2.0. Adapted, not copied; changes are stated in the `SKILL.md` attribution comment. | Kept: evidence-backed boundary review, owner confirmation for suppressing decisions, policy as untrusted data, root-to-leaf composition, diff preview before writing, no commit without a request. |
| `resolve-security-md` helper in the same repository (`plugins/codex-security/mcp-app/src/helpers/resolve-security-md.ts`) | Upstream code | High | Apache-2.0. Behaviour re-implemented in Python, not translated. | Kept: root-to-leaf concatenation, closest-policy precedence, source headers, 1 MiB cap, UTF-8 requirement, whitespace-only skip, symlinks confined to the repository. |
| GitHub docs: [creating a default community health file](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file) | Official docs | High | None. | `SECURITY.md` in `.github/`, root, or `docs/` is the disclosure policy and overrides the organization default, so this skill uses `SECURITY_MODEL.md`. |
| `security-review`, `django-access-review`, and repository review skills | Local prior art | High | Avoid overlap. | Policy states boundaries and reportability; review skills keep the pattern catalogs. `references/consuming-policy.md` is the contract between them. |

## Adaptation Decisions

| Decision | Record |
|----------|--------|
| source intent | Give a scanner the repository context it needs to decide what is and is not a finding. |
| local target | Policies that Sentry's review skills and Warden load, with stable IDs findings can cite. |
| fidelity boundary | Owner confirmation, untrusted-policy handling, and precedence semantics stay equivalent. |
| local replacement | Filename; Node and native launcher replaced with a stdlib Python script run with `uv run`; Sentry severity scale and repository conventions. |
| omitted material | Codex artifact storage, Windows launcher, and MCP helper plumbing. They are runtime-specific and have no equivalent here. |
| rights and attribution | Apache-2.0, the same license as this repository. Modification notices are in `SKILL.md` and the script docstring. |

## Source-Backed Decisions

1. Use `SECURITY_MODEL.md`, not `SECURITY.md`.
   - Reason: a root `SECURITY.md` replaces the organization's disclosure page in every repository that adds one.
2. Resolve policies from the base revision in diff reviews (`--ref`).
   - Reason: upstream reads policy from the code under review, so a pull request could add a policy that excludes its own change.
3. Number invariants and require a finding-class table.
   - Reason: categorization needs a stable label that findings can cite and tools can group on.
4. Require explicit "Overrides of Parent Policy" entries.
   - Reason: with closest-wins precedence alone, a child policy can silently weaken a parent invariant.
5. Add `check` for stale references.
   - Reason: in a real run, a repository's review-skill references named a deleted file and renamed functions, and nothing caught it.
6. Keep suspected gaps and open questions out of the policy.
   - Reason: a gap recorded as a known limitation teaches review tools to ignore it, and committed questions go stale and can point at weaknesses in public repositories.

## Validation Runs

Runs on real repositories. Repository names, weaknesses, and drafted content are omitted.

| Run | Outcome | Skill delta |
|-----|---------|-------------|
| Cold dry run on a public SDK repository by a fresh agent | Followable; 14 ambiguities reported, including `--name SECURITY.md` pulling in disclosure policies. | Resolver skips disclosure copies; clarified scope, severity source, unresolved format, and approval without an owner. |
| Internal AI service repository | The existing review skill's references described auth behaviour the code no longer has, and named a deleted file. Suspected gaps ended up under Known Limitations. Draft had more than 15 `Unresolved` markers. | Added `check`; exposure-first severity; "Enforced by" vs "Monitored by"; suspected gaps go to the user; owner inheritance. |
| Re-run of the same draft with `check` | One stale path copied from CODEOWNERS; no false positives. | None. |
| Large public monorepo | Exposure settled from the repository, so severities were fixed levels. `check` gave false positives on package-relative paths and a symlinked skills directory, and found one stale symbol in an existing review skill. | Package-relative and symlink handling in `check`; run `check` on review-skill references. |
| Review of committed open questions | Questions in the file would go stale and could hint at weaknesses. | Questions presented with the draft, never committed. |
| Public Rust service with a separate docs site | The draft missed a shared cache across instances, retained minidumps, scraping headers, and several limits, because docs were found by filename only. The docs also disagreed with the code in three places. | Read project docs in full and confirm each documented control in code; report doc and code drift to the user. |
| User feedback on question handling | Open questions reached the user as a list at the end instead of being asked. | Ask open decisions interactively as multiple-choice prompts, update the draft from answers, and confirm the user can decide for the owners. |
| Cold re-run on the same public Rust service by a fresh agent | Draft passed `check`, but `check` skipped Rust-qualified names (`Type::method`) and flagged a backticked repository name. The agent found the severity-condition wording, the undefined "default" severity, and where conversation-only questions may live unclear. Owners in the header added noise. | `check` handles `::`; clarified base severity plus conditions, the default severity, partial enforcement, and local notes; owners no longer recorded in the file. |
| Public Rust library with C, Python, and WASM bindings | Invariants named enforcing symbols, but the user asked for an overview of which directories handle untrusted input, unsafe code, and bindings. | Added a Component Map section grouped by input trust level, and a drafting rule for it. |

## Open Gaps

- No automated eval yet. A small suite should cover the upstream fixture, a planted suppressing child policy, and a stale reference.
- `check` cannot tell that a symbol moved to a different file.
- Review skills in this repository do not yet load `SECURITY_MODEL.md`; see `references/consuming-policy.md`.

## Changelog

- Add a Component Map section that lists security-critical paths by input trust level.
- `resolve --ref` and `check` use the parent directories for a scope missing at that revision, so a file a PR adds still gets its base policy chain (found by review).
- Stop recording owners in the policy; `check` validates qualified symbols; clarify severity and question wording.
- Read project docs in full instead of searching by filename; ask open decisions interactively.
- Initial version.
