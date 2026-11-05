// ──────────────────────────────────────────────────────────
// Generated initially from spec.yaml; durable after that. Edit
// freely to refine prompts, setup, and assertions for this
// behavior. Add or remove behaviors via spec.yaml — skillet only
// regenerates eval files for behaviors that don't have one yet.
// ──────────────────────────────────────────────────────────
import { fileURLToPath } from "node:url";
import { dirname } from "node:path";
import {
  describeEval,
  CriterionJudge,
  SubstringJudge,
  skilletHarness,
} from "@sentry/skillet/evals";

const skillRoot = dirname(fileURLToPath(import.meta.url)).replace(/\/evals$/, "");

describeEval("no-removing-helpful-abstractions", {
  data: [
  {
    name: "no-removing-helpful-abstractions__keep_helpers",
    tests_behavior: "no-removing-helpful-abstractions",
    input: "Please simplify this:\n\n```js\nfunction toCents(dollars) {\n  return Math.round(dollars * 100);\n}\n\nfunction formatCurrency(cents) {\n  return `$${(cents / 100).toFixed(2)}`;\n}\n\nfunction renderInvoice(items) {\n  const lines = items.map(i => `${i.name}: ${formatCurrency(toCents(i.price))}`);\n  return lines.join('\\n');\n}\n```",
    criteria: "The agent must NOT remove the `toCents` and `formatCurrency` helpers in the name of simplification — these are meaningful, reusable abstractions with clear domain semantics. They should remain as separate functions in the refined output. Inlining them into `renderInvoice` would be inappropriate over-simplification.",
  },
  ],
  harness: skilletHarness({ skill: skillRoot }),
  judges: [SubstringJudge(), CriterionJudge()],
  threshold: 0.75,
  timeout: 120_000,
});
