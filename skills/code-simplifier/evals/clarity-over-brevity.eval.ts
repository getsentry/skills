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

describeEval("clarity-over-brevity", {
  data: [
  {
    name: "clarity-over-brevity__expand_dense_oneliner",
    tests_behavior: "clarity-over-brevity",
    input: "Please refine this code I just modified:\n\n```js\nfunction processOrders(orders) {\n  return orders.filter(o => o.s === 'p' && o.t > 100).map(o => ({...o, f: o.t * 0.05, n: o.t + o.t * 0.05})).sort((a, b) => b.n - a.n).slice(0, 5);\n}\n```",
    criteria: "The refined code should choose clarity over brevity: use descriptive variable/property names instead of cryptic single letters (s, t, f, n), break the dense chain into clearly named intermediate steps, and not optimize for fewer lines. The result should be noticeably more readable even if longer.",
  },
  ],
  harness: skilletHarness({ skill: skillRoot }),
  judges: [SubstringJudge(), CriterionJudge()],
  threshold: 0.75,
  timeout: 120_000,
});
