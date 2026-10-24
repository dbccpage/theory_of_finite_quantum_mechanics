/-
Narrowed boundary for PGW-DECLARED-INPUT-FLOOR.
The numerals are the bounds named by the node: fifteen rounds, a node
guard of 250, growth below four data, two items, an input count of two,
four engines, and two readings.
This module does not prove a floor and does not run an engine.
-/

def pgwRounds : Nat := 15

def pgwGuard : Nat := 250

def pgwDataCeiling : Nat := 4

def pgwItemBound : Nat := 2

def pgwInputCount : Nat := 2

def pgwEngines : Nat := 4

def pgwReadings : Nat := 2

def pgwDataCandidates : List Nat := [0, 1, 2, 3, 4]

def pgwStrictlyBelow : List Nat :=
  pgwDataCandidates.filter (fun n => decide (n < pgwDataCeiling))

theorem pgwBounds_values :
    pgwRounds = 15 ∧ pgwGuard = 250 ∧ pgwDataCeiling = 4 ∧
      pgwItemBound = 2 ∧ pgwInputCount = 2 ∧ pgwEngines = 4 ∧
      pgwReadings = 2 := by
  decide

theorem pgwInput_eq_items : pgwInputCount = pgwItemBound := by
  decide

theorem pgwOne_below_input : 1 < pgwInputCount := by
  decide

theorem pgwGuard_above_rounds : pgwRounds < pgwGuard := by
  decide

theorem pgwEngines_ne_readings : pgwEngines ≠ pgwReadings := by
  decide

theorem pgwStrictlyBelow_list : pgwStrictlyBelow = [0, 1, 2, 3] := by
  decide

theorem pgwStrictlyBelow_length : pgwStrictlyBelow.length = 4 := by
  decide

theorem pgwCeiling_not_below : decide (pgwDataCeiling < pgwDataCeiling) = false := by
  decide

#print axioms pgwBounds_values
#print axioms pgwInput_eq_items
#print axioms pgwOne_below_input
#print axioms pgwGuard_above_rounds
#print axioms pgwEngines_ne_readings
#print axioms pgwStrictlyBelow_list
#print axioms pgwStrictlyBelow_length
#print axioms pgwCeiling_not_below
