import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
Cosine-law data for lengths 3, 4, 5, and one hand-chosen block trace.

`cosNum a b c` is `b^2 + c^2 - a^2`. The block trace is
`2 (1 + beta^2) / (1 - beta^2) + 2` at `beta = 1/2`. No deficit angle,
4-simplex, or continuum equation is constructed.
-/

namespace DressingFieldReggeGravityFence

def cosNum (a b c : Rat) : Rat := b ^ 2 + c ^ 2 - a ^ 2

def cosLaw (a b c : Rat) : Rat := cosNum a b c / (2 * b * c)

def gamma (beta : Rat) : Rat := (1 + beta ^ 2) / (1 - beta ^ 2)

def blockTrace (beta : Rat) : Rat := gamma beta + gamma beta + 1 + 1

theorem numerator_sum (a b c : Rat) :
    cosNum a b c + cosNum b a c + cosNum c a b = a ^ 2 + b ^ 2 + c ^ 2 := by
  simp only [cosNum]
  ring

theorem lengths_345 :
    cosNum 5 3 4 = 0 ∧
    cosNum 3 4 5 = 32 ∧
    cosNum 4 3 5 = 18 ∧
    cosNum 5 3 4 + cosNum 3 4 5 + cosNum 4 3 5 = 3 ^ 2 + 4 ^ 2 + 5 ^ 2 ∧
    cosLaw 5 3 4 = 0 ∧
    cosLaw 3 4 5 = 4 / 5 ∧
    cosLaw 4 3 5 = 3 / 5 ∧
    cosLaw 5 3 4 + cosLaw 3 4 5 + cosLaw 4 3 5 = 7 / 5 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  all_goals simp only [cosNum, cosLaw]
  all_goals norm_num

theorem block_trace_half :
    (1 : Rat) - (1 / 2) ^ 2 ≠ 0 ∧
    gamma (1 / 2) = 5 / 3 ∧
    (2 * (1 / 2)) / ((1 : Rat) - (1 / 2) ^ 2) = 4 / 3 ∧
    blockTrace (1 / 2) = 16 / 3 ∧
    blockTrace (1 / 2) ≠ 4 ∧
    blockTrace (1 / 2) ≠ 7 / 5 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · norm_num
  · simp only [gamma]; norm_num
  · norm_num
  · simp only [blockTrace, gamma]; norm_num
  · simp only [blockTrace, gamma]; norm_num
  · simp only [blockTrace, gamma]; norm_num

theorem cosine_sum_ne_block_trace :
    cosLaw 5 3 4 + cosLaw 3 4 5 + cosLaw 4 3 5 ≠ blockTrace (1 / 2) := by
  simp only [cosLaw, cosNum, blockTrace, gamma]
  norm_num

#print axioms DressingFieldReggeGravityFence.numerator_sum
#print axioms DressingFieldReggeGravityFence.lengths_345
#print axioms DressingFieldReggeGravityFence.block_trace_half
#print axioms DressingFieldReggeGravityFence.cosine_sum_ne_block_trace

end DressingFieldReggeGravityFence
