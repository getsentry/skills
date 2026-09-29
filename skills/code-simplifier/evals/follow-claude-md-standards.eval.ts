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

describeEval("follow-claude-md-standards", {
  data: [
  {
    name: "follow-claude-md-standards__react_component",
    tests_behavior: "follow-claude-md-standards",
    input: "I just touched UserCard.tsx. Please refine it to follow the standards in CLAUDE.md.",
    criteria: "The refined component must: use the `function` keyword (not an arrow function) for the top-level component, define an explicit `Props` type for the component's props, include an explicit return type annotation on the component function, sort imports alphabetically, and use `.js` extensions on relative imports. The agent should reference CLAUDE.md standards in its reasoning.",
    setup: "cat > CLAUDE.md <<'EOF'\n# Coding Standards\n- Use ES modules with explicit `.js` extensions in imports\n- Sort imports alphabetically\n- Prefer `function` keyword over arrow functions for top-level functions\n- Always include explicit return type annotations on top-level functions\n- React components must have an explicit `Props` type\n- Avoid try/catch when possible\nEOF\ncat > UserCard.tsx <<'EOF'\nimport { formatName } from './utils';\nimport { Avatar } from './Avatar';\n\nconst UserCard = (props) => {\n  return <div><Avatar src={props.avatarUrl} />{formatName(props.name)}</div>;\n};\n\nexport default UserCard;\nEOF",
  },
  ],
  harness: skilletHarness({ skill: skillRoot }),
  judges: [SubstringJudge(), CriterionJudge()],
  threshold: 0.75,
  timeout: 120_000,
});
