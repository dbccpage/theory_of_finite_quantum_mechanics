import CommutativeFlatMoments
import ConcreteMubPolynomials

/-!
# Positive flat coordinate moments and the fourth-basis real variety

AuthorityEffect: None.

All 180 scalar residuals are in the real quadratic span: 108 MU conditions
and 72 candidate orthonormality conditions. A normalized positive degree-two
moment matrix with actual rank equality and the finite relation equations
extracts a common real zero of these residuals, hence an actual complex unitary
fourth basis for the fixed triple. No preconstructed coordinate point, Hilbert
projectors, or extraction map is an input.

The emptiness consequence excludes positive semidefiniteness only for moments
satisfying normalization, flatness and the finite relation equations. It does
not establish variety emptiness or exclude arbitrary nonflat truncations.
-/

namespace MUB.ConcreteMubPolynomialSystem
open MvPolynomial CommutativeFlatMoments

theorem overlapRe_mem_linearSpan (T : Triple) (a : Fin 3) (i j : Fin 6) :
    overlapRe T a i j ∈ linearSpan (σ := Coord) := by
  apply Submodule.sum_mem
  intro k hk
  apply Submodule.add_mem
  · simpa only [← MvPolynomial.smul_eq_C_mul] using
      (linearSpan (σ := Coord)).smul_mem (T a k i).re (X_mem_linearSpan (k,j,false))
  · simpa only [← MvPolynomial.smul_eq_C_mul] using
      (linearSpan (σ := Coord)).smul_mem (T a k i).im (X_mem_linearSpan (k,j,true))

theorem overlapIm_mem_linearSpan (T : Triple) (a : Fin 3) (i j : Fin 6) :
    overlapIm T a i j ∈ linearSpan (σ := Coord) := by
  apply Submodule.sum_mem
  intro k hk
  apply Submodule.sub_mem
  · simpa only [← MvPolynomial.smul_eq_C_mul] using
      (linearSpan (σ := Coord)).smul_mem (T a k i).re (X_mem_linearSpan (k,j,true))
  · simpa only [← MvPolynomial.smul_eq_C_mul] using
      (linearSpan (σ := Coord)).smul_mem (T a k i).im (X_mem_linearSpan (k,j,false))

theorem muPolynomial_mem_quadraticSpan (T : Triple) (a : Fin 3) (i j : Fin 6) :
    muPolynomial T a i j ∈ quadraticSpan (σ := Coord) := by
  unfold muPolynomial
  apply Submodule.sub_mem
  · apply Submodule.add_mem
    · simpa only [pow_two] using linear_mul_mem_quadraticSpan
        (overlapRe_mem_linearSpan T a i j) (overlapRe_mem_linearSpan T a i j)
    · simpa only [pow_two] using linear_mul_mem_quadraticSpan
        (overlapIm_mem_linearSpan T a i j) (overlapIm_mem_linearSpan T a i j)
  · exact linearSpan_le_quadraticSpan (C_mem_linearSpan _)

theorem unitaryRePolynomial_mem_quadraticSpan (i j : Fin 6) :
    unitaryRePolynomial i j ∈ quadraticSpan (σ := Coord) := by
  unfold unitaryRePolynomial
  apply Submodule.sub_mem
  · apply Submodule.sum_mem
    intro k hk
    exact Submodule.add_mem _
      (linear_mul_mem_quadraticSpan (X_mem_linearSpan _) (X_mem_linearSpan _))
      (linear_mul_mem_quadraticSpan (X_mem_linearSpan _) (X_mem_linearSpan _))
  · exact linearSpan_le_quadraticSpan (C_mem_linearSpan _)

theorem unitaryImPolynomial_mem_quadraticSpan (i j : Fin 6) :
    unitaryImPolynomial i j ∈ quadraticSpan (σ := Coord) := by
  unfold unitaryImPolynomial
  apply Submodule.sum_mem
  intro k hk
  exact Submodule.sub_mem _
    (linear_mul_mem_quadraticSpan (X_mem_linearSpan _) (X_mem_linearSpan _))
    (linear_mul_mem_quadraticSpan (X_mem_linearSpan _) (X_mem_linearSpan _))

theorem equationPolynomial_mem_quadraticSpan (T : Triple) (e : EquationIndex) :
    equationPolynomial T e ∈ quadraticSpan (σ := Coord) := by
  cases e with
  | inl e => rcases e with ⟨a,i,j⟩; exact muPolynomial_mem_quadraticSpan T a i j
  | inr e =>
    rcases e with ⟨i,j,b⟩
    cases b
    · exact unitaryRePolynomial_mem_quadraticSpan i j
    · exact unitaryImPolynomial_mem_quadraticSpan i j

/-- Finite degree-at-most-four annihilation equations, with no point input. -/
def FiniteRelationCompatibility (T : Triple) (Λ : Poly →ₗ[ℝ] ℝ) : Prop :=
  ∀ e : EquationIndex, ∀ i : Two (σ := Coord),
    Λ (twoPolynomial i * equationPolynomial T e) = 0

theorem compatible_equation_square_zero (T : Triple) (Λ : Poly →ₗ[ℝ] ℝ)
    (hrel : FiniteRelationCompatibility T Λ) (e : EquationIndex) :
    Λ (equationPolynomial T e ^ 2) = 0 :=
  square_zero_of_finite_relations Λ _ (equationPolynomial_mem_quadraticSpan T e) (hrel e)

theorem variety_nonempty_of_positive_flat (T : Triple) (Λ : Poly →ₗ[ℝ] ℝ)
    (hnorm : Λ 1 = 1) (hflat : (momentTwo Λ).rank = (momentOne Λ).rank)
    (hrel : FiniteRelationCompatibility T Λ) (hM : (momentTwo Λ).PosSemidef) :
    (polynomialVariety T).Nonempty := by
  obtain ⟨x, hx⟩ := real_point_of_positive_flat Λ hnorm hM hflat
  refine ⟨x, (all_equations_vanish_iff T x).mp ?_⟩
  intro e
  exact hx _ (equationPolynomial_mem_quadraticSpan T e) (compatible_equation_square_zero T Λ hrel e)

theorem fourth_basis_of_positive_flat (T : Triple) (Λ : Poly →ₗ[ℝ] ℝ)
    (hnorm : Λ 1 = 1) (hflat : (momentTwo Λ).rank = (momentOne Λ).rank)
    (hrel : FiniteRelationCompatibility T Λ) (hM : (momentTwo Λ).PosSemidef) :
    ∃ U, FourthBasis T U :=
  (polynomialVariety_nonempty_iff T).mp (variety_nonempty_of_positive_flat T Λ hnorm hflat hrel hM)

theorem moment_nonpositive_of_empty_variety (T : Triple) (Λ : Poly →ₗ[ℝ] ℝ)
    (h_empty : polynomialVariety T = ∅) (hnorm : Λ 1 = 1)
    (hflat : (momentTwo Λ).rank = (momentOne Λ).rank)
    (hrel : FiniteRelationCompatibility T Λ) : ¬ (momentTwo Λ).PosSemidef := by
  intro hM
  have h := variety_nonempty_of_positive_flat T Λ hnorm hflat hrel hM
  rw [h_empty] at h
  exact Set.not_nonempty_empty h


theorem evaluation_finite_relations (T : Triple) (x : Coord → ℝ) (hx : Vanishing T x) :
    FiniteRelationCompatibility T (evaluationFunctional x) := by
  intro e i
  simp only [evaluationFunctional_apply, map_mul,
    (all_equations_vanish_iff T x).mpr hx e, mul_zero]

/-- The moment formulation is equivalent to an actual fourth-basis solution. -/
theorem fourth_basis_iff_positive_flat_moments (T : Triple) :
    (∃ U, FourthBasis T U) ↔
      ∃ Λ : Poly →ₗ[ℝ] ℝ, Λ 1 = 1 ∧ (momentTwo Λ).PosSemidef ∧
        (momentTwo Λ).rank = (momentOne Λ).rank ∧ FiniteRelationCompatibility T Λ := by
  constructor
  · rintro ⟨U, hU⟩
    obtain ⟨hnorm, hM, hflat⟩ := evaluation_moment_positive_flat (coordinates U)
    exact ⟨evaluationFunctional (coordinates U), hnorm, hM, hflat,
      evaluation_finite_relations T _ ((coordinates_vanishing_iff T U).mpr hU)⟩
  · rintro ⟨Λ, hnorm, hM, hflat, hrel⟩
    exact fourth_basis_of_positive_flat T Λ hnorm hflat hrel hM

theorem empty_variety_iff_no_positive_flat_moments (T : Triple) :
    polynomialVariety T = ∅ ↔
      ¬ ∃ Λ : Poly →ₗ[ℝ] ℝ, Λ 1 = 1 ∧ (momentTwo Λ).PosSemidef ∧
        (momentTwo Λ).rank = (momentOne Λ).rank ∧ FiniteRelationCompatibility T Λ := by
  rw [polynomialVariety_eq_empty_iff, fourth_basis_iff_positive_flat_moments]

end MUB.ConcreteMubPolynomialSystem

#print axioms MUB.ConcreteMubPolynomialSystem.equationPolynomial_mem_quadraticSpan
#print axioms MUB.ConcreteMubPolynomialSystem.variety_nonempty_of_positive_flat
#print axioms MUB.ConcreteMubPolynomialSystem.fourth_basis_of_positive_flat
#print axioms MUB.ConcreteMubPolynomialSystem.moment_nonpositive_of_empty_variety

#print axioms MUB.ConcreteMubPolynomialSystem.fourth_basis_iff_positive_flat_moments
#print axioms MUB.ConcreteMubPolynomialSystem.empty_variety_iff_no_positive_flat_moments
