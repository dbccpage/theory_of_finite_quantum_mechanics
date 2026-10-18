import SzollosiExecutableSystem

/-!
# Rational interval semantics for the actual quartet expressions

AuthorityEffect: None.

Expression intervals enclose their checked real polynomial values for every
contained assignment. A successful residual zero-exclusion check therefore
excludes actual solutions in that box. The full containing box evaluates to
false under kernel reduction: this method has not excluded that box.

A small phase-interior box gives a reflected off-domain example. It contains
no admissible unit phase and supplies no exclusion of admissible quartets.
These AST intervals are distinct from native sparse-polynomial intervals;
no full native cover or Krawczyk soundness theorem is supplied here.
-/

namespace MUB.SzollosiIntervalExclusion
open SzollosiExecutableSystem SzollosiQuadraticSystem SzollosiTwoCirculant SzollosiQuartetSystem

structure Bounds where
  lo : Rat
  hi : Rat
  deriving DecidableEq, Repr

def Bounds.Contains (b : Bounds) (x : ℝ) : Prop := (b.lo : ℝ) ≤ x ∧ x ≤ (b.hi : ℝ)
def Bounds.point (q : Rat) : Bounds := ⟨q,q⟩
def Bounds.add (a b : Bounds) : Bounds := ⟨a.lo+b.lo,a.hi+b.hi⟩
def Bounds.neg (a : Bounds) : Bounds := ⟨-a.hi,-a.lo⟩
def Bounds.mul (a b : Bounds) : Bounds :=
  ⟨min (min (a.lo*b.lo) (a.lo*b.hi)) (min (a.hi*b.lo) (a.hi*b.hi)),
   max (max (a.lo*b.lo) (a.lo*b.hi)) (max (a.hi*b.lo) (a.hi*b.hi))⟩

theorem fixed_mul_bounds {l u x : ℝ} (h : l ≤ x ∧ x ≤ u) (z : ℝ) :
    min (l*z) (u*z) ≤ x*z ∧ x*z ≤ max (l*z) (u*z) := by
  by_cases hz : 0 ≤ z
  · exact ⟨(min_le_left _ _).trans (mul_le_mul_of_nonneg_right h.1 hz),
      (mul_le_mul_of_nonneg_right h.2 hz).trans (le_max_right _ _)⟩
  · have hz' : z ≤ 0 := le_of_not_ge hz
    exact ⟨(min_le_right _ _).trans (mul_le_mul_of_nonpos_right h.2 hz'),
      (mul_le_mul_of_nonpos_right h.1 hz').trans (le_max_left _ _)⟩

theorem contains_add {a b : Bounds} {x y : ℝ} (hx : a.Contains x) (hy : b.Contains y) :
    (a.add b).Contains (x+y) := by
  simp only [Bounds.Contains,Bounds.add,Rat.cast_add]
  exact ⟨add_le_add hx.1 hy.1,add_le_add hx.2 hy.2⟩

theorem contains_neg {a : Bounds} {x : ℝ} (hx : a.Contains x) : (a.neg).Contains (-x) := by
  simp only [Bounds.Contains,Bounds.neg,Rat.cast_neg]
  exact ⟨neg_le_neg hx.2,neg_le_neg hx.1⟩

theorem contains_mul {a b : Bounds} {x y : ℝ} (hx : a.Contains x) (hy : b.Contains y) :
    (a.mul b).Contains (x*y) := by
  have hxy := fixed_mul_bounds hx y
  have hlo := fixed_mul_bounds hy (a.lo : ℝ)
  have hhi := fixed_mul_bounds hy (a.hi : ℝ)
  simp only [mul_comm y, mul_comm (b.lo : ℝ), mul_comm (b.hi : ℝ)] at hlo hhi
  simp only [Bounds.Contains,Bounds.mul,Rat.cast_min,Rat.cast_max,Rat.cast_mul]
  exact ⟨(min_le_min hlo.1 hhi.1).trans hxy.1,hxy.2.trans (max_le_max hlo.2 hhi.2)⟩

def rangeExpr (box : Variable → Bounds) : Expr → Bounds
  | .constant q => Bounds.point q
  | .input v => box v
  | .add p q => (rangeExpr box p).add (rangeExpr box q)
  | .mul p q => (rangeExpr box p).mul (rangeExpr box q)
  | .neg p => (rangeExpr box p).neg

theorem expression_enclosed (box : Variable → Bounds) (r : Variable → ℝ)
    (hr : ∀ v, (box v).Contains (r v)) (e : Expr) :
    (rangeExpr box e).Contains (e.evalReal r) := by
  induction e with
  | constant q => exact ⟨le_rfl,le_rfl⟩
  | input v => exact hr v
  | add p q hp hq => exact contains_add hp hq
  | mul p q hp hq => exact contains_mul hp hq
  | neg p hp => exact contains_neg hp

theorem equation_enclosed (box : Variable → Bounds) (r : Variable → ℝ)
    (hr : ∀ v, (box v).Contains (r v)) (e : Equation) :
    (rangeExpr box (eEquation e)).Contains (realEval r (equationPolynomial e)) := by
  simpa only [evalReal_polynomial,expression_polynomial] using expression_enclosed box r hr (eEquation e)

def Bounds.excludesZero (b : Bounds) : Bool := decide (b.hi < 0) || decide (0 < b.lo)

theorem excludes_zero_sound (b : Bounds) (h : b.excludesZero = true) : ¬ b.Contains 0 := by
  intro hb
  simp only [Bounds.excludesZero,Bool.or_eq_true,decide_eq_true_eq] at h
  rcases h with h | h
  · have hh : (b.hi : ℝ) < 0 := by exact_mod_cast h
    exact (not_lt_of_ge hb.2) hh
  · have hl : (0 : ℝ) < b.lo := by exact_mod_cast h
    exact (not_lt_of_ge hb.1) hl

def exclusionCheck (box : Variable → Bounds) : Bool :=
  equations.any fun e => (rangeExpr box (eEquation e)).excludesZero

/-- A residual interval disjoint from zero excludes actual polynomial solutions. -/
theorem exclusion_check_sound (box : Variable → Bounds) (h : exclusionCheck box = true)
    (r : Variable → ℝ) (hr : ∀ v, (box v).Contains (r v)) :
    ¬ (∀ e, realEval r (equationPolynomial e) = 0) := by
  intro hz
  obtain ⟨e,_,he⟩ := List.any_eq_true.mp h
  have hb := equation_enclosed box r hr e
  rw [hz e] at hb
  exact excludes_zero_sound _ he hb

def fullBox (v : Variable) : Bounds := ⟨-eRadius v,eRadius v⟩

theorem solution_in_fullBox (r : Variable → ℝ) (h : ∀ e, realEval r (equationPolynomial e) = 0) :
    ∀ v, (fullBox v).Contains (r v) := by
  intro v
  simpa only [fullBox,Bounds.Contains,Rat.cast_neg,eRadius_eq] using solution_in_full_box r h v

/-- This implication requires an actual successful Boolean check, not a stored label. -/
theorem no_quartet_of_full_box_check (h : exclusionCheck fullBox = true) :
    ¬ ∃ p : ParameterCoord → ℝ, (∀ e, MvPolynomial.eval p (parameterPolynomial e) = 0) ∧
      ∃ U V, Quartet (bases (parameterMatrix p) U V) := by
  rw [← exists_solution_iff_quartet]
  rintro ⟨r,hr⟩
  exact exclusion_check_sound fullBox h r (solution_in_fullBox r hr) hr

set_option maxRecDepth 10000 in
set_option maxHeartbeats 2000000 in
theorem full_box_check_unresolved : exclusionCheck fullBox = false := by decide +kernel

/-- A concrete off-domain leaf: the first phase cannot have unit modulus here. -/
def phaseInteriorBox (v : Variable) : Bounds :=
  match v with
  | .inl (i,_) => if i=0 then ⟨-1/2,1/2⟩ else fullBox v
  | .inr _ => fullBox v

/-- This successful computation is a negative domain example, not a full cover. -/
theorem phase_interior_excluded : exclusionCheck phaseInteriorBox = true := by decide +kernel

theorem no_solution_in_phase_interior_box :
    ¬ ∃ r : Variable → ℝ, (∀ v, (phaseInteriorBox v).Contains (r v)) ∧
      (∀ e, realEval r (equationPolynomial e) = 0) := by
  rintro ⟨r,hbox,hzero⟩
  exact exclusion_check_sound phaseInteriorBox phase_interior_excluded r hbox hzero

#print axioms phase_interior_excluded
#print axioms no_solution_in_phase_interior_box
#print axioms expression_enclosed
#print axioms equation_enclosed
#print axioms exclusion_check_sound
#print axioms no_quartet_of_full_box_check
#print axioms full_box_check_unresolved
end MUB.SzollosiIntervalExclusion
