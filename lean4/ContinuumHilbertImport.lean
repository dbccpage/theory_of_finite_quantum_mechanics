-- GP-IMPORT-CONTINUUM-HILBERT. Not a default target.
-- Length-4 window (8, 4, 2, 1) and the identity 3 * sum_{j < n} 4^j + 1 = 4^n.
-- Scalar-field selection, l2 uniformity, and a completion stay outside this module.

namespace ContinuumHilbertImport

def pow4 : Nat → Nat
  | 0 => 1
  | n + 1 => pow4 n * 4

def sumPow4 : Nat → Nat
  | 0 => 0
  | n + 1 => sumPow4 n + pow4 n

theorem closedTail (n : Nat) : 3 * sumPow4 n + 1 = pow4 n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [sumPow4, pow4]
    omega

theorem scaledTailIsOne (n : Nat) : pow4 n - 3 * sumPow4 n = 1 := by
  have h := closedTail n
  omega

theorem sumDiff (n : Nat) : sumPow4 (n + 1) - sumPow4 n = pow4 n := by
  rw [sumPow4]
  omega

theorem halves : 8 = 4 + 4 ∧ 4 = 2 + 2 ∧ 2 = 1 + 1 := by
  decide

theorem windowSquares : 8 * 8 = 64 ∧ 4 * 4 = 16 ∧ 2 * 2 = 4 ∧ 1 * 1 = 1 := by
  decide

theorem windowSum : 8 * 8 + 4 * 4 + 2 * 2 + 1 * 1 = 85 := by
  decide

theorem windowScaled : 3 * 85 + 1 = 256 := by
  decide

theorem pow4Four : pow4 4 = 256 := by
  rfl

theorem windowIsSum : 8 * 8 + 4 * 4 + 2 * 2 + 1 * 1 = sumPow4 4 := by
  rfl

theorem squareDiffs :
    64 - 16 = 48 ∧ 16 - 4 = 12 ∧ 4 - 1 = 3 ∧
      3 * 16 = 48 ∧ 3 * 4 = 12 ∧ 3 * 1 = 3 := by
  decide

theorem noPositiveDoubleOfOne : ¬ ∃ z : Nat, 0 < z ∧ z + z = 1 := by
  intro h
  rcases h with ⟨z, hz, heq⟩
  cases z with
  | zero => omega
  | succ z => omega

#print axioms closedTail
#print axioms scaledTailIsOne
#print axioms sumDiff
#print axioms halves
#print axioms windowSquares
#print axioms windowSum
#print axioms windowScaled
#print axioms pow4Four
#print axioms windowIsSum
#print axioms squareDiffs
#print axioms noPositiveDoubleOfOne

end ContinuumHilbertImport
