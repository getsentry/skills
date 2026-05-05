# Case Study: Router Skill Synthesis

## Scenario

Goal: create a skill that classifies requests into distinct downstream paths without overloading one prompt.

## Input collection approach

This case collected:

1. examples of request categories
2. known ambiguous cases
3. downstream resources for each route
4. historical misroutes and their fixes

Collection stopped only after route criteria and fallback behavior were explicit.

## Coverage matrix used

Required dimensions tracked during synthesis:

1. route categories and triggers
2. ambiguous or overlapping cases
3. downstream ownership per route
4. default/fallback path
5. misroute recovery behavior

## Synthesized artifacts produced

The resulting skill references included:

1. route-selection table
2. one reference or script per route
3. ambiguous-case examples
4. fallback rule for unclear input

## What made this high quality

1. the route table was explicit
2. every route had one clear downstream owner
3. the skill knew what to do when classification was uncertain
