import Mathlib.Data.Int.Basic

/-! AuthorityEffect: None. Numeric identifier and bounded degree guards.
The actual u64 parser, Unicode whitespace classification, formatted text and
derived Rust serialization/error protocols are reviewed runtime boundaries.
Nominal kinds do not assert globally unique generated identifiers.
-/
namespace TFQM.HomologyProtocols

def numericAdmission (n : Nat) : Option Nat := if n = 0 then none else some n

theorem numeric_zero : numericAdmission 0 = none := rfl

theorem numeric_success_iff (n : Nat) : numericAdmission n = some n ↔ n ≠ 0 := by
  by_cases zero : n = 0 <;> simp [numericAdmission, zero]

theorem numeric_preserves_payload (n value : Nat)
    (success : numericAdmission n = some value) : value = n := by
  unfold numericAdmission at success
  split at success
  · contradiction
  · exact (Option.some.inj success).symm

def withinDegree (n : Int) : Prop := -2147483648 ≤ n ∧ n ≤ 2147483647
instance (n : Int) : Decidable (withinDegree n) := inferInstanceAs (Decidable (_ ∧ _))

def predecessor (n : Int) : Option Int := if withinDegree (n - 1) then some (n - 1) else none
def successor (n : Int) : Option Int := if withinDegree (n + 1) then some (n + 1) else none

theorem predecessor_success_iff (n : Int) :
    predecessor n = some (n - 1) ↔ withinDegree (n - 1) := by
  by_cases fits : withinDegree (n - 1) <;> simp [predecessor, fits]

theorem successor_success_iff (n : Int) :
    successor n = some (n + 1) ↔ withinDegree (n + 1) := by
  by_cases fits : withinDegree (n + 1) <;> simp [successor, fits]

theorem predecessor_refusal_iff (n : Int) (admitted : withinDegree n) :
    predecessor n = none ↔ n = -2147483648 := by
  simp only [predecessor]
  unfold withinDegree at *
  split <;> simp_all <;> omega

theorem successor_refusal_iff (n : Int) (admitted : withinDegree n) :
    successor n = none ↔ n = 2147483647 := by
  simp only [successor]
  unfold withinDegree at *
  split <;> simp_all <;> omega

theorem degree_drop_inverts (n : Int) (admitted : withinDegree n)
    (notMin : n ≠ -2147483648) :
    predecessor n = some (n - 1) ∧ successor (n - 1) = some n ∧ n - (n - 1) = 1 := by
  have fits : withinDegree (n - 1) := by unfold withinDegree at *; omega
  have restore : n - 1 + 1 = n := by omega
  simp [predecessor, successor, fits, restore, admitted]

#print axioms numeric_zero
#print axioms numeric_success_iff
#print axioms numeric_preserves_payload
#print axioms predecessor_success_iff
#print axioms successor_success_iff
#print axioms predecessor_refusal_iff
#print axioms successor_refusal_iff
#print axioms degree_drop_inverts

end TFQM.HomologyProtocols
