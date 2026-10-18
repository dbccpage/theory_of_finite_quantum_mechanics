import ConcreteMubMoments
import Mathlib.LinearAlgebra.Isomorphisms
import Mathlib.Analysis.Matrix.Order
/-!
# Finite projector actions extracted from positive flat word moments

AuthorityEffect: None.

The inputs are actual complex word values through degree four, normalized at
the empty word, a positive semidefinite degree-two moment matrix, equality of
its actual rank with the degree-one principal matrix, and explicit contextual
idempotence equations. Complete nonduplicate word lists are reused from
ConcreteMubMoments. No operators or state vectors are supplied as input.

A Gram factor, its common lower-word range, complex linear idempotents and a
normalized state are constructed. The actions are symmetric for the explicit
finite Hermitian pairing and reproduce every entry of the degree-two moment
matrix. The space dimension is the degree-one matrix rank.

This finite extraction does not establish dimension six, rank-one ranges,
basis completeness, same-basis orthogonality, cross-basis MU relations, or the
coordinate-variety bridge for arbitrary input data. It does not assert an
extension to all words of an unrestricted star algebra. Those conclusions
require the corresponding relations and further derivations. The rational
moment API remains separate. FlatMomentBasisRelations derives completeness
and same-basis orthogonality when their contextual equations are added.
-/

namespace MUB.FlatGramExtraction
open scoped Matrix ComplexOrder
variable {n m : Type*} [Fintype n] [Fintype m]

theorem shift_ker_le (B C : Matrix n m ℂ) (hrel : C.conjTranspose * C = C.conjTranspose * B) :
    LinearMap.ker B.mulVecLin ≤ LinearMap.ker C.mulVecLin := by
  intro x hx
  change B *ᵥ x = 0 at hx
  change C *ᵥ x = 0
  apply (Matrix.conjTranspose_mul_self_mulVec_eq_zero C x).mp
  rw [hrel, ← Matrix.mulVec_mulVec, hx, Matrix.mulVec_zero]

omit [Fintype m] in
theorem shift_cross (B C : Matrix n m ℂ) (hrel : C.conjTranspose * C = C.conjTranspose * B) :
    B.conjTranspose * C = C.conjTranspose * B := by
  have h := congrArg Matrix.conjTranspose hrel
  simp only [Matrix.conjTranspose_mul, Matrix.conjTranspose_conjTranspose] at h
  exact h.symm.trans hrel

noncomputable def extractedOperator (B C : Matrix n m ℂ)
    (hrange : LinearMap.range C.mulVecLin ≤ LinearMap.range B.mulVecLin)
    (hrel : C.conjTranspose * C = C.conjTranspose * B) :
    Module.End ℂ (LinearMap.range B.mulVecLin) :=
  let c := LinearMap.codRestrict (LinearMap.range B.mulVecLin) C.mulVecLin
    (fun x => hrange (LinearMap.mem_range_self C.mulVecLin x))
  let hk : LinearMap.ker B.mulVecLin ≤ LinearMap.ker c := by
    intro x hx
    apply Subtype.ext
    exact shift_ker_le B C hrel hx
  ((LinearMap.ker B.mulVecLin).liftQ c hk).comp B.mulVecLin.quotKerEquivRange.symm.toLinearMap

theorem extractedOperator_apply (B C : Matrix n m ℂ)
    (hrange : LinearMap.range C.mulVecLin ≤ LinearMap.range B.mulVecLin)
    (hrel : C.conjTranspose * C = C.conjTranspose * B) (x : m → ℂ) :
    (extractedOperator B C hrange hrel ⟨B *ᵥ x, LinearMap.mem_range_self B.mulVecLin x⟩ : n → ℂ) = C *ᵥ x := by
  dsimp only [extractedOperator, LinearMap.comp_apply, LinearEquiv.coe_coe]
  rw [show B.mulVecLin.quotKerEquivRange.symm
      ⟨B *ᵥ x, LinearMap.mem_range_self B.mulVecLin x⟩ = B.mulVecLin.ker.mkQ x from
    B.mulVecLin.quotKerEquivRange_symm_apply_image x _]
  rfl

theorem range_adjoint_zero (B : Matrix n m ℂ) (v : n → ℂ)
    (hv : v ∈ LinearMap.range B.mulVecLin) (hz : B.conjTranspose *ᵥ v = 0) : v = 0 := by
  obtain ⟨x, rfl⟩ := hv
  exact (Matrix.conjTranspose_mul_self_mulVec_eq_zero B x).mp
    (by simpa only [← Matrix.mulVec_mulVec, Matrix.mulVecLin_apply] using hz)

theorem shift_fixed (B C : Matrix n m ℂ)
    (hrange : LinearMap.range C.mulVecLin ≤ LinearMap.range B.mulVecLin)
    (hrel : C.conjTranspose * C = C.conjTranspose * B)
    (x y : m → ℂ) (hy : B *ᵥ y = C *ᵥ x) : C *ᵥ y = C *ᵥ x := by
  apply sub_eq_zero.mp
  apply range_adjoint_zero B
  · exact (LinearMap.range B.mulVecLin).sub_mem
      (hrange (LinearMap.mem_range_self C.mulVecLin y))
      (hrange (LinearMap.mem_range_self C.mulVecLin x))
  · rw [Matrix.mulVec_sub, sub_eq_zero]
    have hc (z : m → ℂ) : B.conjTranspose *ᵥ (C *ᵥ z) = C.conjTranspose *ᵥ (B *ᵥ z) := by
      rw [Matrix.mulVec_mulVec, Matrix.mulVec_mulVec, shift_cross B C hrel]
    rw [hc y, hy, hc x]
    simpa only [Matrix.mulVec_mulVec] using congrArg (fun M => M *ᵥ x) hrel

theorem extractedOperator_idempotent (B C : Matrix n m ℂ)
    (hrange : LinearMap.range C.mulVecLin ≤ LinearMap.range B.mulVecLin)
    (hrel : C.conjTranspose * C = C.conjTranspose * B) :
    (extractedOperator B C hrange hrel).comp (extractedOperator B C hrange hrel) =
      extractedOperator B C hrange hrel := by
  apply LinearMap.ext
  intro v
  obtain ⟨x, hx⟩ := v.property
  have hv : v = ⟨B *ᵥ x, LinearMap.mem_range_self B.mulVecLin x⟩ := Subtype.ext hx.symm
  rw [hv]
  obtain ⟨y, hy⟩ := hrange (LinearMap.mem_range_self C.mulVecLin x)
  have hp : extractedOperator B C hrange hrel
      ⟨B *ᵥ x, LinearMap.mem_range_self B.mulVecLin x⟩ =
      ⟨B *ᵥ y, LinearMap.mem_range_self B.mulVecLin y⟩ := by
    apply Subtype.ext
    exact (extractedOperator_apply B C hrange hrel x).trans hy.symm
  change extractedOperator B C hrange hrel
    (extractedOperator B C hrange hrel _) = extractedOperator B C hrange hrel _
  apply Subtype.ext
  rw [hp, extractedOperator_apply]
  exact (shift_fixed B C hrange hrel x y hy).trans hy.symm

theorem flat_gram_range {r : Type*} [Fintype r]
    (A : Matrix r n ℂ) (E : Matrix n m ℂ)
    (hflat : (A.conjTranspose * A).rank =
      ((A * E).conjTranspose * (A * E)).rank) :
    LinearMap.range (A * E).mulVecLin = LinearMap.range A.mulVecLin := by
  apply Submodule.eq_of_le_of_finrank_eq
  · rw [Matrix.mulVecLin_mul]
    exact LinearMap.range_comp_le_range _ _
  · change (A * E).rank = A.rank
    simpa only [Matrix.rank_conjTranspose_mul_self] using hflat.symm

omit [Fintype m] in
theorem gram_pullback {r : Type*} [Fintype r]
    (A : Matrix r n ℂ) (E D : Matrix n m ℂ) :
    (A * D).conjTranspose * (A * E) = D.conjTranspose * (A.conjTranspose * A) * E := by
  simp only [Matrix.conjTranspose_mul, Matrix.mul_assoc]

theorem gram_pairing (B C : Matrix n m ℂ) (x y : m → ℂ) :
    finiteHilbertInner (B *ᵥ x) (C *ᵥ y) =
      star x ⬝ᵥ ((B.conjTranspose * C) *ᵥ y) := by
  change star (B *ᵥ x) ⬝ᵥ (C *ᵥ y) = _
  simp only [Matrix.star_mulVec, Matrix.dotProduct_mulVec, Matrix.vecMul_vecMul]

theorem gram_pairing_single [DecidableEq m] (B C : Matrix n m ℂ) (i j : m) :
    finiteHilbertInner (B *ᵥ Pi.single i 1) (C *ᵥ Pi.single j 1) =
      (B.conjTranspose * C) i j := by
  rw [gram_pairing]
  simp [dotProduct, Matrix.mulVec, Pi.single_apply]

theorem extractedOperator_symmetric (B C : Matrix n m ℂ)
    (hrange : LinearMap.range C.mulVecLin ≤ LinearMap.range B.mulVecLin)
    (hrel : C.conjTranspose * C = C.conjTranspose * B)
    (v w : LinearMap.range B.mulVecLin) :
    finiteHilbertInner (v : n → ℂ) (extractedOperator B C hrange hrel w : n → ℂ) =
      finiteHilbertInner (extractedOperator B C hrange hrel v : n → ℂ) (w : n → ℂ) := by
  obtain ⟨x, hx⟩ := v.property
  obtain ⟨y, hy⟩ := w.property
  have hv : v = ⟨B *ᵥ x, LinearMap.mem_range_self B.mulVecLin x⟩ := Subtype.ext hx.symm
  have hw : w = ⟨B *ᵥ y, LinearMap.mem_range_self B.mulVecLin y⟩ := Subtype.ext hy.symm
  rw [hv, hw, extractedOperator_apply, extractedOperator_apply,
    gram_pairing, gram_pairing, shift_cross B C hrel]

theorem extract_of_positive_flat [DecidableEq n]
    (M : Matrix n n ℂ) (E D : Matrix n m ℂ)
    (hM : M.PosSemidef)
    (hflat : M.rank = (E.conjTranspose * M * E).rank)
    (hrel : D.conjTranspose * M * D = D.conjTranspose * M * E) :
    ∃ A : Matrix n n ℂ, A.conjTranspose * A = M ∧
      ∃ P : Module.End ℂ (LinearMap.range (A * E).mulVecLin),
        P.comp P = P ∧
        Module.finrank ℂ (LinearMap.range (A * E).mulVecLin) =
          (E.conjTranspose * M * E).rank ∧
        ∀ x : m → ℂ, (P ⟨(A * E) *ᵥ x,
          LinearMap.mem_range_self (A * E).mulVecLin x⟩ : n → ℂ) = (A * D) *ᵥ x := by
  classical
  open scoped MatrixOrder in
    obtain ⟨A, hA⟩ := CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hM.nonneg
  rw [Matrix.star_eq_conjTranspose] at hA
  have hgram : (A * E).conjTranspose * (A * E) = E.conjTranspose * M * E := by
    rw [gram_pullback, ← hA]
  have hsmall : LinearMap.range (A * E).mulVecLin = LinearMap.range A.mulVecLin := by
    apply flat_gram_range
    rw [← hA, hgram]
    exact hflat
  have hrange : LinearMap.range (A * D).mulVecLin ≤ LinearMap.range (A * E).mulVecLin := by
    rw [hsmall, Matrix.mulVecLin_mul]
    exact LinearMap.range_comp_le_range _ _
  have hrelation : (A * D).conjTranspose * (A * D) = (A * D).conjTranspose * (A * E) := by
    rw [gram_pullback, gram_pullback, ← hA, hrel]
  refine ⟨A, hA.symm, extractedOperator (A * E) (A * D) hrange hrelation,
    extractedOperator_idempotent _ _ _ _, ?_, extractedOperator_apply _ _ _ _⟩
  change (A * E).rank = _
  rw [← Matrix.rank_conjTranspose_mul_self, hgram]

#print axioms extract_of_positive_flat

#print axioms extractedOperator_idempotent
#print axioms flat_gram_range

#print axioms shift_ker_le
#print axioms extractedOperator_apply

theorem extract_family_of_positive_flat {G : Type*} [DecidableEq n]
    (M : Matrix n n ℂ) (E : Matrix n m ℂ) (D : G → Matrix n m ℂ)
    (hM : M.PosSemidef)
    (hflat : M.rank = (E.conjTranspose * M * E).rank)
    (hrel : ∀ g, (D g).conjTranspose * M * D g = (D g).conjTranspose * M * E) :
    ∃ A : Matrix n n ℂ, A.conjTranspose * A = M ∧
      ∃ P : G → Module.End ℂ (LinearMap.range (A * E).mulVecLin),
        Module.finrank ℂ (LinearMap.range (A * E).mulVecLin) =
          (E.conjTranspose * M * E).rank ∧
        ∀ g, (P g).comp (P g) = P g ∧
          (∀ v w : LinearMap.range (A * E).mulVecLin, finiteHilbertInner (v : n → ℂ) (P g w : n → ℂ) =
            finiteHilbertInner (P g v : n → ℂ) (w : n → ℂ)) ∧
          ∀ x : m → ℂ, (P g ⟨(A * E) *ᵥ x,
            LinearMap.mem_range_self (A * E).mulVecLin x⟩ : n → ℂ) = (A * D g) *ᵥ x := by
  classical
  open scoped MatrixOrder in
    obtain ⟨A, hA⟩ := CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hM.nonneg
  rw [Matrix.star_eq_conjTranspose] at hA
  have hgram : (A * E).conjTranspose * (A * E) = E.conjTranspose * M * E := by
    rw [gram_pullback, ← hA]
  have hsmall : LinearMap.range (A * E).mulVecLin = LinearMap.range A.mulVecLin := by
    apply flat_gram_range
    rw [← hA, hgram]
    exact hflat
  have hrange g : LinearMap.range (A * D g).mulVecLin ≤ LinearMap.range (A * E).mulVecLin := by
    rw [hsmall, Matrix.mulVecLin_mul]
    exact LinearMap.range_comp_le_range _ _
  have hrelation g : (A * D g).conjTranspose * (A * D g) = (A * D g).conjTranspose * (A * E) := by
    rw [gram_pullback, gram_pullback, ← hA, hrel g]
  refine ⟨A, hA.symm, (fun g => extractedOperator (A * E) (A * D g) (hrange g) (hrelation g)), ?_, ?_⟩
  · change (A * E).rank = _
    rw [← Matrix.rank_conjTranspose_mul_self, hgram]
  · intro g
    exact ⟨extractedOperator_idempotent _ _ _ _, extractedOperator_symmetric _ _ _ _,
      extractedOperator_apply _ _ _ _⟩

#print axioms extract_family_of_positive_flat

section WordMoments
open MUB.FiniteComplexMubFamily
variable {B ι : Type*} [Fintype B] [Fintype ι] [DecidableEq B] [DecidableEq ι]
abbrev One := Option (B × ι)
abbrev Two := Option ((B × ι) ⊕ ((B × ι) × (B × ι)))

def wordShift (g : B × ι) : One (B := B) (ι := ι) → Two (B := B) (ι := ι)
  | none => some (.inl g)
  | some h => some (.inr (g,h))

omit [Fintype B] [Fintype ι] [DecidableEq B] [DecidableEq ι] in
theorem wordShift_preserves (g : B × ι) (j : One (B := B) (ι := ι)) :
    degreeTwoWords (wordShift g j) = g :: degreeOneWords j := by
  cases j <;> rfl

def selector [DecidableEq n] (f : m → n) : Matrix n m ℂ :=
  fun i j => if i = f j then 1 else 0

omit [Fintype m] in
theorem selector_gram [DecidableEq n] (M : Matrix n n ℂ) (e d : m → n) :
    (selector d).conjTranspose * M * selector e = M.submatrix d e := by
  ext i j
  simp [selector, Matrix.mul_apply, Matrix.conjTranspose_apply, ite_mul, mul_ite]

theorem selector_column [DecidableEq n] [DecidableEq m]
    (A : Matrix n n ℂ) (f : m → n) (j : m) :
    (A * selector f) *ᵥ Pi.single j 1 = A *ᵥ Pi.single (f j) 1 := by
  rw [← Matrix.mulVec_mulVec]
  congr 1
  ext i
  simp [selector, Matrix.mulVec, Pi.single_apply]

noncomputable def wordMomentTwo (L : List (B × ι) → ℂ) :
    Matrix (Two (B := B) (ι := ι)) (Two (B := B) (ι := ι)) ℂ :=
  fun i j => L ((degreeTwoWords i).reverse ++ degreeTwoWords j)

noncomputable def wordMomentOne (L : List (B × ι) → ℂ) :
    Matrix (One (B := B) (ι := ι)) (One (B := B) (ι := ι)) ℂ :=
  fun i j => L ((degreeOneWords i).reverse ++ degreeOneWords j)

theorem wordMoment_principal (L : List (B × ι) → ℂ) :
    (selector (degreeOneInTwo (B := B) (ι := ι))).conjTranspose * wordMomentTwo L * selector (degreeOneInTwo (B := B) (ι := ι)) =
      wordMomentOne L := by
  rw [selector_gram]
  ext i j
  simp only [Matrix.submatrix_apply, wordMomentTwo, wordMomentOne, degreeOneInTwo_preserves_word]

def ContextualProjection (L : List (B × ι) → ℂ) (g : B × ι) : Prop :=
  ∀ i j : One (B := B) (ι := ι),
    L ((degreeOneWords i).reverse ++ g :: g :: degreeOneWords j) =
      L ((degreeOneWords i).reverse ++ g :: degreeOneWords j)

theorem wordMoment_projection_relation (L : List (B × ι) → ℂ) (g : B × ι)
    (hrel : ContextualProjection L g) :
    (selector (wordShift g)).conjTranspose * wordMomentTwo L * selector (wordShift g) =
      (selector (wordShift g)).conjTranspose * wordMomentTwo L * selector (degreeOneInTwo (B := B) (ι := ι)) := by
  rw [selector_gram, selector_gram]
  ext i j
  simpa only [Matrix.submatrix_apply, wordMomentTwo, wordShift_preserves,
    degreeOneInTwo_preserves_word, List.reverse_cons, List.append_assoc,
    List.singleton_append] using hrel i j

def wordState {H : Type*} [AddCommGroup H] [Module ℂ H]
    (P : (B × ι) → Module.End ℂ H) (ψ : H) : Two (B := B) (ι := ι) → H
  | none => ψ
  | some (.inl g) => P g ψ
  | some (.inr (g,h)) => P g (P h ψ)

noncomputable def extractionState
    (A : Matrix (Two (B := B) (ι := ι)) (Two (B := B) (ι := ι)) ℂ) :
    LinearMap.range (A * selector (degreeOneInTwo (B := B) (ι := ι))).mulVecLin :=
  ⟨(A * selector degreeOneInTwo) *ᵥ Pi.single none 1,
    LinearMap.mem_range_self (A * selector degreeOneInTwo).mulVecLin _⟩

theorem wordState_coordinates
    (A : Matrix (Two (B := B) (ι := ι)) (Two (B := B) (ι := ι)) ℂ)
    (P : (B × ι) → Module.End ℂ (LinearMap.range
      (A * selector (degreeOneInTwo (B := B) (ι := ι))).mulVecLin))
    (hP : ∀ g (x : One (B := B) (ι := ι) → ℂ),
      (P g ⟨(A * selector degreeOneInTwo) *ᵥ x,
        LinearMap.mem_range_self (A * selector degreeOneInTwo).mulVecLin x⟩ :
          Two (B := B) (ι := ι) → ℂ) = (A * selector (wordShift g)) *ᵥ x)
    (i : Two (B := B) (ι := ι)) :
    (wordState P (extractionState A) i).val = A *ᵥ Pi.single i 1 := by
  let E : Matrix (Two (B := B) (ι := ι)) (One (B := B) (ι := ι)) ℂ := selector degreeOneInTwo
  let D (g : B × ι) : Matrix (Two (B := B) (ι := ι)) (One (B := B) (ι := ι)) ℂ := selector (wordShift g)
  let ψ := extractionState A
  have hsingle (g : B × ι) : P g ψ =
      ⟨(A * E) *ᵥ Pi.single (some g) 1, LinearMap.mem_range_self (A * E).mulVecLin _⟩ := by
    apply Subtype.ext
    change (P g ⟨(A * E) *ᵥ Pi.single none 1, _⟩ : Two (B := B) (ι := ι) → ℂ) =
      (A * E) *ᵥ Pi.single (some g) 1
    calc
      _ = (A * D g) *ᵥ Pi.single none 1 := hP g _
      _ = A *ᵥ Pi.single (wordShift g none) 1 := selector_column A (wordShift g) none
      _ = (A * E) *ᵥ Pi.single (some g) 1 :=
        (selector_column A (degreeOneInTwo (B := B) (ι := ι)) (some g)).symm
  have hword (i : Two (B := B) (ι := ι)) :
      (wordState P ψ i).val = A *ᵥ Pi.single i 1 := by
    cases i with
    | none =>
      change (A * E) *ᵥ Pi.single none 1 = _
      exact selector_column A degreeOneInTwo none
    | some i =>
      cases i with
      | inl g =>
        change (P g ψ : Two (B := B) (ι := ι) → ℂ) = _
        rw [hsingle]
        exact selector_column A degreeOneInTwo (some g)
      | inr gh =>
        rcases gh with ⟨g,h⟩
        change (P g (P h ψ) : Two (B := B) (ι := ι) → ℂ) = _
        rw [hsingle, hP g]
        exact selector_column A (wordShift g) (some h)
  exact hword i

theorem wordState_representation (L : List (B × ι) → ℂ)
    (A : Matrix (Two (B := B) (ι := ι)) (Two (B := B) (ι := ι)) ℂ)
    (hA : A.conjTranspose * A = wordMomentTwo L)
    (P : (B × ι) → Module.End ℂ (LinearMap.range
      (A * selector (degreeOneInTwo (B := B) (ι := ι))).mulVecLin))
    (hP : ∀ g (x : One (B := B) (ι := ι) → ℂ),
      (P g ⟨(A * selector degreeOneInTwo) *ᵥ x,
        LinearMap.mem_range_self (A * selector degreeOneInTwo).mulVecLin x⟩ :
          Two (B := B) (ι := ι) → ℂ) = (A * selector (wordShift g)) *ᵥ x)
    (i j : Two (B := B) (ι := ι)) :
    finiteHilbertInner (wordState P (extractionState A) i).val
      (wordState P (extractionState A) j).val = wordMomentTwo L i j := by
  rw [wordState_coordinates A P hP, wordState_coordinates A P hP, gram_pairing_single, hA]

theorem extract_word_projectors (L : List (B × ι) → ℂ)
    (hnorm : L [] = 1) (hM : (wordMomentTwo L).PosSemidef)
    (hflat : (wordMomentTwo L).rank = (wordMomentOne L).rank)
    (hrel : ∀ g : B × ι, ContextualProjection L g) :
    ∃ A : Matrix (Two (B := B) (ι := ι)) (Two (B := B) (ι := ι)) ℂ,
      A.conjTranspose * A = wordMomentTwo L ∧
      ∃ P : (B × ι) → Module.End ℂ (LinearMap.range
          (A * selector (degreeOneInTwo (B := B) (ι := ι))).mulVecLin),
        ∃ ψ : LinearMap.range (A * selector (degreeOneInTwo (B := B) (ι := ι))).mulVecLin,
          finiteHilbertInner (ψ : Two (B := B) (ι := ι) → ℂ) ψ = 1 ∧
          Module.finrank ℂ (LinearMap.range
            (A * selector (degreeOneInTwo (B := B) (ι := ι))).mulVecLin) = (wordMomentOne L).rank ∧
          (∀ g, (P g).comp (P g) = P g ∧
            ∀ v w : LinearMap.range (A * selector (degreeOneInTwo (B := B) (ι := ι))).mulVecLin,
              finiteHilbertInner (v : Two (B := B) (ι := ι) → ℂ) (P g w) =
                finiteHilbertInner (P g v : Two (B := B) (ι := ι) → ℂ) w) ∧
          ∀ i j : Two (B := B) (ι := ι),
            finiteHilbertInner (wordState P ψ i).val
              (wordState P ψ j).val = wordMomentTwo L i j := by
  let E : Matrix (Two (B := B) (ι := ι)) (One (B := B) (ι := ι)) ℂ := selector degreeOneInTwo
  let D (g : B × ι) : Matrix (Two (B := B) (ι := ι)) (One (B := B) (ι := ι)) ℂ := selector (wordShift g)
  have hflat' : (wordMomentTwo L).rank = (E.conjTranspose * wordMomentTwo L * E).rank := by
    rw [show E.conjTranspose * wordMomentTwo L * E = wordMomentOne L from wordMoment_principal L]
    exact hflat
  obtain ⟨A, hA, P, hdim, hP⟩ := extract_family_of_positive_flat
    (wordMomentTwo L) E D hM hflat' (fun g => wordMoment_projection_relation L g (hrel g))
  let ψ := extractionState A
  have hrepr i j :
      finiteHilbertInner (wordState P ψ i).val
        (wordState P ψ j).val = wordMomentTwo L i j := by
    exact wordState_representation L A hA P (fun g => (hP g).2.2) i j
  refine ⟨A, hA, P, ψ, ?_, ?_, ?_, hrepr⟩
  · have h := hrepr none none
    simpa only [wordState, wordMomentTwo, degreeTwoWords, List.reverse_nil, List.nil_append, hnorm] using h
  · simpa only [show E.conjTranspose * wordMomentTwo L * E = wordMomentOne L from wordMoment_principal L] using hdim
  · intro g
    exact ⟨(hP g).1, (hP g).2.1⟩

theorem concrete_contextual_projection (family : MUB.FiniteComplexMubFamily ι B ι)
    (ψ : ι → ℂ) (g : B × ι) : ContextualProjection (family.complexWordMoment ψ) g := by
  intro i j
  have hid : family.concreteProjector g.1 g.2 * family.concreteProjector g.1 g.2 =
      family.concreteProjector g.1 g.2 := by
    simpa using family.concreteProjector_same_basis_mul g.1 g.2 g.2
  simp only [MUB.FiniteComplexMubFamily.complexWordMoment,
    MUB.FiniteComplexMubFamily.concreteWordOperator_append,
    MUB.FiniteComplexMubFamily.concreteWordOperator]
  rw [← Matrix.mul_assoc (family.concreteProjector g.1 g.2)
    (family.concreteProjector g.1 g.2), hid]

theorem concrete_moment_extraction_inputs (family : MUB.FiniteComplexMubFamily ι B ι)
    (b₀ b₁ : B) (l₀ : ι) (hne : b₁ ≠ b₀) :
    let L := family.complexWordMoment (family.vector b₀ l₀)
    L [] = 1 ∧ (wordMomentTwo L).PosSemidef ∧
      (wordMomentTwo L).rank = (wordMomentOne L).rank ∧
      ∀ g : B × ι, ContextualProjection L g := by
  exact ⟨family.complexWordMoment_empty_normalized b₀ l₀,
    family.complexMomentMatrix_posSemidef _ _,
    family.concrete_mub_moment_flatness b₀ b₁ l₀ hne,
    fun g => concrete_contextual_projection family _ g⟩

#print axioms concrete_contextual_projection
#print axioms concrete_moment_extraction_inputs

#print axioms wordState_coordinates
#print axioms wordState_representation
#print axioms extract_word_projectors

#print axioms wordMoment_projection_relation
end WordMoments
end MUB.FlatGramExtraction
