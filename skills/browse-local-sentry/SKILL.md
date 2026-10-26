---
name: browse-local-sentry
description: Connects an agent's browser to a local Sentry dev server (dev-ui on *.dev.getsentry.net or the full devserver).
---

# Browse Local Sentry

| Server | URL | Data | Browser |
|--------|-----|------|---------|
| dev-ui (`pnpm run dev-ui`) | `https://<org-slug>.dev.getsentry.net:<port>/`. Ask the user for the org if it is unknown. | Production sentry.io, as the user | The user's own Chrome, the only one with their session |
| Full devserver (`devservices serve`) | `http://dev.getsentry.net:8000/` | Local database | Any |

Run every check in every session. Chrome updates, re-auth, and port changes undo
earlier setup without warning. When a check fails, open the named section of
`references/troubleshooting.md`.

## Rules

- dev-ui acts on production sentry.io as the user, including any staff or
  superuser session. Do not create, edit, or delete anything, and stay in the
  org the user named, unless the user approves the specific action. Use the
  full devserver for flows that change data.
- Never bypass certificate warnings (`thisisunsafe`,
  `--ignore-certificate-errors`, `--acceptInsecureCerts`), log in to sentry.io
  yourself, or type the user's credentials.
- Change the user's MCP config only with their approval.
- In the user's own Chrome, open your own tabs with `background: true`, never
  `isolatedContext`, which has no session. Never navigate, reload, close, read,
  screenshot, run scripts in, or quote the user's tabs. Emulate viewports
  instead of resizing the window, and close your tabs when done.

## Step 1: Find the Server

Use the URL the user gives. Otherwise never assume a port: dev-ui tries 10 ports
upward from `SENTRY_WEBPACK_PROXY_PORT` (default 7999) and prints the one it
took, and the devserver logs to `.artifacts/dev.log`. List listeners with
`lsof -nP -iTCP -sTCP:LISTEN` and match one to its clone with
`lsof -a -p <pid> -d cwd`.

## Step 2: Check the Certificate (dev-ui Only)

Outside any shell sandbox, run
`curl -sS -o /dev/null https://dev.getsentry.net:<port>/` (on macOS,
`/usr/bin/curl`, which reads the keychain). If it fails, see **Certificate**.

## Step 3: Attach to the User's Chrome (dev-ui Only)

Call `list_pages`, or use another tool that already drives the user's signed-in
Chrome. The browser is attached when it lists the user's own tabs. If not, see
**Chrome**.

## Step 4: Check Authentication

Open the server URL in a new tab and read `/api/client-config/`. Continue when
`isAuthenticated` is `true`. If not, see **Authentication**.

After editing frontend source, wait for the rebuild, then reload with the cache
bypassed. If the console shows "An SSL certificate error occurred when fetching
the script.", the certificate is not trusted; return to Step 2.

## When a Step Is Blocked

Stop and tell the user which step failed and the exact action they need to
take. Do not substitute tests, stories, or reasoning for browser QA, and do not
write "browser verification was blocked" into a PR description in place of
doing it.
