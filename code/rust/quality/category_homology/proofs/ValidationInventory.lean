import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Literal reports over unrestricted caller data.
Labels are not checkers or certificates. String rendering, Rust Vec capacity,
derive behavior and source correspondence remain separate reviewed obligations.
-/
namespace TFQM.ValidationInventory

structure Result where
  unit : String
  passed : Bool
  messages : List String

structure Issue (U L S : Type) where
  unit : U
  location : L
  message : String
  severity : S

structure Report (U L S : Type) where
  name : String
  results : List Result
  typed : List (Issue U L S)

def pass (unit : String) : Result := ⟨unit, true, []⟩
def fail (unit : String) (messages : List String) : Result := ⟨unit, false, messages⟩
def empty (name : String) : Report U L S := ⟨name, [], []⟩
def add (r : Report U L S) (v : Result) : Report U L S :=
  {r with results := r.results ++ [v]}
def addViolation (r : Report U L S) (rendered : String) (v : Issue U L S) : Report U L S :=
  {name := r.name, results := r.results ++ [fail rendered [v.message]], typed := r.typed ++ [v]}
def addTyped (r : Report U L S) (unit : String) (vs : List (Issue U L S)) : Report U L S :=
  if vs.isEmpty then add r (pass unit)
  else {name := r.name, results := r.results ++ [fail unit (vs.map Issue.message)], typed := r.typed ++ vs}
def allPassed (r : Report U L S) : Bool :=
  r.results.all Result.passed && r.typed.isEmpty
def failureCount (r : Report U L S) : Nat :=
  (r.results.filter fun v => !v.passed).length
def violationCount (r : Report U L S) : Nat := r.typed.length

theorem empty_passes (name : String) : allPassed (empty name : Report U L S) = true := rfl
theorem empty_name (name : String) : (empty name : Report U L S).name = name := rfl
theorem allPassed_iff (r : Report U L S) :
    allPassed r = true ↔ (∀ v ∈ r.results, v.passed = true) ∧ r.typed = [] := by
  simp [allPassed]
theorem add_preserves (r : Report U L S) (v : Result) :
    (add r v).results = r.results ++ [v] ∧ (add r v).typed = r.typed ∧ (add r v).name = r.name := by
  exact ⟨rfl,rfl,rfl⟩
theorem add_pass_count (r : Report U L S) (unit : String) :
    failureCount (add r (pass unit)) = failureCount r := by
  simp [failureCount, add, pass, List.filter_append]
theorem add_fail_count (r : Report U L S) (unit : String) (messages : List String) :
    failureCount (add r (fail unit messages)) = failureCount r + 1 := by
  simp [failureCount, add, fail, List.filter_append]
theorem violation_projection (r : Report U L S) (rendered : String) (v : Issue U L S) :
    (addViolation r rendered v).results = r.results ++ [fail rendered [v.message]] ∧
    (addViolation r rendered v).typed = r.typed ++ [v] := by exact ⟨rfl,rfl⟩
theorem violation_fails (r : Report U L S) (rendered : String) (v : Issue U L S) :
    allPassed (addViolation r rendered v) = false := by
  simp [allPassed, addViolation]
theorem empty_batch (r : Report U L S) (unit : String) :
    addTyped r unit [] = add r (pass unit) := rfl
theorem nonempty_batch (r : Report U L S) (unit : String) (v : Issue U L S) (vs : List (Issue U L S)) :
    (addTyped r unit (v::vs)).results = r.results ++ [fail unit ((v::vs).map Issue.message)] ∧
    (addTyped r unit (v::vs)).typed = r.typed ++ (v::vs) := by exact ⟨rfl,rfl⟩
theorem nonempty_batch_fails (r : Report U L S) (unit : String) (v : Issue U L S) (vs : List (Issue U L S)) :
    allPassed (addTyped r unit (v::vs)) = false := by
  simp [allPassed, addTyped]
theorem violation_count_append (r : Report U L S) (unit : String) (v : Issue U L S) (vs : List (Issue U L S)) :
    violationCount (addTyped r unit (v::vs)) = violationCount r + (v::vs).length := by
  simp [violationCount, addTyped]
theorem failure_count_bound (r : Report U L S) : failureCount r ≤ r.results.length := by
  exact List.length_filter_le _ _

end TFQM.ValidationInventory

#print axioms TFQM.ValidationInventory.empty_passes
#print axioms TFQM.ValidationInventory.empty_name
#print axioms TFQM.ValidationInventory.allPassed_iff
#print axioms TFQM.ValidationInventory.add_preserves
#print axioms TFQM.ValidationInventory.add_pass_count
#print axioms TFQM.ValidationInventory.add_fail_count
#print axioms TFQM.ValidationInventory.violation_projection
#print axioms TFQM.ValidationInventory.violation_fails
#print axioms TFQM.ValidationInventory.empty_batch
#print axioms TFQM.ValidationInventory.nonempty_batch
#print axioms TFQM.ValidationInventory.nonempty_batch_fails
#print axioms TFQM.ValidationInventory.violation_count_append
#print axioms TFQM.ValidationInventory.failure_count_bound
