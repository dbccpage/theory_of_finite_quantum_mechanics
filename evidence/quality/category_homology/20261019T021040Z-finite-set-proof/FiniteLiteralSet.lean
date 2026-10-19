import Mathlib.Data.Finset.Basic
import Mathlib.Data.List.Nodup

/-! AuthorityEffect: None. Finite literal-string-set admission model.
The nonblank primitive is a declared Boolean predicate, corresponding to the
pinned Rust Unicode-whitespace library check. No Unicode normalization or
mathematical identity beyond stored String equality is assumed. Finset models
the membership behavior of the reviewed BTreeSet; this is not Rust extraction.
-/
namespace TFQM.FiniteLiteralSet

inductive Failure where
  | label
  | element (index : Nat)
  | duplicate (index : Nat)
  | cardinality (declared actual : Nat)
  deriving DecidableEq

def scan (nonblank : String → Bool) (index : Nat) (seen : Finset String) :
    List String → Except Failure Unit
  | [] => .ok ()
  | tag :: rest =>
      if nonblank tag then
        if tag ∈ seen then .error (.duplicate index)
        else scan nonblank (index + 1) (insert tag seen) rest
      else .error (.element index)

theorem scan_success_iff (nonblank : String → Bool) (values : List String)
    (index : Nat) (seen : Finset String) :
    scan nonblank index seen values = .ok () ↔
      (∀ tag ∈ values, nonblank tag = true) ∧ values.Nodup ∧
      (∀ tag ∈ values, tag ∉ seen) := by
  induction values generalizing index seen with
  | nil => simp [scan]
  | cons tag rest ih =>
      by_cases member : tag ∈ seen
      · simp [scan, member, List.nodup_cons]
      · cases valid : nonblank tag <;>
          simp_all [scan, List.nodup_cons, Finset.mem_insert, ih]

theorem first_empty (nonblank : String → Bool) (tag : String) (rest : List String)
    (index : Nat) (seen : Finset String) (empty : nonblank tag = false) :
    scan nonblank index seen (tag :: rest) = .error (.element index) := by
  simp [scan, empty]

theorem first_duplicate (nonblank : String → Bool) (tag : String) (rest : List String)
    (index : Nat) (seen : Finset String) (valid : nonblank tag = true)
    (member : tag ∈ seen) :
    scan nonblank index seen (tag :: rest) = .error (.duplicate index) := by
  simp [scan, valid, member]

def cardinalityCheck (declared : Option Nat) (actual : Nat) : Except Failure Unit :=
  match declared with
  | none => .ok ()
  | some n => if n = actual then .ok () else .error (.cardinality n actual)

theorem cardinality_success_iff (declared : Option Nat) (actual : Nat) :
    cardinalityCheck declared actual = .ok () ↔
      ∀ n, declared = some n → n = actual := by
  cases declared <;> simp [cardinalityCheck]

theorem bind_unit_success (first second : Except Failure Unit) :
    first.bind (fun _ => second) = .ok () ↔ first = .ok () ∧ second = .ok () := by
  cases first with
  | error error => simp [Except.bind]
  | ok value => cases value; simp [Except.bind]

structure Raw where
  label : String
  elements : List String
  declared : Option Nat
  notes : List String

def checks (nonblank : String → Bool) (raw : Raw) : Except Failure Unit :=
  if nonblank raw.label then
    (scan nonblank 0 ∅ raw.elements).bind fun _ =>
      cardinalityCheck raw.declared raw.elements.length
  else .error .label

def lawful (nonblank : String → Bool) (raw : Raw) : Prop :=
  nonblank raw.label = true ∧ (∀ tag ∈ raw.elements, nonblank tag = true) ∧
  raw.elements.Nodup ∧ (∀ n, raw.declared = some n → n = raw.elements.length)

theorem checks_success_iff (nonblank : String → Bool) (raw : Raw) :
    checks nonblank raw = .ok () ↔ lawful nonblank raw := by
  cases label : nonblank raw.label <;>
    simp [checks, lawful, label, bind_unit_success, scan_success_iff, cardinality_success_iff]
  tauto

def admit (nonblank : String → Bool) (raw : Raw) : Except Failure Raw :=
  (checks nonblank raw).map fun _ => raw

theorem admit_preserves_raw (nonblank : String → Bool) (raw result : Raw)
    (accepted : admit nonblank raw = .ok result) : result = raw := by
  unfold admit at accepted
  cases status : checks nonblank raw <;> simp_all [Except.map]

theorem admit_invariants (nonblank : String → Bool) (raw result : Raw)
    (accepted : admit nonblank raw = .ok result) : lawful nonblank result := by
  have same := admit_preserves_raw nonblank raw result accepted
  subst result
  apply (checks_success_iff nonblank raw).mp
  unfold admit at accepted
  cases status : checks nonblank raw <;> simp_all [Except.map]

#print axioms scan_success_iff
#print axioms first_empty
#print axioms first_duplicate
#print axioms cardinality_success_iff
#print axioms bind_unit_success
#print axioms checks_success_iff
#print axioms admit_preserves_raw
#print axioms admit_invariants

end TFQM.FiniteLiteralSet
