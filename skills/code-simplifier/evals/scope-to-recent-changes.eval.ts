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

describeEval("scope-to-recent-changes", {
  data: [
  {
    name: "scope-to-recent-changes__only_touched_file",
    tests_behavior: "scope-to-recent-changes",
    input: "I just edited src/recently-edited.js. Please refine my recent changes for elegance and clarity.",
    criteria: "The agent should only refine src/recently-edited.js (the recently modified file). It must NOT modify src/legacy.js or src/utils.js, and should not propose changes to those out-of-scope files. If the agent mentions them, it should be only to note they are out of scope.",
    setup: "mkdir -p src\ncat > src/recently-edited.js <<'EOF'\nfunction add(a, b) {\n  let result;\n  result = a + b;\n  return result;\n}\nmodule.exports = { add };\nEOF\ncat > src/legacy.js <<'EOF'\n// Old code, untouched in this session\nfunction oldFunc(x) {\n  var y = x;\n  if (y == null) { return null; } else { return y * 2; }\n}\nmodule.exports = { oldFunc };\nEOF\ncat > src/utils.js <<'EOF'\n// Untouched utilities\nfunction format(s) { return ('' + s).trim(); }\nmodule.exports = { format };\nEOF",
  },
  ],
  harness: skilletHarness({ skill: skillRoot }),
  judges: [SubstringJudge(), CriterionJudge()],
  threshold: 0.75,
  timeout: 120_000,
});
