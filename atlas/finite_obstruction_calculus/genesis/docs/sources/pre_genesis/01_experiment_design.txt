# 01. The experiment and its design

**AuthorityEffect:** None.
**Sources:** [`sources/design_derivation_v0.md`](sources/design_derivation_v0.md),
[`sources/analysis_derivation_v1.md`](sources/analysis_derivation_v1.md).

## The question

The design states its research question in one sentence
([v0 line 426](sources/design_derivation_v0.md#L426)):

> When a frontier language model is given an uninterpreted finite inscription
> and is required to distinguish external presentation from internal
> expressibility, what symbolic resources does it introduce, in what order,
> and under what failures does it enlarge the regime?

It rejects the headline "DeepSeek rediscovered the Omega Engine" in advance
([v0 line 422](sources/design_derivation_v0.md#L422)). The point was to watch
what a model adds to a bare mark, not to get it to reproduce a known theory.

## Constrain epistemology, not mathematics

The first principle is in bold at the top of the design
([v0 line 3](sources/design_derivation_v0.md#L3)): the prompt should constrain
epistemology, not mathematics. An earlier "Pontryagin experiment" had
over-specified the stages, statuses, proof path and receipt type, and the model
treated the task as a simulation and considered producing a fake hash
([v0 line 5](sources/design_derivation_v0.md#L5)).

So the model was not told any of the comparison targets: that `<>` stands for
Primitive Difference, that obstructions should be removed or structure added,
that a lift, quotient, tower, DDC trace, Prime algorithm or cochain should
appear, or that `<a>` was the intended next state
([v0 lines 7 to 16](sources/design_derivation_v0.md#L7)). The only distinction
the prompts make explicit is between what an external reader can see and what
the regime can express with the rules it has actually been given.

## Pre-registered branches

The continuation rules were fixed before the first reply was read
([v0 lines 173 to 207](sources/design_derivation_v0.md#L173)):

| Branch | If the model... | Then |
| --- | --- | --- |
| A | proposes `<a>` | continue, present `<a>` as current, ask what was added; do not congratulate it |
| B | proposes another payload such as `<x>` | follow its symbol exactly |
| C | proposes a relation, duplication, nesting or operator | keep it as a native branch; introduce `<a>` in a cloned transcript |
| D | says no continuation is forced | count it as a success; introduce `<a>` as a caller intervention marked "not model-derived but externally supplied" |

Branch D is the important one: "no move" is a correct answer, not a failure.

## Controls and the auditor

- Raw controls: the bare `<>` first, then `[]`, `{}`, `()`, `><`, `||`, `¤§`,
  `a`, `aa`, `ab` ([v0 lines 393 to 412](sources/design_derivation_v0.md#L393)).
- A separate auditor prompt, run blind on a reply, to find the earliest place
  where the reply imported structure it was not given
  ([v0 lines 294 to 331](sources/design_derivation_v0.md#L294)).
- No packet wrapper during discovery
  ([v0 lines 104 to 136](sources/design_derivation_v0.md#L104)).

## Two defects found afterwards

The Trial 1 analysis records two defects in how the design was carried out
([v1 lines 358 to 408](sources/analysis_derivation_v1.md#L358)): the controls
were sent inside ```` ```text ```` code fences, which changes how a model reads
them, and the `<a>` prompt and the collision prompt were sent in one message.
Trial 2 sent the controls raw and the steps one at a time.
