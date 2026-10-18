import SzollosiQuartetSystem
import Mathlib.Algebra.MvPolynomial.Degrees

/-!
# Joint rational quadratic equations for the two-circulant quartet problem

AuthorityEffect: None.

The 440 real coordinates retain eight phase coordinates, three raw complex
six-by-six basis matrices and three auxiliary cross-product matrices. The 618
rational equations have total degree at most two. Raw bases are scaled by sqrt 6;
the cross-product norm-square target is six. Both additional bases remain arbitrary.

Actual quartets containing the constructed phase-family matrix correspond in
both directions to real solutions, also with each phase parameter fixed. Every
solution lies in a rational box: phase and raw basis coordinates in [-1,1],
auxiliary cross-product coordinates in [-3,3]. Boundary phases are retained.

This is a noncomputable Mathlib polynomial specification with semantic Lean
proofs. It is not an executable native coefficient export or an interval
certificate. No solution set is established empty. The system is rectangular;
native rectangular contractor execution and image parity, dephased equivalence
transport, the full 56-cell and three-cusp calculation and its semantic kernel
reflection remain open. RectangularQuadraticExclusion and
SzollosiRectangularExclusion supply the subsequent Lean exclusion soundness
and actual-equation bridge.
-/

noncomputable section

namespace MUB.SzollosiQuadraticSystem
open Matrix
open ConcreteMubPolynomialSystem SzollosiTwoCirculant SzollosiQuartetSystem
open MvPolynomial
open scoped BigOperators

abbrev Slot := Fin 3 × Fin 6 × Fin 6 × Bool
abbrev Variable := ParameterCoord ⊕ (Slot ⊕ Slot)
abbrev QPoly := MvPolynomial Variable ℚ
abbrev CPoly := QPoly × QPoly
abbrev PMatrix := Matrix (Fin 6) (Fin 6) CPoly

def realEval (r : Variable → ℝ) : QPoly →+* ℝ := eval₂Hom (algebraMap ℚ ℝ) r

def complexEval (r : Variable → ℝ) (p : CPoly) : ℂ :=
  ⟨realEval r p.1,realEval r p.2⟩

def matrixEval (r : Variable → ℝ) (A : PMatrix) : Candidate :=
  fun i j => complexEval r (A i j)

def cOne : CPoly := (1,0)
def cStar (p : CPoly) : CPoly := (p.1,-p.2)
def cNeg (p : CPoly) : CPoly := (-p.1,-p.2)
def cMul (p q : CPoly) : CPoly :=
  (p.1*q.1-p.2*q.2,p.1*q.2+p.2*q.1)
def normPolynomial (p : CPoly) : QPoly := p.1^2+p.2^2

theorem complexEval_add (r : Variable → ℝ) (p q : CPoly) :
    complexEval r (p+q) = complexEval r p + complexEval r q := by
  apply Complex.ext <;> simp [complexEval]

theorem complexEval_sum {ι : Type*} (r : Variable → ℝ) (s : Finset ι) (p : ι → CPoly) :
    complexEval r (∑ i ∈ s, p i) = ∑ i ∈ s, complexEval r (p i) := by
  classical
  induction s using Finset.induction_on with
  | empty => apply Complex.ext <;> simp [complexEval]
  | @insert i s hi ih =>
    rw [Finset.sum_insert hi,Finset.sum_insert hi,complexEval_add,ih]

theorem complexEval_star (r : Variable → ℝ) (p : CPoly) :
    complexEval r (cStar p) = star (complexEval r p) := by
  apply Complex.ext <;> simp [complexEval,cStar]

theorem complexEval_neg (r : Variable → ℝ) (p : CPoly) :
    complexEval r (cNeg p) = -complexEval r p := by
  apply Complex.ext <;> simp [complexEval,cNeg]

theorem complexEval_mul (r : Variable → ℝ) (p q : CPoly) :
    complexEval r (cMul p q) = complexEval r p * complexEval r q := by
  apply Complex.ext <;> simp [complexEval,cMul,Complex.mul_re,Complex.mul_im]

theorem normPolynomial_eval (r : Variable → ℝ) (p : CPoly) :
    realEval r (normPolynomial p) = Complex.normSq (complexEval r p) := by
  simp [normPolynomial,complexEval,Complex.normSq_apply,pow_two]

def phasePolynomial (i : Fin 4) : CPoly :=
  (X (.inl (i,false)),X (.inl (i,true)))
def basisPolynomial (a : Fin 3) (i j : Fin 6) : CPoly :=
  (X (.inr (.inl (a,i,j,false))),X (.inr (.inl (a,i,j,true))))
def productPolynomial (a : Fin 3) (i j : Fin 6) : CPoly :=
  (X (.inr (.inr (a,i,j,false))),X (.inr (.inr (a,i,j,true))))

def parameters (r : Variable → ℝ) : ParameterCoord → ℝ := fun p => r (.inl p)
def phase (r : Variable → ℝ) (i : Fin 4) : ℂ := complexEval r (phasePolynomial i)
def basis (r : Variable → ℝ) (a : Fin 3) : Candidate :=
  fun i j => complexEval r (basisPolynomial a i j)
def product (r : Variable → ℝ) (a : Fin 3) : Candidate :=
  fun i j => complexEval r (productPolynomial a i j)

theorem phase_eq_decode (r : Variable → ℝ) (i : Fin 4) :
    phase r i = decodeParameters (parameters r) i := by
  apply Complex.ext <;> simp [phase,phasePolynomial,complexEval,realEval,decodeParameters,parameters]

def pCirculant (a : Fin 3 → CPoly) : Matrix (Fin 3) (Fin 3) CPoly :=
  Matrix.circulant (fun i => a (-i))
def pAdjoint {ι κ : Type*} (A : Matrix ι κ CPoly) : Matrix κ ι CPoly :=
  fun i j => cStar (A j i)
def pRaw (a b : Fin 3 → CPoly) : PMatrix :=
  (Matrix.fromBlocks (pCirculant a) (pCirculant b)
    (pAdjoint (pCirculant b)) (fun i j => cNeg (pAdjoint (pCirculant a) i j))).submatrix
      blockEquiv.symm blockEquiv.symm

theorem pRaw_eval (r : Variable → ℝ) (a b : Fin 3 → CPoly) :
    (fun i j => complexEval r (pRaw a b i j)) =
      rawSix (fun i => complexEval r (a i)) (fun i => complexEval r (b i)) := by
  ext i j
  unfold pRaw rawSix rawBlock
  simp only [Matrix.submatrix_apply]
  cases hi : blockEquiv.symm i with
  | inl k =>
    cases hj : blockEquiv.symm j with
    | inl l => rfl
    | inr l => rfl
  | inr k =>
    cases hj : blockEquiv.symm j with
    | inl l => exact complexEval_star r _
    | inr l => exact (complexEval_neg r _).trans (congrArg Neg.neg (complexEval_star r _))

def phaseRowPolynomial (x y : CPoly) : Fin 3 → CPoly := ![cOne,x,cMul x y]
def rawFamilyPolynomial : PMatrix :=
  pRaw (phaseRowPolynomial (phasePolynomial 0) (phasePolynomial 1))
    (phaseRowPolynomial (phasePolynomial 2) (phasePolynomial 3))

theorem phaseRowPolynomial_eval (r : Variable → ℝ) (x y : CPoly) :
    (fun i => complexEval r (phaseRowPolynomial x y i)) =
      phaseRow (complexEval r x) (complexEval r y) := by
  funext i
  fin_cases i
  · apply Complex.ext <;> simp [phaseRowPolynomial,phaseRow,cOne,complexEval]
  · rfl
  · exact complexEval_mul r x y

theorem rawFamilyPolynomial_eval (r : Variable → ℝ) :
    (fun i j => complexEval r (rawFamilyPolynomial i j)) =
      rawSix (phaseRow (phase r 0) (phase r 1)) (phaseRow (phase r 2) (phase r 3)) := by
  rw [rawFamilyPolynomial,pRaw_eval,phaseRowPolynomial_eval,phaseRowPolynomial_eval]
  rfl

def gramPolynomial (A B : PMatrix) (i j : Fin 6) : CPoly :=
  ∑ k, cMul (cStar (A k i)) (B k j)

theorem gramPolynomial_eval (r : Variable → ℝ) (A B : PMatrix) (i j : Fin 6) :
    complexEval r (gramPolynomial A B i j) =
      ((matrixEval r A).conjTranspose * matrixEval r B) i j := by
  simp only [gramPolynomial,complexEval_sum,complexEval_mul,complexEval_star,
    Matrix.mul_apply,Matrix.conjTranspose_apply,matrixEval]

def pairLeft : Fin 3 → Fin 3 := ![0,0,1]
def pairRight : Fin 3 → Fin 3 := ![1,2,2]

def phaseSumPolynomial (x y : CPoly) : CPoly := x+y+cStar (cMul x y)
def compatibilityPolynomial : CPoly :=
  phaseSumPolynomial (phasePolynomial 0) (phasePolynomial 1) +
    phaseSumPolynomial (phasePolynomial 2) (phasePolynomial 3)

theorem compatibilityPolynomial_eval (r : Variable → ℝ) :
    complexEval r compatibilityPolynomial = phaseSum (phase r 0) (phase r 1) +
      phaseSum (phase r 2) (phase r 3) := by
  simp only [compatibilityPolynomial,phaseSumPolynomial,complexEval_add,
    complexEval_star,complexEval_mul,phaseSum,phase]

def component (p : CPoly) (b : Bool) : QPoly := if b then p.2 else p.1

theorem component_zero_iff (r : Variable → ℝ) (p : CPoly) :
    (∀ b, realEval r (component p b) = 0) ↔ complexEval r p = 0 := by
  constructor
  · intro h
    apply Complex.ext
    · exact h false
    · exact h true
  · intro h b
    cases b
    · exact congrArg Complex.re h
    · exact congrArg Complex.im h

abbrev UnitaryIndex := Fin 2 × Fin 6 × Fin 6 × Bool
abbrev EntryIndex := Fin 2 × Fin 6 × Fin 6
abbrev Equation := ParameterEquation ⊕ (Coord ⊕ (UnitaryIndex ⊕ (EntryIndex ⊕ (Slot ⊕ (Fin 3 × Fin 6 × Fin 6)))))

def candidateIndex (a : Fin 2) : Fin 3 := ⟨a.val+1,by omega⟩

def parameterEquation : ParameterEquation → QPoly
  | .inl i => normPolynomial (phasePolynomial i) - 1
  | .inr b => component compatibilityPolynomial b

def familyEquation (i j : Fin 6) (b : Bool) : QPoly :=
  component (basisPolynomial 0 i j - rawFamilyPolynomial i j) b

def unitaryTarget (i j : Fin 6) : CPoly := (C (if i=j then 6 else 0),0)
def unitaryEquation (a : Fin 2) (i j : Fin 6) (b : Bool) : QPoly :=
  component (gramPolynomial (basisPolynomial (candidateIndex a))
    (basisPolynomial (candidateIndex a)) i j - unitaryTarget i j) b

def entryEquation (a : Fin 2) (i j : Fin 6) : QPoly :=
  normPolynomial (basisPolynomial (candidateIndex a) i j) - 1

def productEquation (a : Fin 3) (i j : Fin 6) (b : Bool) : QPoly :=
  component (productPolynomial a i j - gramPolynomial (basisPolynomial (pairLeft a))
    (basisPolynomial (pairRight a)) i j) b

def overlapEquation (a : Fin 3) (i j : Fin 6) : QPoly :=
  normPolynomial (productPolynomial a i j) - C 6

def equationPolynomial : Equation → QPoly
  | .inl e => parameterEquation e
  | .inr (.inl (i,j,b)) => familyEquation i j b
  | .inr (.inr (.inl (a,i,j,b))) => unitaryEquation a i j b
  | .inr (.inr (.inr (.inl (a,i,j)))) => entryEquation a i j
  | .inr (.inr (.inr (.inr (.inl (a,i,j,b))))) => productEquation a i j b
  | .inr (.inr (.inr (.inr (.inr (a,i,j))))) => overlapEquation a i j

theorem variable_count : Fintype.card Variable = 440 := by simp [Variable,Slot,ParameterCoord]
theorem equation_count : Fintype.card Equation = 618 := by
  simp [Equation,ParameterEquation,UnitaryIndex,EntryIndex,Slot,Coord]

#print axioms pRaw_eval
#print axioms rawFamilyPolynomial_eval
#print axioms gramPolynomial_eval
#print axioms compatibilityPolynomial_eval


def rawFamily (r : Variable → ℝ) : Candidate :=
  rawSix (phaseRow (phase r 0) (phase r 1)) (phaseRow (phase r 2) (phase r 3))

theorem complexEval_sub (r : Variable → ℝ) (p q : CPoly) :
    complexEval r (p-q) = complexEval r p - complexEval r q := by
  apply Complex.ext <;> simp [complexEval]

theorem unitaryTarget_eval (r : Variable → ℝ) (i j : Fin 6) :
    complexEval r (unitaryTarget i j) = ((6 : ℂ) • (1 : Candidate)) i j := by
  by_cases h : i=j <;>
    apply Complex.ext <;> simp [unitaryTarget,complexEval,realEval,h]

theorem matrix_difference_zero_iff (r : Variable → ℝ) (A B : PMatrix) :
    (∀ i j b, realEval r (component (A i j-B i j) b) = 0) ↔
      matrixEval r A = matrixEval r B := by
  constructor
  · intro h
    ext i j
    exact sub_eq_zero.mp ((complexEval_sub r _ _).symm.trans
      ((component_zero_iff r _).mp (h i j)))
  · intro h i j b
    apply (component_zero_iff r _).mpr _ b
    rw [complexEval_sub]
    exact sub_eq_zero.mpr (congrArg (fun M : Candidate => M i j) h)

theorem normSq_unit_iff (z : ℂ) : Complex.normSq z = 1 ↔ z * star z = 1 := by
  rw [Complex.star_def,Complex.mul_conj]
  constructor
  · intro h; rw [h]; rfl
  · intro h; exact_mod_cast h

theorem parameter_zero_iff (r : Variable → ℝ) :
    (∀ e, realEval r (parameterEquation e) = 0) ↔
      ParameterDomain (phase r 0) (phase r 1) (phase r 2) (phase r 3) := by
  constructor
  · intro h
    have hc : ∀ i, phase r i * star (phase r i) = 1 := by
      intro i
      apply (normSq_unit_iff _).mp
      have hi := h (.inl i)
      simpa only [parameterEquation,map_sub,map_one,normPolynomial_eval,sub_eq_zero,phase] using hi
    refine ⟨hc 0,hc 1,hc 2,hc 3,?_⟩
    exact (compatibilityPolynomial_eval r).symm.trans
      ((component_zero_iff r _).mp (fun b => h (.inr b)))
  · rintro ⟨h0,h1,h2,h3,hc⟩ e
    cases e with
    | inl i =>
      have hi : phase r i * star (phase r i) = 1 := by
        fin_cases i <;> assumption
      simpa only [parameterEquation,map_sub,map_one,normPolynomial_eval,sub_eq_zero,phase] using
        (normSq_unit_iff _).mpr hi
    | inr b =>
      exact (component_zero_iff r _).mpr ((compatibilityPolynomial_eval r).trans hc) b

theorem matrixEval_basis (r : Variable → ℝ) (a : Fin 3) :
    matrixEval r (basisPolynomial a) = basis r a := rfl

theorem matrixEval_product (r : Variable → ℝ) (a : Fin 3) :
    matrixEval r (productPolynomial a) = product r a := rfl

theorem matrixEval_rawFamily (r : Variable → ℝ) :
    matrixEval r rawFamilyPolynomial = rawFamily r := rawFamilyPolynomial_eval r

theorem matrixEval_gram (r : Variable → ℝ) (A B : PMatrix) :
    matrixEval r (gramPolynomial A B) = (matrixEval r A).conjTranspose * matrixEval r B := by
  ext i j
  exact gramPolynomial_eval r A B i j

theorem matrixEval_unitaryTarget (r : Variable → ℝ) :
    matrixEval r unitaryTarget = (6 : ℂ) • (1 : Candidate) := by
  ext i j
  exact unitaryTarget_eval r i j

theorem realEval_C (r : Variable → ℝ) (q : ℚ) : realEval r (C q) = (q : ℝ) := by
  simp [realEval]

theorem family_zero_iff (r : Variable → ℝ) :
    (∀ i j b, realEval r (familyEquation i j b) = 0) ↔ basis r 0 = rawFamily r := by
  simpa only [familyEquation,matrixEval_basis,matrixEval_rawFamily] using
    matrix_difference_zero_iff r (basisPolynomial 0) rawFamilyPolynomial

theorem unitary_zero_iff (r : Variable → ℝ) (a : Fin 2) :
    (∀ i j b, realEval r (unitaryEquation a i j b) = 0) ↔
      (basis r (candidateIndex a)).conjTranspose * basis r (candidateIndex a) =
        (6 : ℂ) • (1 : Candidate) := by
  have h := matrix_difference_zero_iff r
      (gramPolynomial (basisPolynomial (candidateIndex a)) (basisPolynomial (candidateIndex a)))
      unitaryTarget
  rw [matrixEval_gram r (basisPolynomial (candidateIndex a)) (basisPolynomial (candidateIndex a)),matrixEval_basis,matrixEval_unitaryTarget] at h
  exact h

theorem entry_zero_iff (r : Variable → ℝ) (a : Fin 2) (i j : Fin 6) :
    realEval r (entryEquation a i j) = 0 ↔ Complex.normSq (basis r (candidateIndex a) i j) = 1 := by
  simp only [entryEquation,map_sub,map_one,normPolynomial_eval,sub_eq_zero]
  rfl

theorem product_zero_iff (r : Variable → ℝ) (a : Fin 3) :
    (∀ i j b, realEval r (productEquation a i j b) = 0) ↔
      product r a = (basis r (pairLeft a)).conjTranspose * basis r (pairRight a) := by
  have h := matrix_difference_zero_iff r (productPolynomial a)
      (gramPolynomial (basisPolynomial (pairLeft a)) (basisPolynomial (pairRight a)))
  rw [matrixEval_gram r (basisPolynomial (pairLeft a)) (basisPolynomial (pairRight a)),matrixEval_basis,matrixEval_basis,matrixEval_product] at h
  exact h

theorem overlap_zero_iff (r : Variable → ℝ) (a : Fin 3) (i j : Fin 6) :
    realEval r (overlapEquation a i j) = 0 ↔ Complex.normSq (product r a i j) = 6 := by
  simp only [overlapEquation,map_sub,normPolynomial_eval,realEval_C,sub_eq_zero]
  norm_num
  rfl

def RawEquations (r : Variable → ℝ) : Prop :=
  ParameterDomain (phase r 0) (phase r 1) (phase r 2) (phase r 3) ∧
  basis r 0 = rawFamily r ∧
  (∀ a : Fin 2, (basis r (candidateIndex a)).conjTranspose * basis r (candidateIndex a) =
    (6 : ℂ) • (1 : Candidate)) ∧
  (∀ a : Fin 2, ∀ i j, Complex.normSq (basis r (candidateIndex a) i j) = 1) ∧
  (∀ a : Fin 3, product r a = (basis r (pairLeft a)).conjTranspose * basis r (pairRight a)) ∧
  (∀ a : Fin 3, ∀ i j, Complex.normSq (product r a i j) = 6)

theorem all_equations_zero_iff (r : Variable → ℝ) :
    (∀ e, realEval r (equationPolynomial e) = 0) ↔ RawEquations r := by
  constructor
  · intro h
    refine ⟨(parameter_zero_iff r).mp (fun e => h (.inl e)),
      (family_zero_iff r).mp (fun i j b => h (.inr (.inl (i,j,b)))),?_,?_,?_,?_⟩
    · intro a
      exact (unitary_zero_iff r a).mp (fun i j b => h (.inr (.inr (.inl (a,i,j,b)))))
    · intro a i j
      exact (entry_zero_iff r a i j).mp (h (.inr (.inr (.inr (.inl (a,i,j))))))
    · intro a
      exact (product_zero_iff r a).mp (fun i j b => h (.inr (.inr (.inr (.inr (.inl (a,i,j,b)))))))
    · intro a i j
      exact (overlap_zero_iff r a i j).mp (h (.inr (.inr (.inr (.inr (.inr (a,i,j)))))))
  · rintro ⟨hp,hf,hu,he,hpdt,ho⟩ e
    rcases e with e | e
    · exact (parameter_zero_iff r).mpr hp e
    rcases e with e | e
    · rcases e with ⟨i,j,b⟩; exact (family_zero_iff r).mpr hf i j b
    rcases e with e | e
    · rcases e with ⟨a,i,j,b⟩; exact (unitary_zero_iff r a).mpr (hu a) i j b
    rcases e with e | e
    · rcases e with ⟨a,i,j⟩; exact (entry_zero_iff r a i j).mpr (he a i j)
    rcases e with e | e
    · rcases e with ⟨a,i,j,b⟩; exact (product_zero_iff r a).mpr (hpdt a) i j b
    · rcases e with ⟨a,i,j⟩; exact (overlap_zero_iff r a i j).mpr (ho a i j)

#print axioms all_equations_zero_iff


def normalize (U : Candidate) : Candidate := normalizer • U

theorem normalizer_normSq : Complex.normSq normalizer = 1/6 := by
  have h := normalizer_square
  simp only [Complex.star_def,Complex.mul_conj] at h
  have hre := congrArg Complex.re h
  norm_num at hre
  exact hre

theorem normalize_gram (U V : Candidate) :
    (normalize U).conjTranspose * normalize V = (1/6 : ℂ) • (U.conjTranspose * V) := by
  have hn : normalizer * star normalizer = (1/6 : ℂ) := by
    rw [normalizer_square]
    norm_num
  simp only [normalize,Matrix.conjTranspose_smul,Matrix.smul_mul,Matrix.mul_smul,smul_smul,hn]

theorem normalize_unitary_iff (U : Candidate) :
    (normalize U).conjTranspose * normalize U = 1 ↔ U.conjTranspose * U = (6 : ℂ) • (1 : Candidate) := by
  rw [normalize_gram]
  constructor
  · intro h
    have h6 := congrArg (fun M : Candidate => (6 : ℂ) • M) h
    simpa [smul_smul] using h6
  · intro h
    rw [h,smul_smul]
    norm_num

theorem normalize_identity_mu_iff (U : Candidate) :
    PairMU 1 (normalize U) ↔ ∀ i j, Complex.normSq (U i j) = 1 := by
  simp only [PairMU,Matrix.conjTranspose_one,Matrix.one_mul,normalize,
    Matrix.smul_apply,smul_eq_mul,Complex.normSq_mul,normalizer_normSq]
  constructor
  · intro h i j
    have hi := h i j
    nlinarith
  · intro h i j
    rw [h i j]
    ring

def RawPairMU (U V : Candidate) : Prop := ∀ i j, Complex.normSq ((U.conjTranspose * V) i j) = 6

theorem normalize_pair_mu_iff (U V : Candidate) :
    PairMU (normalize U) (normalize V) ↔ RawPairMU U V := by
  have hq : Complex.normSq (1/6 : ℂ) = (1/36 : ℝ) := by norm_num [Complex.normSq_apply]
  simp only [PairMU,RawPairMU,normalize_gram,Matrix.smul_apply,smul_eq_mul,Complex.normSq_mul,hq]
  constructor
  · intro h i j
    have hi := h i j
    nlinarith
  · intro h i j
    rw [h i j]
    norm_num

def RawCandidates (H U V : Candidate) : Prop :=
  U.conjTranspose * U = (6 : ℂ) • (1 : Candidate) ∧
  (∀ i j, Complex.normSq (U i j) = 1) ∧ RawPairMU H U ∧
  V.conjTranspose * V = (6 : ℂ) • (1 : Candidate) ∧
  (∀ i j, Complex.normSq (V i j) = 1) ∧ RawPairMU H V ∧ RawPairMU U V

theorem normalize_quartet_iff (H U V : Candidate)
    (hH : (normalize H).conjTranspose * normalize H = 1) (hIH : PairMU 1 (normalize H)) :
    Quartet (bases (normalize H) (normalize U) (normalize V)) ↔ RawCandidates H U V := by
  constructor
  · intro h
    exact ⟨(normalize_unitary_iff U).mp (h.1 2),
      (normalize_identity_mu_iff U).mp (h.2 0 2 (by decide)),
      (normalize_pair_mu_iff H U).mp (h.2 1 2 (by decide)),
      (normalize_unitary_iff V).mp (h.1 3),
      (normalize_identity_mu_iff V).mp (h.2 0 3 (by decide)),
      (normalize_pair_mu_iff H V).mp (h.2 1 3 (by decide)),
      (normalize_pair_mu_iff U V).mp (h.2 2 3 (by decide))⟩
  · rintro ⟨hU,hIU,hHU,hV,hIV,hHV,hUV⟩
    apply (extension_iff_quartet _ _ _ hH hIH).mp
    refine ⟨(normalize_unitary_iff U).mpr hU,(normalize_identity_mu_iff U).mpr hIU,
      (normalize_pair_mu_iff H U).mpr hHU,(normalize_unitary_iff V).mpr hV,?_⟩
    intro a i j
    fin_cases a
    · exact (normalize_identity_mu_iff V).mpr hIV i j
    · exact (normalize_pair_mu_iff H V).mpr hHV i j
    · exact (normalize_pair_mu_iff U V).mpr hUV i j

#print axioms normalize_quartet_iff



def rawParameterMatrix (p : ParameterCoord → ℝ) : Candidate :=
  rawSix (phaseRow (decodeParameters p 0) (decodeParameters p 1))
    (phaseRow (decodeParameters p 2) (decodeParameters p 3))

theorem normalize_rawParameterMatrix (p : ParameterCoord → ℝ) :
    normalize (rawParameterMatrix p) = parameterMatrix p := rfl

theorem rawFamily_eq_parameter (r : Variable → ℝ) :
    rawFamily r = rawParameterMatrix (parameters r) := by
  simp only [rawFamily,rawParameterMatrix,phase_eq_decode]

theorem solution_parameter_equations (r : Variable → ℝ) (h : RawEquations r) :
    ∀ e, eval (parameters r) (parameterPolynomial e) = 0 := by
  apply (parameter_equations_iff _).mpr
  simpa only [phase_eq_decode] using h.1

theorem solution_rawCandidates (r : Variable → ℝ) (h : RawEquations r) :
    RawCandidates (basis r 0) (basis r 1) (basis r 2) := by
  have hm (a : Fin 3) : RawPairMU (basis r (pairLeft a)) (basis r (pairRight a)) := by
    intro i j
    rw [← h.2.2.2.2.1 a]
    exact h.2.2.2.2.2 a i j
  exact ⟨h.2.2.1 0,h.2.2.2.1 0,hm 0,h.2.2.1 1,h.2.2.2.1 1,hm 1,hm 2⟩

theorem quartet_of_solution (r : Variable → ℝ)
    (h : ∀ e, realEval r (equationPolynomial e) = 0) :
    Quartet (bases (parameterMatrix (parameters r)) (normalize (basis r 1)) (normalize (basis r 2))) := by
  have hr := (all_equations_zero_iff r).mp h
  have hp := solution_parameter_equations r hr
  have h0 : normalize (basis r 0) = parameterMatrix (parameters r) := by
    rw [hr.2.1,rawFamily_eq_parameter,normalize_rawParameterMatrix]
  rw [← h0]
  apply (normalize_quartet_iff _ _ _ ?_ ?_).mpr (solution_rawCandidates r hr)
  · rw [h0]; exact parameterMatrix_unitary _ hp
  · rw [h0]; exact parameterMatrix_mu_identity _ hp

def amplifier : ℂ := ((Real.sqrt 6 : ℝ) : ℂ)

theorem normalize_amplify (U : Candidate) : normalize (amplifier • U) = U := by
  have h : amplifier ≠ 0 := by
    unfold amplifier
    exact_mod_cast (ne_of_gt (Real.sqrt_pos.2 (by norm_num : (0 : ℝ) < 6)))
  simp only [normalize,normalizer,amplifier,smul_smul]
  change (amplifier⁻¹ * amplifier) • U = U
  rw [inv_mul_cancel₀ h,one_smul]

def encode (p : ParameterCoord → ℝ) (B D : Fin 3 → Candidate) : Variable → ℝ
  | .inl q => p q
  | .inr (.inl (a,i,j,b)) => if b then (B a i j).im else (B a i j).re
  | .inr (.inr (a,i,j,b)) => if b then (D a i j).im else (D a i j).re

theorem parameters_encode (p : ParameterCoord → ℝ) (B D : Fin 3 → Candidate) :
    parameters (encode p B D) = p := rfl

theorem basis_encode (p : ParameterCoord → ℝ) (B D : Fin 3 → Candidate) (a : Fin 3) :
    basis (encode p B D) a = B a := by
  ext i j
  apply Complex.ext <;> simp [basis,basisPolynomial,complexEval,realEval,encode]

theorem product_encode (p : ParameterCoord → ℝ) (B D : Fin 3 → Candidate) (a : Fin 3) :
    product (encode p B D) a = D a := by
  ext i j
  apply Complex.ext <;> simp [product,productPolynomial,complexEval,realEval,encode]

theorem phase_encode (p : ParameterCoord → ℝ) (B D : Fin 3 → Candidate) (i : Fin 4) :
    phase (encode p B D) i = decodeParameters p i := by
  rw [phase_eq_decode,parameters_encode]

theorem solution_of_quartet (p : ParameterCoord → ℝ) (U V : Candidate)
    (hp : ∀ e, eval p (parameterPolynomial e) = 0)
    (hq : Quartet (bases (parameterMatrix p) U V)) :
    ∃ r, parameters r = p ∧ (∀ e, realEval r (equationPolynomial e) = 0) ∧
      normalize (basis r 1) = U ∧ normalize (basis r 2) = V := by
  let B : Fin 3 → Candidate := ![rawParameterMatrix p,amplifier • U,amplifier • V]
  let D : Fin 3 → Candidate := fun a => (B (pairLeft a)).conjTranspose * B (pairRight a)
  have h0 : normalize (B 0) = parameterMatrix p := normalize_rawParameterMatrix p
  have h1 : normalize (B 1) = U := normalize_amplify U
  have h2 : normalize (B 2) = V := normalize_amplify V
  have hc : RawCandidates (B 0) (B 1) (B 2) := by
    apply (normalize_quartet_iff _ _ _ ?_ ?_).mp
    · rw [h0,h1,h2]; exact hq
    · rw [h0]; exact parameterMatrix_unitary p hp
    · rw [h0]; exact parameterMatrix_mu_identity p hp
  refine ⟨encode p B D,rfl,?_,?_,?_⟩
  · apply (all_equations_zero_iff _).mpr
    refine ⟨?_,?_,?_,?_,?_,?_⟩
    · simpa only [phase_encode] using (parameter_equations_iff p).mp hp
    · rw [basis_encode,rawFamily_eq_parameter,parameters_encode]; rfl
    · intro a
      rw [basis_encode]
      fin_cases a
      · exact hc.1
      · exact hc.2.2.2.1
    · intro a i j
      rw [basis_encode]
      fin_cases a
      · exact hc.2.1 i j
      · exact hc.2.2.2.2.1 i j
    · intro a
      rw [product_encode,basis_encode,basis_encode]
    · intro a i j
      rw [product_encode]
      fin_cases a
      · exact hc.2.2.1 i j
      · exact hc.2.2.2.2.2.1 i j
      · exact hc.2.2.2.2.2.2 i j
  · rw [basis_encode]; exact h1
  · rw [basis_encode]; exact h2

/-- Full existence equivalence; both additional bases remain arbitrary. -/
theorem exists_solution_iff_quartet :
    (∃ r : Variable → ℝ, ∀ e, realEval r (equationPolynomial e) = 0) ↔
      ∃ p : ParameterCoord → ℝ, (∀ e, eval p (parameterPolynomial e) = 0) ∧
        ∃ U V, Quartet (bases (parameterMatrix p) U V) := by
  constructor
  · rintro ⟨r,hr⟩
    exact ⟨parameters r,solution_parameter_equations r ((all_equations_zero_iff r).mp hr),
      normalize (basis r 1),normalize (basis r 2),quartet_of_solution r hr⟩
  · rintro ⟨p,hp,U,V,hq⟩
    rcases solution_of_quartet p U V hp hq with ⟨r,_,hr,_,_⟩
    exact ⟨r,hr⟩

#print axioms quartet_of_solution
#print axioms solution_of_quartet
#print axioms exists_solution_iff_quartet



/-- Separate real and imaginary polynomial degree bounds. -/
def ComplexDegree (p : CPoly) (n : ℕ) : Prop := p.1.totalDegree ≤ n ∧ p.2.totalDegree ≤ n

theorem degree_add {p q : QPoly} {n : ℕ} (hp : p.totalDegree ≤ n) (hq : q.totalDegree ≤ n) :
    (p+q).totalDegree ≤ n := (totalDegree_add p q).trans (max_le hp hq)

theorem degree_sub {p q : QPoly} {n : ℕ} (hp : p.totalDegree ≤ n) (hq : q.totalDegree ≤ n) :
    (p-q).totalDegree ≤ n := (totalDegree_sub p q).trans (max_le hp hq)

theorem degree_mul {p q : QPoly} {n m : ℕ} (hp : p.totalDegree ≤ n) (hq : q.totalDegree ≤ m) :
    (p*q).totalDegree ≤ n+m := (totalDegree_mul p q).trans (Nat.add_le_add hp hq)

theorem complexDegree_mono {p : CPoly} {n m : ℕ} (hp : ComplexDegree p n) (h : n ≤ m) :
    ComplexDegree p m := ⟨hp.1.trans h,hp.2.trans h⟩

theorem complexDegree_add {p q : CPoly} {n : ℕ} (hp : ComplexDegree p n) (hq : ComplexDegree q n) :
    ComplexDegree (p+q) n := ⟨degree_add hp.1 hq.1,degree_add hp.2 hq.2⟩

theorem complexDegree_sub {p q : CPoly} {n : ℕ} (hp : ComplexDegree p n) (hq : ComplexDegree q n) :
    ComplexDegree (p-q) n := ⟨degree_sub hp.1 hq.1,degree_sub hp.2 hq.2⟩

theorem complexDegree_star {p : CPoly} {n : ℕ} (hp : ComplexDegree p n) :
    ComplexDegree (cStar p) n := by
  simpa only [ComplexDegree,cStar,totalDegree_neg] using hp

theorem complexDegree_neg {p : CPoly} {n : ℕ} (hp : ComplexDegree p n) :
    ComplexDegree (cNeg p) n := by
  simpa only [ComplexDegree,cNeg,totalDegree_neg] using hp

theorem complexDegree_mul {p q : CPoly} {n m : ℕ}
    (hp : ComplexDegree p n) (hq : ComplexDegree q m) : ComplexDegree (cMul p q) (n+m) :=
  ⟨degree_sub (degree_mul hp.1 hq.1) (degree_mul hp.2 hq.2),
    degree_add (degree_mul hp.1 hq.2) (degree_mul hp.2 hq.1)⟩

theorem complexDegree_sum {ι : Type*} (s : Finset ι) (p : ι → CPoly) (n : ℕ)
    (h : ∀ i ∈ s, ComplexDegree (p i) n) : ComplexDegree (∑ i ∈ s,p i) n := by
  classical
  induction s using Finset.induction_on with
  | empty => simp [ComplexDegree]
  | @insert i s hi ih =>
    rw [Finset.sum_insert hi]
    exact complexDegree_add (h i (by simp)) (ih (fun j hj => h j (by simp [hj])))

theorem normPolynomial_degree {p : CPoly} {n : ℕ} (hp : ComplexDegree p n) :
    (normPolynomial p).totalDegree ≤ 2*n :=
  degree_add ((totalDegree_pow p.1 2).trans (Nat.mul_le_mul_left 2 hp.1))
    ((totalDegree_pow p.2 2).trans (Nat.mul_le_mul_left 2 hp.2))

theorem component_degree {p : CPoly} {n : ℕ} (hp : ComplexDegree p n) (b : Bool) :
    (component p b).totalDegree ≤ n := by cases b <;> [exact hp.1; exact hp.2]

theorem phasePolynomial_degree (i : Fin 4) : ComplexDegree (phasePolynomial i) 1 := by
  simp [ComplexDegree,phasePolynomial]

theorem basisPolynomial_degree (a : Fin 3) (i j : Fin 6) :
    ComplexDegree (basisPolynomial a i j) 1 := by simp [ComplexDegree,basisPolynomial]

theorem productPolynomial_degree (a : Fin 3) (i j : Fin 6) :
    ComplexDegree (productPolynomial a i j) 1 := by simp [ComplexDegree,productPolynomial]

theorem cOne_degree : ComplexDegree cOne 0 := by simp [ComplexDegree,cOne]

theorem phaseRowPolynomial_degree {x y : CPoly} (hx : ComplexDegree x 1) (hy : ComplexDegree y 1)
    (i : Fin 3) : ComplexDegree (phaseRowPolynomial x y i) 2 := by
  fin_cases i
  · exact complexDegree_mono cOne_degree (by decide)
  · exact complexDegree_mono hx (by decide)
  · exact complexDegree_mul hx hy

theorem pRaw_degree (a b : Fin 3 → CPoly) (n : ℕ)
    (ha : ∀ i, ComplexDegree (a i) n) (hb : ∀ i, ComplexDegree (b i) n) (i j : Fin 6) :
    ComplexDegree (pRaw a b i j) n := by
  unfold pRaw
  simp only [Matrix.submatrix_apply]
  cases hi : blockEquiv.symm i with
  | inl k =>
    cases hj : blockEquiv.symm j with
    | inl l => exact ha _
    | inr l => exact hb _
  | inr k =>
    cases hj : blockEquiv.symm j with
    | inl l => exact complexDegree_star (hb _)
    | inr l => exact complexDegree_neg (complexDegree_star (ha _))

theorem rawFamilyPolynomial_degree (i j : Fin 6) : ComplexDegree (rawFamilyPolynomial i j) 2 :=
  pRaw_degree _ _ 2 (phaseRowPolynomial_degree (phasePolynomial_degree 0) (phasePolynomial_degree 1))
    (phaseRowPolynomial_degree (phasePolynomial_degree 2) (phasePolynomial_degree 3)) i j

theorem gramPolynomial_degree (A B : PMatrix) (n m : ℕ)
    (ha : ∀ i j, ComplexDegree (A i j) n) (hb : ∀ i j, ComplexDegree (B i j) m) (i j : Fin 6) :
    ComplexDegree (gramPolynomial A B i j) (n+m) :=
  complexDegree_sum _ _ _ (fun k _ => complexDegree_mul (complexDegree_star (ha k i)) (hb k j))

theorem phaseSumPolynomial_degree {x y : CPoly} (hx : ComplexDegree x 1) (hy : ComplexDegree y 1) :
    ComplexDegree (phaseSumPolynomial x y) 2 :=
  complexDegree_add (complexDegree_mono (complexDegree_add hx hy) (by decide))
    (complexDegree_star (complexDegree_mul hx hy))

theorem compatibilityPolynomial_degree : ComplexDegree compatibilityPolynomial 2 :=
  complexDegree_add (phaseSumPolynomial_degree (phasePolynomial_degree 0) (phasePolynomial_degree 1))
    (phaseSumPolynomial_degree (phasePolynomial_degree 2) (phasePolynomial_degree 3))

theorem unitaryTarget_degree (i j : Fin 6) : ComplexDegree (unitaryTarget i j) 2 := by
  simp [ComplexDegree,unitaryTarget]

/-- Every coefficient is rational and every equation has total degree at most two. -/
theorem equation_degree (e : Equation) : (equationPolynomial e).totalDegree ≤ 2 := by
  rcases e with e | e
  · rcases e with i | b
    · exact degree_sub (normPolynomial_degree (phasePolynomial_degree i)) (by simp)
    · exact component_degree compatibilityPolynomial_degree b
  rcases e with e | e
  · rcases e with ⟨i,j,b⟩
    exact component_degree (complexDegree_sub
      (complexDegree_mono (basisPolynomial_degree 0 i j) (by decide)) (rawFamilyPolynomial_degree i j)) b
  rcases e with e | e
  · rcases e with ⟨a,i,j,b⟩
    exact component_degree (complexDegree_sub
      (gramPolynomial_degree _ _ 1 1 (basisPolynomial_degree _) (basisPolynomial_degree _) i j)
      (unitaryTarget_degree i j)) b
  rcases e with e | e
  · rcases e with ⟨a,i,j⟩
    exact degree_sub (normPolynomial_degree (basisPolynomial_degree _ i j)) (by simp)
  rcases e with e | e
  · rcases e with ⟨a,i,j,b⟩
    exact component_degree (complexDegree_sub
      (complexDegree_mono (productPolynomial_degree a i j) (by decide))
      (gramPolynomial_degree _ _ 1 1 (basisPolynomial_degree _) (basisPolynomial_degree _) i j)) b
  · rcases e with ⟨a,i,j⟩
    exact degree_sub (normPolynomial_degree (productPolynomial_degree a i j)) (by simp)

theorem solution_basis_unit (r : Variable → ℝ) (h : RawEquations r) (a : Fin 3) (i j : Fin 6) :
    basis r a i j * star (basis r a i j) = 1 := by
  fin_cases a
  · change basis r 0 i j * star (basis r 0 i j) = 1
    have hf := congrArg (fun M : Candidate => M i j) h.2.1
    rw [hf]
    exact rawBlock_entry_unit _ _ (phaseRow_unit _ _ h.1.1 h.1.2.1)
      (phaseRow_unit _ _ h.1.2.2.1 h.1.2.2.2.1) (blockEquiv.symm i) (blockEquiv.symm j)
  · exact (normSq_unit_iff _).mp (h.2.2.2.1 0 i j)
  · exact (normSq_unit_iff _).mp (h.2.2.2.1 1 i j)

theorem normSix_coordinates_bounded (z : ℂ) (h : Complex.normSq z = 6) :
    -3 ≤ z.re ∧ z.re ≤ 3 ∧ -3 ≤ z.im ∧ z.im ≤ 3 := by
  simp only [Complex.normSq_apply] at h
  have hre := sq_nonneg z.re
  have him := sq_nonneg z.im
  constructor
  · nlinarith [sq_nonneg (z.re+3)]
  constructor
  · nlinarith [sq_nonneg (z.re-3)]
  constructor
  · nlinarith [sq_nonneg (z.im+3)]
  · nlinarith [sq_nonneg (z.im-3)]

/-- Rational radii: one for phase and basis entries, three for cross products. -/
def radius : Variable → ℚ
  | .inl _ => 1
  | .inr (.inl _) => 1
  | .inr (.inr _) => 3

/-- A containing box for all solutions, including both variable additional bases. -/
theorem solution_in_full_box (r : Variable → ℝ)
    (h : ∀ e, realEval r (equationPolynomial e) = 0) :
    ∀ i, -(radius i : ℝ) ≤ r i ∧ r i ≤ (radius i : ℝ) := by
  have hr := (all_equations_zero_iff r).mp h
  intro i
  rcases i with q | q
  · simpa only [radius,Rat.cast_one,parameters] using
      parameter_solutions_in_unit_box _ (solution_parameter_equations r hr) q
  rcases q with q | q
  · rcases q with ⟨a,i,j,b⟩
    have hb := unit_phase_coordinates_bounded _ (solution_basis_unit r hr a i j)
    cases b
    · simpa [basis,basisPolynomial,complexEval,realEval,radius] using (And.intro hb.1 hb.2.1)
    · simpa [basis,basisPolynomial,complexEval,realEval,radius] using (And.intro hb.2.2.1 hb.2.2.2)
  · rcases q with ⟨a,i,j,b⟩
    have hb := normSix_coordinates_bounded _ (hr.2.2.2.2.2 a i j)
    cases b
    · simpa [product,productPolynomial,complexEval,realEval,radius] using (And.intro hb.1 hb.2.1)
    · simpa [product,productPolynomial,complexEval,realEval,radius] using (And.intro hb.2.2.1 hb.2.2.2)

#print axioms equation_degree
#print axioms solution_in_full_box



/-- The solution encoding also preserves each fixed phase parameter. -/
theorem exists_solution_with_parameters_iff (p : ParameterCoord → ℝ)
    (hp : ∀ e, eval p (parameterPolynomial e) = 0) :
    (∃ r, parameters r = p ∧ ∀ e, realEval r (equationPolynomial e) = 0) ↔
      ∃ U V, Quartet (bases (parameterMatrix p) U V) := by
  constructor
  · rintro ⟨r,hr,hz⟩
    refine ⟨normalize (basis r 1),normalize (basis r 2),?_⟩
    simpa only [hr] using quartet_of_solution r hz
  · rintro ⟨U,V,hq⟩
    rcases solution_of_quartet p U V hp hq with ⟨r,hr,hz,_,_⟩
    exact ⟨r,hr,hz⟩

/-- Restricting to the rational containing box loses no solutions. -/
theorem exists_bounded_solution_iff_quartet :
    (∃ r : Variable → ℝ, (∀ e, realEval r (equationPolynomial e) = 0) ∧
      ∀ i, -(radius i : ℝ) ≤ r i ∧ r i ≤ (radius i : ℝ)) ↔
      ∃ p : ParameterCoord → ℝ, (∀ e, eval p (parameterPolynomial e) = 0) ∧
        ∃ U V, Quartet (bases (parameterMatrix p) U V) := by
  rw [← exists_solution_iff_quartet]
  constructor
  · rintro ⟨r,hr,_⟩; exact ⟨r,hr⟩
  · rintro ⟨r,hr⟩; exact ⟨r,hr,solution_in_full_box r hr⟩

#print axioms exists_solution_with_parameters_iff
#print axioms exists_bounded_solution_iff_quartet

end MUB.SzollosiQuadraticSystem
