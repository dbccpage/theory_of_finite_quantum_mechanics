import Mathlib.Analysis.InnerProductSpace.JointEigenspace
import Mathlib.Analysis.Matrix.Order
import Mathlib.LinearAlgebra.Isomorphisms
import Mathlib.Algebra.MvPolynomial.Eval

/-!
# Real commuting coordinate extraction from positive flat moments

AuthorityEffect: None.

For finitely many real variables, the matrices use the complete constant/linear
list and the complete constant/linear/ordered-quadratic list. Repeated quadratic
monomials are retained; flatness compares the actual matrix ranks. A real linear
functional supplies the moments. Only products of total degree at most four are
used. Positivity, normalization and rank equality are explicit hypotheses.

A Gram factor and flatness give well-defined symmetric multiplication operators
on the degree-one column space. Commutativity follows from the polynomial
product identities, rather than from a supplied operator family. Joint real
eigenspaces span this finite space, and a joint eigenvector with nonzero state
overlap supplies one common real point. Every quadratic polynomial whose square
has zero moment vanishes at that point. Finite relation compatibility suffices
for square-annihilation when the relation lies in the quadratic span.

This is a finite commutative point-extraction theorem. It does not establish
flatness for arbitrary positive data, variety emptiness, or a noncommutative
projector representation with prescribed rank or dimension.
-/

namespace MUB.CommutativeFlatMoments
open scoped Matrix
variable {n m : Type*} [Fintype n] [Fintype m]

noncomputable def columnMap (B : Matrix n m ℝ) : (m → ℝ) →ₗ[ℝ] EuclideanSpace ℝ n :=
  (WithLp.linearEquiv 2 ℝ (n → ℝ)).symm.toLinearMap.comp B.mulVecLin

noncomputable abbrev ColumnSpace (B : Matrix n m ℝ) := LinearMap.range (columnMap B)

theorem range_transpose_zero (B : Matrix n m ℝ) (v : n → ℝ)
    (hv : v ∈ LinearMap.range B.mulVecLin) (hz : B.conjTranspose *ᵥ v = 0) : v = 0 := by
  obtain ⟨x, rfl⟩ := hv
  exact (Matrix.conjTranspose_mul_self_mulVec_eq_zero B x).mp
    (by simpa only [← Matrix.mulVec_mulVec, Matrix.mulVecLin_apply] using hz)

theorem symmetric_shift_ker (B C : Matrix n m ℝ)
    (hrange : LinearMap.range C.mulVecLin ≤ LinearMap.range B.mulVecLin)
    (hsym : B.conjTranspose * C = C.conjTranspose * B) :
    LinearMap.ker B.mulVecLin ≤ LinearMap.ker C.mulVecLin := by
  intro x hx
  change B *ᵥ x = 0 at hx
  change C *ᵥ x = 0
  apply range_transpose_zero B
  · exact hrange (LinearMap.mem_range_self C.mulVecLin x)
  · rw [Matrix.mulVec_mulVec, hsym, ← Matrix.mulVec_mulVec, hx, Matrix.mulVec_zero]

omit [Fintype n] in
theorem columnMap_range_le (B C : Matrix n m ℝ)
    (hrange : LinearMap.range C.mulVecLin ≤ LinearMap.range B.mulVecLin) :
    LinearMap.range (columnMap C) ≤ LinearMap.range (columnMap B) := by
  rintro v ⟨x, rfl⟩
  obtain ⟨y, hy⟩ := hrange (LinearMap.mem_range_self C.mulVecLin x)
  refine ⟨y, ?_⟩
  change WithLp.toLp 2 (B *ᵥ y) = WithLp.toLp 2 (C *ᵥ x)
  exact congrArg (WithLp.toLp 2) hy

noncomputable def multiplicationOperator (B C : Matrix n m ℝ)
    (hrange : LinearMap.range C.mulVecLin ≤ LinearMap.range B.mulVecLin)
    (hsym : B.conjTranspose * C = C.conjTranspose * B) : Module.End ℝ (ColumnSpace B) :=
  let c := LinearMap.codRestrict (ColumnSpace B) (columnMap C)
    (fun x => columnMap_range_le B C hrange (LinearMap.mem_range_self (columnMap C) x))
  let hk : LinearMap.ker (columnMap B) ≤ LinearMap.ker c := by
    intro x hx
    apply Subtype.ext
    change WithLp.toLp 2 (C *ᵥ x) = 0
    have hx' : B *ᵥ x = 0 := congrArg WithLp.ofLp hx
    have hc : C *ᵥ x = 0 := symmetric_shift_ker B C hrange hsym hx'
    simpa using congrArg (WithLp.toLp 2) hc
  ((LinearMap.ker (columnMap B)).liftQ c hk).comp
    (columnMap B).quotKerEquivRange.symm.toLinearMap

theorem multiplicationOperator_apply (B C : Matrix n m ℝ)
    (hrange : LinearMap.range C.mulVecLin ≤ LinearMap.range B.mulVecLin)
    (hsym : B.conjTranspose * C = C.conjTranspose * B) (x : m → ℝ) :
    (multiplicationOperator B C hrange hsym
      ⟨columnMap B x, LinearMap.mem_range_self (columnMap B) x⟩).val = columnMap C x := by
  dsimp only [multiplicationOperator, LinearMap.comp_apply, LinearEquiv.coe_coe]
  rw [show (columnMap B).quotKerEquivRange.symm
      ⟨columnMap B x, LinearMap.mem_range_self (columnMap B) x⟩ = (columnMap B).ker.mkQ x from
    (columnMap B).quotKerEquivRange_symm_apply_image x _]
  rfl

theorem gram_pairing (B C : Matrix n m ℝ) (x y : m → ℝ) :
    inner ℝ (columnMap B x) (columnMap C y) = x ⬝ᵥ ((B.conjTranspose * C) *ᵥ y) := by
  change inner ℝ (WithLp.toLp 2 (B *ᵥ x)) (WithLp.toLp 2 (C *ᵥ y)) = _
  rw [EuclideanSpace.inner_toLp_toLp, dotProduct_comm]
  simp only [star_trivial, Matrix.conjTranspose_eq_transpose_of_trivial, Matrix.dotProduct_mulVec, Matrix.vecMul_mulVec]

theorem multiplicationOperator_symmetric (B C : Matrix n m ℝ)
    (hrange : LinearMap.range C.mulVecLin ≤ LinearMap.range B.mulVecLin)
    (hsym : B.conjTranspose * C = C.conjTranspose * B) :
    (multiplicationOperator B C hrange hsym).IsSymmetric := by
  intro v w
  obtain ⟨x, hx⟩ := v.property
  obtain ⟨y, hy⟩ := w.property
  have hv : v = ⟨columnMap B x, LinearMap.mem_range_self (columnMap B) x⟩ := Subtype.ext hx.symm
  have hw : w = ⟨columnMap B y, LinearMap.mem_range_self (columnMap B) y⟩ := Subtype.ext hy.symm
  change inner ℝ (multiplicationOperator B C hrange hsym v).val w.val =
    inner ℝ v.val (multiplicationOperator B C hrange hsym w).val
  rw [hv, hw, multiplicationOperator_apply, multiplicationOperator_apply,
    gram_pairing, gram_pairing, hsym]

theorem operators_commute (B C D : Matrix n m ℝ)
    (P Q : Module.End ℝ (ColumnSpace B)) (hP : P.IsSymmetric) (hQ : Q.IsSymmetric)
    (himageP : ∀ x, (P ⟨columnMap B x, LinearMap.mem_range_self (columnMap B) x⟩).val = columnMap C x)
    (himageQ : ∀ x, (Q ⟨columnMap B x, LinearMap.mem_range_self (columnMap B) x⟩).val = columnMap D x)
    (hcross : C.conjTranspose * D = D.conjTranspose * C) : Commute P Q := by
  apply LinearMap.ext
  intro w
  apply ext_inner_left ℝ
  intro v
  change inner ℝ v (P (Q w)) = inner ℝ v (Q (P w))
  calc
    inner ℝ v (P (Q w)) = inner ℝ (P v) (Q w) := (hP v (Q w)).symm
    _ = inner ℝ (Q v) (P w) := by
      obtain ⟨x, hx⟩ := v.property
      obtain ⟨y, hy⟩ := w.property
      have hv : v = ⟨columnMap B x, LinearMap.mem_range_self (columnMap B) x⟩ := Subtype.ext hx.symm
      have hw : w = ⟨columnMap B y, LinearMap.mem_range_self (columnMap B) y⟩ := Subtype.ext hy.symm
      change inner ℝ (P v).val (Q w).val = inner ℝ (Q v).val (P w).val
      rw [hv, hw, himageP, himageQ, himageQ, himageP, gram_pairing, gram_pairing, hcross]
    _ = inner ℝ v (Q (P w)) := hQ v (P w)

theorem flat_gram_range {r : Type*} [Fintype r]
    (A : Matrix r n ℝ) (E : Matrix n m ℝ)
    (hflat : (A.conjTranspose * A).rank = ((A * E).conjTranspose * (A * E)).rank) :
    LinearMap.range (A * E).mulVecLin = LinearMap.range A.mulVecLin := by
  apply Submodule.eq_of_le_of_finrank_eq
  · rw [Matrix.mulVecLin_mul]
    exact LinearMap.range_comp_le_range _ _
  · change (A * E).rank = A.rank
    simpa only [Matrix.rank_conjTranspose_mul_self] using hflat.symm

omit [Fintype m] in
theorem gram_pullback {r : Type*} [Fintype r]
    (A : Matrix r n ℝ) (E D : Matrix n m ℝ) :
    (A * D).conjTranspose * (A * E) = D.conjTranspose * (A.conjTranspose * A) * E := by
  simp only [Matrix.conjTranspose_mul, Matrix.mul_assoc]

theorem extract_commuting_family {G : Type*} [DecidableEq n]
    (M : Matrix n n ℝ) (E : Matrix n m ℝ) (D : G → Matrix n m ℝ)
    (hM : M.PosSemidef) (hflat : M.rank = (E.conjTranspose * M * E).rank)
    (hsym : ∀ g, E.conjTranspose * M * D g = (D g).conjTranspose * M * E)
    (hcross : ∀ g h, (D g).conjTranspose * M * D h = (D h).conjTranspose * M * D g) :
    ∃ A : Matrix n n ℝ, A.conjTranspose * A = M ∧
      ∃ T : G → Module.End ℝ (ColumnSpace (A * E)),
        (∀ g, (T g).IsSymmetric) ∧ (∀ g h, Commute (T g) (T h)) ∧
        Module.finrank ℝ (ColumnSpace (A * E)) = (E.conjTranspose * M * E).rank ∧
        ∀ g (x : m → ℝ), (T g ⟨columnMap (A * E) x,
          LinearMap.mem_range_self (columnMap (A * E)) x⟩).val = columnMap (A * D g) x := by
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
  have hrelation g : (A * E).conjTranspose * (A * D g) = (A * D g).conjTranspose * (A * E) := by
    rw [gram_pullback, gram_pullback, ← hA]
    exact hsym g
  let T g := multiplicationOperator (A * E) (A * D g) (hrange g) (hrelation g)
  have hTsym g : (T g).IsSymmetric := multiplicationOperator_symmetric _ _ _ _
  refine ⟨A, hA.symm, T, hTsym, ?_, ?_, fun g => multiplicationOperator_apply _ _ _ _⟩
  · intro g h
    apply operators_commute (A * E) (A * D g) (A * D h) (T g) (T h) (hTsym g) (hTsym h)
      (multiplicationOperator_apply _ _ _ _) (multiplicationOperator_apply _ _ _ _)
    rw [gram_pullback, gram_pullback, ← hA]
    exact hcross g h
  · have heq : Module.finrank ℝ (ColumnSpace (A * E)) = (A * E).rank := by
      unfold ColumnSpace columnMap
      rw [LinearMap.range_comp, LinearEquiv.finrank_map_eq]
      rfl
    rw [heq, ← Matrix.rank_conjTranspose_mul_self, hgram]

section JointPoint
variable {H G : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H] [FiniteDimensional ℝ H]

theorem exists_visible_joint_eigenvector (T : G → Module.End ℝ H)
    (hsym : ∀ g, (T g).IsSymmetric) (hcomm : ∀ g h, Commute (T g) (T h))
    (ψ : H) (hne : ψ ≠ 0) :
    ∃ χ : G → ℝ, ∃ v : H, (∀ g, T g v = χ g • v) ∧ inner ℝ ψ v ≠ 0 := by
  classical
  have htop := LinearMap.IsSymmetric.iSup_iInf_eq_top_of_commute hsym (fun g h _ => hcomm g h)
  by_contra h
  push Not at h
  let ell : H →ₗ[ℝ] ℝ := (innerSL ℝ ψ).toLinearMap
  have hle : (⨆ χ : G → ℝ, ⨅ g, Module.End.eigenspace (T g) (χ g)) ≤ LinearMap.ker ell := by
    apply iSup_le
    intro χ v hv
    change inner ℝ ψ v = 0
    apply h χ v
    intro g
    exact Module.End.mem_eigenspace_iff.mp ((Submodule.mem_iInf _).mp hv g)
  have hz : inner ℝ ψ ψ = 0 := hle (by rw [htop]; trivial)
  exact hne (inner_self_eq_zero.mp hz)
end JointPoint

section PolynomialMoments
open MvPolynomial
variable {σ : Type*} [Fintype σ] [DecidableEq σ]
abbrev One := Option σ
abbrev Two := Option (σ ⊕ (σ × σ))

noncomputable def onePolynomial : One (σ := σ) → MvPolynomial σ ℝ
  | none => 1
  | some g => X g

noncomputable def twoPolynomial : Two (σ := σ) → MvPolynomial σ ℝ
  | none => 1
  | some (.inl g) => X g
  | some (.inr (g,h)) => X g * X h

def embedding : One (σ := σ) → Two (σ := σ)
  | none => none
  | some g => some (.inl g)

def shift (g : σ) : One (σ := σ) → Two (σ := σ)
  | none => some (.inl g)
  | some h => some (.inr (g,h))

omit [Fintype σ] [DecidableEq σ] in
theorem embedding_polynomial (i : One (σ := σ)) : twoPolynomial (embedding i) = onePolynomial i := by
  cases i <;> rfl

omit [Fintype σ] [DecidableEq σ] in
theorem shift_polynomial (g : σ) (i : One (σ := σ)) :
    twoPolynomial (shift g i) = X g * onePolynomial i := by
  cases i <;> simp [shift, onePolynomial, twoPolynomial]

def selector [DecidableEq n] (f : m → n) : Matrix n m ℝ :=
  fun i j => if i = f j then 1 else 0

omit [Fintype m] in
theorem selector_gram [DecidableEq n] (M : Matrix n n ℝ) (e d : m → n) :
    (selector d).conjTranspose * M * selector e = M.submatrix d e := by
  ext i j
  simp [selector, Matrix.mul_apply, ite_mul, mul_ite]

theorem selector_column [DecidableEq n] [DecidableEq m]
    (A : Matrix n n ℝ) (f : m → n) (j : m) :
    columnMap (A * selector f) (Pi.single j 1) = columnMap A (Pi.single (f j) 1) := by
  change WithLp.toLp 2 ((A * selector f) *ᵥ Pi.single j 1) = WithLp.toLp 2 (A *ᵥ Pi.single (f j) 1)
  congr 1
  rw [← Matrix.mulVec_mulVec]
  congr 1
  ext i
  simp [selector, Matrix.mulVec, Pi.single_apply]

noncomputable def momentTwo (Λ : MvPolynomial σ ℝ →ₗ[ℝ] ℝ) :
    Matrix (Two (σ := σ)) (Two (σ := σ)) ℝ := fun i j => Λ (twoPolynomial i * twoPolynomial j)

noncomputable def momentOne (Λ : MvPolynomial σ ℝ →ₗ[ℝ] ℝ) :
    Matrix (One (σ := σ)) (One (σ := σ)) ℝ := fun i j => Λ (onePolynomial i * onePolynomial j)

theorem moment_principal (Λ : MvPolynomial σ ℝ →ₗ[ℝ] ℝ) :
    (selector (embedding (σ := σ))).conjTranspose * momentTwo Λ * selector embedding = momentOne Λ := by
  rw [selector_gram]
  ext i j
  simp only [Matrix.submatrix_apply, momentTwo, momentOne, embedding_polynomial]

theorem moment_shift_symmetric (Λ : MvPolynomial σ ℝ →ₗ[ℝ] ℝ) (g : σ) :
    (selector (embedding (σ := σ))).conjTranspose * momentTwo Λ * selector (shift g) =
      (selector (shift g)).conjTranspose * momentTwo Λ * selector embedding := by
  rw [selector_gram, selector_gram]
  ext i j
  simp only [Matrix.submatrix_apply, momentTwo, embedding_polynomial, shift_polynomial]
  congr 1
  ring

theorem moment_shifts_commute (Λ : MvPolynomial σ ℝ →ₗ[ℝ] ℝ) (g h : σ) :
    (selector (shift g)).conjTranspose * momentTwo Λ * selector (shift h) =
      (selector (shift h)).conjTranspose * momentTwo Λ * selector (shift g) := by
  rw [selector_gram, selector_gram]
  ext i j
  simp only [Matrix.submatrix_apply, momentTwo, shift_polynomial]
  congr 1
  ring

def stateTwo {H : Type*} [AddCommGroup H] [Module ℝ H]
    (T : σ → Module.End ℝ H) (ψ : H) : Two (σ := σ) → H
  | none => ψ
  | some (.inl g) => T g ψ
  | some (.inr (g,h)) => T g (T h ψ)

noncomputable def constantState
    (A : Matrix (Two (σ := σ)) (Two (σ := σ)) ℝ) : ColumnSpace (A * selector (embedding (σ := σ))) :=
  ⟨columnMap (A * selector embedding) (Pi.single none 1),
    LinearMap.mem_range_self (columnMap (A * selector embedding)) _⟩

theorem state_coordinates
    (A : Matrix (Two (σ := σ)) (Two (σ := σ)) ℝ)
    (T : σ → Module.End ℝ (ColumnSpace (A * selector (embedding (σ := σ)))))
    (himage : ∀ g (x : One (σ := σ) → ℝ),
      (T g ⟨columnMap (A * selector embedding) x,
        LinearMap.mem_range_self (columnMap (A * selector embedding)) x⟩).val =
          columnMap (A * selector (shift g)) x)
    (i : Two (σ := σ)) : (stateTwo T (constantState A) i).val = columnMap A (Pi.single i 1) := by
  let E : Matrix (Two (σ := σ)) (One (σ := σ)) ℝ := selector embedding
  let ψ := constantState A
  have hsingle (g : σ) : T g ψ =
      ⟨columnMap (A * E) (Pi.single (some g) 1), LinearMap.mem_range_self (columnMap (A * E)) _⟩ := by
    apply Subtype.ext
    change (T g ⟨columnMap (A * E) (Pi.single none 1), _⟩).val = columnMap (A * E) (Pi.single (some g) 1)
    calc
      _ = columnMap (A * selector (shift g)) (Pi.single none 1) := himage g _
      _ = columnMap A (Pi.single (shift g none) 1) := selector_column A (shift g) none
      _ = columnMap (A * E) (Pi.single (some g) 1) := (selector_column A embedding (some g)).symm
  cases i with
  | none => exact selector_column A embedding none
  | some i =>
    cases i with
    | inl g =>
      change (T g ψ).val = _
      rw [hsingle]
      exact selector_column A embedding (some g)
    | inr gh =>
      rcases gh with ⟨g,h⟩
      change (T g (T h ψ)).val = _
      rw [hsingle, himage]
      exact selector_column A (shift g) (some h)

theorem extract_polynomial_coordinates (Λ : MvPolynomial σ ℝ →ₗ[ℝ] ℝ)
    (hnorm : Λ 1 = 1) (hM : (momentTwo Λ).PosSemidef)
    (hflat : (momentTwo Λ).rank = (momentOne Λ).rank) :
    ∃ A : Matrix (Two (σ := σ)) (Two (σ := σ)) ℝ, A.conjTranspose * A = momentTwo Λ ∧
      ∃ T : σ → Module.End ℝ (ColumnSpace (A * selector (embedding (σ := σ)))),
        ∃ ψ : ColumnSpace (A * selector (embedding (σ := σ))),
          inner ℝ ψ ψ = 1 ∧ (∀ g, (T g).IsSymmetric) ∧ (∀ g h, Commute (T g) (T h)) ∧
          Module.finrank ℝ (ColumnSpace (A * selector (embedding (σ := σ)))) = (momentOne Λ).rank ∧
          ∀ i j : Two (σ := σ), inner ℝ (stateTwo T ψ i) (stateTwo T ψ j) = momentTwo Λ i j := by
  let E : Matrix (Two (σ := σ)) (One (σ := σ)) ℝ := selector embedding
  let D (g : σ) : Matrix (Two (σ := σ)) (One (σ := σ)) ℝ := selector (shift g)
  have hflat' : (momentTwo Λ).rank = (E.conjTranspose * momentTwo Λ * E).rank := by
    rw [show E.conjTranspose * momentTwo Λ * E = momentOne Λ from moment_principal Λ]
    exact hflat
  obtain ⟨A, hA, T, hsym, hcomm, hdim, himage⟩ := extract_commuting_family
    (momentTwo Λ) E D hM hflat' (moment_shift_symmetric Λ) (moment_shifts_commute Λ)
  let ψ := constantState A
  have hrepr i j : inner ℝ (stateTwo T ψ i) (stateTwo T ψ j) = momentTwo Λ i j := by
    change inner ℝ (stateTwo T ψ i).val (stateTwo T ψ j).val = _
    rw [state_coordinates A T himage, state_coordinates A T himage, gram_pairing, hA]
    simp [dotProduct, Matrix.mulVec, Pi.single_apply]
  refine ⟨A, hA, T, ψ, ?_, hsym, hcomm, ?_, hrepr⟩
  · have h := hrepr none none
    simpa only [stateTwo, momentTwo, twoPolynomial, one_mul, hnorm] using h
  · simpa only [show E.conjTranspose * momentTwo Λ * E = momentOne Λ from moment_principal Λ] using hdim

noncomputable def quadraticSpan : Submodule ℝ (MvPolynomial σ ℝ) :=
  Submodule.span ℝ (Set.range (twoPolynomial (σ := σ)))

section QuadraticZero
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]

omit [DecidableEq σ] in
theorem quadratic_zero_from_representation
    (Λ : MvPolynomial σ ℝ →ₗ[ℝ] ℝ) (T : σ → Module.End ℝ H) (ψ : H)
    (hsym : ∀ g, (T g).IsSymmetric)
    (hrepr : ∀ i j : Two (σ := σ), inner ℝ (stateTwo T ψ i) (stateTwo T ψ j) = momentTwo Λ i j)
    (χ : σ → ℝ) (v : H) (heigen : ∀ g, T g v = χ g • v) (hvisible : inner ℝ ψ v ≠ 0)
    (p : MvPolynomial σ ℝ) (hp : p ∈ quadraticSpan (σ := σ)) (hzero : Λ (p ^ 2) = 0) :
    eval χ p = 0 := by
  classical
  have heval (i : Two (σ := σ)) :
      inner ℝ (stateTwo T ψ i) v = eval χ (twoPolynomial i) * inner ℝ ψ v := by
    cases i with
    | none => simp [stateTwo, twoPolynomial]
    | some i =>
      cases i with
      | inl g =>
        change inner ℝ (T g ψ) v = _
        rw [hsym g, heigen g, inner_smul_right]
        simp [twoPolynomial]
      | inr gh =>
        rcases gh with ⟨g,h⟩
        change inner ℝ (T g (T h ψ)) v = _
        rw [hsym g, heigen g, inner_smul_right, hsym h, heigen h, inner_smul_right]
        simp [twoPolynomial, mul_assoc]
  obtain ⟨c, hc⟩ := (Submodule.mem_span_range_iff_exists_fun ℝ).mp hp
  let w := ∑ i : Two (σ := σ), c i • stateTwo T ψ i
  have hww : inner ℝ w w = Λ (p ^ 2) := by
    rw [← hc, pow_two]
    simp only [w, sum_inner, inner_sum, real_inner_smul_left, inner_smul_right,
      hrepr, momentTwo, Finset.sum_mul, Finset.mul_sum, smul_mul_assoc,
      mul_smul_comm, map_sum, map_smul, smul_eq_mul]
  have hw : w = 0 := inner_self_eq_zero.mp (hww.trans hzero)
  have hval : inner ℝ w v = eval χ p * inner ℝ ψ v := by
    rw [← hc]
    simp only [w, sum_inner, real_inner_smul_left, heval, MvPolynomial.smul_eq_C_mul,
      map_sum, map_mul, eval_C, Finset.sum_mul, mul_assoc]
  have hprod : eval χ p * inner ℝ ψ v = 0 := by
    rw [← hval, hw, inner_zero_left]
  exact (mul_eq_zero.mp hprod).resolve_right hvisible
end QuadraticZero

theorem real_point_of_positive_flat (Λ : MvPolynomial σ ℝ →ₗ[ℝ] ℝ)
    (hnorm : Λ 1 = 1) (hM : (momentTwo Λ).PosSemidef)
    (hflat : (momentTwo Λ).rank = (momentOne Λ).rank) :
    ∃ χ : σ → ℝ, ∀ p : MvPolynomial σ ℝ,
      p ∈ quadraticSpan (σ := σ) → Λ (p ^ 2) = 0 → eval χ p = 0 := by
  obtain ⟨A, hA, T, ψ, hψ, hsym, hcomm, hdim, hrepr⟩ :=
    extract_polynomial_coordinates Λ hnorm hM hflat
  have hne : ψ ≠ 0 := by
    intro hz
    simp [hz] at hψ
  obtain ⟨χ, v, heigen, hvisible⟩ := exists_visible_joint_eigenvector T hsym hcomm ψ hne
  exact ⟨χ, fun p hp hz => quadratic_zero_from_representation Λ T ψ hsym hrepr χ v heigen hvisible p hp hz⟩


noncomputable def linearSpan : Submodule ℝ (MvPolynomial σ ℝ) :=
  Submodule.span ℝ (Set.range (onePolynomial (σ := σ)))

omit [Fintype σ] [DecidableEq σ] in
theorem X_mem_linearSpan (g : σ) : X g ∈ linearSpan (σ := σ) :=
  Submodule.subset_span ⟨some g, rfl⟩

omit [Fintype σ] [DecidableEq σ] in
theorem C_mem_linearSpan (r : ℝ) : C r ∈ linearSpan (σ := σ) := by
  have h : (1 : MvPolynomial σ ℝ) ∈ linearSpan (σ := σ) :=
    Submodule.subset_span ⟨none, rfl⟩
  simpa only [MvPolynomial.smul_eq_C_mul, mul_one] using
    (linearSpan (σ := σ)).smul_mem r h

omit [Fintype σ] [DecidableEq σ] in
theorem linearSpan_le_quadraticSpan :
    linearSpan (σ := σ) ≤ quadraticSpan (σ := σ) := by
  apply Submodule.span_le.mpr
  rintro p ⟨i, rfl⟩
  exact Submodule.subset_span ⟨embedding i, embedding_polynomial i⟩

omit [Fintype σ] [DecidableEq σ] in
theorem linear_mul_mem_quadraticSpan {p q : MvPolynomial σ ℝ}
    (hp : p ∈ linearSpan (σ := σ)) (hq : q ∈ linearSpan (σ := σ)) :
    p * q ∈ quadraticSpan (σ := σ) := by
  induction hp, hq using Submodule.span_induction₂ with
  | mem_mem p q hp hq =>
    rcases hp with ⟨i, rfl⟩
    rcases hq with ⟨j, rfl⟩
    cases i with
    | none =>
      simpa only [onePolynomial, one_mul] using
        linearSpan_le_quadraticSpan (Submodule.subset_span ⟨j, rfl⟩)
    | some g =>
      cases j with
      | none =>
        simpa only [onePolynomial, mul_one] using
          linearSpan_le_quadraticSpan (X_mem_linearSpan g)
      | some h => exact Submodule.subset_span ⟨some (.inr (g,h)), rfl⟩
  | zero_left q hq => simpa only [zero_mul] using (quadraticSpan (σ := σ)).zero_mem
  | zero_right p hp => simpa only [mul_zero] using (quadraticSpan (σ := σ)).zero_mem
  | add_left p q r hp hq hr hpr hqr =>
    simpa only [add_mul] using (quadraticSpan (σ := σ)).add_mem hpr hqr
  | add_right p q r hp hq hr hpq hpr =>
    simpa only [mul_add] using (quadraticSpan (σ := σ)).add_mem hpq hpr
  | smul_left a p q hp hq hpq =>
    simpa only [smul_mul_assoc] using (quadraticSpan (σ := σ)).smul_mem a hpq
  | smul_right a p q hp hq hpq =>
    simpa only [mul_smul_comm] using (quadraticSpan (σ := σ)).smul_mem a hpq

omit [DecidableEq σ] in
theorem square_zero_of_finite_relations (Λ : MvPolynomial σ ℝ →ₗ[ℝ] ℝ)
    (p : MvPolynomial σ ℝ) (hp : p ∈ quadraticSpan (σ := σ))
    (hrel : ∀ i : Two (σ := σ), Λ (twoPolynomial i * p) = 0) : Λ (p ^ 2) = 0 := by
  classical
  obtain ⟨c, hc⟩ := (Submodule.mem_span_range_iff_exists_fun ℝ).mp hp
  calc
    Λ (p ^ 2) = Λ ((∑ i : Two (σ := σ), c i • twoPolynomial i) * p) := by rw [hc, pow_two]
    _ = 0 := by simp only [Finset.sum_mul, smul_mul_assoc, map_sum, map_smul, hrel, smul_zero, Finset.sum_const_zero]


/-- Evaluation provides a normalized real functional; no solver is involved. -/
noncomputable def evaluationFunctional (x : σ → ℝ) : MvPolynomial σ ℝ →ₗ[ℝ] ℝ :=
  (MvPolynomial.aeval x).toLinearMap

omit [Fintype σ] [DecidableEq σ] in
@[simp] theorem evaluationFunctional_apply (x : σ → ℝ) (p : MvPolynomial σ ℝ) :
    evaluationFunctional x p = eval x p := rfl

omit [Fintype σ] [DecidableEq σ] in
theorem momentTwo_evaluation (x : σ → ℝ) :
    momentTwo (evaluationFunctional x) =
      Matrix.vecMulVec (fun i => eval x (twoPolynomial i)) (fun i => eval x (twoPolynomial i)) := by
  ext i j
  simp [momentTwo, Matrix.vecMulVec]

omit [Fintype σ] [DecidableEq σ] in
theorem momentOne_evaluation (x : σ → ℝ) :
    momentOne (evaluationFunctional x) =
      Matrix.vecMulVec (fun i => eval x (onePolynomial i)) (fun i => eval x (onePolynomial i)) := by
  ext i j
  simp [momentOne, Matrix.vecMulVec]

omit [Fintype σ] [DecidableEq σ] in
theorem evaluation_gram_rank_one {ι : Type*} [Fintype ι] (v : ι → ℝ) (i : ι) (hi : v i = 1) :
      (Matrix.vecMulVec v v).rank = 1 := by
  have heq : (Matrix.vecMulVec v v).submatrix (fun _ : Unit => i) (fun _ : Unit => i) =
        (1 : Matrix Unit Unit ℝ) := by
    ext a b
    simp [Matrix.submatrix, Matrix.vecMulVec, hi]
  have hlow := Matrix.rank_submatrix_le (Matrix.vecMulVec v v) (fun _ : Unit => i) (fun _ : Unit => i)
  rw [heq, Matrix.rank_one, Fintype.card_unit] at hlow
  exact le_antisymm (Matrix.rank_vecMulVec_le v v) hlow

omit [DecidableEq σ] in
theorem evaluation_moment_positive_flat (x : σ → ℝ) :
    evaluationFunctional x 1 = 1 ∧ (momentTwo (evaluationFunctional x)).PosSemidef ∧
      (momentTwo (evaluationFunctional x)).rank = (momentOne (evaluationFunctional x)).rank := by
  classical
  refine ⟨by simp, ?_, ?_⟩
  · rw [momentTwo_evaluation]
    simpa only [star_trivial] using
      Matrix.posSemidef_vecMulVec_self_star (fun i => eval x (twoPolynomial i))
  · rw [momentTwo_evaluation, momentOne_evaluation,
      evaluation_gram_rank_one (fun i => eval x (twoPolynomial i)) none (by simp [twoPolynomial]),
      evaluation_gram_rank_one (fun i => eval x (onePolynomial i)) none (by simp [onePolynomial])]

#print axioms evaluation_moment_positive_flat
#print axioms square_zero_of_finite_relations
#print axioms quadratic_zero_from_representation
#print axioms real_point_of_positive_flat
#print axioms extract_polynomial_coordinates
#print axioms moment_shift_symmetric
#print axioms moment_shifts_commute
end PolynomialMoments

#print axioms symmetric_shift_ker
#print axioms multiplicationOperator_symmetric
#print axioms operators_commute
#print axioms extract_commuting_family
#print axioms exists_visible_joint_eigenvector
end MUB.CommutativeFlatMoments
