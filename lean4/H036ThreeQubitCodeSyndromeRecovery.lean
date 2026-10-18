

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

def syndromeOf : BitFlipError → Syndrome
  | .errI  => ⟨1, 1⟩
  | .errX1 => ⟨-1, 1⟩
  | .errX2 => ⟨-1, -1⟩
  | .errX3 => ⟨1, -1⟩

theorem syndromes_pairwise_distinct :
    syndromeOf .errI ≠ syndromeOf .errX1 ∧
    syndromeOf .errI ≠ syndromeOf .errX2 ∧
    syndromeOf .errI ≠ syndromeOf .errX3 ∧
    syndromeOf .errX1 ≠ syndromeOf .errX2 ∧
    syndromeOf .errX1 ≠ syndromeOf .errX3 ∧
    syndromeOf .errX2 ≠ syndromeOf .errX3 := by decide

def decodeSyndrome (s : Syndrome) : Option BitFlipError :=
  if s.s1 = 1 ∧ s.s2 = 1 then some .errI
  else if s.s1 = -1 ∧ s.s2 = 1 then some .errX1
  else if s.s1 = -1 ∧ s.s2 = -1 then some .errX2
  else if s.s1 = 1 ∧ s.s2 = -1 then some .errX3
  else none

theorem syndrome_decoding_exact (e : BitFlipError) :
    decodeSyndrome (syndromeOf e) = some e := by
  cases e <;> rfl

theorem bit_flip_error_recovery_involution (x : Int) (h : x = 1 ∨ x = -1) :
    x * x = 1 := by
  rcases h with rfl | rfl <;> decide

#print axioms syndromes_pairwise_distinct
#print axioms syndrome_decoding_exact
#print axioms bit_flip_error_recovery_involution

end FableHilbertWalk20260819.H036

private def l5aProvenance : String :=
  "Origin: lean4/H036ThreeQubitCodeSyndromeRecovery.lean Claim: syndromes_pairwise_distinct AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
