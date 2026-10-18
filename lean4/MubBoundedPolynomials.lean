import MubBoundedCoordinates
import Mathlib.Algebra.QuadraticAlgebra.Basic

/-!
# Rational polynomial specification for the full bounded quartet problem

AuthorityEffect: None.

Complex polynomial arithmetic uses the quadratic algebra with generator squared
equal to -1. Its two components are actual rational multivariate polynomials.
This is a semantic specification, not a coefficient export or an exclusion.
-/

noncomputable section
namespace MUB.BoundedPolynomials
open BoundedCoordinates BoundedBlockChart BoundedQuartetEquations MonomialTransport
open scoped BigOperators

abbrev Poly := MvPolynomial Coord ℚ
abbrev CPoly := QuadraticAlgebra Poly (-1) 0
abbrev PMat3 := Matrix I3 I3 CPoly
abbrev PMat6 := Matrix I6 I6 CPoly

def realEval (r : Coord → ℝ) : Poly →+* ℝ :=
  MvPolynomial.eval₂Hom (algebraMap ℚ ℝ) r

def complexEval (r : Coord → ℝ) : CPoly →+* ℂ where
  toFun p := ⟨realEval r p.re, realEval r p.im⟩
  map_zero' := by apply Complex.ext <;> simp
  map_one' := by apply Complex.ext <;> simp [QuadraticAlgebra.re_one, QuadraticAlgebra.im_one]
  map_add' p q := by apply Complex.ext <;> simp
  map_mul' p q := by
    apply Complex.ext <;>
      simp [QuadraticAlgebra.re_mul, QuadraticAlgebra.im_mul, Complex.mul_re,
        Complex.mul_im, sub_eq_add_neg]

@[simp] theorem complexEval_star (r : Coord → ℝ) (p : CPoly) :
    complexEval r (star p) = star (complexEval r p) := by
  apply Complex.ext <;> simp [complexEval]

def liftReal (p : Poly) : CPoly := algebraMap Poly CPoly p
def normPoly (p : CPoly) : Poly := p.re ^ 2 + p.im ^ 2

@[simp] theorem complexEval_liftReal (r : Coord → ℝ) (p : Poly) :
    complexEval r (liftReal p) = (realEval r p : ℂ) := by
  apply Complex.ext <;> simp [complexEval, liftReal]

@[simp] theorem normPoly_eval (r : Coord → ℝ) (p : CPoly) :
    realEval r (normPoly p) = Complex.normSq (complexEval r p) := by
  simp [normPoly, complexEval, Complex.normSq_apply, pow_two]

def coordinatePoly (s : Slot) : CPoly :=
  ⟨MvPolynomial.X (s, false), MvPolynomial.X (s, true)⟩

@[simp] theorem variable_eval (r : Coord → ℝ) (s : Slot) :
    complexEval r (coordinatePoly s) = complexAt r s := by
  apply Complex.ext <;> simp [coordinatePoly, complexEval, complexAt, realEval]

def pE : PMat3 := fillE (fun s => coordinatePoly (.inl s))
def pB : PMat3 := fillB (fun s => coordinatePoly (.inr (.inl s)))
def pC : PMat3 := fillC (fun s => coordinatePoly (.inr (.inr (.inl s))))
def pU : PMat6 := fillBasis (fun s => coordinatePoly (.inr (.inr (.inr (.inl s)))))
def pV : PMat6 := fillBasis (fun s => coordinatePoly (.inr (.inr (.inr (.inr s)))))

@[simp] theorem pE_eval (r : Coord → ℝ) : (complexEval r).mapMatrix pE = decodeE r := by
  ext i j
  refine Fin.cases ?_ (fun k => ?_) i
  · simp [pE, decodeE, fillE]
  · refine Fin.cases ?_ (fun l => ?_) j <;> simp [pE, decodeE, fillE]

@[simp] theorem pB_eval (r : Coord → ℝ) : (complexEval r).mapMatrix pB = decodeB r := by
  ext i j
  refine Fin.cases ?_ (fun k => ?_) i <;> simp [pB, decodeB, fillB]

@[simp] theorem pC_eval (r : Coord → ℝ) : (complexEval r).mapMatrix pC = decodeC r := by
  ext i j
  refine Fin.cases ?_ (fun k => ?_) j <;> simp [pC, decodeC, fillC]

@[simp] theorem pU_eval (r : Coord → ℝ) : (complexEval r).mapMatrix pU = decodeU r := by
  ext i j
  obtain ⟨k, rfl⟩ := blockIndex.symm.surjective i
  refine Fin.cases ?_ (fun l => ?_) k <;> simp [pU, decodeU, fillBasis]

@[simp] theorem pV_eval (r : Coord → ℝ) : (complexEval r).mapMatrix pV = decodeV r := by
  ext i j
  obtain ⟨k, rfl⟩ := blockIndex.symm.surjective i
  refine Fin.cases ?_ (fun l => ?_) k <;> simp [pV, decodeV, fillBasis]

@[simp] theorem matrixEval_star {ι : Type*} [Fintype ι] [DecidableEq ι]
    (r : Coord → ℝ) (A : Matrix ι ι CPoly) :
    (complexEval r).mapMatrix A.conjTranspose = ((complexEval r).mapMatrix A).conjTranspose := by
  ext i j
  exact complexEval_star r (A j i)

@[simp] theorem matrixEval_smul {ι : Type*} [Fintype ι] [DecidableEq ι]
    (r : Coord → ℝ) (p : CPoly) (A : Matrix ι ι CPoly) :
    (complexEval r).mapMatrix (p • A) = complexEval r p • (complexEval r).mapMatrix A := by
  ext i j
  exact map_mul (complexEval r) p (A i j)

def pQ : Poly := normPoly pB.det
def pD : CPoly := star pB.det
def pN : PMat3 := -(pC * pE.conjTranspose * pB.adjugate.conjTranspose)
def pS : PMat6 := Matrix.fromBlocks (pD • pE) (pD • pB) (pD • pC) pN

@[simp] theorem pQ_eval (r : Coord → ℝ) : realEval r pQ = detNorm (decodeB r) := by
  rw [pQ, normPoly_eval, RingHom.map_det]
  change Complex.normSq (((complexEval r).mapMatrix pB).det) = _
  rw [pB_eval]
  rfl

@[simp] theorem pD_eval (r : Coord → ℝ) : complexEval r pD = denominator (decodeB r) := by
  rw [pD, complexEval_star, RingHom.map_det]
  change star (((complexEval r).mapMatrix pB).det) = _
  rw [pB_eval]
  rfl

@[simp] theorem pN_eval (r : Coord → ℝ) :
    (complexEval r).mapMatrix pN = numerator (decodeE r) (decodeB r) (decodeC r) := by
  simp only [pN, map_neg, map_mul, matrixEval_star, RingHom.map_adjugate,
    pC_eval, pE_eval, pB_eval, numerator]

@[simp] theorem pS_eval (r : Coord → ℝ) :
    (complexEval r).mapMatrix pS = scaledCompletion (decodeE r) (decodeB r) (decodeC r) := by
  have hb : (complexEval r).mapMatrix pS = Matrix.fromBlocks
      ((complexEval r).mapMatrix (pD • pE)) ((complexEval r).mapMatrix (pD • pB))
      ((complexEval r).mapMatrix (pD • pC)) ((complexEval r).mapMatrix pN) := by
    ext i j
    cases i <;> cases j <;> rfl
  simpa only [matrixEval_smul, pD_eval, pE_eval, pB_eval, pC_eval, pN_eval,
    scaledCompletion] using hb

def component (p : CPoly) (b : Bool) : Poly := if b then p.im else p.re

theorem component_zero_iff (r : Coord → ℝ) (p : CPoly) :
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

def ZeroMatrix {ι : Type*} (r : Coord → ℝ) (A : Matrix ι ι CPoly) : Prop :=
  ∀ i j b, realEval r (component (A i j) b) = 0

theorem zeroMatrix_iff {ι : Type*} [Fintype ι] [DecidableEq ι]
    (r : Coord → ℝ) (A : Matrix ι ι CPoly) :
    ZeroMatrix r A ↔ (complexEval r).mapMatrix A = 0 := by
  unfold ZeroMatrix
  simp_rw [component_zero_iff]
  exact ⟨fun h => Matrix.ext h, fun h i j => congrFun (congrFun h i) j⟩

def UnitMatrix {ι : Type*} (r : Coord → ℝ) (A : Matrix ι ι CPoly) : Prop :=
  ∀ i j, realEval r (normPoly (A i j) - 1) = 0

theorem unitMatrix_iff {ι : Type*} [Fintype ι] [DecidableEq ι]
    (r : Coord → ℝ) (A : Matrix ι ι CPoly) :
    UnitMatrix r A ↔ ∀ i j, Complex.normSq ((complexEval r).mapMatrix A i j) = 1 := by
  simp only [UnitMatrix, map_sub, map_one, normPoly_eval, sub_eq_zero]
  rfl

def Overlap {ι : Type*} [Fintype ι] (r : Coord → ℝ)
    (A B : Matrix ι ι CPoly) (q : Poly) : Prop :=
  ∀ i j, realEval r (normPoly ((A.conjTranspose * B) i j) - q) = 0

theorem overlap_iff {ι : Type*} [Fintype ι] [DecidableEq ι] (r : Coord → ℝ)
    (A B : Matrix ι ι CPoly) (q : Poly) :
    Overlap r A B q ↔ ∀ i j,
      Complex.normSq ((((complexEval r).mapMatrix A).conjTranspose *
        (complexEval r).mapMatrix B) i j) = realEval r q := by
  have ht : (complexEval r).mapMatrix (A.conjTranspose * B) =
      ((complexEval r).mapMatrix A).conjTranspose * (complexEval r).mapMatrix B := by
    rw [map_mul, matrixEval_star]
  have he i j := congrFun (congrFun ht i) j
  simp only [Overlap, map_sub, normPoly_eval, sub_eq_zero]
  change (∀ i j, Complex.normSq ((complexEval r).mapMatrix (A.conjTranspose * B) i j) = _) ↔ _
  rw [ht]

def pTop : PMat3 := pE * pE.conjTranspose + pB * pB.conjTranspose - (6 : CPoly) • 1
def pBottom : PMat3 := liftReal pQ • (pC * pC.conjTranspose) +
  pN * pN.conjTranspose - (6 * liftReal pQ) • 1
def pGram (A : PMat6) : PMat6 := A.conjTranspose * A - (6 : CPoly) • 1

theorem top_iff (r : Coord → ℝ) : ZeroMatrix r pTop ↔
    decodeE r * (decodeE r).conjTranspose + decodeB r * (decodeB r).conjTranspose =
      (6 : ℂ) • (1 : Mat3) := by
  rw [zeroMatrix_iff]
  simp only [pTop, map_sub, map_add, map_mul, matrixEval_star, pE_eval, pB_eval,
    matrixEval_smul, map_ofNat, map_one, sub_eq_zero]

theorem bottom_iff (r : Coord → ℝ) : ZeroMatrix r pBottom ↔
    (detNorm (decodeB r) : ℂ) • (decodeC r * (decodeC r).conjTranspose) +
      numerator (decodeE r) (decodeB r) (decodeC r) *
        (numerator (decodeE r) (decodeB r) (decodeC r)).conjTranspose =
      (6 * (detNorm (decodeB r) : ℂ)) • (1 : Mat3) := by
  rw [zeroMatrix_iff]
  simp only [pBottom, map_sub, map_add, map_mul, matrixEval_star, pC_eval, pN_eval,
    matrixEval_smul, complexEval_liftReal, pQ_eval, map_ofNat, map_one, sub_eq_zero]

theorem gram_iff (r : Coord → ℝ) (A : PMat6) : ZeroMatrix r (pGram A) ↔
    ((complexEval r).mapMatrix A).conjTranspose * (complexEval r).mapMatrix A =
      (6 : ℂ) • (1 : Mat6) := by
  rw [zeroMatrix_iff]
  simp only [pGram, map_sub, map_mul, matrixEval_star, matrixEval_smul,
    map_ofNat, map_one, sub_eq_zero]

structure PolynomialSystem (r : Coord → ℝ) : Prop where
  unitE : UnitMatrix r pE
  unitB : UnitMatrix r pB
  unitC : UnitMatrix r pC
  determinant_bound : (54 / 5 : ℝ) ≤ realEval r pQ
  top : ZeroMatrix r pTop
  bottom : ZeroMatrix r pBottom
  numeratorNorm : ∀ i j, realEval r (normPoly (pN i j) - pQ) = 0
  unitU : UnitMatrix r pU
  unitV : UnitMatrix r pV
  gramU : ZeroMatrix r (pGram pU)
  gramV : ZeroMatrix r (pGram pV)
  muU : Overlap r pS pU (6 * pQ)
  muV : Overlap r pS pV (6 * pQ)
  muUV : Overlap r pU pV 6

theorem numeratorNorm_iff (r : Coord → ℝ) :
    (∀ i j, realEval r (normPoly (pN i j) - pQ) = 0) ↔
      ∀ i j, Complex.normSq (numerator (decodeE r) (decodeB r) (decodeC r) i j) =
        detNorm (decodeB r) := by
  simp only [map_sub, normPoly_eval, pQ_eval, sub_eq_zero]
  change (∀ i j, Complex.normSq ((complexEval r).mapMatrix pN i j) = _) ↔ _
  rw [pN_eval]

theorem polynomialSystem_iff_coordinates (r : Coord → ℝ) : PolynomialSystem r ↔ System r := by
  have hunitE := unitMatrix_iff r pE
  have hunitB := unitMatrix_iff r pB
  have hunitC := unitMatrix_iff r pC
  have hunitU := unitMatrix_iff r pU
  have hunitV := unitMatrix_iff r pV
  have hgramU := gram_iff r pU
  have hgramV := gram_iff r pV
  have hmuU := overlap_iff r pS pU (6 * pQ)
  have hmuV := overlap_iff r pS pV (6 * pQ)
  have hmuUV := overlap_iff r pU pV 6
  simp only [pE_eval, pB_eval, pC_eval, pU_eval, pV_eval, pS_eval,
    map_mul, map_ofNat, pQ_eval] at *
  obtain ⟨hrE, hcE, hrB, hcC, hrU, hrV⟩ := decode_gauges r
  constructor
  · intro h
    exact {
      unitE := hunitE.mp h.unitE, unitB := hunitB.mp h.unitB, unitC := hunitC.mp h.unitC
      rowE := hrE, columnE := hcE, rowB := hrB, columnC := hcC
      determinant_bound := (pQ_eval r) ▸ h.determinant_bound
      topGram := (top_iff r).mp h.top, bottomGram := (bottom_iff r).mp h.bottom
      numeratorNorm := (numeratorNorm_iff r).mp h.numeratorNorm
      rawU := ⟨hunitU.mp h.unitU, hgramU.mp h.gramU⟩
      rawV := ⟨hunitV.mp h.unitV, hgramV.mp h.gramV⟩
      rowU := hrU, rowV := hrV
      scaledMU_U := hmuU.mp h.muU, scaledMU_V := hmuV.mp h.muV
      muUV := hmuUV.mp h.muUV }
  · intro h
    exact {
      unitE := hunitE.mpr h.unitE, unitB := hunitB.mpr h.unitB, unitC := hunitC.mpr h.unitC
      determinant_bound := (pQ_eval r).symm ▸ h.determinant_bound
      top := (top_iff r).mpr h.topGram, bottom := (bottom_iff r).mpr h.bottomGram
      numeratorNorm := (numeratorNorm_iff r).mpr h.numeratorNorm
      unitU := hunitU.mpr h.rawU.1, unitV := hunitV.mpr h.rawV.1
      gramU := hgramU.mpr h.rawU.2, gramV := hgramV.mpr h.rawV.2
      muU := hmuU.mpr h.scaledMU_U, muV := hmuV.mpr h.scaledMU_V
      muUV := hmuUV.mpr h.muUV }

abbrev Equation := (Fin 3 × I3 × I3) ⊕ (I3 × I3) ⊕ (Fin 2 × I6 × I6) ⊕
  (Fin 3 × I6 × I6) ⊕ (Fin 2 × I3 × I3 × Bool) ⊕ (Fin 2 × I6 × I6 × Bool)

theorem equation_count : Fintype.card Equation = 396 := by
  norm_num [Equation, I3, I6, Fintype.card_sum, Fintype.card_prod]

def equationPolynomial : Equation → Poly
  | .inl (a, i, j) => normPoly (![pE, pB, pC] a i j) - 1
  | .inr (.inl (i, j)) => normPoly (pN i j) - pQ
  | .inr (.inr (.inl (a, i, j))) => normPoly (![pU, pV] a i j) - 1
  | .inr (.inr (.inr (.inl (a, i, j)))) =>
      ![normPoly ((pS.conjTranspose * pU) i j) - 6 * pQ,
        normPoly ((pS.conjTranspose * pV) i j) - 6 * pQ,
        normPoly ((pU.conjTranspose * pV) i j) - 6] a
  | .inr (.inr (.inr (.inr (.inl (a, i, j, b))))) => component (![pTop, pBottom] a i j) b
  | .inr (.inr (.inr (.inr (.inr (a, i, j, b))))) => component (pGram (![pU, pV] a) i j) b

def Solution (r : Coord → ℝ) : Prop :=
  (∀ e, realEval r (equationPolynomial e) = 0) ∧ (54 / 5 : ℝ) ≤ realEval r pQ

theorem solution_iff_polynomialSystem (r : Coord → ℝ) : Solution r ↔ PolynomialSystem r := by
  constructor
  · rintro ⟨h, hb⟩
    exact {
      unitE := fun i j => h (.inl (0, i, j))
      unitB := fun i j => h (.inl (1, i, j))
      unitC := fun i j => h (.inl (2, i, j))
      determinant_bound := hb
      top := fun i j b => h (.inr (.inr (.inr (.inr (.inl (0, i, j, b))))))
      bottom := fun i j b => h (.inr (.inr (.inr (.inr (.inl (1, i, j, b))))))
      numeratorNorm := fun i j => h (.inr (.inl (i, j)))
      unitU := fun i j => h (.inr (.inr (.inl (0, i, j))))
      unitV := fun i j => h (.inr (.inr (.inl (1, i, j))))
      gramU := fun i j b => h (.inr (.inr (.inr (.inr (.inr (0, i, j, b))))))
      gramV := fun i j b => h (.inr (.inr (.inr (.inr (.inr (1, i, j, b))))))
      muU := fun i j => h (.inr (.inr (.inr (.inl (0, i, j)))))
      muV := fun i j => h (.inr (.inr (.inr (.inl (1, i, j)))))
      muUV := fun i j => h (.inr (.inr (.inr (.inl (2, i, j))))) }
  · intro h
    refine ⟨?_, h.determinant_bound⟩
    rintro (⟨a, i, j⟩ | ⟨i, j⟩ | ⟨a, i, j⟩ | ⟨a, i, j⟩ | ⟨a, i, j, b⟩ | ⟨a, i, j, b⟩)
    · fin_cases a
      · exact h.unitE i j
      · exact h.unitB i j
      · exact h.unitC i j
    · exact h.numeratorNorm i j
    · fin_cases a
      · exact h.unitU i j
      · exact h.unitV i j
    · fin_cases a
      · exact h.muU i j
      · exact h.muV i j
      · exact h.muUV i j
    · fin_cases a
      · exact h.top i j b
      · exact h.bottom i j b
    · fin_cases a
      · exact h.gramU i j b
      · exact h.gramV i j b

theorem solution_iff_coordinates (r : Coord → ℝ) : Solution r ↔ System r :=
  (solution_iff_polynomialSystem r).trans (polynomialSystem_iff_coordinates r)

theorem solution_inBox (r : Coord → ℝ) (h : Solution r) : InBox r :=
  system_inBox r ((solution_iff_coordinates r).mp h)

theorem exists_quartet_iff_polynomials :
    (∃ Q : Fin 4 → Mat (Fin 6), SzollosiQuartetSystem.Quartet Q) ↔
      ∃ r : Coord → ℝ, Solution r ∧ InBox r := by
  rw [exists_quartet_iff_coordinates]
  simp_rw [solution_iff_coordinates]

theorem no_quartet_iff_no_polynomials :
    (∀ Q : Fin 4 → Mat (Fin 6), ¬ SzollosiQuartetSystem.Quartet Q) ↔
      ∀ r : Coord → ℝ, InBox r → ¬ Solution r := by
  rw [no_quartet_iff_no_coordinates]
  simp_rw [solution_iff_coordinates]

#print axioms complexEval_star
#print axioms normPoly_eval
#print axioms pE_eval
#print axioms pB_eval
#print axioms pC_eval
#print axioms pU_eval
#print axioms pV_eval
#print axioms pQ_eval
#print axioms pD_eval
#print axioms pN_eval
#print axioms pS_eval
#print axioms component_zero_iff
#print axioms zeroMatrix_iff
#print axioms unitMatrix_iff
#print axioms overlap_iff
#print axioms top_iff
#print axioms bottom_iff
#print axioms gram_iff
#print axioms numeratorNorm_iff
#print axioms polynomialSystem_iff_coordinates
#print axioms equation_count
#print axioms solution_iff_polynomialSystem
#print axioms solution_iff_coordinates
#print axioms solution_inBox
#print axioms exists_quartet_iff_polynomials
#print axioms no_quartet_iff_no_polynomials
end MUB.BoundedPolynomials
