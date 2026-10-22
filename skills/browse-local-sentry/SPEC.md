# Browse Local Sentry Specification

## Intent

Get an agent's browser onto a local Sentry dev server, trusted and signed in,
so it can QA and screenshot the real product. Agents otherwise hit an untrusted
certificate or a login wall they cannot pass, then report "browser verification
was blocked" instead of doing the QA.

## Scope

In scope:
- Finding the dev-ui or devserver URL and port.
- The mkcert certificate dev-ui needs.
- Attaching chrome-devtools-mcp to the user's own Chrome for dev-ui.
- Checking and fixing authentication.
- Safety limits for production data and the user's real browser.

Out of scope:
- Installing or running the dev environment (devenv, devservices).
- Screenshot framing, tables, and upload (`pr-screenshots`).
- Seeding data for a specific state.

## Should Not Trigger For

- Browsing production sentry.io or other sites.
- Writing Jest or Playwright tests.
- Dev environment setup failures before a server is running.

## Acceptance Gates

- dev-ui runs in the user's existing Chrome, never a launched profile.
- No mutating actions against production through dev-ui without approval.
- The user's own tabs are never read, navigated, closed, or quoted. Attaching
  may load discarded tabs, which the skill cannot prevent.
- Never bypasses certificate warnings or adds insecure-cert flags.
- Never logs in to sentry.io or types the user's credentials.
- Changes MCP config only with the user's approval, at a pinned version.
- Verifies attachment with `list_pages` and auth with `/api/client-config/`.
- Reports the blocked step and the user's action instead of claiming QA.

## Known Limitations

- Remote debugging, the Chrome connection prompt, `mkcert -install`, and sign-in
  all need the user. The skill can only detect and ask.
- `--autoConnect` needs a locally running Chrome 144+. Sandboxed clients must use
  `--browser-url`, which Chrome only allows with a separate profile, so they
  lose the signed-in session and can only use the full devserver.
- Sentry Cookie Sync learns orgs only from open `:7999` dev-ui tabs and
  `*.sentry.io` tabs. dev-ui on other ports depends on an open sentry.io tab.
- Other tools that drive the user's real Chrome, such as browser extensions,
  should work from Step 4 on but are untested.

## Maintenance Notes

Re-check `SOURCES.md` facts when dev-ui's HTTPS or proxy setup, the
`mkcert-localhost` script, Sentry Cookie Sync, or chrome-devtools-mcp's
connection flags change.

Bump the pinned chrome-devtools-mcp version only after reviewing the release,
and re-run Steps 3 and 4 against it.
