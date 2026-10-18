import MubBalancedQuadraticLift
import Mathlib.Algebra.MvPolynomial.Monad

/-!
# The original 648 equations after affine reduction to 320 real coordinates

AuthorityEffect: None. Substitution preserves evaluation and the degree-two
upper bound. No coefficient-file export or infeasibility result is asserted.
-/

noncomputable section
namespace MUB.BalancedQuadraticPolynomials
open BalancedQuadraticLift BoundedBlockChart
open scoped BigOperators

abbrev Poly := MvPolynomial Coord ℚ
abbrev CPoly := QuadraticAlgebra Poly (-1) 0

def realEval (r : Coord → ℝ) : Poly →+* ℝ := MvPolynomial.eval₂Hom (algebraMap ℚ ℝ) r
def complexEval (r : Coord → ℝ) : CPoly →+* ℂ where
  toFun p := ⟨realEval r p.re,realEval r p.im⟩
  map_zero' := by apply Complex.ext <;> simp
  map_one' := by apply Complex.ext <;> simp [QuadraticAlgebra.re_one,QuadraticAlgebra.im_one]
  map_add' p q := by apply Complex.ext <;> simp
  map_mul' p q := by
    apply Complex.ext <;> simp [QuadraticAlgebra.re_mul,QuadraticAlgebra.im_mul,
      Complex.mul_re,Complex.mul_im,sub_eq_add_neg]

def pCore (a : Fin 3) : Matrix (Fin 5) (Fin 5) CPoly := fun i j =>
  ⟨MvPolynomial.X (.inr (.inr (a,i,j)),false),MvPolynomial.X (.inr (.inr (a,i,j)),true)⟩

theorem pCore_eval (r : Coord → ℝ) (a : Fin 3) (i j : Fin 5) :
    complexEval r (pCore a i j) = core r a i j := by
  apply Complex.ext <;> simp [complexEval,realEval,pCore,core]

theorem completed_core_eval (r : Coord → ℝ) (a : Fin 3) (i j : Fin 6) :
    complexEval r (BalancedCompletion.complete (pCore a) i j) =
      BalancedCompletion.complete (core r a) i j := by
  refine Fin.lastCases ?_ (fun k => ?_) i
  · refine Fin.lastCases ?_ (fun l => ?_) j
    · simp only [BalancedCompletion.complete_corner,map_sub,map_sum,map_ofNat,pCore_eval]
    · simp only [BalancedCompletion.complete_last_row,map_sub,map_sum,map_ofNat,pCore_eval]
  · refine Fin.lastCases ?_ (fun l => ?_) j
    · simp only [BalancedCompletion.complete_last_column,map_sub,map_sum,map_ofNat,pCore_eval]
    · simp only [BalancedCompletion.complete_core,pCore_eval]

def component (p : CPoly) (b : Bool) : Poly := if b then p.im else p.re

def replacement : QuadraticLift.Coord → Poly
  | (.inl s,b) => MvPolynomial.X (.inl s,b)
  | (.inr (.inl (i,j)),b) => MvPolynomial.X (.inr (.inl (i,j)),b)
  | (.inr (.inr (a,i,j)),b) =>
      component (BalancedCompletion.complete (pCore a) (blockIndex i) (blockIndex j)) b

theorem replacement_eval (r : Coord → ℝ) (c : QuadraticLift.Coord) :
    realEval r (replacement c) = expand r c := by
  rcases c with ⟨s,b⟩
  rcases s with s | ⟨i,j⟩ | ⟨a,i,j⟩
  · simp [replacement,realEval,expand]
  · simp [replacement,realEval,expand]
  · have h := completed_core_eval r a (blockIndex i) (blockIndex j)
    cases b
    · exact congrArg Complex.re h
    · exact congrArg Complex.im h

def substitute : QuadraticLiftPolynomials.Poly →ₐ[ℚ] Poly := MvPolynomial.bind₁ replacement

theorem substitute_eval (r : Coord → ℝ) (p : QuadraticLiftPolynomials.Poly) :
    realEval r (substitute p) = QuadraticLiftPolynomials.realEval (expand r) p := by
  simp only [substitute,realEval,MvPolynomial.eval₂Hom_bind₁]
  change MvPolynomial.eval₂Hom (algebraMap ℚ ℝ) (fun c => realEval r (replacement c)) p = _
  simp only [replacement_eval]
  rfl

def equationPolynomial (e : QuadraticLiftPolynomials.Equation) : Poly :=
  substitute (QuadraticLiftPolynomials.equationPolynomial e)
def Solution (r : Coord → ℝ) : Prop := ∀ e, realEval r (equationPolynomial e) = 0

theorem solution_iff_system (r : Coord → ℝ) : Solution r ↔ System r := by
  change (∀ e, realEval r (substitute (QuadraticLiftPolynomials.equationPolynomial e)) = 0) ↔ _
  simp_rw [substitute_eval]
  exact QuadraticLiftPolynomials.solution_iff_system (expand r)

theorem exists_quartet_iff_balanced_polynomials :
    (∃ Q, SzollosiQuartetSystem.Quartet Q) ↔ ∃ r, Solution r ∧ InBox r := by
  rw [exists_quartet_iff_balanced_lift]
  simp_rw [solution_iff_system]

def Affine (p : CPoly) : Prop := p.re.totalDegree ≤ 1 ∧ p.im.totalDegree ≤ 1

theorem affine_sub {p q : CPoly} (hp : Affine p) (hq : Affine q) : Affine (p-q) :=
  ⟨(MvPolynomial.totalDegree_sub _ _).trans (max_le hp.1 hq.1),
    (MvPolynomial.totalDegree_sub _ _).trans (max_le hp.2 hq.2)⟩

theorem affine_sum {ι : Type*} (s : Finset ι) (f : ι → CPoly) (h : ∀ i ∈ s, Affine (f i)) :
    Affine (∑ i ∈ s, f i) := by
  classical
  induction s using Finset.induction_on with
  | empty => simp [Affine]
  | @insert a s ha ih =>
    rw [Finset.sum_insert ha]
    have hp := h a (Finset.mem_insert_self _ _)
    have hq := ih (fun i hi => h i (Finset.mem_insert_of_mem hi))
    exact ⟨(MvPolynomial.totalDegree_add _ _).trans (max_le hp.1 hq.1),
      (MvPolynomial.totalDegree_add _ _).trans (max_le hp.2 hq.2)⟩

theorem pCore_affine (a : Fin 3) (i j : Fin 5) : Affine (pCore a i j) := by
  simp [Affine,pCore]

theorem completed_core_affine (a : Fin 3) (i j : Fin 6) :
    Affine (BalancedCompletion.complete (pCore a) i j) := by
  have h6 : Affine (6 : CPoly) := by
    change (MvPolynomial.C (6 : ℚ)).totalDegree ≤ 1 ∧ (0 : Poly).totalDegree ≤ 1
    simp
  have h24 : Affine (24 : CPoly) := by
    change (MvPolynomial.C (24 : ℚ)).totalDegree ≤ 1 ∧ (0 : Poly).totalDegree ≤ 1
    simp
  have hrow (k : Fin 5) : Affine (∑ l, pCore a k l) :=
    affine_sum _ _ (fun l _ => pCore_affine a k l)
  have hcol (l : Fin 5) : Affine (∑ k, pCore a k l) :=
    affine_sum _ _ (fun k _ => pCore_affine a k l)
  refine Fin.lastCases ?_ (fun k => ?_) i
  · refine Fin.lastCases ?_ (fun l => ?_) j
    · rw [BalancedCompletion.complete_corner]
      exact affine_sub (affine_sum _ _ (fun k _ => hrow k)) h24
    · rw [BalancedCompletion.complete_last_row]
      exact affine_sub h6 (hcol l)
  · refine Fin.lastCases ?_ (fun l => ?_) j
    · rw [BalancedCompletion.complete_last_column]
      exact affine_sub h6 (hrow k)
    · rw [BalancedCompletion.complete_core]
      exact pCore_affine a k l

theorem replacement_degree (c : QuadraticLift.Coord) : (replacement c).totalDegree ≤ 1 := by
  rcases c with ⟨s,b⟩
  rcases s with s | ⟨i,j⟩ | ⟨a,i,j⟩
  · simp [replacement]
  · simp [replacement]
  · have h := completed_core_affine a (blockIndex i) (blockIndex j)
    cases b
    · exact h.1
    · exact h.2

theorem affine_substitution_degree {σ τ : Type*} (f : σ → MvPolynomial τ ℚ)
    (hf : ∀ s, (f s).totalDegree ≤ 1) (p : MvPolynomial σ ℚ) :
    (MvPolynomial.bind₁ f p).totalDegree ≤ p.totalDegree := by
  classical
  conv_lhs => rw [p.as_sum]
  rw [map_sum]
  apply MvPolynomial.totalDegree_finsetSum_le
  intro d hd
  rw [MvPolynomial.bind₁_monomial]
  apply (MvPolynomial.totalDegree_mul _ _).trans
  simp only [MvPolynomial.totalDegree_C,zero_add]
  apply (MvPolynomial.totalDegree_finsetProd _ _).trans
  apply le_trans (Finset.sum_le_sum (fun i _ =>
    (MvPolynomial.totalDegree_pow _ _).trans (by simpa using Nat.mul_le_mul_left (d i) (hf i))))
  exact MvPolynomial.le_totalDegree hd

theorem equation_degree (e : QuadraticLiftPolynomials.Equation) :
    (equationPolynomial e).totalDegree ≤ 2 :=
  (affine_substitution_degree replacement replacement_degree _).trans
    (QuadraticLiftPolynomials.equation_degree e)

#print axioms pCore_eval
#print axioms completed_core_eval
#print axioms replacement_eval
#print axioms substitute_eval
#print axioms solution_iff_system
#print axioms exists_quartet_iff_balanced_polynomials
#print axioms completed_core_affine
#print axioms replacement_degree
#print axioms affine_substitution_degree
#print axioms equation_degree
end MUB.BalancedQuadraticPolynomials
