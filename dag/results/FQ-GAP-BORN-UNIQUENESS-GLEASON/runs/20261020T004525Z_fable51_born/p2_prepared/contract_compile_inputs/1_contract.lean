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
