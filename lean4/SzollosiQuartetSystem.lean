import SzollosiTwoCirculant
import ConcreteMubFlatExtension

/-!
# Variable additional bases for the two-circulant family

AuthorityEffect: None.

The fixed first two bases are the identity and the normalized phase-family
matrix. Both additional bases are arbitrary complex six-by-six matrices.
The candidate-equation equivalence uses all 144 real coordinates for those two
bases, and a rational half-unit box contains every coordinate of a matrix
unbiased to the identity. The emptiness obligation ranges over every admissible
third basis. It does not select a Zauner triplet or establish any variety empty.

Conjecture 3 in Matolcsi et al., arXiv:2503.14752, concerns quadruplets containing
a member of the family: https://arxiv.org/pdf/2503.14752

This module uses parameter-dependent real polynomials. SzollosiQuadraticSystem
adds a joint rational quadratic specification with two-way quartet semantics.
Executable native export, square-system reduction, full cover, equivalence
transport, contractor soundness and reflected exclusion remain open.
-/

namespace MUB.SzollosiQuartetSystem
open Matrix
open ConcreteMubPolynomialSystem SzollosiTwoCirculant

/-- All column overlap norms, without a selected third basis. -/
def PairMU (U V : Candidate) : Prop :=
  ∀ i j, Complex.normSq ((U.conjTranspose * V) i j) = 1/6

def Quartet (B : Fin 4 → Candidate) : Prop :=
  (∀ a, (B a).conjTranspose * B a = 1) ∧ ∀ a b, a ≠ b → PairMU (B a) (B b)

def triple (H U : Candidate) : Triple := ![1,H,U]
def bases (H U V : Candidate) : Fin 4 → Candidate := ![1,H,U,V]

def Extension (H U V : Candidate) : Prop :=
  U.conjTranspose * U = 1 ∧ PairMU 1 U ∧ PairMU H U ∧ FourthBasis (triple H U) V

theorem pairMU_symm {U V : Candidate} (h : PairMU U V) : PairMU V U := by
  intro i j
  have he : (V.conjTranspose * U) i j = star ((U.conjTranspose * V) j i) := by
    have hm : (U.conjTranspose * V).conjTranspose = V.conjTranspose * U := by simp
    rw [← hm]
    rfl
  rw [he, Complex.star_def, Complex.normSq_conj]
  exact h j i

theorem extension_iff_quartet (H U V : Candidate)
    (hH : H.conjTranspose * H = 1) (hIH : PairMU 1 H) :
    Extension H U V ↔ Quartet (bases H U V) := by
  constructor
  · rintro ⟨hU,hIU,hHU,hV,hmu⟩
    have hIV : PairMU 1 V := fun i j => hmu 0 i j
    have hHV : PairMU H V := fun i j => hmu 1 i j
    have hUV : PairMU U V := fun i j => hmu 2 i j
    constructor
    · intro a
      fin_cases a
      · simp [bases]
      · exact hH
      · exact hU
      · exact hV
    · intro a b hab
      fin_cases a <;> fin_cases b
      all_goals first
        | exact (hab rfl).elim
        | exact hIH
        | exact pairMU_symm hIH
        | exact hIU
        | exact pairMU_symm hIU
        | exact hHU
        | exact pairMU_symm hHU
        | exact hIV
        | exact pairMU_symm hIV
        | exact hHV
        | exact pairMU_symm hHV
        | exact hUV
        | exact pairMU_symm hUV
  · rintro ⟨hu,hmu⟩
    refine ⟨hu 2,hmu 0 2 (by decide),hmu 1 2 (by decide),hu 3,?_⟩
    intro a i j
    fin_cases a
    · exact hmu 0 3 (by decide) i j
    · exact hmu 1 3 (by decide) i j
    · exact hmu 2 3 (by decide) i j

noncomputable def parameterMatrix (r : ParameterCoord → ℝ) : Candidate :=
  familyMatrix (decodeParameters r 0) (decodeParameters r 1)
    (decodeParameters r 2) (decodeParameters r 3)

theorem parameterMatrix_unitary (r : ParameterCoord → ℝ)
    (hr : ∀ e, MvPolynomial.eval r (parameterPolynomial e) = 0) :
    (parameterMatrix r).conjTranspose * parameterMatrix r = 1 :=
  (parameter_solution_matrix r hr).1

theorem parameterMatrix_mu_identity (r : ParameterCoord → ℝ)
    (hr : ∀ e, MvPolynomial.eval r (parameterPolynomial e) = 0) :
    PairMU 1 (parameterMatrix r) := by
  intro i j
  simp only [Matrix.conjTranspose_one, Matrix.one_mul]
  have h := (parameter_solution_matrix r hr).2 i j
  simp only [Complex.star_def, Complex.mul_conj] at h
  have hre := congrArg Complex.re h
  norm_num at hre
  exact hre

/-- The two variable bases use all 144 real coordinates. -/
theorem quartet_iff_candidate_equations (r : ParameterCoord → ℝ)
    (hr : ∀ e, MvPolynomial.eval r (parameterPolynomial e) = 0) :
    (∃ U V, Quartet (bases (parameterMatrix r) U V)) ↔
    ∃ u v : Coord → ℝ,
      (candidate u).conjTranspose * candidate u = 1 ∧
      PairMU 1 (candidate u) ∧ PairMU (parameterMatrix r) (candidate u) ∧
      Vanishing (triple (parameterMatrix r) (candidate u)) v := by
  have he := extension_iff_quartet (parameterMatrix r)
  have hH := parameterMatrix_unitary r hr
  have hIH := parameterMatrix_mu_identity r hr
  constructor
  · rintro ⟨U,V,h⟩
    have hx := (he U V hH hIH).mpr h
    refine ⟨coordinates U,coordinates V,?_,?_,?_,?_⟩
    · simpa only [candidate_coordinates] using hx.1
    · simpa only [candidate_coordinates] using hx.2.1
    · simpa only [candidate_coordinates] using hx.2.2.1
    · simpa only [candidate_coordinates] using
        (coordinates_vanishing_iff _ V).mpr hx.2.2.2
  · rintro ⟨u,v,hu,hIU,hHU,hv⟩
    refine ⟨candidate u,candidate v,(he _ _ hH hIH).mp ⟨hu,hIU,hHU,?_⟩⟩
    apply (coordinates_vanishing_iff _ (candidate v)).mp
    simpa only [coordinates_candidate] using hv

/-- A rational half-unit box contains every standard-basis-unbiased entry. -/
theorem mu_identity_coordinates_bounded (U : Candidate) (h : PairMU 1 U) :
    ∀ i, -(1/2 : ℝ) ≤ coordinates U i ∧ coordinates U i ≤ 1/2 := by
  rintro ⟨k,j,b⟩
  have hn := h k j
  simp only [Matrix.conjTranspose_one, Matrix.one_mul, Complex.normSq_apply] at hn
  have hre := sq_nonneg (U k j).re
  have him := sq_nonneg (U k j).im
  cases b
  · change -(1/2 : ℝ) ≤ (U k j).re ∧ (U k j).re ≤ 1/2
    constructor <;> nlinarith
  · change -(1/2 : ℝ) ≤ (U k j).im ∧ (U k j).im ≤ 1/2
    constructor <;> nlinarith

/-- The empty-variety obligation quantifies over every admissible third basis. -/
theorem no_quartet_iff_all_varieties_empty (r : ParameterCoord → ℝ)
    (hr : ∀ e, MvPolynomial.eval r (parameterPolynomial e) = 0) :
    (¬ ∃ U V, Quartet (bases (parameterMatrix r) U V)) ↔
    ∀ U, U.conjTranspose * U = 1 → PairMU 1 U → PairMU (parameterMatrix r) U →
      polynomialVariety (triple (parameterMatrix r) U) = ∅ := by
  constructor
  · intro h U hU hIU hHU
    apply (polynomialVariety_eq_empty_iff _).mpr
    rintro ⟨V,hV⟩
    exact h ⟨U,V,(extension_iff_quartet _ _ _ (parameterMatrix_unitary r hr)
      (parameterMatrix_mu_identity r hr)).mp ⟨hU,hIU,hHU,hV⟩⟩
  · intro h hq
    rcases hq with ⟨U,V,hq⟩
    have he := (extension_iff_quartet _ _ _ (parameterMatrix_unitary r hr)
      (parameterMatrix_mu_identity r hr)).mpr hq
    exact (polynomialVariety_eq_empty_iff _).mp (h U he.1 he.2.1 he.2.2.1) ⟨V,he.2.2.2⟩

#print axioms pairMU_symm
#print axioms extension_iff_quartet
#print axioms quartet_iff_candidate_equations
#print axioms mu_identity_coordinates_bounded
#print axioms no_quartet_iff_all_varieties_empty
end MUB.SzollosiQuartetSystem
