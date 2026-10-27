Status: AI-drafted, awaiting human review.

# COMP-C7-ENCODED-INSTANCE-REDUCTION word predicate

The fixed regime is the rewriting relation `Rules M0`. A word is a finite list of marks of type `Sym G1 (TM1to0.Λ' M1)`. A word is a normal form when it is irreducible for `Rules M0`. The word predicate `P` says that some irreducible word is reachable from the given word.

## The implication

Assume a `Primcodable` structure on that mark type, and assume `startWord` is a computable map from a natural number to a word. The claim is that `P` is then not a computable predicate.

Suppose a decider for `P` exists. Composing that decider with `startWord` yields a decider for the predicate on natural numbers that asks whether the start word of the input reaches an irreducible word. That predicate is `NFReach`. A decider for `NFReach` is already ruled out by `nfReach_not_computable`. Therefore no decider for `P` exists under the two assumptions.

`encoded_instance_reduction` in `lean4/ComputationC7EncodedInstanceReduction.lean` is the same implication as `reach_problem_not_computable` in `lean4/GenesisCompUniv.lean`. Both printed axiom lists are `propext`, `Classical.choice`, and `Quot.sound`.

The Python script checks only the shape of a start map followed by a word predicate on two codes. Non-computability is the Lean implication, not that script.

## What is proved

- If the mark type has a `Primcodable` structure and `startWord` is computable, then `P` is not `ComputablePred`.
- The campaign declaration has that implication as its type.

## What is assumed

- The kernel axioms `propext`, `Classical.choice`, and `Quot.sound`.
- `nfReach_not_computable`, cited by COMP-C7-NF-REACH-UNDECIDABLE.
- `Primcodable` and `Computable` are the Mathlib notions named in the type.

## What is open

- A construction of the `Primcodable` instance.
- A construction of `Computable startWord`.
- The two-code script is not a computability result.
