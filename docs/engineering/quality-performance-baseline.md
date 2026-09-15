# Creative Style Quality and Performance Baseline

## Problem redefinition

The objective of a creative-style system is not to maximize prompt length or the number of visual rules. The engineering target is:

> Maximize visual fidelity to the requested style and constraints per unit of prompt/context complexity, while minimizing unintended additions and unstable outputs.

## MECE evaluation dimensions

1. **Style fidelity**: composition, palette, texture, typography, and declared visual language.
2. **Constraint fidelity**: aspect ratio, required elements, prohibited elements, text-layer rules, and reference-only constraints.
3. **Semantic fidelity**: the generated image still expresses the requested subject and concept.
4. **Variation control**: intended randomness varies outputs without breaking hard constraints.
5. **Efficiency and reliability**: prompt size, redundant instructions, repeated generations, malformed inputs, and regression behavior.

## Fixed evaluation corpus

Use a small versioned corpus covering:

- simple subject + style
- multiple simultaneous hard constraints
- reference-image-driven requests
- typography-sensitive layouts
- negative constraints
- deliberately ambiguous prompts
- adversarial prompts that tempt the system to add unspecified elements

## Quantitative gates

Track constraint pass rate, style-attribute pass rate, unintended-element rate, text accuracy where applicable, and generation/retry count. For prompt changes, compare the same corpus before and after the change.

## P1 optimization gate

A P1 change must provide:

- a measured failure or cost concentration
- one falsifiable hypothesis
- an ablation against the previous prompt/rule set
- no regression on hard constraints
- documented quality trade-offs

Prompt shortening, rule consolidation, or adding more examples is not accepted as an optimization by itself. The result must improve a measurable outcome.

## Experiment loop

`baseline -> classify failures -> identify bottleneck -> single-variable change -> ablation -> regression review -> retain/revert`
