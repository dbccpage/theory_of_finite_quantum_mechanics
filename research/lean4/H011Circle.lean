/-
  H011Circle -- exclude the sign group under a named extra.
  AuthorityEffect: None. Candidate only. Not PROVEN.

  QM_122 remaining job 7.1.3 / STACK item 1. Mixing leftover
  already runs on {+1,-1} (H011.sign_carrier_suffices). The
  named extra is: the phase carrier is not of exponent two.
  That is the discrete shadow of QM_062's connectedness residue
  (a connected one-parameter generator cannot live on two points
  of order dividing two). This host has no topology, so the extra
  is that discrete shadow, written as a proposition, not a Bool
  flag.

  Under the extra the sign group is excluded. The extra does not
  select the circle: Gaussian units and a three-cycle both meet
  it. The circle group is not constructed here. Continuity of a
  one-parameter phase group remains an imported hypothesis.

  AuthorityEffect: None
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import HWKernel
import H010InterferenceNonDescent
import H011U1SelectorBoundary

namespace FableHilbertWalk20260819.H011Circle

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H010

/-- A phase carrier: a subset closed under a supplied composition
    law with a unit. Composition is the only law the extra uses. -/
structure PhaseCarrier (G : Type) where
  mem : G → Prop
  mul : G → G → G
  one : G
  mem_one : mem one
  mem_mul : ∀ a b, mem a → mem b → mem (mul a b)

/-- Named extra, theorem-grade: some phase unit squares away from
    the identity. English name: not of exponent two. QM_062's
    analytic form is connectedness of a one-parameter generator.
    The Bool field `carrier_connectedness` in H011 is not this. -/
def ConnectednessShadow {G : Type} (P : PhaseCarrier G) : Prop :=
  ∃ u, P.mem u ∧ P.mul u u ≠ P.one

/-! ## Sign group {+1, -1} inside Int. -/

def isSign (a : Int) : Prop :=
  a = 1 ∨ a = -1

theorem isSign_mul (a b : Int) (ha : isSign a) (hb : isSign b) :
    isSign (a * b) := by
  rcases ha with ha | ha <;> rcases hb with hb | hb
  · subst ha; subst hb; exact Or.inl rfl
  · subst ha; subst hb; exact Or.inr rfl
  · subst ha; subst hb; exact Or.inr rfl
  · subst ha; subst hb; exact Or.inl rfl

#print axioms isSign_mul

theorem sign_every_square_is_one (a : Int) (h : isSign a) :
    a * a = 1 := by
  rcases h with h | h <;> subst h <;> decide

#print axioms sign_every_square_is_one

def signCarrier : PhaseCarrier Int where
  mem := isSign
  mul := (· * ·)
  one := 1
  mem_one := Or.inl rfl
  mem_mul := isSign_mul

/-- The sign group fails the named extra. -/
theorem sign_fails_connectedness_shadow :
    ¬ ConnectednessShadow signCarrier := by
  intro h
  rcases h with ⟨u, hu, hne⟩
  exact hne (sign_every_square_is_one u hu)

#print axioms sign_fails_connectedness_shadow

/-- Any carrier meeting the extra is not of exponent two, so it
    is not the sign group. -/
theorem sign_excluded_under_connectedness_shadow
    {G : Type} (P : PhaseCarrier G) (h : ConnectednessShadow P) :
    ¬ ∀ u, P.mem u → P.mul u u = P.one := by
  intro hall
  rcases h with ⟨u, hu, hne⟩
  exact hne (hall u hu)

#print axioms sign_excluded_under_connectedness_shadow

/-! ## Gaussian units meet the extra (i² = -1). -/

def isGaussUnit (z : GaussInt) : Prop :=
  z = GaussInt.gone ∨ z = GaussInt.gneg GaussInt.gone ∨
    z = GaussInt.gi ∨ z = GaussInt.gneg GaussInt.gi

theorem isGaussUnit_mul (a b : GaussInt)
    (ha : isGaussUnit a) (hb : isGaussUnit b) :
    isGaussUnit (GaussInt.gmul a b) := by
  rcases ha with ha | ha | ha | ha <;>
    rcases hb with hb | hb | hb | hb
  · subst ha; subst hb; exact Or.inl rfl
  · subst ha; subst hb; exact Or.inr (Or.inl rfl)
  · subst ha; subst hb; exact Or.inr (Or.inr (Or.inl rfl))
  · subst ha; subst hb; exact Or.inr (Or.inr (Or.inr rfl))
  · subst ha; subst hb; exact Or.inr (Or.inl rfl)
  · subst ha; subst hb; exact Or.inl rfl
  · subst ha; subst hb; exact Or.inr (Or.inr (Or.inr rfl))
  · subst ha; subst hb; exact Or.inr (Or.inr (Or.inl rfl))
  · subst ha; subst hb; exact Or.inr (Or.inr (Or.inl rfl))
  · subst ha; subst hb; exact Or.inr (Or.inr (Or.inr rfl))
  · subst ha; subst hb; exact Or.inr (Or.inl rfl)
  · subst ha; subst hb; exact Or.inl rfl
  · subst ha; subst hb; exact Or.inr (Or.inr (Or.inr rfl))
  · subst ha; subst hb; exact Or.inr (Or.inr (Or.inl rfl))
  · subst ha; subst hb; exact Or.inl rfl
  · subst ha; subst hb; exact Or.inr (Or.inl rfl)

#print axioms isGaussUnit_mul

def gaussUnitCarrier : PhaseCarrier GaussInt where
  mem := isGaussUnit
  mul := GaussInt.gmul
  one := GaussInt.gone
  mem_one := Or.inl rfl
  mem_mul := isGaussUnit_mul

theorem gi_sq_ne_one :
    GaussInt.gmul GaussInt.gi GaussInt.gi ≠ GaussInt.gone := by
  intro h
  have hre :
      (GaussInt.gmul GaussInt.gi GaussInt.gi).re = GaussInt.gone.re :=
    congrArg GaussInt.re h
  simp [GaussInt.gmul, GaussInt.gi, GaussInt.gone] at hre

#print axioms gi_sq_ne_one

theorem gauss_units_meet_connectedness_shadow :
    ConnectednessShadow gaussUnitCarrier :=
  ⟨GaussInt.gi, Or.inr (Or.inr (Or.inl rfl)), gi_sq_ne_one⟩

#print axioms gauss_units_meet_connectedness_shadow

/-! ## A three-cycle also meets the extra. The extra therefore
    does not select the four Gaussian units, let alone the circle. -/

def cyc3Carrier : PhaseCarrier (Fin 3) where
  mem := fun _ => True
  mul := (· + ·)
  one := 0
  mem_one := trivial
  mem_mul := fun _ _ _ _ => trivial

theorem cyc3_one_double_ne_zero : (1 : Fin 3) + 1 ≠ 0 := by
  decide

#print axioms cyc3_one_double_ne_zero

theorem cyc3_meets_connectedness_shadow :
    ConnectednessShadow cyc3Carrier :=
  ⟨1, trivial, cyc3_one_double_ne_zero⟩

#print axioms cyc3_meets_connectedness_shadow

/-- Punchline: under the named extra the sign group is excluded;
    two non-isomorphic survivors meet the extra; without the extra
    mixing leftover still runs on plus-and-minus-one. The circle
    group is not among the objects constructed here. -/
theorem sign_excluded_circle_still_imported :
    ¬ ConnectednessShadow signCarrier ∧
      ConnectednessShadow gaussUnitCarrier ∧
      ConnectednessShadow cyc3Carrier ∧
      (∀ q : Bool, iWeights iPsi1 q = iWeights iPsi2 q) ∧
      ¬ (∀ q : Bool, iReadout iPsi1 q = iReadout iPsi2 q) :=
  ⟨sign_fails_connectedness_shadow,
    gauss_units_meet_connectedness_shadow,
    cyc3_meets_connectedness_shadow,
    int_realization.1, int_realization.2⟩

#print axioms sign_excluded_circle_still_imported

end FableHilbertWalk20260819.H011Circle
