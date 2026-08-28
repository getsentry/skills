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
  UsesScopedPackageJudge,
} from "./_judges.js";

const skillRoot = dirname(fileURLToPath(import.meta.url)).replace(/\/evals$/, "");

describeEval(
  "scope-package-name",
  {
    harness: piAiHarness({ agent: skilletAgent({ skillRoot }) }),
    judgeThreshold: 0.75,
  },
  (it) => {
    it(
      "scope-package-name__one-liner-install",
      { timeout: 90_000 },
      async ({ run }) => {
        const result = await run(
          "Give me the one-liner to run skillet via npx so I can try it without installing globally.",
        );

        await expect(result).toSatisfyJudge(UsesScopedPackageJudge);
      },
    );
  },
);
