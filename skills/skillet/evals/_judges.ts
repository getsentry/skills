import { criterionJudge } from "@sentry/skillet/evals";

export const AsksIntentQuestionsJudge = criterionJudge(
  "AsksIntentQuestionsJudge",
  "Asks 3-5 clarifying questions about behaviors, prompts/outputs, mistakes, or trigger phrases before generating or invoking the CLI.",
);

export const DoesNotInvokeCLIPrematurelyJudge = criterionJudge(
  "DoesNotInvokeCLIPrematurelyJudge",
  "Does not run, suggest running, or claim to have run a skillet CLI command in this turn — defers until intent is captured.",
);

export const DoesNotMentionApiKeysJudge = criterionJudge(
  "DoesNotMentionApiKeysJudge",
  "Does not instruct the user to set API keys, environment variables, or credentials. Does not name any provider env var.",
);

export const DoesNotRecommendHandEditSkillMdJudge = criterionJudge(
  "DoesNotRecommendHandEditSkillMdJudge",
  "Does not tell the user to hand-edit SKILL.md. Notes that SKILL.md is regenerated/clobbered and routes prose changes through spec.yaml.",
);

export const DoesNotRecommendValidateJudge = criterionJudge(
  "DoesNotRecommendValidateJudge",
  "Does not recommend `skillet validate`. If the verification concept comes up, uses `verify` instead.",
);

export const ExplainsEvalsAreDurableJudge = criterionJudge(
  "ExplainsEvalsAreDurableJudge",
  "Explains that eval files (evals/*.eval.ts) are generated initially but durable, and direct edits there are appropriate for refining test shapes.",
);

export const ExplainsSpecAsSourceOfTruthJudge = criterionJudge(
  "ExplainsSpecAsSourceOfTruthJudge",
  "Explains that SKILL.md is derived from spec.yaml and regenerated, so behavioral changes flow through the spec (e.g. `skillet spec refine`).",
);

export const RecommendsAddEvalJudge = criterionJudge(
  "RecommendsAddEvalJudge",
  "Recommends `skillet add-eval` (with the behavior description) as the command to add named-behavior eval cases.",
);

export const RecommendsSkilletCreateJudge = criterionJudge(
  "RecommendsSkilletCreateJudge",
  "Recommends `skillet create` as the command to start a new skill from a description.",
);

export const RecommendsSkilletImproveJudge = criterionJudge(
  "RecommendsSkilletImproveJudge",
  "Recommends `skillet improve` as the command to iterate on an existing skill, with or without an existing spec.yaml.",
);

export const RecommendsSpecRefineJudge = criterionJudge(
  "RecommendsSpecRefineJudge",
  "Recommends `skillet spec refine \"<feedback>\"` as the way to change a skill via natural-language feedback.",
);

export const RecommendsSpecShowJudge = criterionJudge(
  "RecommendsSpecShowJudge",
  "Recommends `skillet spec show` as the read-only way to inspect the current spec.",
);

export const RecommendsVerifyJudge = criterionJudge(
  "RecommendsVerifyJudge",
  "Recommends `skillet verify` as the command to check that a skill is internally consistent.",
);

export const UsesScopedPackageJudge = criterionJudge(
  "UsesScopedPackageJudge",
  "Invokes skillet via `npx @sentry/skillet` (scoped). Does not use the unscoped `npx skillet` form.",
);
