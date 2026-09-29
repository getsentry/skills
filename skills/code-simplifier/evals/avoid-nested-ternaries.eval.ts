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

describeEval("avoid-nested-ternaries", {
  data: [
  {
    name: "avoid-nested-ternaries__role_label",
    tests_behavior: "avoid-nested-ternaries",
    input: "Please refine this function I just wrote:\n\n```js\nfunction getRoleLabel(role) {\n  return role === 'admin' ? 'Administrator' : role === 'editor' ? 'Editor' : role === 'viewer' ? 'Viewer' : 'Guest';\n}\n```",
    criteria: "The refined code must replace the nested ternary with either a switch statement, an if/else chain, or a lookup object/map. The result must NOT contain nested ternary operators (a ternary inside another ternary's branches). Behavior must remain the same for admin, editor, viewer, and any other role.",
  },
  ],
  harness: skilletHarness({ skill: skillRoot }),
  judges: [SubstringJudge(), CriterionJudge()],
  threshold: 0.75,
  timeout: 120_000,
});
