Status: AI-drafted, awaiting human review.

# COMP-C7-FIXED-TARGET-OPEN two erasures

The node stays OPEN. This note records two hole replacements. It does not treat the extended rule set R0 prime.

## One-hole replacement

A hole rule is a pair of lists `(lhs, rhs)`. It applies when a word splits as `left ++ lhs ++ right`, and the result is `left ++ rhs ++ right`.

## Two erasures

- `left = []`, `lhs = [1]`, `right = [0]`, `rhs = []` sends `[1, 0]` to `[0]`.
- `left = []`, `lhs = [2]`, `right = [0]`, `rhs = []` sends `[2, 0]` to `[0]`.

Both results are the list `[0]`.

## What is proved

- Erasing the block `[1]` from `[1, 0]` yields `[0]`.
- Erasing the block `[2]` from `[2, 0]` yields `[0]`.

The Lean declarations are `eraseOneToFixed` and `eraseTwoToFixed` in `lean4/ComputationC7FixedTargetOpen.lean`.

## What is assumed

List concatenation in the Lean kernel. No new axiom is declared. The node status stays OPEN.

## What is open

Reach of the extended rule set R0 prime from `startWord x` to one fixed target word exactly when `univFun x` is defined is not given here.
