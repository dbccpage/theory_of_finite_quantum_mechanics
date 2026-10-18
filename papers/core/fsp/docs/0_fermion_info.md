# Primitive orientation, sign gap, and survivor witnesses

**Status:** SOURCE-BOUND FINITE NOTE WITH PHYSICAL ANALOGIES
**AuthorityEffect:** None
**Date:** 2026-09-01

## 1. Finite mathematical core

On `Bool`, the local reference copy defines:

- `D2 false true` as the single directed edge;
- `D2rev` as its reversal;
- `S2` as the symmetrization;
- a swap carrying `D2` to `D2rev`; and
- two swaps restoring the original relation.

The living Tower modules additionally prove that predicates invariant under the
declared swap action cannot distinguish two objects in the same orbit
(`PrimDiffAlternation.invariant_blind`) and instantiate that statement for
`D2` and `D2rev`.

| Statement | Source |
| --- | --- |
| `D2_initial_pointed` | `coda_all_universe/0_genesis/lean4/Derivation/PrimDiff.lean` |
| `oriented_rigid` | same local source |
| `swap_carries_D2_to_D2rev` | same local source |
| `swap_twice_restores_D2` | same local source |
| `bool_irrefl_nonempty_classification` | same local source |
| `sign_gap_invisible_to_invariants` | `coda_all_universe/1_the_tower/lean/PrimDiffRung3.lean` |
| `mark_choice_residual` | `coda_all_universe/1_the_tower/lean/PrimDiffRung4.lean` |
| `alternation` | `coda_all_universe/1_the_tower/lean/PrimDiffAlternation.lean` |

These are finite relational and group-action statements. Their Lean names do
not establish a particle interpretation.

## 2. Survivor-witness bookkeeping

A survivor record such as

```text
(x, y, declared_difference, qx, qy, reason)
```

is an evidence format for retaining a pair that a declared quotient, report, or
invariant failed to identify faithfully. Its meaning depends on the supplied
carrier, map, and verifier. The record is not a fermion and does not by itself
license a physical claim.

## 3. Analogy ledger

| Physics label | Finite pattern | Status |
| --- | --- | --- |
| fermionic orientation | `D2` differs from `D2rev`, while the swap relates them | analogy only |
| Pauli-like exclusion | endpoint identification conflicts with a protected irreflexive witness | analogy only |
| spinor-like two-step return | the declared swap is an involution | analogy only; not a Spin-to-SO representation |
| sign problem | signed contributions may cancel and some invariant packages are orientation-blind | analogy only; no QMC complexity result |

A two-element orbit under an involution is not a 720-degree spinor theorem. A
rigid directed graph is not a fermion. Promoting either analogy requires a
separate bridge specifying the physical carrier, representation, observables,
and empirical or formal replay condition.

## 4. Narrow conclusion

The proved finite statement is that the declared swap relates two distinct
oriented relations and every predicate invariant under that action has the same
truth value on them. Adding a mark can separate a chosen pair but introduces a
mark-choice residual. This is useful obstruction bookkeeping independent of any
particle interpretation.

## 5. Open bridge

A physical bridge would need to show, at minimum:

1. how physical states map to the finite carrier;
2. which group action is represented;
3. which observables are preserved;
4. how amplitudes or statistics are recovered; and
5. which residual remains after the map.

That bridge is not proved here.

`AuthorityEffect: None.`
