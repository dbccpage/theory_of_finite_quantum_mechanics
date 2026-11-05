import Mathlib.Algebra.Group.Hom.Basic
import Mathlib.Data.Real.Basic

/-!
Mixed closure-bound kernel (PaperGS002 Theorem 6.1 / ENC-0238).

The concrete paper uses weighted mixed norms on finite cochain spaces. This file
records the formal core that is independent of that concrete norm packaging:

* `d₁ ∘ d₀ = 0` makes the closure score invariant under exact repairs.
* If every repair representative bounds the closure score, and the scaled
  repair costs are cofinal above the quotient value, then the closure score is
  bounded by the scaled quotient value.
-/

theorem closure_repair_invariant_add
    {C0 C1 C2 : Type*}
    [AddMonoid C0] [AddCommMonoid C1] [AddCommMonoid C2]
    (d0 : C0 →+ C1) (d1 : C1 →+ C2)
    (hcomp : ∀ a : C0, d1 (d0 a) = 0)
    (h : C1) (a : C0) :
    d1 (h + d0 a) = d1 h := by
  rw [d1.map_add, hcomp a, add_zero]

theorem closure_repair_invariant_sub
    {C0 C1 C2 : Type*}
    [AddGroup C0] [AddCommGroup C1] [AddCommGroup C2]
    (d0 : C0 →+ C1) (d1 : C1 →+ C2)
    (hcomp : ∀ a : C0, d1 (d0 a) = 0)
    (h : C1) (a : C0) :
    d1 (h - d0 a) = d1 h := by
  rw [sub_eq_add_neg, d1.map_add, d1.map_neg, hcomp a, neg_zero, add_zero]

theorem closure_bound_from_minimizer
    {A : Type*}
    (K gamma phi : ℝ) (cost : A → ℝ)
    (hmin : ∃ a : A, cost a = phi)
    (hbound : ∀ a : A, gamma ≤ K * cost a) :
    gamma ≤ K * phi := by
  rcases hmin with ⟨a, ha⟩
  simpa [ha] using hbound a

theorem closure_bound_from_cofinal_scaled_repairs
    {A : Type*}
    (K gamma phi : ℝ) (cost : A → ℝ)
    (hcofinal :
      ∀ b : ℝ, K * phi < b → ∃ a : A, K * cost a ≤ b)
    (hbound : ∀ a : A, gamma ≤ K * cost a) :
    gamma ≤ K * phi := by
  refine le_of_forall_gt_imp_ge_of_dense ?_
  intro b hb
  rcases hcofinal b hb with ⟨a, ha⟩
  exact le_trans (hbound a) ha

#print axioms closure_repair_invariant_add
#print axioms closure_repair_invariant_sub
#print axioms closure_bound_from_minimizer
#print axioms closure_bound_from_cofinal_scaled_repairs
