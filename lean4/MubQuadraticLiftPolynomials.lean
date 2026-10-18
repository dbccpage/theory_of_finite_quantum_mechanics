import MubQuadraticLift
import Mathlib.Algebra.QuadraticAlgebra.Basic

/-!
# Rational quadratic equations for the full quartet lift

AuthorityEffect: None.
The transition graph equations retain all three actual pairwise overlaps.
-/
noncomputable section
namespace MUB.QuadraticLiftPolynomials
open QuadraticLift BoundedBlockChart MonomialTransport
open BoundedCoordinates (fillE fillB fillC fillBasis)
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

def normPoly (p : CPoly) : Poly := p.re ^ 2 + p.im ^ 2

@[simp] theorem normPoly_eval (r : Coord → ℝ) (p : CPoly) :
    realEval r (normPoly p) = Complex.normSq (complexEval r p) := by
  simp [normPoly, complexEval, Complex.normSq_apply, pow_two]

def coordinatePoly (s : LiftSlot) : CPoly :=
  ⟨MvPolynomial.X (s, false), MvPolynomial.X (s, true)⟩

@[simp] theorem variable_eval (r : Coord → ℝ) (s : LiftSlot) :
    complexEval r (coordinatePoly s) = complexAt r s := by
  apply Complex.ext <;> simp [coordinatePoly, complexEval, complexAt, realEval]

def oldVariable (s : BoundedCoordinates.Slot) : CPoly := coordinatePoly (.inl s)
@[simp] theorem oldVariable_eval (r : Coord → ℝ) (s : BoundedCoordinates.Slot) :
    complexEval r (oldVariable s) = BoundedCoordinates.complexAt (base r) s := by
  exact variable_eval r (.inl s)

def pE : PMat3 := fillE (fun s => oldVariable (.inl s))
def pB : PMat3 := fillB (fun s => oldVariable (.inr (.inl s)))
def pC : PMat3 := fillC (fun s => oldVariable (.inr (.inr (.inl s))))
def pU : PMat6 := fillBasis (fun s => oldVariable (.inr (.inr (.inr (.inl s)))))
def pV : PMat6 := fillBasis (fun s => oldVariable (.inr (.inr (.inr (.inr s)))))

@[simp] theorem pE_eval (r : Coord → ℝ) : (complexEval r).mapMatrix pE = E r := by
  ext i j
  refine Fin.cases ?_ (fun k => ?_) i
  · simp [pE, E, BoundedCoordinates.decodeE, fillE]
  · refine Fin.cases ?_ (fun l => ?_) j <;> simp [pE, E, BoundedCoordinates.decodeE, fillE]

@[simp] theorem pB_eval (r : Coord → ℝ) : (complexEval r).mapMatrix pB = B r := by
  ext i j
  refine Fin.cases ?_ (fun k => ?_) i <;> simp [pB, B, BoundedCoordinates.decodeB, fillB]

@[simp] theorem pC_eval (r : Coord → ℝ) : (complexEval r).mapMatrix pC = C r := by
  ext i j
  refine Fin.cases ?_ (fun k => ?_) j <;> simp [pC, C, BoundedCoordinates.decodeC, fillC]

@[simp] theorem pU_eval (r : Coord → ℝ) : (complexEval r).mapMatrix pU = U r := by
  ext i j
  obtain ⟨k, rfl⟩ := blockIndex.symm.surjective i
  refine Fin.cases ?_ (fun l => ?_) k <;> simp [pU, U, BoundedCoordinates.decodeU, fillBasis]

@[simp] theorem pV_eval (r : Coord → ℝ) : (complexEval r).mapMatrix pV = V r := by
  ext i j
  obtain ⟨k, rfl⟩ := blockIndex.symm.surjective i
  refine Fin.cases ?_ (fun l => ?_) k <;> simp [pV, V, BoundedCoordinates.decodeV, fillBasis]

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

def pD : PMat3 := fun i j => coordinatePoly (.inr (.inl (i,j)))
def pW : Fin 3 → PMat6 := fun a i j => coordinatePoly (.inr (.inr (a,i,j)))
def pH : PMat6 := Matrix.fromBlocks pE pB pC pD

@[simp] theorem pD_eval (r : Coord → ℝ) : (complexEval r).mapMatrix pD = D r := by
  funext i j
  exact variable_eval r _
@[simp] theorem pW_eval (r : Coord → ℝ) (a : Fin 3) :
    (complexEval r).mapMatrix (pW a) = W r a := by
  funext i j
  exact variable_eval r _
@[simp] theorem pH_eval (r : Coord → ℝ) : (complexEval r).mapMatrix pH = H r := by
  have h : (complexEval r).mapMatrix pH = Matrix.fromBlocks
      ((complexEval r).mapMatrix pE) ((complexEval r).mapMatrix pB)
      ((complexEval r).mapMatrix pC) ((complexEval r).mapMatrix pD) := by
    funext i j
    cases i <;> cases j <;> rfl
  simpa only [pE_eval, pB_eval, pC_eval, pD_eval, H] using h

def pBases : Fin 3 → PMat6 := ![pH,pU,pV]
def bases (r : Coord → ℝ) : Fin 3 → Mat6 := ![H r,U r,V r]
def pTransitions : Fin 3 → PMat6 :=
  ![pH.conjTranspose * pU, pH.conjTranspose * pV, pU.conjTranspose * pV]

@[simp] theorem pBases_eval (r : Coord → ℝ) (a : Fin 3) :
    (complexEval r).mapMatrix (pBases a) = bases r a := by
  fin_cases a
  · exact pH_eval r
  · exact pU_eval r
  · exact pV_eval r
@[simp] theorem pTransitions_eval (r : Coord → ℝ) (a : Fin 3) :
    (complexEval r).mapMatrix (pTransitions a) = transitions (H r) (U r) (V r) a := by
  fin_cases a
  · change (complexEval r).mapMatrix (pH.conjTranspose * pU) = _
    rw [map_mul, matrixEval_star, pH_eval, pU_eval]
    rfl
  · change (complexEval r).mapMatrix (pH.conjTranspose * pV) = _
    rw [map_mul, matrixEval_star, pH_eval, pV_eval]
    rfl
  · change (complexEval r).mapMatrix (pU.conjTranspose * pV) = _
    rw [map_mul, matrixEval_star, pU_eval, pV_eval]
    rfl

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

def pGram (A : PMat6) : PMat6 := A.conjTranspose * A - (6 : CPoly) • 1

theorem gram_iff (r : Coord → ℝ) (A : PMat6) : ZeroMatrix r (pGram A) ↔
    ((complexEval r).mapMatrix A).conjTranspose * (complexEval r).mapMatrix A =
      (6 : ℂ) • (1 : Mat6) := by
  rw [zeroMatrix_iff]
  simp only [pGram, map_sub, map_mul, matrixEval_star, matrixEval_smul,
    map_ofNat, map_one, sub_eq_zero]

theorem hadamard_iff (r : Coord → ℝ) (A : PMat6) :
    UnitMatrix r A ∧ ZeroMatrix r (pGram A) ↔ RawHadamard ((complexEval r).mapMatrix A) := by
  rw [unitMatrix_iff, gram_iff]
  simp only [RawHadamard, I6, Fintype.card_sum, Fintype.card_fin, Nat.cast_add, Nat.cast_ofNat]
  norm_num

theorem graph_iff (r : Coord → ℝ) :
    (∀ a, ZeroMatrix r (pW a - pTransitions a)) ↔ W r = transitions (H r) (U r) (V r) := by
  simp only [zeroMatrix_iff, map_sub, pW_eval, pTransitions_eval, sub_eq_zero]
  exact ⟨fun h => funext h, fun h a => congrFun h a⟩

abbrev Equation := (Fin 3 × I6 × I6) ⊕ (Fin 3 × I6 × I6 × Bool) ⊕
  (Fin 3 × I6 × I6 × Bool) ⊕ (Fin 3 × I6 × I6)

theorem equation_count : Fintype.card Equation = 648 := by
  norm_num [Equation, I6, Fintype.card_sum, Fintype.card_prod]

def equationPolynomial : Equation → Poly
  | .inl (a,i,j) => normPoly (pBases a i j) - 1
  | .inr (.inl (a,i,j,b)) => component (pGram (pBases a) i j) b
  | .inr (.inr (.inl (a,i,j,b))) => component ((pW a - pTransitions a) i j) b
  | .inr (.inr (.inr (a,i,j))) => normPoly (pW a i j) - 6

def Solution (r : Coord → ℝ) : Prop := ∀ e, realEval r (equationPolynomial e) = 0

theorem solution_parts (r : Coord → ℝ) : Solution r ↔
    (∀ a, UnitMatrix r (pBases a)) ∧ (∀ a, ZeroMatrix r (pGram (pBases a))) ∧
    (∀ a, ZeroMatrix r (pW a - pTransitions a)) ∧
    (∀ a i j, realEval r (normPoly (pW a i j) - 6) = 0) := by
  constructor
  · intro h
    exact ⟨fun a i j => h (.inl (a,i,j)),
      fun a i j b => h (.inr (.inl (a,i,j,b))),
      fun a i j b => h (.inr (.inr (.inl (a,i,j,b)))),
      fun a i j => h (.inr (.inr (.inr (a,i,j))))⟩
  · rintro ⟨hu,hg,ht,hn⟩ e
    rcases e with ⟨a,i,j⟩ | ⟨a,i,j,b⟩ | ⟨a,i,j,b⟩ | ⟨a,i,j⟩
    · exact hu a i j
    · exact hg a i j b
    · exact ht a i j b
    · exact hn a i j

theorem solution_iff_system (r : Coord → ℝ) : Solution r ↔ System r := by
  have hn : (∀ a i j, realEval r (normPoly (pW a i j) - 6) = 0) ↔
      ∀ a i j, Complex.normSq (W r a i j) = 6 := by
    simp only [map_sub, normPoly_eval, map_ofNat, sub_eq_zero]
    simp only [pW, variable_eval, W]
  rw [solution_parts]
  constructor
  · rintro ⟨hu,hg,ht,hno⟩
    have hb (a : Fin 3) := (hadamard_iff r (pBases a)).mp ⟨hu a,hg a⟩
    simp only [pBases_eval] at hb
    exact ⟨hb 0,hb 1,hb 2,(graph_iff r).mp ht,hn.mp hno⟩
  · intro h
    have hb (a : Fin 3) : RawHadamard (bases r a) := by
      fin_cases a
      · exact h.rawH
      · exact h.rawU
      · exact h.rawV
    have hp (a : Fin 3) := (hadamard_iff r (pBases a)).mpr ((pBases_eval r a).symm ▸ hb a)
    exact ⟨fun a => (hp a).1,fun a => (hp a).2,(graph_iff r).mpr h.graph,hn.mpr h.overlapNorm⟩

theorem exists_quartet_iff_quadratic_solution :
    (∃ Q, SzollosiQuartetSystem.Quartet Q) ↔ ∃ r, Solution r ∧ InBox r := by
  rw [exists_quartet_iff_lift]
  simp_rw [solution_iff_system]

theorem overlap_norm_at_zero (a : Fin 3) (i j : I6) :
    realEval (fun _ => 0) (equationPolynomial (.inr (.inr (.inr (a,i,j))))) = -6 := by
  simp only [equationPolynomial, map_sub, map_ofNat, normPoly_eval, pW, variable_eval]
  norm_num [complexAt, Complex.normSq_apply]

theorem zero_not_solution : ¬ Solution (fun _ => 0) := by
  intro h
  have hn := h (.inr (.inr (.inr (0,Sum.inl 0,Sum.inl 0))))
  rw [overlap_norm_at_zero] at hn
  norm_num at hn

#print axioms equation_count
#print axioms pH_eval
#print axioms pTransitions_eval
#print axioms hadamard_iff
#print axioms graph_iff
#print axioms solution_parts
#print axioms solution_iff_system
#print axioms exists_quartet_iff_quadratic_solution
#print axioms overlap_norm_at_zero
#print axioms zero_not_solution
end MUB.QuadraticLiftPolynomials
