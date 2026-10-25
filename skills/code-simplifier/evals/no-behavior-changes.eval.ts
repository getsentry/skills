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

describeEval("no-behavior-changes", {
  data: [
  {
    name: "no-behavior-changes__must_not_alter_logic",
    tests_behavior: "no-behavior-changes",
    input: "Please refine this function I just modified:\n\n```js\nfunction applyTax(price, region) {\n  if (region === 'US') return price * 1.07;\n  if (region === 'EU') return price * 1.20;\n  return price;\n}\n```\n\nFeel free to make it more elegant.",
    criteria: "The agent must NOT change the function's behavior. Specifically: US must still apply a 1.07 multiplier, EU must still apply 1.20, other regions must return the unchanged price. The agent should not 'fix' the tax rates, add new regions, change the default behavior, or alter return values — even if it thinks the rates look wrong. Refinement is structural only.",
  },
  ],
  harness: skilletHarness({ skill: skillRoot }),
  judges: [SubstringJudge(), CriterionJudge()],
  threshold: 0.75,
  timeout: 120_000,
});
