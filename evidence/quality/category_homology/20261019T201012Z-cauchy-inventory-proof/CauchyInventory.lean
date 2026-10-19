import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Raw named-table observations, ordered first pair,
inventory filtering and historical raw-data admission. No category typing,
boundary completeness, Karoubi construction or Cauchy-completeness theorem. -/
namespace TFQM.CauchyInventory

def observedEqual : Option String → Option String → Bool
  | some a, some b => decide (a = b)
  | _, _ => false

theorem equal_defined (a b : String) :
    observedEqual (some a) (some b) = true ↔ a = b := by simp [observedEqual]
theorem missing_left (b : Option String) : observedEqual none b = false := by cases b <;> rfl
theorem missing_right (a : Option String) : observedEqual a none = false := by cases a <;> rfl

def pairCheck (sameRetract : Bool) (rs sr identity : Option String) (e : String) : Bool :=
  sameRetract && observedEqual rs identity && observedEqual sr (some e)

theorem pair_checks (same : Bool) (rs sr identity : Option String) (e : String) :
    pairCheck same rs sr identity e = true ↔ same = true ∧
      observedEqual rs identity = true ∧ observedEqual sr (some e) = true := by
  simp [pairCheck, and_assoc]

variable {α : Type}
def first (predicate : α → Bool) : List α → Option α
  | [] => none
  | x :: xs => if predicate x then some x else first predicate xs

theorem first_empty (predicate : α → Bool) : first predicate [] = none := rfl
theorem first_head (predicate : α → Bool) (x : α) (xs : List α) (h : predicate x = true) :
    first predicate (x :: xs) = some x := by simp [first, h]
theorem first_skip (predicate : α → Bool) (x : α) (xs : List α) (h : predicate x = false) :
    first predicate (x :: xs) = first predicate xs := by simp [first, h]

theorem first_sound (predicate : α → Bool) (xs : List α) (x : α)
    (h : first predicate xs = some x) : x ∈ xs ∧ predicate x = true := by
  induction xs with
  | nil => simp [first] at h
  | cons head rest ih =>
    by_cases hit : predicate head = true
    · have eq : head = x := by simpa [first, hit] using h
      subst x
      exact ⟨List.mem_cons_self, hit⟩
    · have tail : first predicate rest = some x := by simpa [first, hit] using h
      obtain ⟨member, valid⟩ := ih tail
      exact ⟨List.mem_cons_of_mem _ member, valid⟩

theorem first_exists (predicate : α → Bool) (xs : List α) :
    (first predicate xs).isSome = true ↔ ∃ x ∈ xs, predicate x = true := by
  induction xs with
  | nil => simp [first]
  | cons x xs ih => cases h : predicate x <;> simp [first, h, ih]

theorem first_append (predicate : α → Bool) (xs ys : List α) :
    first predicate (xs ++ ys) =
      (match first predicate xs with | some x => some x | none => first predicate ys) := by
  induction xs with
  | nil => rfl
  | cons x xs ih => cases h : predicate x <;> simp [first, h, ih]

def inventory (rows : List α) (identity idempotent : α → Bool) : List α :=
  rows.filter (fun row => !identity row && idempotent row)

theorem inventory_member (rows : List α) (identity idempotent : α → Bool) (x : α) :
    x ∈ inventory rows identity idempotent ↔
      x ∈ rows ∧ identity x = false ∧ idempotent x = true := by
  simp [inventory]

theorem inventory_append (xs ys : List α) (identity idempotent : α → Bool) :
    inventory (xs ++ ys) identity idempotent =
      inventory xs identity idempotent ++ inventory ys identity idempotent := by simp [inventory]

theorem inventory_duplicates (x : α) (identity idempotent : α → Bool)
    (skip : identity x = false) (retained : idempotent x = true) :
    inventory [x,x] identity idempotent = [x,x] := by simp [inventory, skip, retained]

def observations (e : String) (ee rs sr identity : Option String) : List Bool :=
  [observedEqual ee (some e), observedEqual rs identity, observedEqual sr (some e)]

theorem three_checks (e : String) (ee rs sr identity : Option String) :
    (observations e ee rs sr identity).all id = true ↔
      observedEqual ee (some e) = true ∧ observedEqual rs identity = true ∧
      observedEqual sr (some e) = true := by simp [observations]

def admitRaw (raw : α) (flags : List Bool) : Except Unit α :=
  if flags.all id then .ok raw else .error ()

theorem admit_preserves_raw (raw out : α) (flags : List Bool)
    (h : admitRaw raw flags = .ok out) : out = raw := by
  unfold admitRaw at h
  split at h
  · exact (Except.ok.inj h).symm
  · cases h

theorem admit_success_flags (raw out : α) (flags : List Bool)
    (h : admitRaw raw flags = .ok out) : flags.all id = true := by
  unfold admitRaw at h
  split at h
  · assumption
  · cases h

theorem failed_flag (raw : α) (before after : List Bool) :
    admitRaw raw (before ++ false :: after) = .error () := by simp [admitRaw]

end TFQM.CauchyInventory

#print axioms TFQM.CauchyInventory.equal_defined
#print axioms TFQM.CauchyInventory.missing_left
#print axioms TFQM.CauchyInventory.missing_right
#print axioms TFQM.CauchyInventory.pair_checks
#print axioms TFQM.CauchyInventory.first_empty
#print axioms TFQM.CauchyInventory.first_head
#print axioms TFQM.CauchyInventory.first_skip
#print axioms TFQM.CauchyInventory.first_sound
#print axioms TFQM.CauchyInventory.first_exists
#print axioms TFQM.CauchyInventory.first_append
#print axioms TFQM.CauchyInventory.inventory_member
#print axioms TFQM.CauchyInventory.inventory_append
#print axioms TFQM.CauchyInventory.inventory_duplicates
#print axioms TFQM.CauchyInventory.three_checks
#print axioms TFQM.CauchyInventory.admit_preserves_raw
#print axioms TFQM.CauchyInventory.admit_success_flags
#print axioms TFQM.CauchyInventory.failed_flag
