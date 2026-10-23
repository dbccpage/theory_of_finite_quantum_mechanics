import Mathlib.Algebra.Group.Hom.Basic
import Mathlib.Data.Real.Basic

/-!
Weak-duality / certificate kernel for PaperGS002 Theorem 4.2 (ENC-0237).

The paper's full theorem is a finite-dimensional Fenchel--Rockafellar strong
duality statement. This file formalizes the elementary certificate side:

* a divergence-free additive witness is invariant under exact repairs;
* if a witness value is bounded by the cost of every repair representative,
  then it is bounded by the primal quotient value.
-/

theorem dual_witness_repair_invariant_sub
    {C0 C1 : Type*}
    [AddGroup C0] [AddCommGroup C1]
    (d0 : C0 →+ C1) (witness : C1 →+ ℝ)
    (hdiv : ∀ a : C0, witness (d0 a) = 0)
    (ω : C1) (a : C0) :
    witness (ω - d0 a) = witness ω := by
  rw [sub_eq_add_neg, witness.map_add, witness.map_neg, hdiv a, neg_zero, add_zero]

theorem dual_witness_bound_from_minimizer
    {A : Type*}
    (value primal : ℝ) (cost : A → ℝ)
    (hmin : ∃ a : A, cost a = primal)
    (hbound : ∀ a : A, value ≤ cost a) :
    value ≤ primal := by
  rcases hmin with ⟨a, ha⟩
  simpa [ha] using hbound a

theorem dual_witness_bound_from_cofinal_repairs
    {A : Type*}
    (value primal : ℝ) (cost : A → ℝ)
    (hcofinal : ∀ b : ℝ, primal < b → ∃ a : A, cost a ≤ b)
    (hbound : ∀ a : A, value ≤ cost a) :
    value ≤ primal := by
  refine le_of_forall_gt_imp_ge_of_dense ?_
  intro b hb
  rcases hcofinal b hb with ⟨a, ha⟩
  exact le_trans (hbound a) ha

#print axioms dual_witness_repair_invariant_sub
#print axioms dual_witness_bound_from_minimizer
#print axioms dual_witness_bound_from_cofinal_repairs
