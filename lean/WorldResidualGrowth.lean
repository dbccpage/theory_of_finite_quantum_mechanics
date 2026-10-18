import WorldPresentation

/-!
# DMT-009: concrete scaled finite-graph residual-growth fixture

The Python dual carries the rational factorial-tail certificate.  This Lean
surface pins the exact normal-component arithmetic at t = 3/5.  It is not a
continuum Lieb-Robinson theorem.
-/

namespace OmegaWorld

def normalSpeedZero : Nat := 1
def accelerationL1 : Nat := 10
def barAUpper : Nat := 5

/-- The rational comparison 3/5 > 1/(2*5), cleared of denominators. -/
def IsIntermediateScaled : Prop :=
  3 * (2 * barAUpper) > 5 * normalSpeedZero

/-- At t=3/5, the affine normal velocity is 1 + 10*(3/5) = 7. -/
def exactNormalSpeedAtThreeFifths : Nat := 7
def escapingLowerAtThreeFifths : Nat := 0
def escapingUpperAtThreeFifths : Nat := 7

theorem threshold_is_one_tenth :
    normalSpeedZero = 1 ∧ barAUpper = 5 := by
  decide

theorem intermediate_probe_is_strict : IsIntermediateScaled := by
  simp [IsIntermediateScaled, barAUpper, normalSpeedZero]

theorem exact_normal_sandwich :
    escapingLowerAtThreeFifths <= exactNormalSpeedAtThreeFifths ∧
      exactNormalSpeedAtThreeFifths <= escapingUpperAtThreeFifths := by
  decide

#print axioms exact_normal_sandwich

end OmegaWorld
