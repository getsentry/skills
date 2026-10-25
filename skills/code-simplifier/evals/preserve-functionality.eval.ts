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

describeEval("preserve-functionality", {
  data: [
  {
    name: "preserve-functionality__refactor_discount_calc",
    tests_behavior: "preserve-functionality",
    input: "I just modified this function. Please refine it for elegance and clarity:\n\n```js\nfunction calculateDiscount(price, customerType) {\n  let discount = 0;\n  if (customerType === 'premium') {\n    discount = price * 0.2;\n  } else if (customerType === 'regular') {\n    discount = price * 0.1;\n  } else {\n    discount = 0;\n  }\n  return price - discount;\n}\n```\n\nThe inputs and outputs must remain identical for all customer types.",
    criteria: "The refined code must preserve identical behavior: premium customers get 20% off, regular customers get 10% off, and all other customer types get no discount. The function must return price minus the appropriate discount. The agent should not introduce new behaviors, change the discount percentages, change which customer types map to which discounts, or alter return values.",
  },
  ],
  harness: skilletHarness({ skill: skillRoot }),
  judges: [SubstringJudge(), CriterionJudge()],
  threshold: 0.75,
  timeout: 120_000,
});
