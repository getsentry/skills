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

describeEval("reduce-complexity", {
  data: [
  {
    name: "reduce-complexity__simplify_nested_logic",
    tests_behavior: "reduce-complexity",
    input: "I just edited this function. Please refine it:\n\n```js\nfunction getStatus(user) {\n  // Check if user exists\n  let result;\n  if (user) {\n    if (user.active) {\n      if (user.verified) {\n        result = 'active';\n      } else {\n        result = 'pending';\n      }\n    } else {\n      result = 'inactive';\n    }\n  } else {\n    result = 'unknown';\n  }\n  return result; // return the result\n}\n```",
    criteria: "The refined code should reduce nesting (e.g., via early returns or guard clauses), remove the obvious comments (`// Check if user exists`, `// return the result`), and produce clearer, flatter control flow. The behavior must remain identical for all four cases (no user, inactive, unverified active, verified active).",
  },
  ],
  harness: skilletHarness({ skill: skillRoot }),
  judges: [SubstringJudge(), CriterionJudge()],
  threshold: 0.75,
  timeout: 120_000,
});
