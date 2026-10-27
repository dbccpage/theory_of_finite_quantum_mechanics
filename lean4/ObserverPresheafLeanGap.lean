-- OPS-LEAN-GAP. Not a default target.
-- One Boolean box: four parity constraints with no common assignment.
-- Global sections, the noncontextual fraction, Vorob'ev, and the Rust gate stay outside this module.

namespace ObserverPresheafLeanGap

theorem lhsSum :
    ∀ a ap b bp : Bool,
      ((a ^^ b) ^^ (a ^^ bp) ^^ (ap ^^ b) ^^ (ap ^^ bp)) = false := by
  decide

theorem rhsSum : (false ^^ false ^^ false ^^ true) = true := by
  decide

theorem noAssignment :
    ∀ a ap b bp : Bool,
      ¬ ((a ^^ b) = false ∧ (a ^^ bp) = false ∧ (ap ^^ b) = false ∧ (ap ^^ bp) = true) := by
  decide

theorem sixteen : 2 * 2 * 2 * 2 = 16 := by
  decide

#print axioms lhsSum
#print axioms rhsSum
#print axioms noAssignment
#print axioms sixteen

end ObserverPresheafLeanGap
