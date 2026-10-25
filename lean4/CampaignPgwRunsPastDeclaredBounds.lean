/-
Narrowed boundary for PGW-RUNS-PAST-DECLARED-BOUNDS.
Five records are compared with the declared line:
rounds at most 15, nodes at most 250, data below 4, items at most 2.
This module does not replay a forward run and does not decide unboundedness.
-/

def pgwBoundInside (rounds nodes data items : Nat) : Bool :=
  decide (rounds ≤ 15) && decide (nodes ≤ 250) && decide (data < 4) && decide (items ≤ 2)

theorem pgwBoundOnLine : pgwBoundInside 15 250 3 2 = true := by
  decide

theorem pgwBoundRoundPast : pgwBoundInside 16 250 3 2 = false := by
  decide

theorem pgwBoundNodePast : pgwBoundInside 15 251 3 2 = false := by
  decide

theorem pgwBoundDataFour : pgwBoundInside 15 250 4 2 = false := by
  decide

theorem pgwBoundItemPast : pgwBoundInside 15 250 3 3 = false := by
  decide

#print axioms pgwBoundOnLine
#print axioms pgwBoundRoundPast
#print axioms pgwBoundNodePast
#print axioms pgwBoundDataFour
#print axioms pgwBoundItemPast
