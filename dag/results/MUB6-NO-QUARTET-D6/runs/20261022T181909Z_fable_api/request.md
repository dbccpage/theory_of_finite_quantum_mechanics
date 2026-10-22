# Problem: exclude a concrete Hadamard matrix from every MUB quartet in ℂ⁶

You are working on DAG node `MUB6-NO-QUARTET-D6` ("no four pairwise mutually unbiased bases exist in ℂ⁶", open) in a Lean 4 project. You have no tools. Everything you need is in this message, and your answer will be compiled and audited by the host.

## What the repository already proves

`MUB.SzollosiCommonRays.no_quartet_of_no_unbiased_ray_pair`, in `lean4/SzollosiCommonRays.lean` (included below) with the quartet system of `lean4/SzollosiQuartetSystem.lean` (included below), states the following.

> If no two common rays of a 6×6 complex Hadamard matrix H are unbiased, then H is in no MUB quartet containing the identity.

A **common ray** is a unit vector unbiased to both the standard basis and the columns of H/√6 (see `CommonRay` in the file). Read the exact Lean definitions below and follow them, not this paraphrase.

What is open is to **discharge that hypothesis for a concrete H**. Known external context, which you must not cite as proof:
- The Fourier matrix F₆ and the Szöllősi family are the standard candidates.
- OpenAI's `openai/math` proves N(6) ≤ 5. That is imported as an assumption here and does not decide quartets.
- Jaming–Matolcsi–Móra–Szöllősi–Weiner (2009) studied extensions of F₆ by computer-assisted means.

## The task

Pick a concrete 6×6 complex Hadamard matrix H with exact algebraic entries. **F₆, with entries ω^{jk}, ω = e^{2πi/6}, is the first choice.** Then prove in Lean 4 that no two common rays of H are unbiased, and conclude, using `no_quartet_of_no_unbiased_ray_pair`, that H lies in no MUB quartet containing the identity.

To do it you must:
- characterise or parametrise the common rays of (I, H) exactly. For F₆ the vectors unbiased to I and F₆ have a known structure, and you should derive it;
- show that any two of them have an overlap with |⟨z, w⟩|² ≠ 1/6.

If the full statement is out of reach, prove the largest honest finite piece and state exactly what is missing. Examples:
- the exact parametrisation of the common rays of F₆, as a Lean theorem;
- the exclusion of a stated sub-family;
- a reduction to a finite polynomial-system check together with that check.

Do not replace the claim by a floating-point computation. Every number must be exact: elements of ℚ(√−3), ℚ(ζ₁₂) or ℚ, or Mathlib's `ℂ` with exact algebraic witnesses.

## Deliverable format

1. **A short mathematical argument,** in plain prose, first.
2. **One or more complete Lean files.** Each goes in a fenced block whose first line is `-- FILE: lean4/<Name>.lean`. Suggested name: `lean4/MubFourierSixNoQuartet.lean`.
   - Target: Lean `4.35.0` with Mathlib `v4.35.0` (sha `56a005855ea17e0b0958f73ec801ae140b0a1679`).
   - You may `import SzollosiCommonRays` and `import SzollosiQuartetSystem`.
   - **Forbidden:** `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`. The host rejects any file that contains them, and requires `#print axioms` to show only `propext`, `Classical.choice`, `Quot.sound`.
   - End each file with `#print axioms` lines for its main theorems.
3. **A final section "WHAT IS PROVED".** State exactly the theorem(s) the Lean establishes, and anything left unproved. Do not overstate. The host compares this section with the compiled statements.

## Included repository files


### lean4/SzollosiCommonRays.lean
```lean
import MubMonomialTransport
import Mathlib.Tactic.NormNum

/-!
# Common rays and concrete quartet completion

AuthorityEffect: None.

Raw vectors have unit-modulus entries and first coordinate one. Their
normalization is by sqrt(6). The predicates use the existing concrete
RawHadamard, RawMU and HasRawQuartet definitions. No finiteness assumption
on the common-ray set is needed for the equivalence or pair obstruction.
-/

noncomputable section
namespace MUB.SzollosiCommonRays
open MonomialTransport
open scoped BigOperators

abbrev Vec := Fin 6 → ℂ
abbrev SixMatrix := Mat (Fin 6)

def overlap (z w : Vec) : ℂ := ∑ i, star (z i) * w i
def column (U : SixMatrix) (j : Fin 6) : Vec := fun i => U i j

def CommonRay (H : SixMatrix) (z : Vec) : Prop :=
  z 0 = 1 ∧ (∀ i, Complex.normSq (z i) = 1) ∧
    ∀ k, Complex.normSq (overlap (column H k) z) = 6

def RayBasis (H U : SixMatrix) : Prop :=
  RawHadamard U ∧ ∀ j, CommonRay H (column U j)

def rephase (U : SixMatrix) : SixMatrix :=
  action U (Equiv.refl _) (Equiv.refl _) (fun _ => 1) (fun j => star (U 0 j))

theorem overlap_columns (U V : SixMatrix) (i j : Fin 6) :
    overlap (column U i) (column V j) = (U.conjTranspose * V) i j := by
  rfl

theorem rephase_phase_unit (U : SixMatrix) (hU : RawHadamard U) :
    ∀ j, Complex.normSq (star (U 0 j)) = 1 := by
  intro j
  simpa [Complex.star_def, Complex.normSq_conj] using hU.1 0 j

theorem rephase_first_row (U : SixMatrix) (hU : RawHadamard U) (j : Fin 6) :
    rephase U 0 j = 1 := by
  have h := congrArg (fun t : ℝ => (t : ℂ)) (hU.1 0 j)
  simpa [rephase, action, Complex.star_def, Complex.normSq_eq_conj_mul_self,
    mul_comm] using h

theorem rephase_hadamard (U : SixMatrix) (hU : RawHadamard U) :
    RawHadamard (rephase U) := by
  exact action_hadamard U _ _ _ _ (by intro i; simp)
    (rephase_phase_unit U hU) hU

theorem rephase_mu_right (H U : SixMatrix) (hU : RawHadamard U)
    (hHU : RawMU H U) : RawMU H (rephase U) := by
  have h := action_mu H U (Equiv.refl _) (Equiv.refl _) (Equiv.refl _)
    (fun _ => 1) (fun _ => 1) (fun j => star (U 0 j))
    (by intro i; simp) (by intro i; simp) (rephase_phase_unit U hU) hHU
  have hid : action H (Equiv.refl _) (Equiv.refl _)
      (fun _ => 1) (fun _ => 1) = H := by
    ext i j
    simp [action]
  rw [hid] at h
  exact h

theorem rephase_mu_both (U V : SixMatrix) (hU : RawHadamard U)
    (hV : RawHadamard V) (hUV : RawMU U V) :
    RawMU (rephase U) (rephase V) := by
  exact action_mu U V (Equiv.refl _) (Equiv.refl _) (Equiv.refl _)
    (fun _ => 1) (fun j => star (U 0 j)) (fun j => star (V 0 j))
    (by intro i; simp) (rephase_phase_unit U hU) (rephase_phase_unit V hV) hUV

theorem rephase_rayBasis (H U : SixMatrix) (hU : RawHadamard U)
    (hHU : RawMU H U) : RayBasis H (rephase U) := by
  refine ⟨rephase_hadamard U hU, ?_⟩
  intro j
  refine ⟨rephase_first_row U hU j, ?_, ?_⟩
  · intro i
    exact (rephase_hadamard U hU).1 i j
  · intro k
    rw [overlap_columns]
    simpa using rephase_mu_right H U hU hHU k j

theorem rayBasis_mu (H U : SixMatrix) (h : RayBasis H U) : RawMU H U := by
  intro i j
  simpa [overlap_columns] using (h.2 j).2.2 i

/-- Two common-ray bases with all cross overlaps unbiased are exactly a completion. -/
theorem quartet_iff_ray_bases (H : SixMatrix) (hH : RawHadamard H) :
    HasRawQuartet H ↔
      ∃ U V, RayBasis H U ∧ RayBasis H V ∧ RawMU U V := by
  constructor
  · rintro ⟨_, U, V, hU, hV, hHU, hHV, hUV⟩
    exact ⟨rephase U, rephase V, rephase_rayBasis H U hU hHU,
      rephase_rayBasis H V hV hHV, rephase_mu_both U V hU hV hUV⟩
  · rintro ⟨U, V, hU, hV, hUV⟩
    exact ⟨hH, U, V, hU.1, hV.1, rayBasis_mu H U hU,
      rayBasis_mu H V hV, hUV⟩

/-- The stronger pair obstruction works even for an infinite common-ray set. -/
theorem no_quartet_of_no_unbiased_ray_pair (H : SixMatrix)
    (hpair : ∀ z w, CommonRay H z → CommonRay H w →
      Complex.normSq (overlap z w) ≠ 6) : ¬ HasRawQuartet H := by
  intro hq
  obtain ⟨U, V, hU, hV, hUV⟩ := (quartet_iff_ray_bases H hq.1).mp hq
  apply hpair (column U 0) (column V 0) (hU.2 0) (hV.2 0)
  rw [overlap_columns]
  simpa using hUV 0 0

#print axioms quartet_iff_ray_bases
#print axioms no_quartet_of_no_unbiased_ray_pair

end MUB.SzollosiCommonRays

```


### lean4/SzollosiQuartetSystem.lean
```lean
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

```
