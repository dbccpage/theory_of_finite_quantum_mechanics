import Mathlib

/- Effect-additive Busch-type inputs; not a Gleason proof. -/
namespace BornFable

structure OrderedQUnit (V : Type*) [AddCommGroup V] [Module ℚ V] where
  le : V → V → Prop
  le_refl : ∀ x, le x x
  le_trans : ∀ x y z, le x y → le y z → le x z
  add_le_add_right : ∀ x y z, le x y → le (x + z) (y + z)
  smul_nonneg : ∀ (q : ℚ) (x : V), 0 ≤ q → le 0 x → le 0 (q • x)
  u : V
  u_nonneg : le 0 u

variable {V : Type*} [AddCommGroup V] [Module ℚ V]

def OrderedQUnit.Effect (S : OrderedQUnit V) (a : V) : Prop := S.le 0 a ∧ S.le a S.u

structure EffectValuation (S : OrderedQUnit V) where
  v : V → ℚ
  unit : v S.u = 1
  nonneg : ∀ a, S.Effect a → 0 ≤ v a
  additive : ∀ a b, S.Effect a → S.Effect b → S.Effect (a + b) → v (a + b) = v a + v b


end BornFable

namespace BornMatrixCheck
abbrev M := Fin 3 → ℚ
def qf (A : M) (x y : ℚ) : ℚ := A 0*x*x + 2*A 1*x*y + A 2*y*y
def unitM : M := (fun i => if i.val = 0 then 1 else if i.val = 1 then 0 else 1)
def leM (A B : M) : Prop := ∀ x y : ℚ, qf A x y ≤ qf B x y
lemma qf_add (A B : M) (x y : ℚ) : qf (A+B) x y = qf A x y + qf B x y := by
  dsimp [qf]
  ring
lemma qf_scale (q : ℚ) (A : M) (x y : ℚ) : qf (q • A) x y = q * qf A x y := by
  simp only [qf, Pi.smul_apply, smul_eq_mul]
  ring
lemma qf_zero (x y : ℚ) : qf (0 : M) x y = 0 := by simp [qf]
def space : BornFable.OrderedQUnit M where
  le := leM
  le_refl := by intro A x y; exact le_rfl
  le_trans := by intro A B C h h' x y; exact le_trans (h x y) (h' x y)
  add_le_add_right := by
    intro A B C h x y
    change qf (A+C) x y ≤ qf (B+C) x y
    rw [qf_add, qf_add]
    simpa [add_comm] using (_root_.add_le_add_right (h x y) (qf C x y))
  smul_nonneg := by
    intro q A hq hA x y
    rw [qf_zero, qf_scale]
    exact mul_nonneg hq (by simpa [qf] using hA x y)
  u := unitM
  u_nonneg := by
    intro x y
    norm_num [leM, qf, unitM]
    nlinarith [sq_nonneg x, sq_nonneg y]
def a : M := (fun i => if i.val = 0 then 1 else 0)
def b : M := (fun i => if i.val = 0 then 4/5 else if i.val = 1 then -2/5 else 1/5)
def e22 : M := (fun i => if i.val = 2 then 1 else 0)
theorem a_effect : space.Effect a := by
  constructor <;> intro x y <;> norm_num [space, leM, qf, a, unitM]
  · nlinarith [sq_nonneg x]
  · nlinarith [sq_nonneg y]
theorem b_effect : space.Effect b := by
  constructor <;> intro x y <;> norm_num [space, leM, qf, b, unitM]
  · nlinarith [sq_nonneg (2*x-y)]
  · nlinarith [sq_nonneg (x+2*y)]
theorem e22_effect : space.Effect e22 := by
  constructor <;> intro x y <;> norm_num [space, leM, qf, e22, unitM]
  · nlinarith [sq_nonneg y]
  · nlinarith [sq_nonneg x]
theorem lower_half_bound : space.le (-((1/2 : ℚ) • space.u)) (a-b) := by
  intro x y
  norm_num [space, leM, qf, a, b, unitM, Pi.smul_apply, smul_eq_mul]
  nlinarith [sq_nonneg (7*x+4*y), sq_nonneg y]
theorem upper_half_bound : space.le (a-b) ((1/2 : ℚ) • space.u) := by
  intro x y
  norm_num [space, leM, qf, a, b, unitM, Pi.smul_apply, smul_eq_mul]
  nlinarith [sq_nonneg (3*x-4*y), sq_nonneg y]
def positiveControl : BornFable.EffectValuation space where
  v A := A 0
  unit := by norm_num [space, unitM]
  nonneg := by
    intro A hA
    have h := hA.1 1 0
    simpa [space, leM, qf] using h
  additive := by intro A B _ _ _; rfl
theorem control_values : positiveControl.v a = 1 ∧ positiveControl.v b = 4/5 := by
  norm_num [positiveControl, a, b]
def badLinear (A : M) : ℚ := 2*A 0-A 2
theorem bad_unital : badLinear space.u = 1 := by norm_num [badLinear, space, unitM]
theorem bad_additive (A B : M) : badLinear (A+B) = badLinear A + badLinear B := by
  dsimp [badLinear]
  ring
theorem bad_not_positive : badLinear e22 = -1 := by norm_num [badLinear, e22]
#print axioms a_effect
#print axioms b_effect
#print axioms lower_half_bound
#print axioms upper_half_bound
#print axioms control_values
#print axioms bad_unital
#print axioms bad_additive
#print axioms bad_not_positive
end BornMatrixCheck
