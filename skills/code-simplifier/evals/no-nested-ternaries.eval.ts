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

describeEval("no-nested-ternaries", {
  data: [
  {
    name: "no-nested-ternaries__must_not_introduce_them",
    tests_behavior: "no-nested-ternaries",
    input: "Please make this more concise:\n\n```js\nfunction getDiscount(tier) {\n  if (tier === 'gold') {\n    return 0.3;\n  } else if (tier === 'silver') {\n    return 0.2;\n  } else if (tier === 'bronze') {\n    return 0.1;\n  } else {\n    return 0;\n  }\n}\n```",
    criteria: "The refined code must NOT use nested ternary operators (a ternary expression inside another ternary's true or false branch). A switch, if/else chain, or lookup table is acceptable. A single non-nested ternary is acceptable. The agent should not collapse the if/else chain into chained `?:` expressions.",
  },
  ],
  harness: skilletHarness({ skill: skillRoot }),
  judges: [SubstringJudge(), CriterionJudge()],
  threshold: 0.75,
  timeout: 120_000,
});
