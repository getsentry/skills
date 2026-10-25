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
  ExplainsEvalsAreDurableJudge,
  ExplainsSpecAsSourceOfTruthJudge,
  RecommendsSpecRefineJudge,
} from "./_judges.js";

const skillRoot = dirname(fileURLToPath(import.meta.url)).replace(/\/evals$/, "");

describeEval(
  "explain-spec-as-source-of-truth",
  {
    harness: piAiHarness({ agent: skilletAgent({ skillRoot }) }),
    judgeThreshold: 0.75,
  },
  (it) => {
    it(
      "explain-spec-as-source-of-truth__editing-skill-md",
      { timeout: 90_000 },
      async ({ run }) => {
        const result = await run(
          "I want to tweak the wording in SKILL.md to make it clearer. Can I just open it and edit?",
        );

        await expect(result).toSatisfyJudge(ExplainsSpecAsSourceOfTruthJudge);
        await expect(result).toSatisfyJudge(RecommendsSpecRefineJudge);
      },
    );

    it(
      "explain-spec-as-source-of-truth__editing-eval-files",
      { timeout: 90_000 },
      async ({ run }) => {
        const result = await run(
          "Can I hand-edit the files under evals/ to tighten up the assertions, or will skillet overwrite them?",
        );

        await expect(result).toSatisfyJudge(ExplainsEvalsAreDurableJudge);
      },
    );
  },
);
