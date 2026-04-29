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

describeEval("no-prioritizing-line-count", {
  data: [
  {
    name: "no-prioritizing-line-count__readability_wins",
    tests_behavior: "no-prioritizing-line-count",
    input: "Please make this as short as possible:\n\n```js\nfunction categorize(score) {\n  if (score >= 90) {\n    return 'A';\n  }\n  if (score >= 80) {\n    return 'B';\n  }\n  if (score >= 70) {\n    return 'C';\n  }\n  return 'F';\n}\n```",
    criteria: "Even though the user asked for it to be 'as short as possible', the agent must NOT sacrifice readability for fewer lines. It should not produce a dense nested ternary or a cryptic one-liner. The agent should explain or implicitly demonstrate that clarity takes priority over line count, and the result should remain easy to read.",
  },
  ],
  harness: skilletHarness({ skill: skillRoot }),
  judges: [SubstringJudge(), CriterionJudge()],
  threshold: 0.75,
  timeout: 120_000,
});
