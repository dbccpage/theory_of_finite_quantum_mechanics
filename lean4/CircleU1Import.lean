-- GP-IMPORT-CIRCLE-U1. Not a default target.
-- Integer slice: signs square to 1, the pairs (1, 1) and (1, -1) differ,
-- the pair 0, 1 has square norm 1 and multiplies to (-1, 0), and one three-step cycle.
-- The circle group and continuity of a one-parameter phase group stay outside this module.

namespace CircleU1Import

def isSign (a : Int) : Prop := a = 1 ∨ a = -1

theorem signSquare (a : Int) (h : isSign a) : a * a = 1 := by
  rcases h with rfl | rfl
  · decide
  · decide

theorem pairsDiffer : ((1, 1) : Int × Int) ≠ (1, -1) := by
  decide

theorem pairCoordsAreSigns :
    isSign (1 : Int) ∧ isSign (1 : Int) ∧ isSign (1 : Int) ∧ isSign (-1 : Int) :=
  ⟨Or.inl rfl, Or.inl rfl, Or.inl rfl, Or.inr rfl⟩

def gMul (a b c d : Int) : Int × Int := (a * c - b * d, a * d + b * c)

def gNorm (a b : Int) : Int := a * a + b * b

theorem iNorm : gNorm 0 1 = 1 := by
  decide

theorem iSquare : gMul 0 1 0 1 = (-1, 0) := by
  decide

theorem iSquareNeOne : gMul 0 1 0 1 ≠ (1, 0) := by
  decide

def cyc (n : Nat) : Nat :=
  if n = 0 then 1 else if n = 1 then 2 else if n = 2 then 0 else n

theorem cycTwice : cyc (cyc 0) = 2 := by
  decide

theorem cycThrice : cyc (cyc (cyc 0)) = 0 := by
  decide

#print axioms signSquare
#print axioms pairsDiffer
#print axioms pairCoordsAreSigns
#print axioms iNorm
#print axioms iSquare
#print axioms iSquareNeOne
#print axioms cycTwice
#print axioms cycThrice

end CircleU1Import
