# Model Family Notes

Use this file to adapt prompts to model behavior instead of assuming all model families respond the same way.

## OpenAI

### Reasoning models

- Prefer straightforward `developer` instructions with a clear end goal.
- Keep prompts simple and direct.
- Avoid explicitly requesting chain-of-thought or "think step by step" behavior.
- Use delimiters such as markdown headings, XML tags, or section titles when the prompt mixes multiple content blocks.
- Try zero-shot first. Add few-shot examples only when the output contract or edge cases need them.
- Be explicit about constraints, success criteria, and completion conditions.
- Tool schemas are disclosed via the Responses API `tools` parameter. Keep tool policy (when/why/whether to call) in the prompt; do not restate tool names or argument schemas.

### GPT-style non-reasoning models

- Use more explicit instructions than you would for a reasoning model.
- Spell out the logic, data, and schema the model should use.
- Precise format instructions and tightly matched examples are especially helpful.
- Good default for tasks where deterministic formatting matters more than open-ended planning.

## Anthropic Claude

- Clear, direct instructions outperform vague prompting.
- A lightweight role statement can materially improve consistency.
- XML-style tags are especially useful when mixing instructions, context, examples, and variable inputs.
- Three to five strong examples are often a good default when examples are needed.
- For long context, place long documents before the question and put the actual query near the end.
- When grounding in long documents, asking for relevant quotes first can improve downstream analysis.
- If tool use or progress-update behavior matters, specify it explicitly rather than assuming the model will infer it.
- When you call the Messages API with `tools`, the API injects the tool definitions into a special system prompt automatically. Keep your user-authored system prompt focused on policy; put tool detail in each tool's `description` field rather than re-listing schemas in prose.

## Gemini

- Use clear, specific instructions.
- Few-shot examples are recommended by default; keep them structurally consistent.
- Prefer positive demonstrations over anti-pattern-only demonstrations.
- Break complex tasks into smaller components or chained prompts when one large prompt becomes hard to steer.
- Use system instructions when the target runtime supports them.
- Thinking is dynamic by default on modern Gemini thinking models; tune it only when latency or deeper reasoning warrants it.
- Gemini long-context workflows can benefit from many-shot in-context learning when you have a large bank of representative examples.
- Tool schemas are disclosed via the Gemini API `tools` (function declarations) parameter. Keep the prompt focused on tool policy; do not re-list function names or parameter schemas.

## Cross-family adapter rules

- Keep a provider-agnostic base prompt whenever possible.
- Add a small adapter layer per family rather than forking the entire prompt immediately.
- Retest after changing model family or snapshot.
- Do not transport reasoning-model assumptions, few-shot defaults, or formatting quirks blindly across providers.
- When behavior diverges sharply, keep the shared contract stable and specialize only the parts that actually fail in evals.
