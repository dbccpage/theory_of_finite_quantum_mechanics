import Mathlib.Data.Int.Basic

/-! AuthorityEffect: None. Literal metadata parameter gates only.
These checked programs specify threshold/tag admission, not HoTT truncations,
exact categories, diagonal functors, Kan universal properties or Rust/MIR.
Fixed-width representation and error text correspondence are source reviewed.
-/
namespace TFQM.ParameterMetadata

def signedLevel (n : Int) : Except String Unit :=
  if n < -2 then .error "level below -2" else .ok ()

theorem signed_success_iff (n : Int) :
    signedLevel n = .ok () ↔ -2 ≤ n := by
  simp [signedLevel]

def optionalLevel : Option Int → Except String Unit
  | none => .ok ()
  | some n => signedLevel n

theorem optional_level_success_iff (level : Option Int) :
    optionalLevel level = .ok () ↔ ∀ n, level = some n → -2 ≤ n := by
  cases level <;> simp [optionalLevel, signed_success_iff]

def positiveBound : Option Nat → Except String Unit
  | none => .ok ()
  | some n => if n = 0 then .error "zero bound" else .ok ()

theorem positive_bound_success_iff (bound : Option Nat) :
    positiveBound bound = .ok () ↔ ∀ n, bound = some n → 0 < n := by
  cases bound <;> simp [positiveBound, Nat.pos_iff_ne_zero]

def arity (n : Nat) : Except String Unit :=
  if n < 2 then .error "arity below two" else .ok ()

theorem arity_success_iff (n : Nat) : arity n = .ok () ↔ 2 ≤ n := by
  simp [arity, not_lt]

def variance (tag : String) : Except String Unit :=
  if tag = "covariant" ∨ tag = "contravariant" then .ok ()
  else .error "unknown variance"

theorem variance_success_iff (tag : String) :
    variance tag = .ok () ↔ tag = "covariant" ∨ tag = "contravariant" := by
  by_cases allowed : tag = "covariant" ∨ tag = "contravariant"
  · simp [variance, allowed]
  · simp [variance, allowed]

def thenCheck (first second : Except String Unit) : Except String Unit :=
  match first with
  | .error error => .error error
  | .ok () => second

theorem first_error (error : String) (later : Except String Unit) :
    thenCheck (.error error) later = .error error := rfl

theorem accepted_prefix (later : Except String Unit) :
    thenCheck (.ok ()) later = later := rfl

#print axioms signed_success_iff
#print axioms optional_level_success_iff
#print axioms positive_bound_success_iff
#print axioms arity_success_iff
#print axioms variance_success_iff
#print axioms first_error
#print axioms accepted_prefix

end TFQM.ParameterMetadata
