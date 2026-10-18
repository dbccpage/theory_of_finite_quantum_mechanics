import «semiring_transport_kernel»

/-!
LT-N — finite graded path-sum: the sliced composition step.

Paper: `11_finite_weighted_transport_calculus_for_qm.md` (T1/T2);
`12_gtta_feynman_finite_shadow_histories.md` (Part 1).

The algebraic heart of "enumerated graded path-sum = transfer-matrix product" is
finite-sum right-distributivity (`SemiringTransportKernel.lsum_mul_right`, the
already-checked core). This module packages it as the **sliced composition step**
and exercises it on a concrete two-object middle slice over ℕ.

The composition is canonical **only after slicing** (grading): the companion
`QM.UngradedOvercount` (LT-O) exhibits the 3:1 over-count incurred when the slice
is dropped. The continuum generator `exp(tH)` stays `OracleNeeded`. Mathlib-free;
builds on `OmegaCore` only. No Born rule / inner product; no authority minted.
-/

namespace QM

open OmegaCosmology.Primitives.SemiringTransportKernel

/-- **Sliced composition step (T1/T2).** Extending every enumerated partial path by
a common final edge of weight `y` distributes into the path-sum:
`(Σ paths) · y = Σ (path · y)`. Applied slice-by-slice, this is exactly why the
enumerated graded path-sum equals the transfer-matrix product. -/
theorem pathsum_extend_right {R : Type} [FWSemiring R] (y : R) (paths : List R) :
    FWSemiring.mul (lsum paths) y = lsum (paths.map (fun w => FWSemiring.mul w y)) :=
  lsum_mul_right y paths

/-- Concrete graded transfer replay over ℕ. A two-object middle slice `{b₀, b₁}` of
`a → b_i → c` with first edges `(a→b₀, a→b₁) = (2, 3)` and second edges
`(b₀→c, b₁→c) = (5, 7)`. The graded path-sum `Σ_i (a→b_i)·(b_i→c)` is the `(a,c)`
transfer entry `2·5 + 3·7 = 31`. -/
theorem transfer_replay_2slice :
    lsum (R := Nat) [2 * 5, 3 * 7] = 31 := by decide

end QM

#print axioms QM.pathsum_extend_right
#print axioms QM.transfer_replay_2slice
