
import WorldPresentation



namespace OmegaWorld

def normalSpeedZero : Nat := 1
def accelerationL1 : Nat := 10
def barAUpper : Nat := 5

def IsIntermediateScaled : Prop :=
  3 * (2 * barAUpper) > 5 * normalSpeedZero

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

def clearedNormalNumerator : Nat :=
  normalSpeedZero * 5 + accelerationL1 * 3

theorem affine_speed_from_parameters :
    clearedNormalNumerator = exactNormalSpeedAtThreeFifths * 5 ∧
      IsIntermediateScaled ∧
      escapingLowerAtThreeFifths ≤ exactNormalSpeedAtThreeFifths ∧
      exactNormalSpeedAtThreeFifths ≤ escapingUpperAtThreeFifths := by
  unfold clearedNormalNumerator exactNormalSpeedAtThreeFifths IsIntermediateScaled
    escapingLowerAtThreeFifths escapingUpperAtThreeFifths normalSpeedZero
    accelerationL1 barAUpper
  decide

#print axioms exact_normal_sandwich
#print axioms affine_speed_from_parameters

end OmegaWorld

private def l5aProvenance : String :=
  "Origin: lean4/WorldResidualGrowth.lean Claim: threshold_is_one_tenth AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
