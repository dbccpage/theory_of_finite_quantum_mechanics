import Mathlib.Data.Int.Basic

/-! AuthorityEffect: None. Literal record guards and diagnostic inventories.
No associativity of formatted skill names, functor laws, HoTT semantics,
registry binding, density matrix or zeta theorem follows from these programs.
String/Vec and raw BigRational correspondence is a separate source review.
-/
namespace TFQM.RootRecords

def joinable (target nextSource category nextCategory : String) : Bool :=
  decide (target = nextSource ∧ category = nextCategory)

theorem joinable_iff (t s c d : String) : joinable t s c d = true ↔ t = s ∧ c = d := by
  simp [joinable]

theorem foreign_category_refused (t s c d : String) (foreign : c ≠ d) :
    joinable t s c d = false := by
  simp [joinable, foreign]

def missingLabels (checks : List (Bool × String)) : List String :=
  checks.filterMap fun (ok, message) => if ok then none else some message

theorem report_empty : missingLabels [] = [] := rfl

theorem report_valid_head (message : String) (tail : List (Bool × String)) :
    missingLabels ((true, message) :: tail) = missingLabels tail := rfl

theorem report_failed_head (message : String) (tail : List (Bool × String)) :
    missingLabels ((false, message) :: tail) = message :: missingLabels tail := rfl

def countThreshold (count level : Nat) : Bool := decide (level ≤ count)

theorem threshold_iff (count level : Nat) : countThreshold count level = true ↔ level ≤ count := by
  simp [countThreshold]

def massGuard (nonblank : Bool) (numerator denominator : Int) : Except String Unit :=
  if !nonblank then .error "empty residual label"
  else if denominator ≤ 0 ∨ numerator < 0 then .error "weight must be a defined nonnegative rational"
  else .ok ()

theorem mass_success_iff (nonblank : Bool) (n d : Int) :
    massGuard nonblank n d = .ok () ↔ nonblank = true ∧ 0 ≤ n ∧ 0 < d := by
  cases nonblank with
  | false => simp [massGuard]
  | true => simp [massGuard]; omega

theorem mass_label_first (n d : Int) :
    massGuard false n d = .error "empty residual label" := rfl

#print axioms joinable_iff
#print axioms foreign_category_refused
#print axioms report_empty
#print axioms report_valid_head
#print axioms report_failed_head
#print axioms threshold_iff
#print axioms mass_success_iff
#print axioms mass_label_first

end TFQM.RootRecords
