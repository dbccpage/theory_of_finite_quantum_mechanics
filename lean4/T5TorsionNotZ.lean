
import Std





namespace OvernightT5

def IsTorsion (x : Int) : Prop :=
  ∃ n : Nat, 0 < n ∧ (n : Int) * x = 0

theorem one_not_torsion : ¬ IsTorsion 1 := by
  intro h
  rcases h with ⟨n, hn, heq⟩
  have : (n : Int) = 0 := by
    simpa using heq
  exact Nat.ne_of_gt hn (Int.ofNat_eq_zero.mp this)

theorem residue_one_is_torsion (n : Nat) (_hn : 0 < n) :
    ((n : Int) * 1) % n = 0 := by
  simp

theorem every_residue_killed_by_modulus (a : Int) {n : Int} (_hn : 0 < n) :
    (n * a) % n = 0 := by
  have h : n ∣ n * a := ⟨a, rfl⟩
  exact Int.dvd_iff_emod_eq_zero.mp h

structure ScopeBoundary where
  oneNotTorsion : Bool
  unboundedOrdersForceZ : Bool
  qmodzDualIsU1 : Bool
  piFromExactQ : Bool
  authorityEffectNone : Bool
deriving DecidableEq, Repr

def scopeBoundary : ScopeBoundary :=
  { oneNotTorsion := true
    unboundedOrdersForceZ := false
    qmodzDualIsU1 := false
    piFromExactQ := false
    authorityEffectNone := true }

theorem scope_boundary_refuses_kills :
    scopeBoundary.oneNotTorsion = true ∧
      scopeBoundary.unboundedOrdersForceZ = false ∧
      scopeBoundary.qmodzDualIsU1 = false ∧
      scopeBoundary.piFromExactQ = false ∧
      scopeBoundary.authorityEffectNone = true := by
  decide

#print axioms one_not_torsion
#print axioms every_residue_killed_by_modulus
#print axioms scope_boundary_refuses_kills

end OvernightT5

private def l5aProvenance : String :=
  "Origin: lean4/T5TorsionNotZ.lean Claim: one_not_torsion AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
