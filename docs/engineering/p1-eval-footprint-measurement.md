# P1 measurement: creative-style evaluation footprint

## Problem redefinition

For a prompt-heavy creative skill, the suspected cost center is the amount of instruction and evaluation material carried into each generation request. The relevant question is whether duplicated rules or always-loaded guidance materially increase prompt footprint or iteration count without improving output quality.

## Hypothesis

Some instruction blocks may have low marginal quality contribution while increasing prompt length and conflict surface. Measure contribution before removing or consolidating anything.

## Fixed corpus

Use the existing representative evaluation cases across style families, hard constraints, reference use, typography, and negative constraints.

For each case record:

- instruction/prompt token estimate
- number of rule blocks
- duplicated or near-duplicated rule count
- hard-constraint pass rate
- style-attribute pass rate
- unintended-element rate
- retry/iteration count

## Ablation

Measure current behavior, then remove or consolidate one rule block at a time. Keep generation settings and reference inputs fixed. A removal is accepted only when quality is statistically indistinguishable or improved and prompt footprint decreases.

## P1 gate

Do not optimize for shorter prompts alone. The candidate must reduce prompt/context cost or retries while preserving the existing quality envelope.

This PR is measurement-only and does not change generation guidance.
