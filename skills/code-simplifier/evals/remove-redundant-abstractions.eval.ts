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

describeEval("remove-redundant-abstractions", {
  data: [
  {
    name: "remove-redundant-abstractions__trivial_wrapper",
    tests_behavior: "remove-redundant-abstractions",
    input: "Please refine this code I just touched:\n\n```js\nfunction isNotEmpty(arr) {\n  return arr.length > 0;\n}\n\nfunction isPositive(n) {\n  return n > 0;\n}\n\nfunction processItems(items, count) {\n  if (isNotEmpty(items) && isPositive(count)) {\n    return items.slice(0, count);\n  }\n  return [];\n}\n```",
    expectedContains: "items.length",
  },
  ],
  harness: skilletHarness({ skill: skillRoot }),
  judges: [SubstringJudge(), CriterionJudge()],
  threshold: 0.75,
  timeout: 120_000,
});
