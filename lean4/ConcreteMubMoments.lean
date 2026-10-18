import ConcreteMubProjectors
import Mathlib.LinearAlgebra.Matrix.PosDef

/-!
# Complex word moments from a supplied finite MUB family

AuthorityEffect: None.

This is a forward construction in actual complex matrices. The state is a vector
from one supplied basis, and the degree-one test words contain every projector
from a different basis. MU makes all those overlaps nonzero, so these columns
span the coordinate space. The complete, nonduplicate word lists of degrees at
most one and two therefore give positive semidefinite moment matrices of rank
`Fintype.card ι`, with the first matrix an actual principal submatrix of the
second. The rank equality is a conclusion, not an input field.

This does not construct a MUB family, extract operators from an arbitrary
positive functional, or connect the real zero set of 108 specified polynomials
to these complex word moments. The rational API in MomentPositivityObligation
remains separate; no unproved realification is used here.
-/

namespace MUB.FiniteComplexMubFamily
open scoped BigOperators Matrix ComplexOrder
variable {ι B J : Type*} [Fintype ι] [DecidableEq ι] [Fintype B] [DecidableEq B]

noncomputable def concreteWordOperator (family : FiniteComplexMubFamily ι B ι) :
    List (B × ι) → Matrix ι ι ℂ
  | [] => 1
  | g :: w => family.concreteProjector g.1 g.2 * family.concreteWordOperator w

theorem concreteWordOperator_append (family : FiniteComplexMubFamily ι B ι)
    (u v : List (B × ι)) :
    family.concreteWordOperator (u ++ v) =
      family.concreteWordOperator u * family.concreteWordOperator v := by
  induction u with
  | nil => simp [concreteWordOperator]
  | cons g u ih => simp [concreteWordOperator, ih, Matrix.mul_assoc]

theorem concreteWordOperator_reverse (family : FiniteComplexMubFamily ι B ι)
    (w : List (B × ι)) :
    family.concreteWordOperator w.reverse = (family.concreteWordOperator w).conjTranspose := by
  induction w with
  | nil => simp [concreteWordOperator]
  | cons g w ih =>
    simp [List.reverse_cons, concreteWordOperator_append, concreteWordOperator,
      ih, family.concreteProjector_self_adjoint]

noncomputable def complexWordMoment (family : FiniteComplexMubFamily ι B ι)
    (ψ : ι → ℂ) (w : List (B × ι)) : ℂ :=
  finiteHilbertInner ψ (family.concreteWordOperator w *ᵥ ψ)

noncomputable def complexMomentMatrix (family : FiniteComplexMubFamily ι B ι)
    (ψ : ι → ℂ) (words : J → List (B × ι)) : Matrix J J ℂ :=
  fun i j => family.complexWordMoment ψ ((words i).reverse ++ words j)

noncomputable def wordStateColumns (family : FiniteComplexMubFamily ι B ι)
    (ψ : ι → ℂ) (words : J → List (B × ι)) : Matrix ι J ℂ :=
  fun i j => (family.concreteWordOperator (words j) *ᵥ ψ) i

theorem complexMomentMatrix_eq_gram [Fintype J]
    (family : FiniteComplexMubFamily ι B ι) (ψ : ι → ℂ)
    (words : J → List (B × ι)) :
    family.complexMomentMatrix ψ words =
      (family.wordStateColumns ψ words).conjTranspose * family.wordStateColumns ψ words := by
  ext i j
  simp only [complexMomentMatrix, complexWordMoment, concreteWordOperator_append,
    concreteWordOperator_reverse]
  change star ψ ⬝ᵥ ((family.concreteWordOperator (words i)).conjTranspose *
    family.concreteWordOperator (words j)) *ᵥ ψ = _
  rw [← Matrix.mulVec_mulVec, Matrix.dotProduct_mulVec, Matrix.vecMul_conjTranspose, star_star]
  rfl

theorem complexMomentMatrix_posSemidef [Fintype J] [DecidableEq J]
    (family : FiniteComplexMubFamily ι B ι) (ψ : ι → ℂ)
    (words : J → List (B × ι)) : (family.complexMomentMatrix ψ words).PosSemidef := by
  rw [complexMomentMatrix_eq_gram]
  exact Matrix.posSemidef_conjTranspose_mul_self _

theorem complexMomentMatrix_rank [Fintype J]
    (family : FiniteComplexMubFamily ι B ι) (ψ : ι → ℂ)
    (words : J → List (B × ι)) :
    (family.complexMomentMatrix ψ words).rank = (family.wordStateColumns ψ words).rank := by
  rw [complexMomentMatrix_eq_gram, Matrix.rank_conjTranspose_mul_self]

theorem wordStateColumns_rank_of_singletons [Fintype J]
    (family : FiniteComplexMubFamily ι B ι) (b₀ b₁ : B) (l₀ : ι) (h : b₁ ≠ b₀)
    (words : J → List (B × ι)) (single : ι → J)
    (hsingle : ∀ l, words (single l) = [(b₁, l)]) :
    (family.wordStateColumns (family.vector b₀ l₀) words).rank = Fintype.card ι := by
  let U : Matrix ι ι ℂ := fun i l => family.vector b₁ l i
  let α : ι → ℂ := fun l => finiteHilbertInner (family.vector b₁ l) (family.vector b₀ l₀)
  have hα : ∀ l, α l ≠ 0 := by
    intro l hzero
    have hmu := family.cross_basis_unbiased h l l₀
    have hcard : (Fintype.card ι : ℂ) ≠ 0 := by
      let : Nonempty ι := ⟨l₀⟩
      exact_mod_cast (Fintype.card_ne_zero (α := ι))
    change α l * star (α l) = _ at hmu
    rw [hzero, zero_mul] at hmu
    exact (inv_ne_zero hcard) hmu.symm
  have hU : U.conjTranspose * U = 1 := by
    ext i j
    change finiteHilbertInner (family.vector b₁ i) (family.vector b₁ j) = _
    simpa only [Matrix.one_apply] using family.same_basis_inner b₁ i j
  let A := family.wordStateColumns (family.vector b₀ l₀) words
  have hsub : A.submatrix id single = U * Matrix.diagonal α := by
    ext i l
    simp only [A, wordStateColumns, Matrix.submatrix_apply, id_eq, hsingle,
      concreteWordOperator, Matrix.mul_one, concreteProjector, Matrix.vecMulVec_mulVec,
      Matrix.mul_diagonal, Pi.smul_apply, op_smul_eq_smul, smul_eq_mul]
    change α l * U i l = U i l * α l
    exact mul_comm _ _
  have hinv : (Matrix.diagonal (fun l => (α l)⁻¹) * U.conjTranspose) *
      (A.submatrix id single) = 1 := by
    rw [hsub, Matrix.mul_assoc, ← Matrix.mul_assoc U.conjTranspose, hU,
      Matrix.one_mul, Matrix.diagonal_mul_diagonal]
    ext i j
    simp [hα]
  have hfull : Fintype.card ι ≤ (A.submatrix id single).rank := by
    have hr := Matrix.rank_mul_le_right
      (Matrix.diagonal (fun l => (α l)⁻¹) * U.conjTranspose) (A.submatrix id single)
    rwa [hinv, Matrix.rank_one] at hr
  exact le_antisymm (Matrix.rank_le_card_height A)
    (hfull.trans (Matrix.rank_submatrix_le A id single))

def degreeOneWords : Option (B × ι) → List (B × ι)
  | none => []
  | some g => [g]

def degreeTwoWords : Option ((B × ι) ⊕ ((B × ι) × (B × ι))) → List (B × ι)
  | none => []
  | some (.inl g) => [g]
  | some (.inr (g, h)) => [g, h]

omit [Fintype ι] [DecidableEq ι] [Fintype B] [DecidableEq B] in
theorem degreeOneWords_injective : Function.Injective (degreeOneWords (B := B) (ι := ι)) := by
  intro x y h
  cases x <;> cases y <;> simp_all [degreeOneWords]

omit [Fintype ι] [DecidableEq ι] [Fintype B] [DecidableEq B] in
theorem degreeTwoWords_injective : Function.Injective (degreeTwoWords (B := B) (ι := ι)) := by
  intro x y h
  cases x with
  | none =>
    cases y with
    | none => rfl
    | some y => cases y <;> simp_all [degreeTwoWords]
  | some x =>
    cases y with
    | none => cases x <;> simp_all [degreeTwoWords]
    | some y => cases x <;> cases y <;> simp_all [degreeTwoWords, Prod.ext_iff]

omit [Fintype ι] [DecidableEq ι] [Fintype B] [DecidableEq B] in
theorem degreeOneWords_complete (w : List (B × ι)) (hlen : w.length ≤ 1) :
    ∃ i, degreeOneWords i = w := by
  cases w with
  | nil => exact ⟨none, rfl⟩
  | cons g w =>
    cases w with
    | nil => exact ⟨some g, rfl⟩
    | cons h w => simp at hlen

omit [Fintype ι] [DecidableEq ι] [Fintype B] [DecidableEq B] in
theorem degreeTwoWords_complete (w : List (B × ι)) (hlen : w.length ≤ 2) :
    ∃ i, degreeTwoWords i = w := by
  cases w with
  | nil => exact ⟨none, rfl⟩
  | cons g w =>
    cases w with
    | nil => exact ⟨some (.inl g), rfl⟩
    | cons h w =>
      cases w with
      | nil => exact ⟨some (.inr (g, h)), rfl⟩
      | cons k w => simp at hlen

def degreeOneInTwo (i : Option (B × ι)) : Option ((B × ι) ⊕ ((B × ι) × (B × ι))) :=
  i.map Sum.inl

omit [Fintype ι] [DecidableEq ι] [Fintype B] [DecidableEq B] in
theorem degreeOneInTwo_preserves_word (i : Option (B × ι)) :
    degreeTwoWords (degreeOneInTwo i) = degreeOneWords i := by
  cases i <;> rfl

theorem complexMomentMatrix_principal_degree_one
    (family : FiniteComplexMubFamily ι B ι) (ψ : ι → ℂ) :
    (family.complexMomentMatrix ψ degreeTwoWords).submatrix degreeOneInTwo degreeOneInTwo =
      family.complexMomentMatrix ψ degreeOneWords := by
  ext i j
  simp only [Matrix.submatrix_apply, complexMomentMatrix, degreeOneInTwo_preserves_word]

theorem complexWordMoment_empty_normalized (family : FiniteComplexMubFamily ι B ι)
    (b : B) (l : ι) : family.complexWordMoment (family.vector b l) [] = 1 := by
  simpa [complexWordMoment, concreteWordOperator] using family.same_basis_inner b l l

omit [Fintype ι] [DecidableEq ι] [Fintype B] [DecidableEq B] in
theorem degreeOneInTwo_injective : Function.Injective (degreeOneInTwo (B := B) (ι := ι)) := by
  intro i j h
  apply degreeOneWords_injective
  rw [← degreeOneInTwo_preserves_word i, ← degreeOneInTwo_preserves_word j, h]

theorem complexMomentMatrix_full_rank_of_singletons [Fintype J]
    (family : FiniteComplexMubFamily ι B ι) (b₀ b₁ : B) (l₀ : ι) (h : b₁ ≠ b₀)
    (words : J → List (B × ι)) (single : ι → J)
    (hsingle : ∀ l, words (single l) = [(b₁, l)]) :
    (family.complexMomentMatrix (family.vector b₀ l₀) words).rank = Fintype.card ι := by
  rw [complexMomentMatrix_rank]
  exact family.wordStateColumns_rank_of_singletons b₀ b₁ l₀ h words single hsingle

theorem concrete_mub_degree_one_moment_rank
    (family : FiniteComplexMubFamily ι B ι) (b₀ b₁ : B) (l₀ : ι) (h : b₁ ≠ b₀) :
    (family.complexMomentMatrix (family.vector b₀ l₀) degreeOneWords).rank = Fintype.card ι := by
  exact family.complexMomentMatrix_full_rank_of_singletons b₀ b₁ l₀ h degreeOneWords
    (fun l => some (b₁, l)) (fun _ => rfl)

theorem concrete_mub_degree_two_moment_rank
    (family : FiniteComplexMubFamily ι B ι) (b₀ b₁ : B) (l₀ : ι) (h : b₁ ≠ b₀) :
    (family.complexMomentMatrix (family.vector b₀ l₀) degreeTwoWords).rank = Fintype.card ι := by
  exact family.complexMomentMatrix_full_rank_of_singletons b₀ b₁ l₀ h degreeTwoWords
    (fun l => some (.inl (b₁, l))) (fun _ => rfl)

theorem concrete_mub_moment_flatness
    (family : FiniteComplexMubFamily ι B ι) (b₀ b₁ : B) (l₀ : ι) (h : b₁ ≠ b₀) :
    (family.complexMomentMatrix (family.vector b₀ l₀) degreeTwoWords).rank =
      (family.complexMomentMatrix (family.vector b₀ l₀) degreeOneWords).rank := by
  rw [family.concrete_mub_degree_two_moment_rank b₀ b₁ l₀ h,
    family.concrete_mub_degree_one_moment_rank b₀ b₁ l₀ h]

end MUB.FiniteComplexMubFamily

#print axioms MUB.FiniteComplexMubFamily.complexMomentMatrix_posSemidef
#print axioms MUB.FiniteComplexMubFamily.concrete_mub_moment_flatness
