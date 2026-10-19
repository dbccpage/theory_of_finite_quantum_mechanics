import BornRedundancy

/- The quotient here is on weight vectors, not amplitude rays.
   Origin: FQ-BORN-NORMALIZATION-REDUNDANCY. AuthorityEffect: None. -/
namespace QuantumMechanics.PromptBornRay
open BornRedundancy

theorem normalization_idempotent (w : List Rat) (mass_nonzero : listSum w ≠ 0) :
    normalize (normalize w) = normalize w := normalize_idempotent w mass_nonzero

theorem unit_mass_fixedpoint (w : List Rat) (hw : listSum w = 1) : normalize w = w := by
  unfold normalize
  rw [hw, one_inv, smul_one]

theorem positive_weight_ray_classification (u v : List Rat)
    (hu : 0 < listSum u) (hv : 0 < listSum v) :
    normalize u = normalize v ↔ ∃ c : Rat, 0 < c ∧ v = smul c u :=
  ray_quotient_classification u v hu hv

theorem normalization_constant_on_positive_weight_ray (w : List Rat) (c : Rat)
    (hc : 0 < c) (hw : 0 < listSum w) :
    normalize (smul c w) = normalize w :=
  normalize_smul c w (ne_zero_of_pos hc) (ne_zero_of_pos hw)

def weightsOfRealPair (x y : Rat) : List Rat := [x*x, y*y]

theorem equal_born_weights_do_not_classify_amplitude_rays :
    weightsOfRealPair 1 1 = weightsOfRealPair 1 (-1) ∧
    ¬ ∃ c : Rat, c * 1 = 1 ∧ c * 1 = -1 := by
  constructor
  · decide
  · rintro ⟨c,h0,h1⟩
    simp only [Rat.mul_one] at h0 h1
    have impossible : (1 : Rat) = -1 := h0.symm.trans h1
    exact (by decide : (1 : Rat) ≠ -1) impossible

end QuantumMechanics.PromptBornRay
#print axioms QuantumMechanics.PromptBornRay.normalization_idempotent
#print axioms QuantumMechanics.PromptBornRay.unit_mass_fixedpoint
#print axioms QuantumMechanics.PromptBornRay.positive_weight_ray_classification
#print axioms QuantumMechanics.PromptBornRay.normalization_constant_on_positive_weight_ray
#print axioms QuantumMechanics.PromptBornRay.equal_born_weights_do_not_classify_amplitude_rays
