import QuadraticGaussReduction
/-!
Finite-field phase-vector overlap identities.

This module records the Hilbert-overlap kernel for the odd-prime-power Weyl
route without constructing a full Hilbert/GTMUR transport theorem. The vectors
are represented by their unnormalised phase functions

  `x ↦ ψ (a*x^2 + b*x)`.

The theorems below prove that their unnormalised inner product is a linear character sum on a
fixed slope, and a quadratic Gauss sum across distinct slopes. Together with
`MUB.quadraticGauss_complex_normSq`, this is the finite-field inner-product
surface needed before algebraic coefficient-field and representation transport
can be certified.
-/

namespace MUB

open scoped BigOperators

noncomputable def quadraticPhaseOverlap
    {F : Type*} [Field F] [Fintype F]
    (ψ : AddChar F ℂ) (a b c d : F) : ℂ :=
  ∑ x : F, star (ψ (a * x ^ 2 + b * x)) * ψ (c * x ^ 2 + d * x)

theorem quadraticPhaseOverlap_eq_quadraticGaussSum
    {F : Type*} [Field F] [Fintype F]
    (ψ : AddChar F ℂ) (hchar : 0 < ringChar F) (a b c d : F) :
    quadraticPhaseOverlap ψ a b c d =
      quadraticGaussSum ψ (c - a) (d - b) := by
  unfold quadraticPhaseOverlap quadraticGaussSum
  apply Finset.sum_congr rfl
  intro x _hx
  have hphase :
      (c * x ^ 2 + d * x) - (a * x ^ 2 + b * x) =
        (c - a) * x ^ 2 + (d - b) * x := by
    ring
  calc
    star (ψ (a * x ^ 2 + b * x)) * ψ (c * x ^ 2 + d * x)
        = ψ (-(a * x ^ 2 + b * x)) * ψ (c * x ^ 2 + d * x) := by
            have hstar :
                star (ψ (a * x ^ 2 + b * x)) =
                  ψ (-(a * x ^ 2 + b * x)) := by
              change (starRingEnd ℂ) (ψ (a * x ^ 2 + b * x)) =
                ψ (-(a * x ^ 2 + b * x))
              rw [AddChar.starComp_apply hchar (φ := ψ)]
              rfl
            rw [hstar]
    _ = ψ ((c * x ^ 2 + d * x) - (a * x ^ 2 + b * x)) := by
            have harg :
                -(a * x ^ 2 + b * x) + (c * x ^ 2 + d * x) =
                  (c * x ^ 2 + d * x) - (a * x ^ 2 + b * x) := by
              ring
            rw [← AddChar.map_add_eq_mul, harg]
    _ = ψ ((c - a) * x ^ 2 + (d - b) * x) := by
            rw [hphase]

theorem quadraticPhaseOverlap_self
    {F : Type*} [Field F] [Fintype F]
    (ψ : AddChar F ℂ) (hchar : 0 < ringChar F) (a b : F) :
    quadraticPhaseOverlap ψ a b a b = Fintype.card F := by
  rw [quadraticPhaseOverlap_eq_quadraticGaussSum ψ hchar]
  unfold quadraticGaussSum
  simp

theorem quadraticPhaseOverlap_same_slope_orthogonal
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive) (hchar : 0 < ringChar F)
    (a b d : F) (hbd : b ≠ d) :
    quadraticPhaseOverlap ψ a b a d = 0 := by
  have hdb : d - b ≠ 0 := sub_ne_zero.mpr hbd.symm
  rw [quadraticPhaseOverlap_eq_quadraticGaussSum ψ hchar]
  unfold quadraticGaussSum
  calc
    (∑ x : F, ψ ((a - a) * x ^ 2 + (d - b) * x))
        = ∑ x : F, ψ (x * (d - b)) := by
            apply Finset.sum_congr rfl
            intro x _hx
            ring_nf
    _ = 0 := by
            rw [finite_field_primitive_additive_character_linear_orthogonality
              ψ hψ (d - b)]
            simp [hdb]

theorem quadraticPhaseOverlap_cross_slope_normSq
    {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (ψ : AddChar F ℂ) (hψ : ψ.IsPrimitive) (hchar : 0 < ringChar F)
    (h2 : (2 : F) ≠ 0) {a c b d : F} (hac : a ≠ c) :
    quadraticPhaseOverlap ψ a b c d *
        star (quadraticPhaseOverlap ψ a b c d) =
      Fintype.card F := by
  have hca : c - a ≠ 0 := sub_ne_zero.mpr hac.symm
  rw [quadraticPhaseOverlap_eq_quadraticGaussSum ψ hchar]
  exact quadraticGauss_complex_normSq ψ hψ hchar hca h2

end MUB

#print axioms MUB.quadraticPhaseOverlap_eq_quadraticGaussSum
#print axioms MUB.quadraticPhaseOverlap_self
#print axioms MUB.quadraticPhaseOverlap_same_slope_orthogonal
#print axioms MUB.quadraticPhaseOverlap_cross_slope_normSq
