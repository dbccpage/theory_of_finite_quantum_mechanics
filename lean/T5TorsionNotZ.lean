import Std

/-!
Overnight T5: unbounded finite orders do not select `Z`.

`1` in `Int` is not torsion. Every displayed element of a
cyclic group of order `n` (modelled as remainder modulo `n`)
is torsion. A group in which a generating unit has infinite
order cannot be isomorphic to a group in which every displayed
element is torsion.

This does not construct the Prufer colimit inside Lean 4
without a colimit library. The Python twin enumerates the
Prufer and `Q/Z` witnesses. Together they refute
`UNBOUNDED_FINITE_PERIOD_IMPLIES_Z`.

AuthorityEffect: None.
-/

namespace OvernightT5

def IsTorsion (x : Int) : Prop :=
  ∃ n : Nat, 0 < n ∧ (n : Int) * x = 0

theorem one_not_torsion : ¬ IsTorsion 1 := by
  intro h
  rcases h with ⟨n, hn, heq⟩
  have : (n : Int) = 0 := by
    simpa using heq
  exact Nat.ne_of_gt hn (Int.ofNat_eq_zero.mp this)

/-- The class of `1` modulo `n` is killed by `n` itself. -/
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
