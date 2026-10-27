/-
Narrowed boundary for PGW-STREAM-AT-FOUR-ITEMS.
A refusal recorded at item count 3 is not a refusal at item count 4.
The short-circuit flag skips a later target; clearing it leaves that target searchable.
This module does not compute a stream tree.
-/

def pgwStreamRefusesAt (k items : Nat) (refused : Bool) : Bool :=
  decide (items = k) && refused

def pgwStreamSearched (shortCircuit : Bool) (refusalAt target : Nat) : Bool :=
  if shortCircuit then decide (target ≤ refusalAt) else true

theorem pgwStreamAtThree : pgwStreamRefusesAt 3 3 true = true := by
  decide

theorem pgwStreamThreeNotFour : pgwStreamRefusesAt 4 3 true = false := by
  decide

theorem pgwStreamFourRefuses : pgwStreamRefusesAt 4 4 true = true := by
  decide

theorem pgwStreamFourAccepts : pgwStreamRefusesAt 4 4 false = false := by
  decide

theorem pgwStreamShortCircuitSkipsFour : pgwStreamSearched true 3 4 = false := by
  decide

theorem pgwStreamOpenSearchReachesFour : pgwStreamSearched false 3 4 = true := by
  decide

theorem pgwStreamShortCircuitKeepsThree : pgwStreamSearched true 3 3 = true := by
  decide

#print axioms pgwStreamAtThree
#print axioms pgwStreamThreeNotFour
#print axioms pgwStreamFourRefuses
#print axioms pgwStreamFourAccepts
#print axioms pgwStreamShortCircuitSkipsFour
#print axioms pgwStreamOpenSearchReachesFour
#print axioms pgwStreamShortCircuitKeepsThree
