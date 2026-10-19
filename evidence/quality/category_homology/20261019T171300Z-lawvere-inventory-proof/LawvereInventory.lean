import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Exact slot admission and raw finite declared-name
inventory. No typed Lawvere theory, profunctor or Cauchy-completeness theorem.
Borrowed Rust indexes, String ordering and library binary search are reviewed
representation obligations, not compiler extraction of this pure model. -/
namespace TFQM.LawvereInventory

def checkedSlot (limit i j : Nat) : Option Nat :=
  if i + j ≤ limit then some (i + j) else none

theorem slot_fits (limit i j : Nat) (h : i + j ≤ limit) :
    checkedSlot limit i j = some (i + j) := by simp [checkedSlot,h]
theorem slot_refused (limit i j : Nat) (h : limit < i + j) :
    checkedSlot limit i j = none := by simp [checkedSlot, Nat.not_le.mpr h]
theorem slot_exact (limit i j value : Nat) (h : checkedSlot limit i j = some value) :
    value = i + j ∧ value ≤ limit := by
  simp only [checkedSlot] at h
  split at h <;> simp_all
theorem slot_max_zero (limit : Nat) : checkedSlot limit limit 0 = some limit := by
  simp [checkedSlot]
theorem slot_max_positive (limit j : Nat) (h : 0 < j) : checkedSlot limit limit j = none := by
  apply slot_refused
  omega

def observedEqual : Option String → Option String → Bool
  | some left, some right => decide (left = right)
  | _, _ => false

theorem equal_defined (left right : String) :
    observedEqual (some left) (some right) = true ↔ left = right := by simp [observedEqual]
theorem absent_left (right : Option String) : observedEqual none right = false := by
  cases right <;> rfl
theorem absent_right (left : Option String) : observedEqual left none = false := by
  cases left <;> rfl

def hasPair (names : List String) (pair : String → String → Bool) : Bool :=
  names.any (fun r => names.any (fun s => pair r s))

theorem pair_iff (names : List String) (pair : String → String → Bool) :
    hasPair names pair = true ↔ ∃ r ∈ names, ∃ s ∈ names, pair r s = true := by
  simp [hasPair]

def unsplit (names : List String) (unary idem split : String → Bool) : List String :=
  names.filter (fun name => unary name && idem name && !split name)

theorem unsplit_member (names : List String) (unary idem split : String → Bool) (name : String) :
    name ∈ unsplit names unary idem split ↔
      name ∈ names ∧ unary name = true ∧ idem name = true ∧ split name = false := by
  simp [unsplit, and_assoc]
theorem unsplit_empty (unary idem split : String → Bool) : unsplit [] unary idem split = [] := rfl
theorem unsplit_append (first last : List String) (unary idem split : String → Bool) :
    unsplit (first ++ last) unary idem split =
      unsplit first unary idem split ++ unsplit last unary idem split := by simp [unsplit]
theorem unsplit_duplicate (name : String) (unary idem split : String → Bool)
    (hu : unary name = true) (hi : idem name = true) (hs : split name = false) :
    unsplit [name,name] unary idem split = [name,name] := by simp [unsplit,hu,hi,hs]
theorem split_excluded (names : List String) (unary idem split : String → Bool) (name : String)
    (hs : split name = true) : name ∉ unsplit names unary idem split := by simp [unsplit_member,hs]

end TFQM.LawvereInventory

#print axioms TFQM.LawvereInventory.slot_fits
#print axioms TFQM.LawvereInventory.slot_refused
#print axioms TFQM.LawvereInventory.slot_exact
#print axioms TFQM.LawvereInventory.slot_max_zero
#print axioms TFQM.LawvereInventory.slot_max_positive
#print axioms TFQM.LawvereInventory.equal_defined
#print axioms TFQM.LawvereInventory.absent_left
#print axioms TFQM.LawvereInventory.absent_right
#print axioms TFQM.LawvereInventory.pair_iff
#print axioms TFQM.LawvereInventory.unsplit_member
#print axioms TFQM.LawvereInventory.unsplit_empty
#print axioms TFQM.LawvereInventory.unsplit_append
#print axioms TFQM.LawvereInventory.unsplit_duplicate
#print axioms TFQM.LawvereInventory.split_excluded
