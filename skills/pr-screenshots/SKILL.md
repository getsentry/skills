---
name: pr-screenshots
description: Capture UI screenshots of the real product and lay them out in a pull request description as before/after tables, then upload them with `gh --attach`.
---

# PR Screenshots

Screenshots in a PR are QA evidence. Each one shows what the real product
renders at one location, framed so a reviewer who has never opened the page can
tell what changed.

## Step 1: List the Locations

List every place in the product that the diff reaches: each page, drawer,
modal, or widget that renders a changed component, found by tracing its
callers and consumers. Then add the states the change affects at each of them,
such as loading, error, empty, hover, selected, menu open, expanded, scrolled,
narrow viewport, and light or dark theme.

Each location and state gets its own row. Never group surfaces into one row:
"GridEditable, as in Discover, dashboards and insights" is three rows.

## Step 2: Capture From the Real Product

| Rule | Detail |
|------|--------|
| Real build only | Screenshot the running app on the PR branch for "after" and on the base branch for "before". Never screenshot a story, mock page, or harness built for the PR, unless the change is to that story. |
| No injected changes | Never inject CSS or change the DOM to imitate the change. Stubbing API responses is fine; the frontend code must be the real code. |
| Seed missing data | If a state needs data no account has, create it in a local environment. Do not report a location as impossible to screenshot until seeding has been tried, and then say exactly what failed. |
| Identical framing | Capture the same region at the same dimensions for both shots of a pair, even when one state is taller. Emulate a fixed viewport instead of resizing the user's own browser window. |
| Context | Keep the heading or label that names the thing, nearby rows or controls, and a little padding on every side. For a hover, focus, or open-menu state, keep the trigger and the overlay in one frame. When the bug only makes sense in its page, show more of the page. |
| No empty bands | Crop out browser chrome, app navigation, and regions the change does not touch. For full-width layouts, shrink the viewport instead of leaving wide blank space beside short content. |

## Step 3: Redact and Audit

1. Blur only private values: emails, usernames, customer or organization names
   and slugs, IDs, and internal hostnames. Keep keys, labels, and non-sensitive
   values readable, such as `browser.name` → `chrome`.
2. Paint over each region before blurring it so the blur can't be reversed.
   Never use solid black or dark boxes, and never blur whole tables or rows.
3. Read every image before uploading it and check for credentials: tokens, auth
   headers, cookies, signed URLs, secret keys, and webhook endpoints. Remove
   real leaks. Do not treat a public client DSN as a leak.

## Step 4: Choose the Table Shape

| Change | Shape |
|--------|-------|
| Visual change to existing UI | **Changed** table, plus an **Unchanged** table for locations the diff reaches that render the same. |
| New page or feature | No before/after. A few "after" screenshots, each introduced by a short sentence. When the new UI appears in several locations, use a `Location \| Screenshot` table instead. |
| Alternatives with no "before", such as prototype treatments or design options | `Treatment \| Screenshot` table, one row per alternative. |
| A change that differs by theme | Add a light and a dark row for each location, such as `Explore › Logs, dark`. For new UI, use `Light \| Dark` columns instead. |

Pixel-diff every before/after pair, then confirm by eye. Move a pair with no
visible difference, including anti-aliasing noise, to **Unchanged** with one
image. Leave out a table that would be empty.

```markdown
**Changed**

| Location | Before | After |
| --- | --- | --- |
| Explore › Logs | ![Explore › Logs before](./shots/logs-before.png) | ![Explore › Logs after](./shots/logs-after.png) |
| Explore › Logs, loading | ![Explore › Logs, loading before](./shots/logs-loading-before.png) | ![Explore › Logs, loading after](./shots/logs-loading-after.png) |

**Unchanged**

| Location | Before & After |
| --- | --- |
| Trace view › Logs | ![Trace view › Logs](./shots/trace-logs.png) |
```

Formatting rules:

- Name the first column `Location`, or `Treatment` for alternatives. Never
  leave its header empty.
- Write each location as a `›` breadcrumb of what the reader clicks through,
  then a comma and the state: `Monitors › cron monitor details › Check-Ins, loading`.
- Use only the columns shown above. Never add a "What changed" or notes column;
  the screenshots show the change.
- Give each image alt text naming its row and side, such as
  `Explore › Logs before`.
- Label the tables with bold `**Changed**` and `**Unchanged**` lines. Do not add
  an intro sentence describing where or how the screenshots were taken.
- Use Markdown tables by default, because `gh --attach` rewrites only Markdown
  image references. Switch to an HTML table only when cells must span rows, such
  as a light and dark row under one location
  (`Location | Theme | Before | After` with `rowspan="2"` on the location cell).
  Do not add `align` attributes.

## Step 5: Upload With gh

`gh pr create`, `gh pr edit`, `gh pr comment`, and the matching `gh issue`
commands accept `--attach '<path>#<alt text>'` (gh 2.99.0+). If `gh` rejects
the flag, ask the user to upgrade it. Do not push asset branches, commit
images, or upload through the browser's comment box.

Write the body file with relative Markdown image references, then pass the same
paths to `--attach`. gh uploads each file and rewrites the matching reference
to the uploaded URL in place:

```bash
gh pr edit 123 --body-file pr-body.md \
  --attach './shots/logs-before.png' --attach './shots/logs-after.png'
```

| Behavior | Detail |
|----------|--------|
| Paths | Resolve against the current directory, and must match the body's references exactly. |
| Unreferenced attachments | Get appended to the end of the body as `![alt](url)`. |
| No body flag | `gh pr edit --attach` keeps the existing body and appends the images. |
| HTML tables | `<img src="./x.png">` is not rewritten. Attach first, copy the appended URLs into the `<img>` tags, delete the appended lines, then write the final body with `--body-file`. |

Before writing a body the user may have edited, fetch it again and compare it
with the version you last read. Keep the user's wording and table edits, swap in
only your rows and URLs, and keep the body's line endings. Removing an image
from the body does not delete the uploaded file.

## Step 6: Keep Screenshots Current

When a later commit changes what a screenshot shows, retake the affected pairs,
re-check which pairs belong in **Changed** and **Unchanged**, and update the
body without waiting to be asked.
