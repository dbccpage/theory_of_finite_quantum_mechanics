import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Descriptive flag records and checked natural-level
updates only. No interpretation of descriptions as higher cells or homotopies. -/
namespace TFQM.CondensationMetadata

structure Row where
  level : Nat
  flag : Bool
  description : String
  deriving DecidableEq

structure Metadata where
  level : Nat
  rows : List Row
  deriving DecidableEq

def appendChecked (maximum : Nat) (m : Metadata) (description : String) (flag : Bool) :
    Except Unit Metadata :=
  if m.level + 1 ≤ maximum then
    .ok { level := m.level + 1, rows := m.rows ++ [⟨m.level + 1, flag, description⟩] }
  else .error ()

theorem update_success (maximum : Nat) (m : Metadata) (description : String) (flag : Bool)
    (fits : m.level + 1 ≤ maximum) :
    appendChecked maximum m description flag =
      .ok { level := m.level + 1, rows := m.rows ++ [⟨m.level + 1, flag, description⟩] } := by
  simp [appendChecked, fits]

theorem update_refused (maximum : Nat) (m : Metadata) (description : String) (flag : Bool)
    (full : maximum < m.level + 1) :
    appendChecked maximum m description flag = .error () := by
  simp [appendChecked, Nat.not_le.mpr full]

theorem boundary_refused (maximum : Nat) (rows : List Row) (description : String) (flag : Bool) :
    appendChecked maximum ⟨maximum, rows⟩ description flag = .error () := by
  exact update_refused maximum _ description flag (Nat.lt_succ_self maximum)

theorem next_level_bound (maximum : Nat) (m : Metadata) (description : String) (flag : Bool)
    (out : Metadata) (success : appendChecked maximum m description flag = .ok out) :
    out.level = m.level + 1 ∧ out.level ≤ maximum := by
  unfold appendChecked at success
  split at success
  · cases success
    exact ⟨rfl, by assumption⟩
  · cases success

def failing (row : Row) : Bool := decide (row.level > 0) && !row.flag
def flaggedFailures (rows : List Row) : List Row := rows.filter failing

theorem base_ignored (flag : Bool) (description : String) :
    failing ⟨0, flag, description⟩ = false := by simp [failing]

theorem asserted_ignored (level : Nat) (description : String) :
    failing ⟨level, true, description⟩ = false := by simp [failing]

theorem positive_false (level : Nat) (description : String) (positive : level > 0) :
    failing ⟨level, false, description⟩ = true := by simp [failing, positive]

theorem flags_append (left right : List Row) :
    flaggedFailures (left ++ right) = flaggedFailures left ++ flaggedFailures right := by
  simp [flaggedFailures]

theorem flags_empty : flaggedFailures [] = [] := rfl

theorem duplicate_failure (row : Row) (fails : failing row = true) :
    flaggedFailures [row, row] = [row, row] := by simp [flaggedFailures, fails]

def allAsserted (rows : List Row) : Bool := rows.all Row.flag

theorem all_empty : allAsserted [] = true := rfl
theorem all_append (left right : List Row) :
    allAsserted (left ++ right) = (allAsserted left && allAsserted right) := by
  simp [allAsserted]

theorem false_base_can_pass (description : String) :
    flaggedFailures [⟨0, false, description⟩] = [] ∧
      allAsserted [⟨0, false, description⟩] = false := by
  simp [flaggedFailures, failing, allAsserted]

end TFQM.CondensationMetadata

#print axioms TFQM.CondensationMetadata.update_success
#print axioms TFQM.CondensationMetadata.update_refused
#print axioms TFQM.CondensationMetadata.boundary_refused
#print axioms TFQM.CondensationMetadata.next_level_bound
#print axioms TFQM.CondensationMetadata.base_ignored
#print axioms TFQM.CondensationMetadata.asserted_ignored
#print axioms TFQM.CondensationMetadata.positive_false
#print axioms TFQM.CondensationMetadata.flags_append
#print axioms TFQM.CondensationMetadata.flags_empty
#print axioms TFQM.CondensationMetadata.duplicate_failure
#print axioms TFQM.CondensationMetadata.all_empty
#print axioms TFQM.CondensationMetadata.all_append
#print axioms TFQM.CondensationMetadata.false_base_can_pass
