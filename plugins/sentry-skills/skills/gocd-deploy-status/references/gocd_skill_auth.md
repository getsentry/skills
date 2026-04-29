# GoCD Skill Authentication

## Overview

The GoCD skill authenticates through two layers:

1. **IAP (Identity-Aware Proxy)** — Google's reverse proxy that protects `deploy.getsentry.net`. Every request must carry a valid OIDC identity token.
2. **GoCD API token** — A bearer token that authenticates the caller to the GoCD application itself.

Both are obtained via `gcloud` — engineers only need `gcloud auth login` with their `@sentry.io` account.

## GoCD API Token

Default source: GCP Secret Manager.

- **Project**: `dicd-team-devinfra-cd`
- **Secret**: `gocd-access-token`
- **Retrieved via**: `gcloud secrets versions access latest --secret=gocd-access-token --project=dicd-team-devinfra-cd`

Any engineer with access to the `dicd-team-devinfra-cd` project can read this secret.

### Override via env var

If `GOCD_ACCESS_TOKEN` is set in the environment, the skill uses that value instead of fetching from Secret Manager. This is the recommended path for engineers running with a personal read-only token minted from their own GoCD account -- it scopes blast radius to view-only operations and produces per-user audit trails on the GoCD side.

## IAP Authentication via Service Account Impersonation

### Why impersonation?

Google Cloud IAP requires an OIDC identity token whose `aud` (audience) claim matches the IAP backend client ID. For user accounts, `gcloud auth print-identity-token --audiences=...` is not supported — the `--audiences` flag only works for service accounts.

The standard workaround is **service account impersonation**: the engineer's own credentials are used to call the IAM API, which mints an identity token on behalf of a service account that has IAP access.

### How it works

```
Engineer (ming.chen@sentry.io)
    │
    ├─ gcloud auth login  (authenticates as themselves)
    │
    └─ gcloud auth print-identity-token \
         --impersonate-service-account=<SA> \
         --audiences=<IAP_CLIENT_ID> \
         --include-email
              │
              ├─ gcloud uses the engineer's credentials to call:
              │    IAM API → projects/-/serviceAccounts/<SA>:generateIdToken
              │
              └─ IAM API returns an ID token with:
                   iss: accounts.google.com
                   aud: <IAP_CLIENT_ID>  ← matches IAP's expected audience
                   email: <SA>@...       ← IAP checks this against its policy
```

The `--include-email` flag is critical — without it, the token lacks the `email` claim and IAP cannot match it against its access policy.

### IAM setup

| Principal | Role | Resource |
|---|---|---|
| `group:role-deploy-user@sentry.io` | `roles/iam.serviceAccountTokenCreator` | The impersonated SA |
| The impersonated SA | `roles/iap.httpsResourceAccessor` | GoCD IAP web resource |

The `role-deploy-user@sentry.io` group is the same group that grants access to the GoCD web UI, so any engineer who can see GoCD in a browser can also use this skill.

### Why service account impersonation is secure

1. **No keys are distributed.** The service account has no exported key files. Engineers authenticate as themselves — their own `gcloud auth login` session is the only credential on disk. There is nothing to leak or rotate.

2. **Every call is audited.** Cloud Audit Logs record which user impersonated the SA, when, and what API call they made. This is more traceable than shared API keys or tokens.

3. **Access is instantly revocable.** Remove someone from `role-deploy-user@sentry.io` and they lose impersonation rights immediately. No keys to rotate, no tokens to invalidate.

4. **Tokens are short-lived.** Each impersonated identity token is valid for ~1 hour and is minted fresh per invocation. There is no long-lived credential to steal.

5. **Least privilege.** The SA only has `iap.httpsResourceAccessor` — it can pass through IAP, nothing else. The engineer only has `serviceAccountTokenCreator` on this one SA — they cannot impersonate other service accounts.

6. **No credential sharing.** Each engineer uses their own identity. Compare this to a shared `GOCD_ACCESS_TOKEN` environment variable that gets copy-pasted between machines with no attribution.

### Current configuration

| Setting | Value |
|---|---|
| Impersonated SA | `incident-scout-bot@incident-scout-bot.iam.gserviceaccount.com` |
| IAP audience | `610575311308-9bsjtgqg4jm01mt058rncpopujgk3627.apps.googleusercontent.com` |
| GoCD host | `https://deploy.getsentry.net` |

## Alternatives considered

| Approach | Why not |
|---|---|
| `GOCD_ACCESS_TOKEN` env var | Shared secret, no audit trail, must be manually distributed |
| `gcloud auth print-identity-token --audiences=...` (user account) | Not supported by gcloud for user accounts |
| Browser OAuth flow + cached refresh token | Interactive on first use, refresh tokens can expire after 6 months of inactivity |
| Service account key file | Keys can be leaked, must be rotated, Google recommends avoiding them |
| `gcloud auth print-identity-token` (no audience) | Token audience doesn't match IAP client ID — rejected with 401 |
