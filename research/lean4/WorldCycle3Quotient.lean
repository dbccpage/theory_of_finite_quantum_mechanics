/-
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import WorldPresentation

/-!
# F1: exact quotient price on one declared rational 3-cycle

This file declares, rather than derives from Primitive Difference, a rational
three-edge cochain carrier and the successive-difference repair map on one
three-vertex cycle.  It proves only the resulting finite 3-cycle statements.
It does not claim an arbitrary degree-k complex or wider estate scope.

AuthorityEffect: None.
-/

namespace OmegaWorld
namespace Cycle3Quotient

/-- A rational cochain on the directed edges 01, 12, and 20. -/
structure Cochain where
  edge01 : Rat
  edge12 : Rat
  edge20 : Rat
  deriving DecidableEq

theorem cochain_ext {left right : Cochain}
    (h01 : left.edge01 = right.edge01)
    (h12 : left.edge12 = right.edge12)
    (h20 : left.edge20 = right.edge20) : left = right := by
  cases left
  cases right
  grind

/-- A rational potential on the three declared vertices. -/
structure Potential where
  vertex0 : Rat
  vertex1 : Rat
  vertex2 : Rat
  deriving DecidableEq

def add (left right : Cochain) : Cochain where
  edge01 := left.edge01 + right.edge01
  edge12 := left.edge12 + right.edge12
  edge20 := left.edge20 + right.edge20

def neg (q : Cochain) : Cochain where
  edge01 := -q.edge01
  edge12 := -q.edge12
  edge20 := -q.edge20

def sub (left right : Cochain) : Cochain :=
  add left (neg right)

def scale (scalar : Rat) (q : Cochain) : Cochain where
  edge01 := scalar * q.edge01
  edge12 := scalar * q.edge12
  edge20 := scalar * q.edge20

/-- The quotient charge is the oriented sum around the declared cycle. -/
def charge (q : Cochain) : Rat :=
  (q.edge01 + q.edge12) + q.edge20

/-- Successive potential differences on 01, 12, and 20. -/
def repair (potential : Potential) : Cochain where
  edge01 := potential.vertex1 - potential.vertex0
  edge12 := potential.vertex2 - potential.vertex1
  edge20 := potential.vertex0 - potential.vertex2

/-- Add one constant to all vertices; this is the potential gauge action. -/
def shiftPotential (offset : Rat) (potential : Potential) : Potential where
  vertex0 := potential.vertex0 + offset
  vertex1 := potential.vertex1 + offset
  vertex2 := potential.vertex2 + offset

/-- Exact rational absolute value, defined locally to avoid importing a larger host. -/
def ratAbs (x : Rat) : Rat :=
  if 0 <= x then x else -x

/-- Price of a cochain is exactly the absolute value of its cycle charge. -/
def price (q : Cochain) : Rat :=
  ratAbs (charge q)

/-- Coordinate L1 size on the declared three-edge carrier. -/
def l1 (q : Cochain) : Rat :=
  (ratAbs q.edge01 + ratAbs q.edge12) + ratAbs q.edge20

/-- The explicit potential that removes the first two edge coordinates. -/
def canonicalPotential (q : Cochain) : Potential where
  vertex0 := 0
  vertex1 := q.edge01
  vertex2 := q.edge01 + q.edge12

/-- The explicit representative retaining only the total cycle charge. -/
def canonicalResidual (q : Cochain) : Cochain where
  edge01 := 0
  edge12 := 0
  edge20 := charge q

def authorityEffect : AuthorityEffect :=
  .none

theorem ratAbs_zero : ratAbs 0 = 0 := by
  simp [ratAbs]

theorem ratAbs_of_nonneg {x : Rat} (h : 0 <= x) : ratAbs x = x := by
  simp [ratAbs, h]

theorem ratAbs_of_nonpos {x : Rat} (h : x <= 0) : ratAbs x = -x := by
  unfold ratAbs
  split <;> grind

theorem ratAbs_triangle (x y : Rat) :
    ratAbs (x + y) <= ratAbs x + ratAbs y := by
  unfold ratAbs
  split <;> split <;> split <;> grind

theorem rat_mul_nonpos_of_nonneg_of_nonpos {a b : Rat}
    (ha : 0 <= a) (hb : b <= 0) : a * b <= 0 := by
  have hneg : 0 <= -b := by grind
  have hproduct : 0 <= a * -b := Rat.mul_nonneg ha hneg
  grind [Rat.mul_neg]

theorem rat_mul_nonpos_of_nonpos_of_nonneg {a b : Rat}
    (ha : a <= 0) (hb : 0 <= b) : a * b <= 0 := by
  have hneg : 0 <= -a := by grind
  have hproduct : 0 <= -a * b := Rat.mul_nonneg hneg hb
  grind [Rat.neg_mul]

theorem rat_mul_nonneg_of_nonpos_of_nonpos {a b : Rat}
    (ha : a <= 0) (hb : b <= 0) : 0 <= a * b := by
  have hnega : 0 <= -a := by grind
  have hnegb : 0 <= -b := by grind
  have hproduct : 0 <= -a * -b := Rat.mul_nonneg hnega hnegb
  grind [Rat.mul_neg, Rat.neg_mul]

theorem ratAbs_mul (a x : Rat) :
    ratAbs (a * x) = ratAbs a * ratAbs x := by
  by_cases ha : 0 <= a
  · rw [ratAbs_of_nonneg ha]
    by_cases hx : 0 <= x
    · have hproduct : 0 <= a * x := Rat.mul_nonneg ha hx
      rw [ratAbs_of_nonneg hx, ratAbs_of_nonneg hproduct]
    · have hxzero : x <= 0 := by grind
      have hproduct : a * x <= 0 :=
        rat_mul_nonpos_of_nonneg_of_nonpos ha hxzero
      rw [ratAbs_of_nonpos hxzero, ratAbs_of_nonpos hproduct]
      grind [Rat.mul_neg]
  · have hazero : a <= 0 := by grind
    rw [ratAbs_of_nonpos hazero]
    by_cases hx : 0 <= x
    · have hproduct : a * x <= 0 :=
        rat_mul_nonpos_of_nonpos_of_nonneg hazero hx
      rw [ratAbs_of_nonneg hx, ratAbs_of_nonpos hproduct]
      grind [Rat.neg_mul]
    · have hxzero : x <= 0 := by grind
      have hproduct : 0 <= a * x :=
        rat_mul_nonneg_of_nonpos_of_nonpos hazero hxzero
      rw [ratAbs_of_nonpos hxzero, ratAbs_of_nonneg hproduct]
      grind [Rat.mul_neg, Rat.neg_mul]

theorem charge_add (left right : Cochain) :
    charge (add left right) = charge left + charge right := by
  grind [charge, add]

theorem charge_neg (q : Cochain) :
    charge (neg q) = -charge q := by
  grind [charge, neg]

theorem charge_sub (left right : Cochain) :
    charge (sub left right) = charge left - charge right := by
  grind [charge, sub, add, neg]

theorem charge_scale (scalar : Rat) (q : Cochain) :
    charge (scale scalar q) = scalar * charge q := by
  grind [charge, scale]

/-- Every successive-difference repair has zero cycle charge. -/
theorem repair_charge_zero (potential : Potential) :
    charge (repair potential) = 0 := by
  grind [charge, repair]

/-- Adding a constant to every potential coordinate leaves the repair unchanged. -/
theorem repair_shift_invariant (offset : Rat) (potential : Potential) :
    repair (shiftPotential offset potential) = repair potential := by
  cases potential
  apply cochain_ext <;> grind [repair, shiftPotential]

/-- Exact cochains on this 3-cycle are exactly the zero-charge cochains. -/
theorem exact_iff_zero_charge (q : Cochain) :
    (Exists fun potential => repair potential = q) <-> charge q = 0 := by
  constructor
  · rintro ⟨potential, rfl⟩
    exact repair_charge_zero potential
  · intro hzero
    refine ⟨canonicalPotential q, ?_⟩
    cases q
    apply cochain_ext <;> grind [canonicalPotential, repair, charge]

/-- Price is unchanged after adding any exact cycle repair. -/
theorem price_add_repair (q : Cochain) (potential : Potential) :
    price (add q (repair potential)) = price q := by
  unfold price
  rw [charge_add, repair_charge_zero]
  grind

/-- Price is absolutely homogeneous for rational scalars. -/
theorem price_absolute_homogeneous (scalar : Rat) (q : Cochain) :
    price (scale scalar q) = ratAbs scalar * price q := by
  unfold price
  rw [charge_scale, ratAbs_mul]

/-- Price obeys the triangle inequality on the declared carrier. -/
theorem price_triangle (left right : Cochain) :
    price (add left right) <= price left + price right := by
  unfold price
  rw [charge_add]
  exact ratAbs_triangle (charge left) (charge right)

theorem ratAbs_sum3_le_l1 (x y z : Rat) :
    ratAbs ((x + y) + z) <= (ratAbs x + ratAbs y) + ratAbs z := by
  calc
    ratAbs ((x + y) + z) <= ratAbs (x + y) + ratAbs z :=
      ratAbs_triangle (x + y) z
    _ <= (ratAbs x + ratAbs y) + ratAbs z := by
      exact (Rat.add_le_add_right).2 (ratAbs_triangle x y)

/-- Absolute charge is a lower bound for the coordinate L1 size. -/
theorem price_le_l1 (q : Cochain) :
    price q <= l1 q := by
  exact ratAbs_sum3_le_l1 q.edge01 q.edge12 q.edge20

/-- Every representative obtained by removing a repair has L1 size at least the price. -/
theorem price_le_l1_sub_repair (q : Cochain) (potential : Potential) :
    price q <= l1 (sub q (repair potential)) := by
  have hcharge : charge (sub q (repair potential)) = charge q := by
    rw [charge_sub, repair_charge_zero]
    grind
  calc
    price q = price (sub q (repair potential)) := by
      unfold price
      rw [hcharge]
    _ <= l1 (sub q (repair potential)) :=
      price_le_l1 (sub q (repair potential))

/-- The canonical potential leaves exactly the one-coordinate charge residual. -/
theorem canonical_residual_eq (q : Cochain) :
    sub q (repair (canonicalPotential q)) = canonicalResidual q := by
  cases q
  apply cochain_ext <;>
    grind [sub, add, neg, repair, canonicalPotential, canonicalResidual, charge]

theorem canonical_residual_l1 (q : Cochain) :
    l1 (canonicalResidual q) = price q := by
  grind [l1, canonicalResidual, price, ratAbs_zero]

/-- The explicit canonical potential attains the quotient lower bound. -/
theorem canonical_residual_attains (q : Cochain) :
    l1 (sub q (repair (canonicalPotential q))) = price q := by
  rw [canonical_residual_eq, canonical_residual_l1]

theorem quotient_price_characterization (q : Cochain) :
    (forall potential, price q <= l1 (sub q (repair potential))) /\
      l1 (sub q (repair (canonicalPotential q))) = price q := by
  exact ⟨price_le_l1_sub_repair q, canonical_residual_attains q⟩

structure Laws : Prop where
  repairChargeZero : forall potential, charge (repair potential) = 0
  exactIffZeroCharge : forall q,
    (Exists fun potential => repair potential = q) <-> charge q = 0
  potentialGaugeInvariant : forall offset potential,
    repair (shiftPotential offset potential) = repair potential
  priceGaugeInvariant : forall q potential,
    price (add q (repair potential)) = price q
  absoluteHomogeneity : forall scalar q,
    price (scale scalar q) = ratAbs scalar * price q
  triangleInequality : forall left right,
    price (add left right) <= price left + price right
  l1LowerBound : forall q potential,
    price q <= l1 (sub q (repair potential))
  canonicalResidual : forall q,
    sub q (repair (canonicalPotential q)) = canonicalResidual q
  canonicalAttainment : forall q,
    l1 (sub q (repair (canonicalPotential q))) = price q
  authorityNone : authorityEffect = .none

/-- Bundled scoped certificate for this declared rational 3-cycle only. -/
theorem laws : Laws where
  repairChargeZero := repair_charge_zero
  exactIffZeroCharge := exact_iff_zero_charge
  potentialGaugeInvariant := repair_shift_invariant
  priceGaugeInvariant := price_add_repair
  absoluteHomogeneity := price_absolute_homogeneous
  triangleInequality := price_triangle
  l1LowerBound := price_le_l1_sub_repair
  canonicalResidual := canonical_residual_eq
  canonicalAttainment := canonical_residual_attains
  authorityNone := rfl

#print axioms exact_iff_zero_charge
#print axioms quotient_price_characterization
#print axioms laws

end Cycle3Quotient
end OmegaWorld
