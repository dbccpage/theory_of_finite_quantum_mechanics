/-!
Numeral slice of FQ-GAP-C500-ORIGINAL-TARGETS.
AuthorityEffect: None.
The module has no import. It counts the target numerals and clause-list
lengths named in the C500 gap register. It does not read an evidence file
and it does not discharge an original target contract.
-/

namespace OriginalTargetNumerals

def lo (k : Nat) : Nat := 276 + 25 * k
def hi (k : Nat) : Nat := 300 + 25 * k

theorem spanLen (k : Nat) : hi k - lo k + 1 = 25 := by
  simp [hi, lo]
  omega

theorem abut (k : Nat) : hi k + 1 = lo (k + 1) := by
  simp [hi, lo]
  omega

theorem tenRunEndpoints : lo 1 = 301 ∧ hi 10 = 550 := by
  decide

theorem tenRunCover : hi 10 - lo 1 + 1 = 250 ∧ 10 * 25 = 250 := by
  decide

def clauseCounts : List Nat := [0, 2, 4, 2, 4, 1, 1, 1, 1, 5]

theorem clauseCountsLength : clauseCounts.length = 10 := rfl

theorem clauseCountSum : clauseCounts.sum = 21 := by
  decide

theorem lastClauseCountStrict :
    clauseCounts.getLast? = some 5 ∧ ∀ c ∈ clauseCounts.dropLast, c < 5 := by
  decide

inductive Block10Clause where
  | M2
  | M5
  | M7
  | J1
  | J2
  deriving DecidableEq

def block10Clauses : List Block10Clause :=
  [.M2, .M5, .M7, .J1, .J2]

theorem block10ClauseCount : block10Clauses.length = 5 := rfl

theorem block10ClausesNodup : block10Clauses.Nodup := by
  decide

#print axioms spanLen
#print axioms abut
#print axioms tenRunEndpoints
#print axioms tenRunCover
#print axioms clauseCountsLength
#print axioms clauseCountSum
#print axioms lastClauseCountStrict
#print axioms block10ClauseCount
#print axioms block10ClausesNodup

end OriginalTargetNumerals
