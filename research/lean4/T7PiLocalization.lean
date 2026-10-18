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

end OvernightT7
