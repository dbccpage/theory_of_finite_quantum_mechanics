import Mathlib.Data.Nat.Basic

/-! AuthorityEffect: None. Literal shape and typed-error programs only.
No category identity, smallness, cone commutativity or universal property is
proved. Rust String/Vec representation and source correspondence are reviewed
separately from these kernel-checked guard and error-tag invariants.
-/
namespace TFQM.ShapeInventory

inductive Failure where
  | shape (detail : String)
  | law (detail : String)
  | precondition (detail : String)
  deriving DecidableEq

def context (location : String) : Failure → Failure
  | .shape detail => .shape (location ++ ": " ++ detail)
  | .law detail => .law detail
  | .precondition detail => .precondition detail

theorem context_shape (location detail : String) :
    context location (.shape detail) = .shape (location ++ ": " ++ detail) := rfl

theorem context_law (location detail : String) :
    context location (.law detail) = .law detail := rfl

theorem context_precondition (location detail : String) :
    context location (.precondition detail) = .precondition detail := rfl

def contextualize (location : String) : Except Failure Unit → Except Failure Unit
  | .error error => .error (context location error)
  | .ok () => .ok ()

theorem contextual_failure (location : String) (error : Failure) :
    contextualize location (.error error) = .error (context location error) := rfl

theorem context_success_iff (location : String) (result : Except Failure Unit) :
    contextualize location result = .ok () ↔ result = .ok () := by
  cases result with
  | error error => simp [contextualize]
  | ok value => cases value; rfl

def endomorphismBoundary (source target : String) : Except Failure Unit :=
  if source = target then .ok () else .error (.shape "non-endomorphism")

theorem endomorphism_success_iff (source target : String) :
    endomorphismBoundary source target = .ok () ↔ source = target := by
  by_cases same : source = target <;> simp [endomorphismBoundary, same]

def alignment (supplied expected : Nat) : Except Failure Unit :=
  if supplied = 0 ∨ supplied = expected then .ok ()
  else .error (.shape "misaligned optional inventory")

theorem alignment_success_iff (supplied expected : Nat) :
    alignment supplied expected = .ok () ↔ supplied = 0 ∨ supplied = expected := by
  by_cases allowed : supplied = 0 ∨ supplied = expected <;> simp [alignment, allowed]

def requireMembers (count : Nat) : Except Failure Unit :=
  if count = 0 then .error (.shape "empty inventory") else .ok ()

theorem members_success_iff (count : Nat) : requireMembers count = .ok () ↔ 0 < count := by
  simp [requireMembers, Nat.pos_iff_ne_zero]

def labelBinding (objects : Nat) (child parent : String) : Except Failure Unit :=
  if objects = 0 ∨ child = parent then .ok ()
  else .error (.shape "presentation label mismatch")

theorem label_binding_success_iff (objects : Nat) (child parent : String) :
    labelBinding objects child parent = .ok () ↔ objects = 0 ∨ child = parent := by
  by_cases allowed : objects = 0 ∨ child = parent <;> simp [labelBinding, allowed]

#print axioms context_shape
#print axioms context_law
#print axioms context_precondition
#print axioms contextual_failure
#print axioms context_success_iff
#print axioms endomorphism_success_iff
#print axioms alignment_success_iff
#print axioms members_success_iff
#print axioms label_binding_success_iff

end TFQM.ShapeInventory
