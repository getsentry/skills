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

describeEval("no-combining-concerns", {
  data: [
  {
    name: "no-combining-concerns__keep_separated",
    tests_behavior: "no-combining-concerns",
    input: "Please refine this code I just edited. There's a UserProfile component, a fetchUser function, and a formatUser function — feel free to clean it up:\n\n```jsx\nasync function fetchUser(id) {\n  const res = await fetch(`/api/users/${id}`);\n  return res.json();\n}\n\nfunction formatUser(user) {\n  return { ...user, displayName: `${user.first} ${user.last}` };\n}\n\nfunction UserProfile({ id }) {\n  const [user, setUser] = useState(null);\n  useEffect(() => { fetchUser(id).then(u => setUser(formatUser(u))); }, [id]);\n  return user ? <div>{user.displayName}</div> : null;\n}\n```",
    criteria: "The agent must NOT merge fetching, formatting, and rendering concerns into a single function or component. The data-fetching logic, formatting logic, and the React component should remain as distinct concerns (separate functions or hooks). Combining them all into one mega-function in the name of 'simplicity' is unacceptable.",
  },
  ],
  harness: skilletHarness({ skill: skillRoot }),
  judges: [SubstringJudge(), CriterionJudge()],
  threshold: 0.75,
  timeout: 120_000,
});
