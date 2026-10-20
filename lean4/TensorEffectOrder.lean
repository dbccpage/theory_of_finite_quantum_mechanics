import TensorComposition
import Mathlib.Geometry.Convex.Cone.Pointed
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Order

/-! Trace duality and binary effects in the constructed Hermitian coordinates.
Bounds use unnormalized states: `0 ≤ e(x) ≤ u(x)`. This formulation retains
the cone's scale and does not postulate an operational effect or test set. -/
open Matrix Module
open scoped BigOperators ComplexOrder MatrixOrder Matrix.Norms.L2Operator
noncomputable section
namespace TensorEffectOrder
open TensorTomography TensorComposition TensorConeReconstruction
variable {d : Type*} [Fintype d] [DecidableEq d]

def Positive (E : Herm d) : Prop := E.val.PosSemidef
def Binary (E : Herm d) : Prop := Positive E ∧ Positive (1 - E)

theorem pairing_nonneg {E A : Herm d} (hE : Positive E) (hA : Positive A) :
    0 ≤ pairing E A := by
  apply positive_mem_of_rankOne {B | 0 ≤ (E.val * B).trace.re}
    (by simp) (by
      intro B hB C hC
      change 0 ≤ (E.val * B).trace.re at hB
      change 0 ≤ (E.val * C).trace.re at hC
      change 0 ≤ (E.val * (B + C)).trace.re
      simpa only [Matrix.mul_add, Matrix.trace_add, Complex.add_re] using add_nonneg hB hC)
    (fun v => ?_) hA
  change 0 ≤ (E.val * rankOne v).trace.re
  rw [Matrix.trace_mul_comm, trace_rankOne]
  exact hE.re_dotProduct_nonneg v

/-- Self-duality is derived from vector tests and finite Gram decomposition. -/
theorem positive_iff_pairing (E : Herm d) :
    Positive E ↔ ∀ A : Herm d, Positive A → 0 ≤ pairing E A := by
  constructor
  · exact fun h A hA => pairing_nonneg h hA
  · intro h
    exact Matrix.PosSemidef.of_dotProduct_mulVec_nonneg E.property (fun v =>
      quadratic_nonneg_of_pairing E v (by
        have hs : pairing (hermRankOne v) E = pairing E (hermRankOne v) :=
          pairing_symm.eq _ _
        rw [hs]
        exact h (hermRankOne v) (Matrix.posSemidef_vecMulVec_self_star v)))

@[simp] theorem pairing_one (A : Herm d) : pairing (1 : Herm d) A = A.val.trace.re := by
  simp [pairing_apply]

/-- The order interval follows from positivity of both outcomes of a binary test. -/
theorem binary_iff_bounds (E : Herm d) :
    Binary E ↔ ∀ A : Herm d, Positive A →
      0 ≤ pairing E A ∧ pairing E A ≤ A.val.trace.re := by
  constructor
  · rintro ⟨hE, hC⟩ A hA
    refine ⟨pairing_nonneg hE hA, ?_⟩
    have h := pairing_nonneg hC hA
    change 0 ≤ pairing (1 - E) A at h
    rw [map_sub, LinearMap.sub_apply, pairing_one] at h
    exact sub_nonneg.mp h
  · intro h
    constructor
    · exact (positive_iff_pairing E).mpr (fun A hA => (h A hA).1)
    · apply (positive_iff_pairing (1 - E)).mpr
      intro A hA
      rw [map_sub, LinearMap.sub_apply, pairing_one]
      exact sub_nonneg.mpr (h A hA).2

theorem binary_iff_interval (E : Herm d) :
    Binary E ↔ 0 ≤ E.val ∧ E.val ≤ 1 := by
  change E.val.PosSemidef ∧ (1 - E.val).PosSemidef ↔ _
  rw [← Matrix.nonneg_iff_posSemidef, ← Matrix.le_iff]

/-- The homogeneous bounds are equivalent to probabilities in [0,1] on all
trace-one states, including the degenerate zero-dimensional case. -/
theorem binary_iff_normalized (E : Herm d) :
    Binary E ↔ ∀ A : Herm d, Positive A → A.val.trace.re = 1 →
      0 ≤ pairing E A ∧ pairing E A ≤ 1 := by
  rw [binary_iff_bounds]
  constructor
  · intro h A hA htrace
    simpa only [htrace] using h A hA
  · intro h A hA
    have ht : 0 ≤ A.val.trace.re := (Complex.nonneg_iff.mp hA.trace_nonneg).1
    by_cases hz : A.val.trace.re = 0
    · have hi : A.val.trace.im = 0 := by
        simpa using trace_pair_im (1 : Herm d) A
      have hzero : A = 0 := Subtype.ext (hA.trace_eq_zero_iff.mp (Complex.ext hz hi))
      subst A
      simp
    · have ht' : 0 < A.val.trace.re := lt_of_le_of_ne ht (Ne.symm hz)
      let B : Herm d := A.val.trace.re⁻¹ • A
      have hB : Positive B := hA.smul (inv_nonneg.mpr ht)
      have htr : B.val.trace.re = 1 := by
        change ((A.val.trace.re⁻¹ : ℝ) • A.val).trace.re = 1
        simp [Matrix.trace_smul, hz]
      have hb := h B hB htr
      have he : pairing E B = A.val.trace.re⁻¹ * pairing E A := by
        simp [B]
      rw [he] at hb
      have hlow := mul_nonneg ht hb.1
      have hupp := mul_le_mul_of_nonneg_left hb.2 ht
      simpa only [← mul_assoc, mul_inv_cancel₀ hz, one_mul, mul_one] using
        And.intro hlow hupp

/-- Every positive ray contains a binary effect; no availability is asserted. -/
theorem positive_ray_binary (A : Herm d) (hA : Positive A) :
    ∃ (r : ℝ) (E : Herm d), 0 ≤ r ∧ Binary E ∧ A = r • E := by
  let r : ℝ := ‖A.val‖ + 1
  have hr : 0 < r := by dsimp [r]; positivity
  let E : Herm d := r⁻¹ • A
  have hE : Positive E := hA.smul (le_of_lt (inv_pos.mpr hr))
  have hnorm : ‖E.val‖ ≤ 1 := by
    change ‖r⁻¹ • A.val‖ ≤ 1
    rw [norm_smul, Real.norm_of_nonneg (le_of_lt (inv_pos.mpr hr))]
    rw [inv_mul_eq_div, div_le_one hr]
    dsimp [r]
    linarith [norm_nonneg A.val]
  refine ⟨r, E, hr.le, (binary_iff_interval E).mpr ⟨hE.nonneg, ?_⟩, ?_⟩
  · exact (CStarAlgebra.norm_le_one_iff_of_nonneg E.val hE.nonneg).mp hnorm
  · dsimp [E]
    rw [smul_smul, mul_inv_cancel₀ hr.ne', one_smul]

#print axioms positive_iff_pairing
#print axioms binary_iff_bounds
#print axioms binary_iff_normalized
#print axioms positive_ray_binary
end TensorEffectOrder
