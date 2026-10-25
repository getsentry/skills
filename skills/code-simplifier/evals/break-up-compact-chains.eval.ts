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

describeEval("break-up-compact-chains", {
  data: [
  {
    name: "break-up-compact-chains__named_intermediates",
    tests_behavior: "break-up-compact-chains",
    input: "Please refine this function I just wrote:\n\n```js\nfunction topActiveUsers(users) {\n  return users.filter(u => u.active).map(u => ({ name: u.name, score: u.posts * 2 + u.comments })).sort((a, b) => b.score - a.score).slice(0, 10);\n}\n```",
    criteria: "The refined code must break the compact chain into clearly named intermediate variables that show each step (e.g., `activeUsers`, `usersWithScores`, `sortedUsers`, `topTen` or similarly descriptive names). The single chained expression should be replaced with multiple statements assigned to readable names.",
  },
  ],
  harness: skilletHarness({ skill: skillRoot }),
  judges: [SubstringJudge(), CriterionJudge()],
  threshold: 0.75,
  timeout: 120_000,
});
