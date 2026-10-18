import FlatMomentProjectorExtraction

/-!
# Complete orthogonal basis actions from positive flat word moments

AuthorityEffect: None.

The input is normalized complex word values with a positive semidefinite
complete degree-two matrix, actual equality with the lower matrix rank, and
explicit same-basis product and completeness equations in every lower-word
context. Operators and a state are constructed, rather than supplied.

The common finite space has dimension equal to the lower moment rank. Its
symmetric linear actions satisfy the same-basis product rule and each basis
sums to the identity. A normalized state represents every degree-two matrix
entry. Concrete moments from a supplied finite MUB family satisfy all input
relations. The normalized zero-action word assignment fails completeness.

This does not infer dimension six, nonzero rank-one ranges for every outcome,
cross-basis MU equations, a full star-algebra extension, or transport arbitrary
word data to the coordinate-polynomial variety. Positivity and flatness alone
do not supply the contextual product and completeness equations.
-/

namespace MUB.FlatGramExtraction
open scoped Matrix ComplexOrder
variable {n m J : Type*} [Fintype n] [Fintype m] [Fintype J]

theorem images_orthogonal (B C D : Matrix n m ℂ)
    (P Q : Module.End ℂ (LinearMap.range B.mulVecLin))
    (hrel : C.conjTranspose * C = C.conjTranspose * B)
    (hcross : C.conjTranspose * D = 0)
    (hP : ∀ x : m → ℂ, (P ⟨B *ᵥ x, LinearMap.mem_range_self B.mulVecLin x⟩ : n → ℂ) = C *ᵥ x)
    (hQ : ∀ x : m → ℂ, (Q ⟨B *ᵥ x, LinearMap.mem_range_self B.mulVecLin x⟩ : n → ℂ) = D *ᵥ x) :
    P.comp Q = 0 := by
  apply LinearMap.ext
  intro v
  obtain ⟨x, hx⟩ := v.property
  have hv : v = ⟨B *ᵥ x, LinearMap.mem_range_self B.mulVecLin x⟩ := Subtype.ext hx.symm
  obtain ⟨y, hy⟩ := (Q v).property
  have hq : Q v = ⟨B *ᵥ y, LinearMap.mem_range_self B.mulVecLin y⟩ := Subtype.ext hy.symm
  have hby : B *ᵥ y = D *ᵥ x := by
    calc
      _ = (Q v).val := hy
      _ = _ := by rw [hv]; exact hQ x
  apply Subtype.ext
  change (P (Q v)).val = 0
  rw [hq, hP]
  apply range_adjoint_zero B
  · rw [← hP y]
    exact (P ⟨B *ᵥ y, LinearMap.mem_range_self B.mulVecLin y⟩).property
  · rw [Matrix.mulVec_mulVec, shift_cross B C hrel,
      ← Matrix.mulVec_mulVec, hby, Matrix.mulVec_mulVec, hcross, Matrix.zero_mulVec]

theorem images_complete (B : Matrix n m ℂ) (C : J → Matrix n m ℂ)
    (P : J → Module.End ℂ (LinearMap.range B.mulVecLin))
    (hsum : B.conjTranspose * (∑ j, C j) = B.conjTranspose * B)
    (hP : ∀ j (x : m → ℂ), (P j ⟨B *ᵥ x, LinearMap.mem_range_self B.mulVecLin x⟩ : n → ℂ) = C j *ᵥ x) :
    ∑ j, P j = LinearMap.id := by
  have hs (x : m → ℂ) : (∑ j, C j *ᵥ x) = B *ᵥ x := by
    apply sub_eq_zero.mp
    apply range_adjoint_zero B
    · apply (LinearMap.range B.mulVecLin).sub_mem
      · apply Submodule.sum_mem
        intro j _
        rw [← hP j x]
        exact (P j ⟨B *ᵥ x, LinearMap.mem_range_self B.mulVecLin x⟩).property
      · exact LinearMap.mem_range_self B.mulVecLin x
    · rw [Matrix.mulVec_sub, ← Matrix.sum_mulVec, Matrix.mulVec_mulVec,
        Matrix.mulVec_mulVec, hsum, sub_self]
  apply LinearMap.ext
  intro v
  obtain ⟨x, hx⟩ := v.property
  have hv : v = ⟨B *ᵥ x, LinearMap.mem_range_self B.mulVecLin x⟩ := Subtype.ext hx.symm
  apply Subtype.ext
  change ((∑ j, P j) v).val = v.val
  rw [LinearMap.sum_apply, Submodule.coe_sum, hv]
  simp only [hP]
  exact hs x

section WordMoments
open MUB.FiniteComplexMubFamily
variable {B ι : Type*} [Fintype B] [Fintype ι] [DecidableEq B] [DecidableEq ι]

def ContextualSameBasis (L : List (B × ι) → ℂ) (b : B) : Prop :=
  ∀ (l k : ι) (i j : One (B := B) (ι := ι)),
    L ((degreeOneWords i).reverse ++ (b,l) :: (b,k) :: degreeOneWords j) =
      if l = k then L ((degreeOneWords i).reverse ++ (b,l) :: degreeOneWords j) else 0

def ContextualCompleteness (L : List (B × ι) → ℂ) (b : B) : Prop :=
  ∀ i j : One (B := B) (ι := ι),
    (∑ l : ι, L ((degreeOneWords i).reverse ++ (b,l) :: degreeOneWords j)) =
      L ((degreeOneWords i).reverse ++ degreeOneWords j)

omit [Fintype B] [Fintype ι] [DecidableEq B] in
theorem contextual_same_basis_projection (L : List (B × ι) → ℂ)
    (hrel : ∀ b, ContextualSameBasis L b) (g : B × ι) : ContextualProjection L g := by
  intro i j
  simpa using hrel g.1 g.2 g.2 i j

theorem wordMoment_same_basis_cross (L : List (B × ι) → ℂ)
    (b : B) (l k : ι) (hne : l ≠ k) (hrel : ContextualSameBasis L b) :
    (selector (wordShift (b,l))).conjTranspose * wordMomentTwo L * selector (wordShift (b,k)) = 0 := by
  rw [selector_gram]
  ext i j
  simpa only [Matrix.submatrix_apply, wordMomentTwo, wordShift_preserves,
    List.reverse_cons, List.append_assoc, List.singleton_append, hne, if_false,
    Matrix.zero_apply] using hrel l k i j

theorem wordMoment_complete (L : List (B × ι) → ℂ) (b : B)
    (hrel : ContextualCompleteness L b) :
    (selector (degreeOneInTwo (B := B) (ι := ι))).conjTranspose * wordMomentTwo L *
      (∑ l : ι, selector (wordShift (b,l))) =
      (selector (degreeOneInTwo (B := B) (ι := ι))).conjTranspose * wordMomentTwo L *
        selector (degreeOneInTwo (B := B) (ι := ι)) := by
  rw [Matrix.mul_sum, wordMoment_principal]
  simp_rw [selector_gram]
  ext i j
  simpa only [Matrix.sum_apply, Matrix.submatrix_apply, wordMomentTwo,
    wordMomentOne, degreeOneInTwo_preserves_word, wordShift_preserves] using hrel i j

theorem extract_word_basis (L : List (B × ι) → ℂ)
    (hnorm : L [] = 1) (hM : (wordMomentTwo L).PosSemidef)
    (hflat : (wordMomentTwo L).rank = (wordMomentOne L).rank)
    (hprod : ∀ b, ContextualSameBasis L b)
    (hsum : ∀ b, ContextualCompleteness L b) :
    ∃ A : Matrix (Two (B := B) (ι := ι)) (Two (B := B) (ι := ι)) ℂ,
      A.conjTranspose * A = wordMomentTwo L ∧
      ∃ P : (B × ι) → Module.End ℂ (LinearMap.range
          (A * selector (degreeOneInTwo (B := B) (ι := ι))).mulVecLin),
        ∃ ψ : LinearMap.range (A * selector (degreeOneInTwo (B := B) (ι := ι))).mulVecLin,
          finiteHilbertInner (ψ : Two (B := B) (ι := ι) → ℂ) ψ = 1 ∧
          Module.finrank ℂ (LinearMap.range
            (A * selector (degreeOneInTwo (B := B) (ι := ι))).mulVecLin) = (wordMomentOne L).rank ∧
          (∀ b (l k : ι), (P (b,l)).comp (P (b,k)) = if l = k then P (b,l) else 0) ∧
          (∀ b, ∑ l : ι, P (b,l) = LinearMap.id) ∧
          (∀ g (v w : LinearMap.range (A * selector (degreeOneInTwo (B := B) (ι := ι))).mulVecLin),
            finiteHilbertInner (v : Two (B := B) (ι := ι) → ℂ) (P g w) =
              finiteHilbertInner (P g v : Two (B := B) (ι := ι) → ℂ) w) ∧
          ∀ i j : Two (B := B) (ι := ι),
            finiteHilbertInner (wordState P ψ i).val (wordState P ψ j).val = wordMomentTwo L i j := by
  let E : Matrix (Two (B := B) (ι := ι)) (One (B := B) (ι := ι)) ℂ := selector degreeOneInTwo
  let D (g : B × ι) : Matrix (Two (B := B) (ι := ι)) (One (B := B) (ι := ι)) ℂ := selector (wordShift g)
  have hflat' : (wordMomentTwo L).rank = (E.conjTranspose * wordMomentTwo L * E).rank := by
    rw [show E.conjTranspose * wordMomentTwo L * E = wordMomentOne L from wordMoment_principal L]
    exact hflat
  obtain ⟨A, hA, P, hdim, hP⟩ := extract_family_of_positive_flat
    (wordMomentTwo L) E D hM hflat'
    (fun g => wordMoment_projection_relation L g (contextual_same_basis_projection L hprod g))
  have hcross (b : B) (l k : ι) (hne : l ≠ k) :
      (A * D (b,l)).conjTranspose * (A * D (b,k)) = 0 := by
    rw [gram_pullback, hA]
    exact wordMoment_same_basis_cross L b l k hne (hprod b)
  have hrel (g : B × ι) :
      (A * D g).conjTranspose * (A * D g) = (A * D g).conjTranspose * (A * E) := by
    rw [gram_pullback, gram_pullback, hA]
    exact wordMoment_projection_relation L g (contextual_same_basis_projection L hprod g)
  have horth (b : B) (l k : ι) (hne : l ≠ k) : (P (b,l)).comp (P (b,k)) = 0 :=
    images_orthogonal (A * E) (A * D (b,l)) (A * D (b,k))
      (P (b,l)) (P (b,k)) (hrel (b,l)) (hcross b l k hne)
      (hP (b,l)).2.2 (hP (b,k)).2.2
  have hcomplete (b : B) : ∑ l : ι, P (b,l) = LinearMap.id := by
    apply images_complete (A * E) (fun l => A * D (b,l)) (fun l => P (b,l))
    · calc
        (A * E).conjTranspose * (∑ l : ι, A * D (b,l)) =
            (A * E).conjTranspose * (A * ∑ l : ι, D (b,l)) := by
              congr 1
              rw [Matrix.mul_sum]
        _ = E.conjTranspose * (A.conjTranspose * A) * (∑ l : ι, D (b,l)) :=
          gram_pullback A (∑ l : ι, D (b,l)) E
        _ = E.conjTranspose * wordMomentTwo L * (∑ l : ι, D (b,l)) := by rw [hA]
        _ = E.conjTranspose * wordMomentTwo L * E := wordMoment_complete L b (hsum b)
        _ = (A * E).conjTranspose * (A * E) := by rw [gram_pullback, hA]
    · exact fun l => (hP (b,l)).2.2
  let ψ := extractionState A
  have hrepr i j : finiteHilbertInner (wordState P ψ i).val (wordState P ψ j).val =
      wordMomentTwo L i j := wordState_representation L A hA P (fun g => (hP g).2.2) i j
  refine ⟨A, hA, P, ψ, ?_, ?_, ?_, hcomplete, ?_, hrepr⟩
  · have h := hrepr none none
    simpa only [wordState, wordMomentTwo, degreeTwoWords, List.reverse_nil, List.nil_append, hnorm] using h
  · simpa only [show E.conjTranspose * wordMomentTwo L * E = wordMomentOne L from wordMoment_principal L] using hdim
  · intro b l k
    split_ifs with h
    · subst k
      exact (hP (b,l)).1
    · exact horth b l k h
  · exact fun g => (hP g).2.1

theorem concrete_contextual_same_basis (family : MUB.FiniteComplexMubFamily ι B ι)
    (ψ : ι → ℂ) (b : B) : ContextualSameBasis (family.complexWordMoment ψ) b := by
  intro l k i j
  simp only [complexWordMoment, concreteWordOperator_append, concreteWordOperator]
  rw [← Matrix.mul_assoc (family.concreteProjector b l) (family.concreteProjector b k),
    family.concreteProjector_same_basis_mul]
  split_ifs <;> simp [finiteHilbertInner]

theorem concrete_contextual_completeness (family : MUB.FiniteComplexMubFamily ι B ι)
    (ψ : ι → ℂ) (b : B) : ContextualCompleteness (family.complexWordMoment ψ) b := by
  intro i j
  have hwords :
      (∑ l : ι, family.concreteWordOperator ((degreeOneWords i).reverse ++ (b,l) :: degreeOneWords j)) =
        family.concreteWordOperator ((degreeOneWords i).reverse ++ degreeOneWords j) := by
    simp only [concreteWordOperator_append, concreteWordOperator]
    simp_rw [← Matrix.mul_assoc]
    rw [← Matrix.sum_mul, ← Matrix.mul_sum, family.concreteProjector_complete, Matrix.mul_one]
  have h := congrArg (fun N : Matrix ι ι ℂ => finiteHilbertInner ψ (N *ᵥ ψ)) hwords
  simp only [Matrix.sum_mulVec, finiteHilbertInner, Finset.sum_apply,
    Finset.mul_sum] at h
  rw [Finset.sum_comm] at h
  exact h

theorem concrete_moment_basis_inputs (family : MUB.FiniteComplexMubFamily ι B ι)
    (b₀ b₁ : B) (l₀ : ι) (hne : b₁ ≠ b₀) :
    let L := family.complexWordMoment (family.vector b₀ l₀)
    L [] = 1 ∧ (wordMomentTwo L).PosSemidef ∧
      (wordMomentTwo L).rank = (wordMomentOne L).rank ∧
      (∀ b, ContextualSameBasis L b) ∧ ∀ b, ContextualCompleteness L b := by
  exact ⟨family.complexWordMoment_empty_normalized b₀ l₀,
    family.complexMomentMatrix_posSemidef _ _,
    family.concrete_mub_moment_flatness b₀ b₁ l₀ hne,
    fun b => concrete_contextual_same_basis family _ b,
    fun b => concrete_contextual_completeness family _ b⟩

omit [Fintype B] [DecidableEq B] [DecidableEq ι] in
theorem zero_action_moments_reject_completeness (b : B) :
    ¬ ContextualCompleteness (fun w : List (B × ι) => if w = [] then (1 : ℂ) else 0) b := by
  intro h
  have hz := h none none
  simp [degreeOneWords] at hz

#print axioms zero_action_moments_reject_completeness
#print axioms concrete_contextual_completeness
#print axioms concrete_moment_basis_inputs
#print axioms extract_word_basis
#print axioms concrete_contextual_same_basis
#print axioms images_orthogonal
#print axioms images_complete
#print axioms wordMoment_same_basis_cross
#print axioms wordMoment_complete
end WordMoments
end MUB.FlatGramExtraction
