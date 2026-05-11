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

describeEval("follow-refinement-process", {
  data: [
  {
    name: "follow-refinement-process__structured_steps",
    tests_behavior: "follow-refinement-process",
    input: "I just modified this function. Walk me through refining it:\n\n```js\nfunction summarize(items) {\n  // loop through items\n  let total = 0;\n  for (let i = 0; i < items.length; i++) {\n    total = total + items[i].price;\n  }\n  return total;\n}\n```",
    criteria: "The agent should follow a structured refinement process: identify what was recently modified, analyze for elegance/consistency opportunities, apply standards, verify functionality is unchanged, confirm the result is simpler/more maintainable, and document only significant changes (not trivial ones). The response should reflect these phases rather than just dumping a rewrite.",
  },
  ],
  harness: skilletHarness({ skill: skillRoot }),
  judges: [SubstringJudge(), CriterionJudge()],
  threshold: 0.75,
  timeout: 120_000,
});
