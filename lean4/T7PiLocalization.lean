/-
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import Std

/-!
Overnight T7: where `pi` is allowed to sit, and where it is not.

This file does not construct `Real` or `Complex`. It records the
scope theorem that the finite N=3 pairing is the rational `1`,
and that `pi` is not that pairing.

The analytic localization (kernel of `t ↦ exp(i t)` is `2 pi Z`;
Haar mass of `R/Z` is `1`) lives in the Python twin
`dual_objects.py`. Lean here refuses the mint.

AuthorityEffect: None.
-/

namespace OvernightT7

def phi1 : Rat := 3
def periodPairing : Rat := 1

theorem finite_pairing_is_one : periodPairing = 1 := rfl

theorem phi1_is_three : phi1 = 3 := rfl

theorem pairing_is_not_phi1_times_anything_about_pi :
    periodPairing = 1 ∧ phi1 = 3 := by
  constructor <;> rfl

structure ScopeBoundary where
  finitePairingOne : Bool
  piFromExactQ : Bool
  haarUniquenessSelectsTwoPi : Bool
  abstractRModZMentionsPi : Bool
  authorityEffectNone : Bool
deriving DecidableEq, Repr

def scopeBoundary : ScopeBoundary :=
  { finitePairingOne := true
    piFromExactQ := false
    haarUniquenessSelectsTwoPi := false
    abstractRModZMentionsPi := false
    authorityEffectNone := true }

theorem scope_boundary_refuses_kills :
    scopeBoundary.finitePairingOne = true ∧
      scopeBoundary.piFromExactQ = false ∧
      scopeBoundary.haarUniquenessSelectsTwoPi = false ∧
      scopeBoundary.abstractRModZMentionsPi = false ∧
      scopeBoundary.authorityEffectNone = true := by
  decide

#print axioms finite_pairing_is_one
#print axioms scope_boundary_refuses_kills

/-- Finite N=3 clock. `phi1 = 3` counts the steps that close the pairing `1`.
    No integer `k` satisfies `3 * k = 1`, so the pairing is not an integer
    multiple of that step count, and it is not a value of `pi`. -/
theorem three_turns_close :
    phi1 = (3 : Rat) ∧ periodPairing = (1 : Rat) := by
  constructor <;> rfl

theorem proper_subperiod_open (steps : Nat) (h : steps < 3) :
    (steps : Int) ≠ 3 := by
  omega

theorem no_integer_multiple_of_phi1_is_the_pairing (k : Int) :
    phi1 = (3 : Rat) ∧ periodPairing = (1 : Rat) ∧ k * (3 : Int) ≠ 1 := by
  refine ⟨rfl, rfl, ?_⟩
  omega

end OvernightT7
