import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Analysis.Normed.Group.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
# mixed_vector_duality

Formalization of Weak Vector Fenchel Duality for ℓ¹(E; ℓ²) Mixed Observer Geometries.

Grounded in Paper GS-003 ("Vector and Quantum Observer Geometries: Gauge Relativity and Trace Metric Bounds"),
Section "Generalization: Mixed Vector Obstruction".

Given:
  - A finite vertex set V and finite edge set E
  - Stalk vector space W equipped with a real inner product space structure
  - A linear coboundary operator d_0 : (V → W) → (E → W)
  - An observed vector defect cochain ω : E → W
  - The mixed vector gauge J_21(r) = ∑_e ‖r_e‖

A dual circulation witness φ : E → W satisfies:
  1. Divergence-free (circulation) constraint: ∀ α : V → W, ∑_e ⟪φ_e, (d_0 α)_e⟫ = 0
  2. Pointwise Euclidean unit-bound: ∀ e : E, ‖φ_e‖ ≤ 1

Weak Vector Duality:
  For any candidate repair α : V → W and any dual witness φ:
    ∑_e ⟪φ_e, ω_e⟫ ≤ ∑_e ‖ω_e - (d_0 α)_e‖ = J_21(ω - d_0 α)

Consequently, the dual objective bounds the quotient obstruction from below:
    ∑_e ⟪φ_e, ω_e⟫ ≤ Φ_21([ω]).

AuthorityEffect: None.
-/

namespace MixedVectorDuality

open scoped BigOperators

variable {V E W : Type*} [Fintype E] [NormedAddCommGroup W] [InnerProductSpace ℝ W]

/-- The mixed vector gauge: sum of stalk Euclidean norms across all edges. -/
def J_21 (r : E → W) : ℝ :=
  ∑ e : E, ‖r e‖

/-- Total dual pairing between a dual vector cochain φ and a primal cochain ω. -/
def dualPairing (φ ω : E → W) : ℝ :=
  ∑ e : E, @inner ℝ W _ (φ e) (ω e)

/-- Divergence-free circulation constraint: φ has zero pairing with all exact coboundaries d_0 α. -/
def IsDivergenceFree (d0 : (V → W) → (E → W)) (φ : E → W) : Prop :=
  ∀ α : V → W, dualPairing φ (d0 α) = 0

/-- Pointwise Euclidean unit-norm bound on every edge. -/
def IsUnitBounded (φ : E → W) : Prop :=
  ∀ e : E, ‖φ e‖ ≤ 1

/-- A valid dual circulation witness is divergence-free and unit-bounded. -/
structure DualWitness (d0 : (V → W) → (E → W)) (φ : E → W) : Prop where
  divFree : IsDivergenceFree d0 φ
  unitBound : IsUnitBounded φ

/-- Pointwise Cauchy-Schwarz bound on a single edge stalk:
    if ‖φ_e‖ ≤ 1, then ⟪φ_e, r_e⟫ ≤ ‖r_e‖. -/
theorem stalk_cauchy_schwarz_unit (u r : W) (hu : ‖u‖ ≤ 1) :
    @inner ℝ W _ u r ≤ ‖r‖ := by
  have h_cs := real_inner_le_norm u r
  have hr_nonneg : 0 ≤ ‖r‖ := norm_nonneg r
  have h_prod : ‖u‖ * ‖r‖ ≤ 1 * ‖r‖ := mul_le_mul_of_nonneg_right hu hr_nonneg
  rw [one_mul] at h_prod
  exact h_cs.trans h_prod

/-- Global dual pairing is bounded by the mixed gauge for any unit-bounded cochain. -/
theorem dualPairing_le_J_21 (φ r : E → W) (hφ : IsUnitBounded φ) :
    dualPairing φ r ≤ J_21 r := by
  unfold dualPairing J_21
  apply Finset.sum_le_sum
  intro e _
  exact stalk_cauchy_schwarz_unit (φ e) (r e) (hφ e)

/-- Linearity of dual pairing under gauge subtraction. -/
theorem dualPairing_sub (φ : E → W) (ω : E → W) (η : E → W) :
    dualPairing φ (ω - η) = dualPairing φ ω - dualPairing φ η := by
  unfold dualPairing
  simp_rw [Pi.sub_apply, inner_sub_right, Finset.sum_sub_distrib]

/-- Divergence-free projection invariance: pairing with (ω - d_0 α) equals pairing with ω. -/
theorem dualPairing_repair_invariance (d0 : (V → W) → (E → W)) (φ : E → W)
    (hdiv : IsDivergenceFree d0 φ) (ω : E → W) (α : V → W) :
    dualPairing φ (ω - d0 α) = dualPairing φ ω := by
  have h_sub := dualPairing_sub φ ω (d0 α)
  have h_div := hdiv α
  linarith

/-- Weak Vector Fenchel Duality (Pointwise Formulation):
    For any valid dual witness φ and any candidate repair α,
    the dual pairing with ω is a lower bound on the residual mixed norm. -/
theorem weak_vector_duality_pointwise (d0 : (V → W) → (E → W)) (φ : E → W) (ω : E → W)
    (hφ : DualWitness d0 φ) (α : V → W) :
    dualPairing φ ω ≤ J_21 (ω - d0 α) := by
  have h_inv := dualPairing_repair_invariance d0 φ hφ.divFree ω α
  rw [← h_inv]
  exact dualPairing_le_J_21 φ (ω - d0 α) hφ.unitBound

/-- Structure representing an optimal quotient obstruction value Φ_21([ω]). -/
structure OptimalVectorQuotient (d0 : (V → W) → (E → W)) (ω : E → W) where
  val : ℝ
  attained : ∃ α_opt : V → W, val = J_21 (ω - d0 α_opt)
  is_min : ∀ α : V → W, val ≤ J_21 (ω - d0 α)

/-- Weak Vector Fenchel Duality (Quotient Formulation):
    For any valid dual witness φ, the dual pairing with ω lower-bounds the optimal quotient obstruction. -/
theorem weak_vector_duality_quotient (d0 : (V → W) → (E → W)) (φ : E → W) (ω : E → W)
    (hφ : DualWitness d0 φ) (opt : OptimalVectorQuotient d0 ω) :
    dualPairing φ ω ≤ opt.val := by
  rcases opt.attained with ⟨α_opt, h_opt⟩
  rw [h_opt]
  exact weak_vector_duality_pointwise d0 φ ω hφ α_opt

/-- Duality Gap Certificate:
    If a repair α* and a dual witness φ* achieve equality, both are optimal,
    and the duality gap is zero. -/
theorem duality_gap_zero_certificate (d0 : (V → W) → (E → W)) (φ_opt : E → W) (ω : E → W)
    (α_opt : V → W) (hφ : DualWitness d0 φ_opt)
    (heq : dualPairing φ_opt ω = J_21 (ω - d0 α_opt)) :
    ∀ α : V → W, J_21 (ω - d0 α_opt) ≤ J_21 (ω - d0 α) := by
  intro α
  rw [← heq]
  exact weak_vector_duality_pointwise d0 φ_opt ω hφ α

end MixedVectorDuality

#print axioms MixedVectorDuality.stalk_cauchy_schwarz_unit
#print axioms MixedVectorDuality.dualPairing_le_J_21
#print axioms MixedVectorDuality.dualPairing_sub
#print axioms MixedVectorDuality.dualPairing_repair_invariance
#print axioms MixedVectorDuality.weak_vector_duality_pointwise
#print axioms MixedVectorDuality.weak_vector_duality_quotient
#print axioms MixedVectorDuality.duality_gap_zero_certificate
