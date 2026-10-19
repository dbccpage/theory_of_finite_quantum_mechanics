import Mathlib.Data.List.Basic

/-!
AuthorityEffect: None.

Ordered finite metadata checks. A Boolean is the public String::is_empty
predicate's negation, not a mathematical-law premise. Source review must bind
each actual field, diagnostic and return path to this model. These theorems
do not verify serde, Rust/MIR, allocations, or any category-theoretic law.
-/

namespace TFQM.MetadataValidation

def validate : List (String × Bool) → Except String Unit
  | [] => .ok ()
  | (name, valid) :: rest => if valid then validate rest else .error name

theorem success_iff (fields : List (String × Bool)) :
    validate fields = .ok () ↔ ∀ field ∈ fields, field.2 = true := by
  induction fields with
  | nil => simp [validate]
  | cons field rest ih =>
    rcases field with ⟨name, valid⟩
    cases valid <;> simp [validate, ih]

theorem failed_head (name : String) (rest : List (String × Bool)) :
    validate ((name, false) :: rest) = .error name := by
  simp [validate]

theorem valid_head (name : String) (rest : List (String × Bool)) :
    validate ((name, true) :: rest) = validate rest := by
  simp [validate]

theorem first_error_preserved (prefix : List (String × Bool))
    (all_valid : ∀ field ∈ prefix, field.2 = true)
    (name : String) (rest : List (String × Bool)) :
    validate (prefix ++ (name, false) :: rest) = .error name := by
  induction prefix with
  | nil => simp [validate]
  | cons field tail ih =>
    rcases field with ⟨label, valid⟩
    have head_valid : valid = true := all_valid (label, valid) (by simp)
    have tail_valid : ∀ field ∈ tail, field.2 = true := by
      intro field member
      exact all_valid field (by simp [member])
    simp [validate, head_valid, ih tail_valid]

def inspect (raw : α) (fields : List (String × Bool)) : Except String α :=
  (validate fields).map fun _ => raw

theorem inspect_preserves_raw (raw : α) (fields : List (String × Bool))
    (value : α) (accepted : inspect raw fields = .ok value) : value = raw := by
  unfold inspect at accepted
  cases result : validate fields <;> simp_all

theorem failed_check_returns_no_value (raw : α) (fields : List (String × Bool))
    (name : String) (failed : validate fields = .error name) :
    inspect raw fields = .error name := by
  simp [inspect, failed]

#print axioms success_iff
#print axioms failed_head
#print axioms valid_head
#print axioms first_error_preserved
#print axioms inspect_preserves_raw
#print axioms failed_check_returns_no_value

end TFQM.MetadataValidation
