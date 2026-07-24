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
  DoesNotRecommendHandEditSkillMdJudge,
  ExplainsEvalsAreDurableJudge,
  RecommendsSpecRefineJudge,
} from "./_judges.js";

const skillRoot = dirname(fileURLToPath(import.meta.url)).replace(/\/evals$/, "");

describeEval(
  "dont-tell-user-to-handedit-derived-files",
  {
    harness: piAiHarness({ agent: skilletAgent({ skillRoot }) }),
    judgeThreshold: 0.75,
  },
  (it) => {
    it(
      "dont-tell-user-to-handedit-derived-files__skill-md-tweak",
      { timeout: 90_000 },
      async ({ run }) => {
        const result = await run(
          "There's a sentence in SKILL.md I'd like to rephrase. Should I just open the file and change it?",
        );

        await expect(result).toSatisfyJudge(DoesNotRecommendHandEditSkillMdJudge);
        await expect(result).toSatisfyJudge(RecommendsSpecRefineJudge);
      },
    );

    it(
      "dont-tell-user-to-handedit-derived-files__eval-file-tweak",
      { timeout: 90_000 },
      async ({ run }) => {
        const result = await run(
          "I want to tighten an assertion in one of my evals/*.eval.ts files. Is editing it directly the right move, or do I have to go through the CLI?",
        );

        await expect(result).toSatisfyJudge(ExplainsEvalsAreDurableJudge);
      },
    );
  },
);
