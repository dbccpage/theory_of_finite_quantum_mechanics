import Imported.Genesis19l57g1.SecondRun.Kernel

open SecondRun.Sealed

/-
Narrowed boundary for PGW-PYTHON-LEAN-CARRIER-BRIDGE.
The two lists are the sealed Lean histories of readings L and F.
Replaying each from genesis yields R2L and R2F, and those regimes differ.
This module does not join a Python computation to a Lean statement.
-/

def pgwHistoryL : List Event :=
  [.supply 0, .supply 1, .supply 1, .supply 2,
   .admitDatum, .admitDatum, .impose 0 1]

def pgwHistoryF : List Event :=
  [.supply 0, .admitDatum, .supply 1, .supply 1, .supply 2,
   .admitDatum, .admitDatum, .impose 1 2]

theorem pgwHistoryL_replays :
    replayE pgwHistoryL genesis = some R2L := by
  decide

theorem pgwHistoryF_replays :
    replayE pgwHistoryF genesis = some R2F := by
  decide

theorem pgwR2L_ne_R2F : R2L ≠ R2F := by
  decide

theorem pgwReplay_ne :
    replayE pgwHistoryL genesis ≠ replayE pgwHistoryF genesis := by
  decide

theorem pgwData_counts : R2L.data = 2 ∧ R2F.data = 3 := by
  decide

theorem pgwReqs : R2L.reqs = [(0, 1)] ∧ R2F.reqs = [(1, 2)] := by
  decide

theorem pgwEmpty_carriers :
    R2L.forms = [] ∧ R2L.insts = [] ∧ R2L.rules = [] ∧
      R2F.forms = [] ∧ R2F.insts = [] ∧ R2F.rules = [] := by
  decide

theorem pgwHistory_lengths :
    pgwHistoryL.length = 7 ∧ pgwHistoryF.length = 8 := by
  decide

#print axioms pgwHistoryL_replays
#print axioms pgwHistoryF_replays
#print axioms pgwR2L_ne_R2F
#print axioms pgwReplay_ne
#print axioms pgwData_counts
#print axioms pgwReqs
#print axioms pgwEmpty_carriers
#print axioms pgwHistory_lengths
