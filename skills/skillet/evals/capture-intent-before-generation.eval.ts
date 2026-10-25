// ──────────────────────────────────────────────────────────
// Generated initially from spec.yaml; durable after that. Edit
// freely to refine prompts, setup, and assertions for this
// behavior. Add or remove behaviors via spec.yaml — skillet only
// regenerates eval files for behaviors that don't have one yet.
// ──────────────────────────────────────────────────────────
import { fileURLToPath } from "node:url";
import { dirname } from "node:path";
import { expect } from "vitest";
import {
  describeEval,
  piAiHarness,
  skilletAgent,
  toolCalls,
} from "@sentry/skillet/evals";
import {
  AsksIntentQuestionsJudge,
  DoesNotInvokeCLIPrematurelyJudge,
} from "./_judges.js";

const skillRoot = dirname(fileURLToPath(import.meta.url)).replace(/\/evals$/, "");

describeEval(
  "capture-intent-before-generation",
  {
    harness: piAiHarness({ agent: skilletAgent({ skillRoot }) }),
    judgeThreshold: 0.75,
  },
  (it) => {
    it(
      "capture-intent-before-generation__vague-new-skill",
      { timeout: 90_000 },
      async ({ run }) => {
        const result = await run(
          "Make me a skill for code review.",
        );

        // Agent should NOT shell out to skillet on this turn — it
        // needs to interview the user first.
        const names = toolCalls(result.session).map((c) => c.name);
        expect(names).not.toContain("Bash");
        expect(names).not.toContain("bash");

        await expect(result).toSatisfyJudge(AsksIntentQuestionsJudge);
        await expect(result).toSatisfyJudge(DoesNotInvokeCLIPrematurelyJudge);
      },
    );
  },
);
