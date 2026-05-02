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

describeEval("no-out-of-scope-refinement", {
  data: [
  {
    name: "no-out-of-scope-refinement__do_not_touch_unrelated",
    tests_behavior: "no-out-of-scope-refinement",
    input: "I just edited src/just-edited.js. Please refine my work.",
    criteria: "The agent must NOT modify src/old-billing.js or src/old-auth.js, and must not propose unsolicited refactors of those files. Refinement should be limited to src/just-edited.js. If the agent notices issues elsewhere, it may briefly mention them as out of scope but must not change them.",
    setup: "mkdir -p src\ncat > src/just-edited.js <<'EOF'\nfunction greet(name) {\n  let msg;\n  msg = 'Hello, ' + name;\n  return msg;\n}\nmodule.exports = { greet };\nEOF\ncat > src/old-billing.js <<'EOF'\n// Untouched in this session — legacy billing logic\nfunction calcBill(items) {\n  var total = 0;\n  for (var i = 0; i < items.length; i++) { total = total + items[i].amt; }\n  return total;\n}\nmodule.exports = { calcBill };\nEOF\ncat > src/old-auth.js <<'EOF'\n// Untouched legacy auth\nfunction checkAuth(t) { if (t == null) { return false; } else { return t.length > 0; } }\nmodule.exports = { checkAuth };\nEOF",
  },
  ],
  harness: skilletHarness({ skill: skillRoot }),
  judges: [SubstringJudge(), CriterionJudge()],
  threshold: 0.75,
  timeout: 120_000,
});
