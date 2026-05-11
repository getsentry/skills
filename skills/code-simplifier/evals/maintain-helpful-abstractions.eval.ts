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

describeEval("maintain-helpful-abstractions", {
  data: [
  {
    name: "maintain-helpful-abstractions__keep_validation_helpers",
    tests_behavior: "maintain-helpful-abstractions",
    input: "Please refine this code:\n\n```js\nfunction validateEmail(email) {\n  return /^[^@]+@[^@]+\\.[^@]+$/.test(email);\n}\n\nfunction validatePhone(phone) {\n  return /^\\+?[0-9]{10,15}$/.test(phone);\n}\n\nfunction validateZip(zip) {\n  return /^[0-9]{5}(-[0-9]{4})?$/.test(zip);\n}\n\nfunction registerUser(data) {\n  if (!validateEmail(data.email)) return { ok: false, error: 'email' };\n  if (!validatePhone(data.phone)) return { ok: false, error: 'phone' };\n  if (!validateZip(data.zip)) return { ok: false, error: 'zip' };\n  return { ok: true };\n}\n```\n\nI just touched these.",
    criteria: "The agent must preserve the separate `validateEmail`, `validatePhone`, and `validateZip` helper abstractions (or equivalently named clear abstractions) rather than inlining all the regex tests into `registerUser`. These helpers are clearly useful for organization and reuse, so they should not be eliminated in the name of simplification.",
  },
  ],
  harness: skilletHarness({ skill: skillRoot }),
  judges: [SubstringJudge(), CriterionJudge()],
  threshold: 0.75,
  timeout: 120_000,
});
