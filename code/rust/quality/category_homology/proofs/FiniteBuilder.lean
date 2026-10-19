import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Raw overwrite tables, loop-boundary admission and
ordered identity-completion updates. No free-category or fresh-name theorem.
Rust borrowed maps, owned tuple keys, cloning and certificate delegation remain
separate representation/source obligations; category laws are checked elsewhere.
-/
namespace TFQM.FiniteBuilder

abbrev Table := (String × String) → Option String
def update (table : Table) (key : String × String) (value : String) : Table :=
  fun query => if query = key then some value else table query

theorem update_self (table : Table) (key : String × String) (value : String) :
    update table key value key = some value := by simp [update]
theorem update_other (table : Table) (key query : String × String) (value : String) (h : query ≠ key) :
    update table key value query = table query := by simp [update,h]
theorem update_shadow (table : Table) (key : String × String) (first last : String) :
    update (update table key first) key last = update table key last := by
  funext query
  by_cases h : query = key <;> simp [update,h]

def checkedBoundary (object : String) : Option (String × String) → Bool
  | none => true
  | some (source,target) => decide (source = object ∧ target = object)
theorem checked_missing (object : String) : checkedBoundary object none = true := rfl
theorem checked_existing_iff (object source target : String) :
    checkedBoundary object (some (source,target)) = true ↔ source = object ∧ target = object := by
  simp [checkedBoundary]

structure Morphism where
  name : String
  source : String
  target : String

def completeOne (ids : String → Option String) (m : Morphism) (table : Table) : Table :=
  let first := match ids m.source with
    | none => table
    | some identity => update table (identity,m.name) m.name
  match ids m.target with
    | none => first
    | some identity => update first (m.name,identity) m.name

theorem no_identities (ids : String → Option String) (m : Morphism) (table : Table)
    (hs : ids m.source = none) (ht : ids m.target = none) :
    completeOne ids m table = table := by simp [completeOne,hs,ht]
theorem source_only (ids : String → Option String) (m : Morphism) (table : Table) (identity : String)
    (hs : ids m.source = some identity) (ht : ids m.target = none) :
    completeOne ids m table = update table (identity,m.name) m.name := by simp [completeOne,hs,ht]
theorem target_only (ids : String → Option String) (m : Morphism) (table : Table) (identity : String)
    (hs : ids m.source = none) (ht : ids m.target = some identity) :
    completeOne ids m table = update table (m.name,identity) m.name := by simp [completeOne,hs,ht]
theorem both_identities (ids : String → Option String) (m : Morphism) (table : Table) (sourceId targetId : String)
    (hs : ids m.source = some sourceId) (ht : ids m.target = some targetId) :
    completeOne ids m table = update (update table (sourceId,m.name) m.name) (m.name,targetId) m.name := by
  simp [completeOne,hs,ht]

def complete (ids : String → Option String) (morphisms : List Morphism) (table : Table) : Table :=
  morphisms.foldl (fun state m => completeOne ids m state) table
theorem complete_empty (ids : String → Option String) (table : Table) : complete ids [] table = table := rfl
theorem complete_append (ids : String → Option String) (first last : List Morphism) (table : Table) :
    complete ids (first ++ last) table = complete ids last (complete ids first table) := by
  simp [complete, List.foldl_append]

end TFQM.FiniteBuilder

#print axioms TFQM.FiniteBuilder.update_self
#print axioms TFQM.FiniteBuilder.update_other
#print axioms TFQM.FiniteBuilder.update_shadow
#print axioms TFQM.FiniteBuilder.checked_missing
#print axioms TFQM.FiniteBuilder.checked_existing_iff
#print axioms TFQM.FiniteBuilder.no_identities
#print axioms TFQM.FiniteBuilder.source_only
#print axioms TFQM.FiniteBuilder.target_only
#print axioms TFQM.FiniteBuilder.both_identities
#print axioms TFQM.FiniteBuilder.complete_empty
#print axioms TFQM.FiniteBuilder.complete_append
