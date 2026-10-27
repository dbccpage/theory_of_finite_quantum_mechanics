import «semiring_transport_kernel»

/-!
LT-O — the ungraded path-sum over-counts (gradedness is load-bearing).

Paper: `11_finite_weighted_transport_calculus_for_qm.md` (T1 caution; §F
counterexample).

For the linear graph `a → b → c` there is exactly ONE path, through the single
middle node `b`, so the GRADED (sliced) path-sum is the single product
`w_ab · w_bc`. An UNGRADED enumeration — summing over ALL objects `{a, b, c}` as if
any could be the middle — yields `3 · (w_ab · w_bc)`, a 3:1 over-count. With unit
weights the graded sum is `1` and the ungraded sum is `3`; they are unequal, so the
grading (the slice) is **necessary, not cosmetic**.

The over-count is invisible to the degree-1 cochain norms: the linear graph is
coboundary-free, so `Φ1 = Γ2 = 0` and `H¹ = 0` — the defect is a *gradedness*
phenomenon, distinct from obstruction mass. Concrete, decidable witness; Mathlib-free;
no authority minted.
-/

namespace QM

open FiniteCosmology.Primitives.SemiringTransportKernel

/-- The graded path-sum over the single middle slice `{b}` of `a → b → c`, unit
weights: one real path. -/
def gradedSum : Nat := lsum (R := Nat) [1 * 1]

/-- The ungraded enumeration over all three objects `{a, b, c}`, unit weights. -/
def ungradedSum : Nat := lsum (R := Nat) [1 * 1, 1 * 1, 1 * 1]

/-- The graded path-sum counts the one real path. -/
theorem graded_eq_one : gradedSum = 1 := by decide

/-- The ungraded enumeration triple-counts. -/
theorem ungraded_eq_three : ungradedSum = 3 := by decide

/-- **Gradedness is load-bearing:** the ungraded enumeration over-counts the graded
path-sum 3:1 — they are not equal, so the slice cannot be dropped. -/
theorem ungraded_overcounts : ungradedSum ≠ gradedSum := by decide

end QM

#print axioms QM.graded_eq_one
#print axioms QM.ungraded_eq_three
#print axioms QM.ungraded_overcounts
