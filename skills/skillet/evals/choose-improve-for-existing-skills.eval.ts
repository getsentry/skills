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
  RecommendsSkilletImproveJudge,
  UsesScopedPackageJudge,
} from "./_judges.js";

const skillRoot = dirname(fileURLToPath(import.meta.url)).replace(/\/evals$/, "");

describeEval(
  "choose-improve-for-existing-skills",
  {
    harness: piAiHarness({ agent: skilletAgent({ skillRoot }) }),
    judgeThreshold: 0.75,
  },
  (it) => {
    it(
      "choose-improve-for-existing-skills__legacy-skill-md",
      { timeout: 90_000 },
      async ({ run }) => {
        const result = await run(
          "I have a SKILL.md file from another project but no spec.yaml. I want to clean it up and add a couple of missing behaviors. What's the workflow?",
        );

        await expect(result).toSatisfyJudge(RecommendsSkilletImproveJudge);
        await expect(result).toSatisfyJudge(UsesScopedPackageJudge);
      },
    );
  },
);
