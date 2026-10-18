import ConcreteMubProjectors
import Mathlib.Algebra.MvPolynomial.Eval

/-!
# Coordinate polynomials for a fixed dimension-six triple

AuthorityEffect: None.

The candidate basis is an actual complex 6-by-6 matrix encoded by 72 real
coordinates. There are 108 MU residual polynomials and 72 real/imaginary
orthonormality residuals. These are 180 indexed constraints; independence is
not asserted. Their evaluations agree with the complex overlap and matrix
products. The MU residual also equals the corresponding projector cross-trace
minus one sixth. Their span is an actual polynomial ideal, and its real zero
set is identified with the candidate fourth-basis solutions.

A supplied complete complex MUB family gives a point in the zero set for its
first three bases, using its fourth basis as the candidate. No zero-set
emptiness, full moduli cover, GNS extraction, or moment nonpositivity is derived.
The fixed triple has real coefficients through its complex entries. Rational
interval enclosures for parameterized triples and cusp collars remain needed
before a native contractor can reflect claims about those families.
-/

namespace MUB.ConcreteMubPolynomialSystem
open scoped BigOperators Matrix
open MvPolynomial
/-- Row, column and real/imaginary component of a candidate entry. -/
abbrev Coord := Fin 6 × Fin 6 × Bool
abbrev Candidate := Matrix (Fin 6) (Fin 6) ℂ
abbrev Triple := Fin 3 → Candidate
abbrev Poly := MvPolynomial Coord ℝ

def coordinates (U : Candidate) : Coord → ℝ :=
  fun x => if x.2.2 then (U x.1 x.2.1).im else (U x.1 x.2.1).re

def candidate (x : Coord → ℝ) : Candidate :=
  fun k j => ⟨x (k,j,false), x (k,j,true)⟩

theorem candidate_coordinates (U : Candidate) : candidate (coordinates U) = U := by
  ext k j; rfl

theorem coordinates_candidate (x : Coord → ℝ) : coordinates (candidate x) = x := by
  funext i
  rcases i with ⟨k,j,b⟩
  cases b <;> rfl

noncomputable def overlapRe (T : Triple) (a : Fin 3) (i j : Fin 6) : Poly :=
  ∑ k, (C (T a k i).re * X (k,j,false) + C (T a k i).im * X (k,j,true))
noncomputable def overlapIm (T : Triple) (a : Fin 3) (i j : Fin 6) : Poly :=
  ∑ k, (C (T a k i).re * X (k,j,true) - C (T a k i).im * X (k,j,false))
/-- Squared overlap minus one sixth, for each of the 108 MU indices. -/
noncomputable def muPolynomial (T : Triple) (a : Fin 3) (i j : Fin 6) : Poly :=
  overlapRe T a i j ^ 2 + overlapIm T a i j ^ 2 - C (1/6 : ℝ)

noncomputable def unitaryRePolynomial (i j : Fin 6) : Poly :=
  (∑ k, (X (k,i,false) * X (k,j,false) + X (k,i,true) * X (k,j,true))) -
    C (if i=j then (1 : ℝ) else 0)
noncomputable def unitaryImPolynomial (i j : Fin 6) : Poly :=
  ∑ k, (X (k,i,false) * X (k,j,true) - X (k,i,true) * X (k,j,false))

def overlap (T : Triple) (U : Candidate) (a : Fin 3) (i j : Fin 6) : ℂ :=
  ∑ k, star (T a k i) * U k j

theorem overlapRe_eval (T : Triple) (U : Candidate) (a : Fin 3) (i j : Fin 6) :
    eval (coordinates U) (overlapRe T a i j) = (overlap T U a i j).re := by
  simp [overlapRe, overlap, coordinates, Complex.mul_re]

theorem overlapIm_eval (T : Triple) (U : Candidate) (a : Fin 3) (i j : Fin 6) :
    eval (coordinates U) (overlapIm T a i j) = (overlap T U a i j).im := by
  simp [overlapIm, overlap, coordinates, Complex.mul_im, sub_eq_add_neg]

theorem muPolynomial_eval (T : Triple) (U : Candidate) (a : Fin 3) (i j : Fin 6) :
    eval (coordinates U) (muPolynomial T a i j) =
      Complex.normSq (overlap T U a i j) - 1/6 := by
  simp [muPolynomial, overlapRe_eval, overlapIm_eval, Complex.normSq_apply, pow_two]

theorem unitaryRePolynomial_eval (U : Candidate) (i j : Fin 6) :
    eval (coordinates U) (unitaryRePolynomial i j) =
      ((U.conjTranspose * U) i j).re - (if i=j then 1 else 0) := by
  simp [unitaryRePolynomial, coordinates, Matrix.mul_apply, Matrix.conjTranspose_apply,
    Complex.mul_re]

theorem unitaryImPolynomial_eval (U : Candidate) (i j : Fin 6) :
    eval (coordinates U) (unitaryImPolynomial i j) = ((U.conjTranspose * U) i j).im := by
  simp [unitaryImPolynomial, coordinates, Matrix.mul_apply, Matrix.conjTranspose_apply,
    Complex.mul_im, sub_eq_add_neg]

noncomputable def columnProjector (U : Candidate) (l : Fin 6) : Candidate :=
  Matrix.vecMulVec (fun k => U k l) (fun k => star (U k l))

theorem columnProjector_cross_trace (T : Triple) (U : Candidate)
    (a : Fin 3) (i j : Fin 6) :
    Matrix.trace (columnProjector (T a) i * columnProjector U j) =
      (Complex.normSq (overlap T U a i j) : ℂ) := by
  have ht : Matrix.trace (columnProjector (T a) i * columnProjector U j) =
      overlap T U a i j * star (overlap T U a i j) := by
    rw [columnProjector, columnProjector, Matrix.vecMulVec_mul_vecMulVec,
      Matrix.trace_vecMulVec]
    simp only [dotProduct, Pi.smul_apply, smul_eq_mul, overlap,
      star_sum, star_mul, star_star]
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro k hk
    ring
  simpa only [Complex.star_def, Complex.mul_conj] using ht

theorem muPolynomial_eval_projector_trace (T : Triple) (U : Candidate)
    (a : Fin 3) (i j : Fin 6) :
    (eval (coordinates U) (muPolynomial T a i j) : ℂ) =
      Matrix.trace (columnProjector (T a) i * columnProjector U j) - (1/6 : ℂ) := by
  rw [muPolynomial_eval, Complex.ofReal_sub, columnProjector_cross_trace]
  norm_num

theorem unitary_equations_iff (U : Candidate) :
    (∀ i j, eval (coordinates U) (unitaryRePolynomial i j) = 0 ∧
      eval (coordinates U) (unitaryImPolynomial i j) = 0) ↔ U.conjTranspose * U = 1 := by
  simp only [unitaryRePolynomial_eval, unitaryImPolynomial_eval, sub_eq_zero]
  constructor
  · intro h
    ext i j
    apply Complex.ext
    · by_cases hij : i = j <;> simpa [Matrix.one_apply, hij] using (h i j).1
    · by_cases hij : i = j <;> simpa [Matrix.one_apply, hij] using (h i j).2
  · intro h i j
    rw [h]
    by_cases hij : i = j <;> simp [Matrix.one_apply, hij]

noncomputable def Vanishing (T : Triple) (x : Coord → ℝ) : Prop :=
  (∀ a i j, eval x (muPolynomial T a i j) = 0) ∧
  (∀ i j, eval x (unitaryRePolynomial i j) = 0 ∧ eval x (unitaryImPolynomial i j) = 0)

def FourthBasis (T : Triple) (U : Candidate) : Prop :=
  U.conjTranspose * U = 1 ∧ ∀ a i j, Complex.normSq (overlap T U a i j) = 1/6

theorem coordinates_vanishing_iff (T : Triple) (U : Candidate) :
    Vanishing T (coordinates U) ↔ FourthBasis T U := by
  simp only [Vanishing, FourthBasis, muPolynomial_eval, sub_eq_zero, unitary_equations_iff]
  exact and_comm

/-- Simultaneous real vanishing locus including candidate orthonormality. -/
noncomputable def polynomialVariety (T : Triple) : Set (Coord → ℝ) :=
  {x | Vanishing T x}

theorem polynomialVariety_nonempty_iff (T : Triple) :
    (polynomialVariety T).Nonempty ↔ ∃ U, FourthBasis T U := by
  constructor
  · rintro ⟨x, hx⟩
    refine ⟨candidate x, (coordinates_vanishing_iff T (candidate x)).mp ?_⟩
    change Vanishing T x at hx
    simpa only [coordinates_candidate] using hx
  · rintro ⟨U, hU⟩
    exact ⟨coordinates U, (coordinates_vanishing_iff T U).mpr hU⟩

theorem polynomialVariety_eq_empty_iff (T : Triple) :
    polynomialVariety T = ∅ ↔ ¬ ∃ U, FourthBasis T U := by
  rw [← polynomialVariety_nonempty_iff, Set.not_nonempty_iff_eq_empty]

abbrev EquationIndex := (Fin 3 × Fin 6 × Fin 6) ⊕ Coord

noncomputable def equationPolynomial (T : Triple) : EquationIndex → Poly
  | .inl (a,i,j) => muPolynomial T a i j
  | .inr (i,j,false) => unitaryRePolynomial i j
  | .inr (i,j,true) => unitaryImPolynomial i j

theorem all_equations_vanish_iff (T : Triple) (x : Coord → ℝ) :
    (∀ e, eval x (equationPolynomial T e) = 0) ↔ Vanishing T x := by
  constructor
  · intro h
    exact ⟨fun a i j => h (.inl (a,i,j)),
      fun i j => ⟨h (.inr (i,j,false)), h (.inr (i,j,true))⟩⟩
  · rintro ⟨hmu, hu⟩ e
    cases e with
    | inl e => rcases e with ⟨a,i,j⟩; exact hmu a i j
    | inr e =>
      rcases e with ⟨i,j,b⟩
      cases b
      · exact (hu i j).1
      · exact (hu i j).2

/-- The ideal generated by the 180 indexed scalar residuals. -/
noncomputable def polynomialIdeal (T : Triple) : Ideal Poly :=
  Ideal.span (Set.range (equationPolynomial T))

theorem polynomialIdeal_le_eval_kernel_iff (T : Triple) (x : Coord → ℝ) :
    polynomialIdeal T ≤ RingHom.ker (eval x) ↔ Vanishing T x := by
  rw [polynomialIdeal, Ideal.span_le, Set.range_subset_iff]
  exact all_equations_vanish_iff T x

theorem total_equation_count : Fintype.card EquationIndex = 180 := by simp [EquationIndex, Coord]

theorem coordinate_count : Fintype.card Coord = 72 := by decide

theorem mu_equation_count : Fintype.card (Fin 3 × Fin 6 × Fin 6) = 108 := by decide

abbrev CompleteFamily := MUB.FiniteComplexMubFamily (Fin 6) (Fin 7) (Fin 6)

def familyBasis (family : CompleteFamily) (b : Fin 7) : Candidate :=
  fun k j => family.vector b j k

def familyTriple (family : CompleteFamily) : Triple :=
  fun a => familyBasis family ⟨a.val, by omega⟩

theorem family_fourth_basis (family : CompleteFamily) :
    FourthBasis (familyTriple family) (familyBasis family 3) := by
  constructor
  · ext i j
    change MUB.finiteHilbertInner (family.vector 3 i) (family.vector 3 j) = _
    simpa only [Matrix.one_apply] using family.same_basis_inner 3 i j
  · intro a i j
    have hne : (⟨a.val, by omega⟩ : Fin 7) ≠ 3 := by
      intro heq
      have hv : a.val = 3 := congrArg Fin.val heq
      have ha := a.isLt
      omega
    have hmu := family.cross_basis_unbiased hne i j
    change overlap (familyTriple family) (familyBasis family 3) a i j *
      star (overlap (familyTriple family) (familyBasis family 3) a i j) = _ at hmu
    simp only [Complex.star_def, Complex.mul_conj] at hmu
    have hre := congrArg Complex.re hmu
    norm_num at hre
    exact hre

theorem family_triple_variety_nonempty (family : CompleteFamily) :
    (polynomialVariety (familyTriple family)).Nonempty := by
  exact (polynomialVariety_nonempty_iff _).mpr ⟨familyBasis family 3, family_fourth_basis family⟩

theorem no_family_of_empty_triple_variety (family : CompleteFamily)
    (h_empty : polynomialVariety (familyTriple family) = ∅) : False := by
  have h := family_triple_variety_nonempty family
  rw [h_empty] at h
  exact Set.not_nonempty_empty h

end MUB.ConcreteMubPolynomialSystem

#print axioms MUB.ConcreteMubPolynomialSystem.family_triple_variety_nonempty

#print axioms MUB.ConcreteMubPolynomialSystem.polynomialVariety_eq_empty_iff

#print axioms MUB.ConcreteMubPolynomialSystem.polynomialIdeal_le_eval_kernel_iff

#print axioms MUB.ConcreteMubPolynomialSystem.muPolynomial_eval_projector_trace
