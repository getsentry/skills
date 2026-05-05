# Case Study: Subagent-Fork Skill Synthesis

## Scenario

Goal: create a skill that runs a self-contained task in isolated context and returns a concise summary.

## Input collection approach

This case collected:

1. official provider docs for skill execution in forked context
2. examples of self-contained tasks that benefit from isolation
3. failure cases where passive guidance was incorrectly put into subagents
4. summary expectations for returning results to the main thread

## Coverage matrix used

Required dimensions tracked during synthesis:

1. why isolation helps
2. task prompt clarity
3. output/summary contract
4. tool/model assumptions
5. portability constraints

## Synthesized artifacts produced

The resulting skill references included:

1. actionable task body
2. expected summary schema
3. portability note
4. anti-pattern showing passive guidance that should stay inline

## What made this high quality

1. the skill body was a task, not a convention list
2. the isolation benefit was concrete
3. the result expected back in the main thread was explicit
