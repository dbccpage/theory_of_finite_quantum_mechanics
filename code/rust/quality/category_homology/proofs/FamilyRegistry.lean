import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Raw string membership/ordered target accumulation
and key-list registration. No category,functor,agent or provenance certification. -/
namespace TFQM.FamilyRegistry

def addTarget (source : String) (active : String → Bool) (seen : List String) (candidate : String) :
    List String :=
  if candidate ≠ source ∧ active candidate = true ∧ candidate ∉ seen then seen ++ [candidate] else seen

theorem source_rejected (source : String) (active : String → Bool) (seen : List String) :
    addTarget source active seen source = seen := by simp [addTarget]

theorem inactive_rejected (source : String) (active : String → Bool) (seen : List String)
    (candidate : String) (inactive : active candidate = false) :
    addTarget source active seen candidate = seen := by simp [addTarget, inactive]

theorem existing_unchanged (source : String) (active : String → Bool) (seen : List String)
    (candidate : String) (present : candidate ∈ seen) :
    addTarget source active seen candidate = seen := by simp [addTarget, present]

theorem fresh_appended (source : String) (active : String → Bool) (seen : List String)
    (candidate : String) (different : candidate ≠ source) (enabled : active candidate = true)
    (fresh : candidate ∉ seen) :
    addTarget source active seen candidate = seen ++ [candidate] := by
  simp [addTarget, different, enabled, fresh]

theorem prefix_preserved (source : String) (active : String → Bool) (seen : List String)
    (candidate : String) : ∃ suffix, addTarget source active seen candidate = seen ++ suffix := by
  unfold addTarget
  split
  · exact ⟨[candidate], rfl⟩
  · exact ⟨[], (List.append_nil seen).symm⟩

def collect (source : String) (active : String → Bool) (candidates seen : List String) : List String :=
  candidates.foldl (addTarget source active) seen

theorem collect_append (source : String) (active : String → Bool)
    (first second seen : List String) :
    collect source active (first ++ second) seen =
      collect source active second (collect source active first seen) := by
  simp [collect]

theorem duplicate_unchanged (source : String) (active : String → Bool) (seen : List String)
    (candidate : String) (present : candidate ∈ seen) :
    collect source active [candidate, candidate] seen = seen := by
  simp [collect, addTarget, present]

def targets (source : String) (active : String → Bool) (candidates : List String) : List String :=
  if active source then collect source active candidates [] else []

theorem inactive_source_empty (source : String) (active : String → Bool) (candidates : List String)
    (inactive : active source = false) : targets source active candidates = [] := by
  simp [targets, inactive]

theorem empty_rules (source : String) (active : String → Bool) : targets source active [] = [] := by
  cases h : active source <;> simp [targets, collect, h]

def register (table : String → List String) (key value : String) : String → List String :=
  fun query => if query = key then table query ++ [value] else table query

theorem register_self (table : String → List String) (key value : String) :
    register table key value key = table key ++ [value] := by simp [register]

theorem register_other (table : String → List String) (key value query : String) (other : query ≠ key) :
    register table key value query = table query := by simp [register, other]

theorem register_twice (table : String → List String) (key first second : String) :
    register (register table key first) key second key = table key ++ [first, second] := by
  simp [register, List.append_assoc]

end TFQM.FamilyRegistry

#print axioms TFQM.FamilyRegistry.source_rejected
#print axioms TFQM.FamilyRegistry.inactive_rejected
#print axioms TFQM.FamilyRegistry.existing_unchanged
#print axioms TFQM.FamilyRegistry.fresh_appended
#print axioms TFQM.FamilyRegistry.prefix_preserved
#print axioms TFQM.FamilyRegistry.collect_append
#print axioms TFQM.FamilyRegistry.duplicate_unchanged
#print axioms TFQM.FamilyRegistry.inactive_source_empty
#print axioms TFQM.FamilyRegistry.empty_rules
#print axioms TFQM.FamilyRegistry.register_self
#print axioms TFQM.FamilyRegistry.register_other
#print axioms TFQM.FamilyRegistry.register_twice
