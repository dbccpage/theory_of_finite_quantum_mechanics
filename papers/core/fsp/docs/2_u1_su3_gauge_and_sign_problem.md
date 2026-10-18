# Finite symmetry data and proposed U(1)/SU(3) lifts

**Status:** DRAFT ANALOGY AND BRIDGE REGISTER
**AuthorityEffect:** None
**Date:** 2026-09-01

## 1. Result boundary

The cited local Genesis sources contain finite relations, permutations,
simplicial chains, and boundary-cancellation statements. They do not derive
continuous `U(1)`, `SU(3)`, quantum chromodynamics, confinement, asymptotic
freedom, or a solution to the fermion sign problem.

In particular:

- `S3` has six elements;
- `SU(3)` is an eight-dimensional continuous Lie group; and
- no completion or representation functor from the former to the latter is
  supplied by `PrimDiff.lean`, `BoundaryCancellation.lean`, or
  `HigherStructure.lean`.

Calling `SU(3)` a “continuous completion” of `S3` is therefore refused in
this note. Any SU(3) layer is an external, priced enrichment.

## 2. Finite source material

| Finite object | Supported statement | Source class |
| --- | --- | --- |
| `D2`, `D2rev`, `S2` | Two-point directed and symmetric relations with a swap action | named local Lean definitions/theorems |
| finite permutations | Combinatorial relabeling actions | finite group theory |
| simplicial boundary maps | Consecutive boundary maps cancel in the declared complex | named local Lean theorem / standard chain identity |
| alternating three-index tensor | Can be declared over a chosen rank-three module | external algebraic construction |
| Gell-Mann matrices | A standard basis for `su(3)` after a complex vector space and inner product are supplied | external mathematics |

The last two rows are not outputs of Primitive Difference.

## 3. Admissible bridge shape

A future bridge to a continuous gauge model must state:

1. **source carrier:** the finite relation, chain complex, or representation;
2. **target carrier:** the exact vector space, Lie algebra, or group;
3. **map:** an explicit homomorphism or functor;
4. **preserved structure:** operations, observables, and equations;
5. **added structure:** scalar field, topology, metric, differentiability, and
   completion data;
6. **residual:** information lost or newly chosen; and
7. **replay:** Lean theorem, exact computation, or cited external theorem.

Without these fields, “U(1) lift” and “SU(3) lift” are research labels only.

## 4. Sign-problem boundary

The finite cancellation identity `boundary (boundary x) = 0` and examples of
odd-pair cancellation do not imply a polynomial-time algorithm for generic
fermionic quantum Monte Carlo. General sign-problem hardness results quantify
over specified Hamiltonian families and encodings; this document supplies no
reduction that changes those classes.

Potential research routes may compare:

- exact algebraic pairing on a declared finite census;
- basis or representation changes;
- meron-style cluster decompositions;
- tensor-network contractions; and
- bounded obstruction certificates.

Each route must preserve the original partition function or explicitly report
the approximation and residual. Discarding negative terms is not cancellation.

## 5. Narrow conclusion

The present finite corpus supplies symmetry and cancellation patterns that can
motivate U(1), SU(3), and sign-problem experiments. It does not derive those
physical theories. The bridge is open and must be paid for by explicit target
structure and correspondence theorems.

`AuthorityEffect: None.`
