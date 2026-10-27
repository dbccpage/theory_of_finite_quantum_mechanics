-- TFQ-0183. Not a default target.
-- Integer skeleton of one count triple 4, 4, 1.
-- A superconducting device, a physical Majorana mode, and every other grid stay outside this module.

namespace TetronFourModeCounts

def modeCount : Nat := 4
def channelCount : Nat := 4
def islandCount : Nat := 1

theorem counts : modeCount = 4 ∧ channelCount = 4 ∧ islandCount = 1 := by
  decide

theorem eulerChar : (modeCount : Int) - channelCount + islandCount = 1 := by
  decide

theorem bettiArithmetic :
    ((channelCount : Int) - islandCount) - ((modeCount : Int) - 1) = 0 := by
  decide

theorem cornerParity : (1 + 1) % 2 = 0 ∧ modeCount * 2 = 8 ∧ 8 % 2 = 0 := by
  decide

theorem fourNeTwo : modeCount ≠ 2 := by
  decide

#print axioms counts
#print axioms eulerChar
#print axioms bettiArithmetic
#print axioms cornerParity
#print axioms fourNeTwo

end TetronFourModeCounts
