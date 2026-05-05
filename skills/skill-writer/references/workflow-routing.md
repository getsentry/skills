# Routing Workflows

Use this workflow when the incoming request must be classified and sent to different downstream prompts, references, scripts, or tools.

## Choose this workflow when

- distinct request classes benefit from specialized downstream handling
- one broad prompt would create conflicts or false positives
- misroutes can be detected and recovered

## Required contract

1. Route-selection criteria.
2. Default route or clarification fallback.
3. Misroute recovery.
4. Downstream contract for each route.

## Example

```markdown
1. Classify the request:

   **Billing question?** -> Load `references/billing.md`
   **Refund request?** -> Run `scripts/refund_intake.py`
   **Technical bug?** -> Load `references/triage.md`

2. If classification is uncertain, ask one clarification question before continuing.
```
