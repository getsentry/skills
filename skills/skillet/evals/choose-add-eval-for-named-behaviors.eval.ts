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
} from "@sentry/skillet/evals";
import {
  RecommendsAddEvalJudge,
} from "./_judges.js";

const skillRoot = dirname(fileURLToPath(import.meta.url)).replace(/\/evals$/, "");

describeEval(
  "choose-add-eval-for-named-behaviors",
  {
    harness: piAiHarness({ agent: skilletAgent({ skillRoot }) }),
    judgeThreshold: 0.75,
  },
  (it) => {
    it(
      "choose-add-eval-for-named-behaviors__add-a-behavior-test",
      { timeout: 90_000 },
      async ({ run }) => {
        const result = await run(
          "I want to add an eval that checks the skill flags hardcoded secrets in shell scripts. What command do I use?",
        );

        await expect(result).toSatisfyJudge(RecommendsAddEvalJudge);
      },
    );
  },
);
