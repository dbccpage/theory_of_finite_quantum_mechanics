import HilbertPhaseTransport
/-!
Complex Hilbert normalization for odd-prime-power phase vectors.

`MUB.HilbertPhaseTransport` proves the unnormalised trace-character overlap
kernel. This file proves the scalar normalization algebra over `ℂ`: multiplying
the overlap by `1 / card F` gives orthonormal same-slope vectors and squared
cross-slope overlap `1 / card F`.

This is intentionally not a coefficient-field theorem. It does not construct a
uniform algebraic field `Q(ζ_p, sqrt(p^k))`; it only proves the analytic
normalization identities needed before such a field transport can be accepted.
-/

namespace MUB

open scoped BigOperators

noncomputable def sqrtCardNormalizer
    (F : Type*) [Fintype F] : ℂ :=
  ((Real.sqrt (Fintype.card F : ℝ) : ℂ)⁻¹)

theorem real_sqrt_nat_inv_mul_inv (n : ℕ) :
    (Real.sqrt (n : ℝ))⁻¹ * (Real.sqrt (n : ℝ))⁻¹ = ((n : ℝ)⁻¹) := by
  have hnonneg : 0 ≤ (n : ℝ) := by exact_mod_cast Nat.zero_le n
  have hsquare : Real.sqrt (n : ℝ) * Real.sqrt (n : ℝ) = (n : ℝ) := by
    rw [← sq]
    exact Real.sq_sqrt hnonneg
  rw [← mul_inv_rev]
  rw [hsquare]

theorem sqrtCardNormalizer_star_mul
    (F : Type*) [Fintype F] :
    star (sqrtCardNormalizer F) * sqrtCardNormalizer F =
      (Fintype.card F : ℂ)⁻¹ := by
  unfold sqrtCardNormalizer
  have hreal :=
    congrArg (fun x : ℝ => (x : ℂ))
      (real_sqrt_nat_inv_mul_inv (Fintype.card F))
  rw [Complex.ofReal_mul, Complex.ofReal_inv, Complex.ofReal_inv,
    Complex.ofReal_natCast] at hreal
  change (starRingEnd ℂ) (((Real.sqrt (Fintype.card F : ℝ) : ℂ)⁻¹)) *
      (((Real.sqrt (Fintype.card F : ℝ) : ℂ)⁻¹)) =
    (Fintype.card F : ℂ)⁻¹
  rw [map_inv₀, Complex.conj_ofReal]
  exact hreal

noncomputable def normalizedQuadraticPhaseOverlap
    {F : Type*} [Field F] [Fintype F]
    (ψ : AddChar F ℂ) (a b c d : F) : ℂ :=
  (Fintype.card F : ℂ)⁻¹ * quadraticPhaseOverlap ψ a b c d

theorem normalizedQuadraticPhaseOverlap_from_sqrt_normalizer
    {F : Type*} [Field F] [Fintype F]
    (ψ : AddChar F ℂ) (a b c d : F) :
    normalizedQuadraticPhaseOverlap ψ a b c d =
      (star (sqrtCardNormalizer F) * sqrtCardNormalizer F) *
        quadraticPhaseOverlap ψ a b c d := by
  unfold normalizedQuadraticPhaseOverlap
  rw [sqrtCardNormalizer_star_mul]

theorem normalizedQuadraticPhaseOverlap_self
    {F : Type*} [Field F] [Fintype F]
    (ψ : AddChar F ℂ) (hchar : 0 < ringChar F) (a b : F) :
    normalizedQuadraticPhaseOverlap ψ a b a b = 1 := by
  unfold normalizedQuadraticPhaseOverlap
  rw [quadraticPhaseOverlap_self ψ hchar]
  have hcard_pos : 0 < Fintype.card F := Fintype.card_pos_iff.mpr ⟨(0 : F)⟩
  have hcard_ne : (Fintype.card F : ℂ) ≠ 0 := by
    exact_mod_cast (ne_of_gt hcard_pos)
  exact inv_mul_cancel₀ hcard_ne

theorem normalizedQuadraticPhaseOverlap_same_slope_orthogonal
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive) (hchar : 0 < ringChar F)
    (a b d : F) (hbd : b ≠ d) :
    normalizedQuadraticPhaseOverlap ψ a b a d = 0 := by
  unfold normalizedQuadraticPhaseOverlap
  rw [quadraticPhaseOverlap_same_slope_orthogonal ψ hψ hchar a b d hbd]
  simp

theorem normalizedQuadraticPhaseOverlap_cross_slope_normSq
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive) (hchar : 0 < ringChar F)
    (h2 : (2 : F) ≠ 0) {a c b d : F} (hac : a ≠ c) :
    normalizedQuadraticPhaseOverlap ψ a b c d *
        star (normalizedQuadraticPhaseOverlap ψ a b c d) =
      (Fintype.card F : ℂ)⁻¹ := by
  unfold normalizedQuadraticPhaseOverlap
  rw [star_mul]
  have hO :=
    quadraticPhaseOverlap_cross_slope_normSq ψ hψ hchar h2
      (a := a) (c := c) (b := b) (d := d) hac
  have hcard_pos : 0 < Fintype.card F := Fintype.card_pos_iff.mpr ⟨(0 : F)⟩
  have hcard_ne : (Fintype.card F : ℂ) ≠ 0 := by
    exact_mod_cast (ne_of_gt hcard_pos)
  have hstar_inv : star ((Fintype.card F : ℂ)⁻¹) =
      (Fintype.card F : ℂ)⁻¹ := by
    change (starRingEnd ℂ) ((Fintype.card F : ℂ)⁻¹) =
      (Fintype.card F : ℂ)⁻¹
    rw [map_inv₀]
    norm_num [Complex.conj_ofReal]
  rw [hstar_inv]
  calc
    (Fintype.card F : ℂ)⁻¹ * quadraticPhaseOverlap ψ a b c d *
        (star (quadraticPhaseOverlap ψ a b c d) *
          (Fintype.card F : ℂ)⁻¹)
        = (Fintype.card F : ℂ)⁻¹ * (Fintype.card F : ℂ)⁻¹ *
            (quadraticPhaseOverlap ψ a b c d *
              star (quadraticPhaseOverlap ψ a b c d)) := by
          ring
    _ = (Fintype.card F : ℂ)⁻¹ * (Fintype.card F : ℂ)⁻¹ *
          (Fintype.card F : ℂ) := by
          rw [hO]
    _ = (Fintype.card F : ℂ)⁻¹ := by
          field_simp [hcard_ne]

end MUB

#print axioms MUB.sqrtCardNormalizer_star_mul
#print axioms MUB.normalizedQuadraticPhaseOverlap_from_sqrt_normalizer
#print axioms MUB.normalizedQuadraticPhaseOverlap_self
#print axioms MUB.normalizedQuadraticPhaseOverlap_same_slope_orthogonal
#print axioms MUB.normalizedQuadraticPhaseOverlap_cross_slope_normSq
