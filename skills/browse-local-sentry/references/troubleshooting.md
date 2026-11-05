# Troubleshooting

## Certificate

dev-ui serves HTTPS with `config/localhost.pem` when that file exists at
startup, and otherwise with a self-signed fallback that browsers reject. The
fallback is the usual cause of "blocked by the local development certificate".

Run these commands outside any shell sandbox. Inside one, curl rejects even a
trusted certificate and openssl may fail to connect.

If curl failed with anything other than `SSL certificate problem`, recheck the
port and that the command ran outside a sandbox. On a certificate error, verify
the served certificate against this machine's mkcert CA:

```bash
f=$(mktemp)
openssl s_client -connect 127.0.0.1:<port> -servername dev.getsentry.net </dev/null | openssl x509 > "$f"
[ -s "$f" ] || echo "no certificate captured"
openssl verify -CAfile "$(mkcert -CAROOT)/rootCA.pem" "$f"
```

If no certificate was captured, openssl could not connect: recheck the port and
the sandbox instead of using this table.

| Result | Fix |
|--------|-----|
| `OK` | The local CA is not trusted. Ask the user to run `mkcert -install`, which prompts for a password. If it says the CA is already installed, the probe ran in a sandbox; rerun it outside. |
| `certificate has expired` | mkcert certificates last about two years. Ask the user to run `pnpm mkcert-localhost` again, then restart dev-ui. |
| Any other error, or `mkcert` is not installed | dev-ui is serving its fallback or a certificate from another CA. If `config/localhost.pem` in the clone running dev-ui passes the same `openssl verify`, restart dev-ui. Otherwise ask the user to run `pnpm mkcert-localhost` (needs [mkcert](https://github.com/FiloSottile/mkcert)), then restart dev-ui. `config/*.pem` is gitignored, so every clone and worktree needs its own copy. |

The CA is trusted machine-wide, so every Chrome profile accepts the certificate
once it is installed.

## Chrome

chrome-devtools-mcp needs `--autoConnect`. Without it, the server launches its
own dedicated profile, which has no sentry.io session. These commands change the
user's MCP config beyond this session, so show them to the user and run them
only with their approval. Keep the pinned version: the server gets full control
of a browser signed in to production.

| Client | Command |
|--------|---------|
| Claude Code | `claude mcp remove chrome-devtools` (any scope; ignore "not found"), then `claude mcp add chrome-devtools --scope user -- npx chrome-devtools-mcp@1.12.0 --autoConnect`. If the tools come from the `chrome-devtools-mcp@chrome-devtools-plugins` plugin, whose args are fixed, also run `claude plugin disable chrome-devtools-mcp@chrome-devtools-plugins`. |
| Codex | `codex mcp add chrome-devtools -- npx chrome-devtools-mcp@1.12.0 --autoConnect` |
| Other | Set the server's args to `["chrome-devtools-mcp@1.12.0", "--autoConnect"]` |

After changing the config, ask the user to reconnect the MCP server. Then ask
them to open `chrome://inspect/#remote-debugging` in their everyday Chrome
(version 144 or newer), enable remote debugging, and accept Chrome's prompt to
allow the connection. Call `list_pages` again.

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Could not find DevToolsActivePort` or "Could not connect to Chrome" | Chrome is not running, or remote debugging is off | Ask the user to enable it, then call `list_pages` |
| `EPERM: operation not permitted` or `DevToolsActivePort` errors on macOS with remote debugging on | The agent's host app cannot read Chrome's profile folder | Ask the user to allow the terminal or IDE under System Settings > Privacy & Security > Files & Folders > Google Chrome |
| `Network.enable timed out` or "socket connection was closed" | The connection prompt was not accepted, another MCP server or tool holds the connection, or many frozen tabs (Chrome 149 and older) | Ask the user to accept the prompt, close other connected agents, or close unused tabs |
| `The browser is already running for` a cache directory, or only a lone `about:blank` | `--autoConnect` is missing or misspelled, so the server launched its own profile | Fix the args and reconnect |
| Attached to a browser or profile the user does not work in | autoConnect uses the default profile of stable Chrome | Ask the user to sign in to Sentry in that profile, or add `--channel=beta`, `--channel=dev`, or `--channel=canary` to match their browser |
| The server fails to start with `npx` not found | The client launched it without the shell's `PATH` (nvm, volta) | Add an `env.PATH` entry or use an absolute `npx` path |

## Authentication

| Server | If `isAuthenticated` is `false` |
|--------|--------------------------------|
| dev-ui | Ask the user to install [Sentry Cookie Sync](https://chromewebstore.google.com/detail/sentry-cookie-sync/kchlmkcdfohlmobgojmipoppgpedhijh) in the attached Chrome profile, then log into sentry.io there and keep a `https://<org-slug>.sentry.io` tab open. The extension copies that session to `dev.getsentry.net` only for orgs it sees in open tabs. Then reload. SSO cannot help elsewhere: dev-ui does not proxy `/identity/` routes, and Okta device trust rejects fresh profiles. |
| Full devserver | Sign in with a local account. If none exists, create one with `sentry createuser --email <email> --password <password> --superuser --no-input`. |
