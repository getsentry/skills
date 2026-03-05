# Case Study: Security Review Skill Synthesis

## Scenario

Goal: build a skill that finds real vulnerabilities while minimizing false positives.

## Input collection approach

This case required balanced collection across offensive and defensive material:

1. Canonical standards and cheat sheets.
2. Framework/language-specific secure coding docs.
3. Real-world exploit writeups and postmortems.
4. Fixed vulnerability diffs and secure rewrites.
5. Benign patterns often misclassified as vulnerabilities.
6. Existing in-repo security skills and review heuristics.

Collection continued until each vulnerability class had both exploit and mitigation evidence.

## Coverage matrix used

Required dimensions tracked during synthesis:

1. Vulnerability class definitions and prerequisites.
2. Exploitable dataflow examples.
3. False-positive controls.
4. Severity/confidence calibration.
5. Concrete remediation patterns.
6. Framework-specific caveats and exceptions.

## Synthesized artifacts produced

The resulting skill references included:

1. True-positive case with exploitation path.
2. False-positive case with proof of safety.
3. Fix/remediation case with corrected code pattern.
4. Severity and confidence decision rubric.
5. Evidence checklist to prevent pattern-only claims.

## Source-to-decision trace (sample)

1. Source class: exploit writeups.
   Decision: require attacker-controlled input path in every high-confidence finding.
   Why: removed pattern-only false alarms.
2. Source class: benign counterexamples.
   Decision: add explicit safe-pattern checks before reporting.
   Why: reduced repeated false positives on sanitized data paths.
3. Source class: fixed vulnerability diffs.
   Decision: include remediation examples as patch-shaped guidance.
   Why: improved downstream fix quality and speed.

## Concrete artifacts (sample)

1. True-positive case:
   Input pattern: untrusted data reaches shell/API call without escaping.
   Output: finding includes source, sink, exploit path, and minimal patch recommendation.
2. False-positive case:
   Input pattern: potentially dangerous API with validated allowlist and strict escaping.
   Output: no vulnerability finding; include reason for non-reporting.
3. Remediation case:
   Before: dynamic query construction from user input.
   After: parameterized query plus validation guard.

## What made this high quality

1. It was trained on both attacks and safe counterexamples.
2. Findings required evidence of exploitability, not keyword matching.
3. Remediation guidance was concrete and immediately applicable.
