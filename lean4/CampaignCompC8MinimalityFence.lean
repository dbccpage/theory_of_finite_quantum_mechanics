/-
COMP-C8-MINIMALITY-FENCE, one closed tape.
Mark A, mark B and the blank are the numbers 1, 2 and 0.
The word mark A then mark B, followed by one blank cell, is the list 1, 2, 0.
The blank number differs from each mark number.
No machine and no minimality sentence.
-/

namespace CampaignCompC8MinimalityFence

def markA : Nat := 1
def markB : Nat := 2
def blank : Nat := 0

def appendBlank (word : List Nat) : List Nat := word ++ [blank]

theorem oneWordThenBlank :
    markA = 1 ∧ markB = 2 ∧ blank = 0 ∧ appendBlank [markA, markB] = [1, 2, 0] := by
  decide

theorem blankDiffersFromMarks : blank ≠ markA ∧ blank ≠ markB := by
  decide

#print axioms oneWordThenBlank
#print axioms blankDiffersFromMarks

end CampaignCompC8MinimalityFence
