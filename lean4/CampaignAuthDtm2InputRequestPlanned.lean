/-
AUTH-DTM2-INPUT-REQUEST-PLANNED, one closed request list.
Header tag 1, fuel 2, machine-code length 1, segment [7], input word [3, 4].
Concatenation is the list 1, 2, 1, 7, 3, 4.
The list 0, 2, 1, 7, 3, 4 begins with 0, not with the header tag.
No evaluator and no configuration trace.
-/

namespace CampaignAuthDtm2InputRequestPlanned

def header : Nat := 1
def fuel : Nat := 2
def machineLength : Nat := 1
def machineSegment : List Nat := [7]
def inputWord : List Nat := [3, 4]

def encodeRequest : List Nat :=
  [header, fuel, machineLength] ++ machineSegment ++ inputWord

theorem oneRequestEncoding :
    header = 1 ∧ fuel = 2 ∧ machineLength = 1 ∧
      machineSegment = [7] ∧ inputWord = [3, 4] ∧
      encodeRequest = [1, 2, 1, 7, 3, 4] := by
  decide

theorem zeroHeadDiffersFromHeader :
    [0, 2, 1, 7, 3, 4].head? = some 0 ∧ header = 1 ∧ some 0 ≠ some header := by
  decide

#print axioms oneRequestEncoding
#print axioms zeroHeadDiffersFromHeader

end CampaignAuthDtm2InputRequestPlanned
