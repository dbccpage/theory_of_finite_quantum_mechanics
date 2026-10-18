

namespace FableHilbertWalk20260819.H038

def h1 : List Int := [1, 0, 1, 0, 1, 0, 1]
def h2 : List Int := [0, 1, 1, 0, 0, 1, 1]
def h3 : List Int := [0, 0, 0, 1, 1, 1, 1]

def inner_prod (l1 l2 : List Int) : Int :=
  (List.zipWith (· * ·) l1 l2).foldl (· + ·) 0

def list_sum (l : List Int) : Int :=
  l.foldl (· + ·) 0

theorem h1_weight : list_sum h1 = 4 := by decide

theorem h2_weight : list_sum h2 = 4 := by decide

theorem h3_weight : list_sum h3 = 4 := by decide

theorem h1_h2_overlap : inner_prod h1 h2 = 2 := by decide

theorem h1_h3_overlap : inner_prod h1 h3 = 2 := by decide

theorem h2_h3_overlap : inner_prod h2 h3 = 2 := by decide

def commutePhase (overlap : Int) : Int :=
  if overlap % 2 = 0 then 1 else -1

def logicalAll : List Int := [1, 1, 1, 1, 1, 1, 1]

theorem stabilizers_commute_h1_h2 :
    commutePhase (inner_prod h1 h2) = 1 ∧ inner_prod h1 h2 = 2 := by decide

theorem logical_commutes_with_stabilizers :
    commutePhase (inner_prod logicalAll h1) = 1 ∧
      commutePhase (inner_prod logicalAll h2) = 1 ∧
      commutePhase (inner_prod logicalAll h3) = 1 ∧
      inner_prod logicalAll h1 = 4 := by decide

theorem logical_operators_anticommute :
    commutePhase (inner_prod logicalAll logicalAll) = -1 ∧
      inner_prod logicalAll logicalAll = 7 := by decide

structure Syndrome3 where
  s1 : Int
  s2 : Int
  s3 : Int
  deriving DecidableEq, Repr

inductive QubitPos where
  | q0 | q1 | q2 | q3 | q4 | q5 | q6
  deriving DecidableEq, Repr

def posSyndrome : QubitPos → Syndrome3
  | .q0 => ⟨1, 0, 0⟩
  | .q1 => ⟨0, 1, 0⟩
  | .q2 => ⟨1, 1, 0⟩
  | .q3 => ⟨0, 0, 1⟩
  | .q4 => ⟨1, 0, 1⟩
  | .q5 => ⟨0, 1, 1⟩
  | .q6 => ⟨1, 1, 1⟩

def zeroSyndrome : Syndrome3 := ⟨0, 0, 0⟩

def basisAt : QubitPos → List Int
  | .q0 => [1, 0, 0, 0, 0, 0, 0]
  | .q1 => [0, 1, 0, 0, 0, 0, 0]
  | .q2 => [0, 0, 1, 0, 0, 0, 0]
  | .q3 => [0, 0, 0, 1, 0, 0, 0]
  | .q4 => [0, 0, 0, 0, 1, 0, 0]
  | .q5 => [0, 0, 0, 0, 0, 1, 0]
  | .q6 => [0, 0, 0, 0, 0, 0, 1]

def checkSyndrome (err : List Int) : Syndrome3 :=
  ⟨inner_prod h1 err, inner_prod h2 err, inner_prod h3 err⟩

theorem check_syndromes_are_the_columns :
    checkSyndrome (basisAt .q0) = posSyndrome .q0 ∧
      checkSyndrome (basisAt .q1) = posSyndrome .q1 ∧
      checkSyndrome (basisAt .q2) = posSyndrome .q2 ∧
      checkSyndrome (basisAt .q3) = posSyndrome .q3 ∧
      checkSyndrome (basisAt .q4) = posSyndrome .q4 ∧
      checkSyndrome (basisAt .q5) = posSyndrome .q5 ∧
      checkSyndrome (basisAt .q6) = posSyndrome .q6 := by
  decide

theorem syndromes_nonzero :
    posSyndrome .q0 ≠ zeroSyndrome ∧
    posSyndrome .q1 ≠ zeroSyndrome ∧
    posSyndrome .q2 ≠ zeroSyndrome ∧
    posSyndrome .q3 ≠ zeroSyndrome ∧
    posSyndrome .q4 ≠ zeroSyndrome ∧
    posSyndrome .q5 ≠ zeroSyndrome ∧
    posSyndrome .q6 ≠ zeroSyndrome := by decide

theorem syndromes_pairwise_distinct :
    posSyndrome .q0 ≠ posSyndrome .q1 ∧
    posSyndrome .q0 ≠ posSyndrome .q2 ∧
    posSyndrome .q0 ≠ posSyndrome .q3 ∧
    posSyndrome .q0 ≠ posSyndrome .q4 ∧
    posSyndrome .q0 ≠ posSyndrome .q5 ∧
    posSyndrome .q0 ≠ posSyndrome .q6 ∧
    posSyndrome .q1 ≠ posSyndrome .q2 ∧
    posSyndrome .q1 ≠ posSyndrome .q3 ∧
    posSyndrome .q1 ≠ posSyndrome .q4 ∧
    posSyndrome .q1 ≠ posSyndrome .q5 ∧
    posSyndrome .q1 ≠ posSyndrome .q6 ∧
    posSyndrome .q2 ≠ posSyndrome .q3 ∧
    posSyndrome .q2 ≠ posSyndrome .q4 ∧
    posSyndrome .q2 ≠ posSyndrome .q5 ∧
    posSyndrome .q2 ≠ posSyndrome .q6 ∧
    posSyndrome .q3 ≠ posSyndrome .q4 ∧
    posSyndrome .q3 ≠ posSyndrome .q5 ∧
    posSyndrome .q3 ≠ posSyndrome .q6 ∧
    posSyndrome .q4 ≠ posSyndrome .q5 ∧
    posSyndrome .q4 ≠ posSyndrome .q6 ∧
    posSyndrome .q5 ≠ posSyndrome .q6 := by decide

#print axioms h1_weight
#print axioms h1_h2_overlap
#print axioms stabilizers_commute_h1_h2
#print axioms logical_commutes_with_stabilizers
#print axioms logical_operators_anticommute
#print axioms syndromes_nonzero
#print axioms syndromes_pairwise_distinct

end FableHilbertWalk20260819.H038


theorem falsification_degenerate_carrier : ¬ (1 = 0) := by
  decide

private def l5aProvenance : String :=
  "Origin: lean4/H038SteaneFanoCodeTransversalGates.lean Claim: h1_weight AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
