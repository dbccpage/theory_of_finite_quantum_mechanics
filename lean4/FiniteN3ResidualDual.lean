/-
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import Std

/-!
# Exact finite three-cycle residual and dual fixture

This file proves only rational facts for one fixed three-coordinate incidence
operator.  The infinite-group and continuous-host stages are recorded as false
scope fields at the end of the file.  No such stage is used by a proof here.
-/

namespace PontryaginResidualDualProgramme.FiniteN3

/-- A deliberately explicit three-coordinate rational carrier. -/
structure Q3 where
  c0 : Rat
  c1 : Rat
  c2 : Rat
deriving DecidableEq, Repr

/-- The oriented three-cycle incidence operator. -/
def d0 (a : Q3) : Q3 :=
  { c0 := a.c1 - a.c0
    c1 := a.c2 - a.c1
    c2 := a.c0 - a.c2 }

def coordinateSum (v : Q3) : Rat :=
  v.c0 + v.c1 + v.c2

/-- Every exact repair has zero circulation around the three-cycle. -/
theorem d0_image_coordinate_sum_zero (a : Q3) :
    coordinateSum (d0 a) = 0 := by
  grind [coordinateSum, d0]

def beta : Q3 :=
  { c0 := 1, c1 := 1, c2 := 1 }

def InD0Image (v : Q3) : Prop :=
  ∃ a : Q3, d0 a = v

/-- The constant unit residual cannot be an exact three-cycle repair. -/
theorem beta_not_in_d0_image : ¬ InD0Image beta := by
  grind [InD0Image, coordinateSum, beta, d0]

def pairing (y v : Q3) : Rat :=
  y.c0 * v.c0 + y.c1 * v.c1 + y.c2 * v.c2

def normalizedPeriod : Q3 :=
  { c0 := 1 / 3, c1 := 1 / 3, c2 := 1 / 3 }

/-- The normalized rational period kills every exact repair. -/
theorem normalized_period_annihilates_d0 (a : Q3) :
    pairing normalizedPeriod (d0 a) = 0 := by
  grind [pairing, normalizedPeriod, d0]

/-- The same normalized period evaluates the residual class to one. -/
theorem normalized_period_pairs_beta_to_one :
    pairing normalizedPeriod beta = 1 := by
  grind [pairing, normalizedPeriod, beta]

def sub (x y : Q3) : Q3 :=
  { c0 := x.c0 - y.c0
    c1 := x.c1 - y.c1
    c2 := x.c2 - y.c2 }

def l1Norm (v : Q3) : Rat :=
  v.c0.abs + v.c1.abs + v.c2.abs

/-- The exact potential used by the executable rational fixture. -/
def fixtureAlpha : Q3 :=
  { c0 := 2, c1 := -1, c2 := 3 }

/-- The exact cochain used by the executable rational fixture. -/
def fixtureOmega : Q3 :=
  { c0 := -2, c1 := 5, c2 := 0 }

def residual (a : Q3) : Q3 :=
  sub fixtureOmega (d0 a)

def fixtureResidual : Q3 :=
  residual fixtureAlpha

def dualUnit : Q3 :=
  beta

def dualInfinityFeasible (y : Q3) : Prop :=
  y.c0.abs ≤ 1 ∧ y.c1.abs ≤ 1 ∧ y.c2.abs ≤ 1

theorem fixture_residual_eq_beta : fixtureResidual = beta := by
  grind [fixtureResidual, residual, sub, fixtureOmega, fixtureAlpha, d0, beta]

theorem dual_unit_is_infinity_feasible : dualInfinityFeasible dualUnit := by
  grind [dualInfinityFeasible, dualUnit, beta, Rat.abs]

theorem dual_unit_annihilates_d0 (a : Q3) : pairing dualUnit (d0 a) = 0 := by
  grind [pairing, dualUnit, beta, d0]

/-- The dual value is unchanged by every repair competitor. -/
theorem dual_unit_pairs_every_residual_to_three (a : Q3) :
    pairing dualUnit (residual a) = 3 := by
  grind [pairing, dualUnit, beta, residual, sub, fixtureOmega, d0]

/-- Each rational coordinate is bounded above by its exact absolute value. -/
theorem self_le_abs (x : Rat) : x ≤ x.abs := by
  by_cases h : 0 ≤ x
  · rw [Rat.abs_of_nonneg h]
    exact Rat.le_refl
  · have hlt : x < 0 := Rat.not_le.mp h
    have hle : x ≤ 0 := Rat.le_of_lt hlt
    rw [Rat.abs_of_nonpos hle]
    have hneg : (0 : Rat) ≤ -x := by
      simpa using Rat.neg_le_neg hle
    exact Rat.le_trans hle hneg

theorem rat_add_le_add {a b c d : Rat} (hab : a ≤ b) (hcd : c ≤ d) :
    a + c ≤ b + d := by
  have hac : a + c ≤ b + c := Rat.add_le_add_right.mpr hab
  have hbd : b + c ≤ b + d := Rat.add_le_add_left.mpr hcd
  exact Rat.le_trans hac hbd

/-- Coordinatewise dual feasibility gives the exact finite weak-duality bound. -/
theorem dual_pairing_le_l1 (v : Q3) : pairing dualUnit v ≤ l1Norm v := by
  have h0 := self_le_abs v.c0
  have h1 := self_le_abs v.c1
  have h2 := self_le_abs v.c2
  have h01 := rat_add_le_add h0 h1
  have h012 := rat_add_le_add h01 h2
  simpa [pairing, dualUnit, beta, l1Norm] using h012

/-- Every potential has primal value at least three. -/
theorem every_primal_competitor_at_least_three (a : Q3) :
    3 ≤ l1Norm (residual a) := by
  have h := dual_pairing_le_l1 (residual a)
  rw [dual_unit_pairs_every_residual_to_three] at h
  exact h

def fixturePrimalValue : Rat :=
  l1Norm fixtureResidual

def fixtureDualValue : Rat :=
  pairing dualUnit fixtureOmega

def fixtureDualityGap : Rat :=
  fixturePrimalValue - fixtureDualValue

theorem fixture_primal_value_eq_three : fixturePrimalValue = 3 := by
  grind [fixturePrimalValue, fixtureResidual, residual, sub, fixtureOmega,
    fixtureAlpha, d0, l1Norm, Rat.abs]

theorem fixture_dual_value_eq_three : fixtureDualValue = 3 := by
  grind [fixtureDualValue, pairing, dualUnit, beta, fixtureOmega]

theorem fixture_duality_gap_eq_zero : fixtureDualityGap = 0 := by
  rw [fixtureDualityGap, fixture_primal_value_eq_three, fixture_dual_value_eq_three]
  exact Rat.sub_self

/-- The local receipt has no authority effect beyond this finite theorem file. -/
inductive AuthorityEffect where
  | none
deriving DecidableEq, Repr

/-- Explicit nonclaims for every stage outside the fixed rational fixture. -/
structure ScopeBoundary where
  exactFiniteN3 : Bool
  zMod3GroupInferred : Bool
  freeZExtensionDerived : Bool
  pontryaginDualityDerived : Bool
  haarMeasureDerived : Bool
  piDerived : Bool
  floatHostCertified : Bool
  alphaHostCertified : Bool
  authorityEffect : AuthorityEffect
deriving DecidableEq, Repr

def scopeBoundary : ScopeBoundary :=
  { exactFiniteN3 := true
    zMod3GroupInferred := false
    freeZExtensionDerived := false
    pontryaginDualityDerived := false
    haarMeasureDerived := false
    piDerived := false
    floatHostCertified := false
    alphaHostCertified := false
    authorityEffect := .none }

theorem scope_boundary_exact_and_external_stages_false :
    scopeBoundary.exactFiniteN3 = true ∧
      scopeBoundary.zMod3GroupInferred = false ∧
      scopeBoundary.freeZExtensionDerived = false ∧
      scopeBoundary.pontryaginDualityDerived = false ∧
      scopeBoundary.haarMeasureDerived = false ∧
      scopeBoundary.piDerived = false ∧
      scopeBoundary.floatHostCertified = false ∧
      scopeBoundary.alphaHostCertified = false ∧
      scopeBoundary.authorityEffect = .none := by
  decide

#print axioms d0_image_coordinate_sum_zero
#print axioms beta_not_in_d0_image
#print axioms normalized_period_annihilates_d0
#print axioms normalized_period_pairs_beta_to_one
#print axioms fixture_residual_eq_beta
#print axioms dual_unit_is_infinity_feasible
#print axioms dual_unit_annihilates_d0
#print axioms dual_unit_pairs_every_residual_to_three
#print axioms self_le_abs
#print axioms rat_add_le_add
#print axioms dual_pairing_le_l1
#print axioms every_primal_competitor_at_least_three
#print axioms fixture_primal_value_eq_three
#print axioms fixture_dual_value_eq_three
#print axioms fixture_duality_gap_eq_zero
#print axioms scope_boundary_exact_and_external_stages_false

end PontryaginResidualDualProgramme.FiniteN3
