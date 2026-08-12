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

describeEval("no-overly-clever-solutions", {
  data: [
  {
    name: "no-overly-clever-solutions__avoid_cryptic_tricks",
    tests_behavior: "no-overly-clever-solutions",
    input: "Please refine this for elegance:\n\n```js\nfunction parityLabel(n) {\n  if (n % 2 === 0) {\n    return 'even';\n  }\n  return 'odd';\n}\n```",
    criteria: "The refined code must remain easy to understand. The agent must NOT introduce overly clever tricks such as bitwise hacks (`n & 1`), array-indexing tricks (`['even','odd'][n & 1]`), or other cryptic micro-optimizations that obscure intent. A simple ternary or the original if/else is fine; clever golf-style code is not.",
  },
  ],
  harness: skilletHarness({ skill: skillRoot }),
  judges: [SubstringJudge(), CriterionJudge()],
  threshold: 0.75,
  timeout: 120_000,
});
