import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Omega

/-! AuthorityEffect: None. Exact rational aggregate and bounded rank/level
admission. This does not validate all fusion laws or mechanize allocation. -/
namespace TFQM.FusionAdmission

def liftRatio (n d : Int) : Option Rat :=
  if d=0 then none else some ((n : Rat)/(d : Rat))

def aggregate (values : List Rat) (total : Rat) : Prop := values.sum=total ∧ 0<total

theorem zero_denominator_refused (n : Int) : liftRatio n 0=none := by simp [liftRatio]

theorem exact_lift (n d : Int) (hd : d≠0) : liftRatio n d=some ((n : Rat)/(d : Rat)) := by
  simp [liftRatio,hd]

theorem aggregate_exact (values : List Rat) (total : Rat) :
    aggregate values total ↔ values.sum=total ∧ 0<total := Iff.rfl

theorem aggregate_nonpositive (values : List Rat) (total : Rat) (h : total≤0) :
    ¬aggregate values total := by
  intro hgood
  exact (not_lt_of_ge h) hgood.2

theorem aggregate_permutation (values other : List Rat) (h : values.Perm other) (total : Rat) :
    aggregate values total ↔ aggregate other total := by
  simp only [aggregate,h.sum_eq]

theorem cancellation_preserves_aggregate (values : List Rat) (x total : Rat) :
    aggregate (x::(-x)::values) total ↔ aggregate values total := by
  simp [aggregate]

theorem sum_step (values : List Rat) (x : Rat) : (x::values).sum=x+values.sum := rfl

def rankAdmitted (r : Nat) : Prop := 0<r ∧ r≤32

theorem rank_admission (r : Nat) : rankAdmitted r ↔ 1≤r ∧ r≤32 := by
  simp [rankAdmitted]

theorem bounded_cube (r : Nat) (h : rankAdmitted r) : r*r*r≤32768 := by
  exact Nat.le_trans (Nat.mul_le_mul (Nat.mul_le_mul h.2 h.2) h.2) (by decide)

theorem admitted_level (k : Nat) : (0<k ∧ rankAdmitted (k+1)) ↔ 1≤k ∧ k≤31 := by
  unfold rankAdmitted
  omega

theorem level_addition_fits (k maximum : Nat) (hk : k≤31) (hm : 32≤maximum) : k+1≤maximum := by omega

theorem maximum_level_overflows (maximum : Nat) : ¬maximum+1≤maximum := by omega

theorem su2_subtraction_exact (k i j : Nat) (hi : i≤k) (hj : j≤k) :
    i+j≤2*k := by omega

#print axioms zero_denominator_refused
#print axioms exact_lift
#print axioms aggregate_exact
#print axioms aggregate_nonpositive
#print axioms aggregate_permutation
#print axioms cancellation_preserves_aggregate
#print axioms sum_step
#print axioms rank_admission
#print axioms bounded_cube
#print axioms admitted_level
#print axioms level_addition_fits
#print axioms maximum_level_overflows
#print axioms su2_subtraction_exact
end TFQM.FusionAdmission
