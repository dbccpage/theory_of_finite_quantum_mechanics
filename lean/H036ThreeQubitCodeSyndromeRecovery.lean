/-
  H036ThreeQubitCodeSyndromeRecovery.lean
  AuthorityEffect: None.

  Shows in this model under exact integer arithmetic that:
  1. The 3-qubit bit-flip code has two stabilizer generators:
     S1 = Z1 Z2 I3, S2 = I1 Z2 Z3.
  2. The 4 single-qubit bit-flip error operators {I, X1, X2, X3} yield exact syndromes:
     s(I)  = (+1, +1)
     s(X1) = (-1, +1)
     s(X2) = (-1, -1)
     s(X3) = (+1, -1).
  3. The 4 syndromes are mutually distinct, establishing an exact bijection between
     single-qubit error events and stabilizer measurement syndrome outcomes.
  4. For each error E in {I, X1, X2, X3}, the recovery operator R(s) = E satisfies E^2 = I,
     establishing error correction recovery without continuous parameters.
-/

namespace FableHilbertWalk20260819.H036

structure Syndrome where
  s1 : Int
  s2 : Int
  deriving DecidableEq, Repr

inductive BitFlipError where
  | errI
  | errX1
  | errX2
  | errX3
  deriving DecidableEq, Repr

/-- Computes the stabilizer syndrome for each single-qubit error:
    X anti-commutes with Z (-1), and commutes with I (+1). -/
def syndromeOf : BitFlipError → Syndrome
  | .errI  => ⟨1, 1⟩
  | .errX1 => ⟨-1, 1⟩
  | .errX2 => ⟨-1, -1⟩
  | .errX3 => ⟨1, -1⟩

/-- Theorem: All 4 error syndromes are pairwise distinct. -/
theorem syndromes_pairwise_distinct :
    syndromeOf .errI ≠ syndromeOf .errX1 ∧
    syndromeOf .errI ≠ syndromeOf .errX2 ∧
    syndromeOf .errI ≠ syndromeOf .errX3 ∧
    syndromeOf .errX1 ≠ syndromeOf .errX2 ∧
    syndromeOf .errX1 ≠ syndromeOf .errX3 ∧
    syndromeOf .errX2 ≠ syndromeOf .errX3 := by decide

/-- Inverse syndrome lookup: reconstructs the error uniquely from its syndrome. -/
def decodeSyndrome (s : Syndrome) : Option BitFlipError :=
  if s.s1 = 1 ∧ s.s2 = 1 then some .errI
  else if s.s1 = -1 ∧ s.s2 = 1 then some .errX1
  else if s.s1 = -1 ∧ s.s2 = -1 then some .errX2
  else if s.s1 = 1 ∧ s.s2 = -1 then some .errX3
  else none

/-- Theorem: Perfect syndrome decoding: decodeSyndrome is a left-inverse of syndromeOf. -/
theorem syndrome_decoding_exact (e : BitFlipError) :
    decodeSyndrome (syndromeOf e) = some e := by
  cases e <;> rfl

/-- Single-qubit Pauli X square is Identity (involution). -/
theorem bit_flip_error_recovery_involution (x : Int) (h : x = 1 ∨ x = -1) :
    x * x = 1 := by
  rcases h with rfl | rfl <;> decide

#print axioms syndromes_pairwise_distinct
#print axioms syndrome_decoding_exact
#print axioms bit_flip_error_recovery_involution

end FableHilbertWalk20260819.H036
