import Mathlib.LinearAlgebra.Matrix.Rank

/-! AuthorityEffect: None. A two-step exact rational differential and its
admission checker. Dynamic storage shape and canonical-Q guards justify the
matrix representation separately. No Rust/MIR refinement, allocation theorem,
provenance authentication or computation of homology/ranks is claimed.
-/
namespace TFQM.TwoStepComplex

open Matrix

structure Admitted (a b c : Nat) where
  first : Matrix (Fin a) (Fin b) ℚ
  second : Matrix (Fin b) (Fin c) ℚ
  zeroProduct : first * second = 0

noncomputable def admit {a b c : Nat}
    (first : Matrix (Fin a) (Fin b) ℚ) (second : Matrix (Fin b) (Fin c) ℚ) :
    Option (Admitted a b c) := by
  classical
  exact if law : first * second = 0 then some ⟨first, second, law⟩ else none

theorem admission_success_iff {a b c : Nat}
    (first : Matrix (Fin a) (Fin b) ℚ) (second : Matrix (Fin b) (Fin c) ℚ) :
    (∃ result, admit first second = some result) ↔ first * second = 0 := by
  classical
  by_cases law : first * second = 0 <;> simp [admit, law]

theorem admission_failure {a b c : Nat}
    (first : Matrix (Fin a) (Fin b) ℚ) (second : Matrix (Fin b) (Fin c) ℚ)
    (bad : first * second ≠ 0) : admit first second = none := by
  classical
  simp [admit, bad]

theorem admission_preserves {a b c : Nat}
    (first : Matrix (Fin a) (Fin b) ℚ) (second : Matrix (Fin b) (Fin c) ℚ)
    (result : Admitted a b c) (success : admit first second = some result) :
    result.first = first ∧ result.second = second := by
  classical
  unfold admit at success
  split at success
  · have same := Option.some.inj success
    cases same
    exact ⟨rfl, rfl⟩
  · cases success

theorem input_zero_product {a b c : Nat}
    (first : Matrix (Fin a) (Fin b) ℚ) (second : Matrix (Fin b) (Fin c) ℚ)
    (result : Admitted a b c) (success : admit first second = some result) :
    first * second = 0 := by
  have preserved := admission_preserves first second result success
  rw [← preserved.1, ← preserved.2]
  exact result.zeroProduct

theorem differential_square_zero {a b c : Nat} (result : Admitted a b c)
    (vector : Fin c → ℚ) : result.first *ᵥ (result.second *ᵥ vector) = 0 := by
  rw [Matrix.mulVec_mulVec, result.zeroProduct, Matrix.zero_mulVec]

theorem image_is_cycle {a b c : Nat} (result : Admitted a b c)
    (vector : Fin b → ℚ) (in_image : ∃ input, result.second *ᵥ input = vector) :
    result.first *ᵥ vector = 0 := by
  obtain ⟨input, same⟩ := in_image
  rw [← same]
  exact differential_square_zero result input

def gates {Error Value : Type} : List (Except Error Unit) → Value → Except Error Value
  | [], value => .ok value
  | .error error :: _, _ => .error error
  | .ok () :: rest, value => gates rest value

theorem failed_gate {Error Value : Type} (error : Error)
    (tail : List (Except Error Unit)) (value : Value) :
    gates (.error error :: tail) value = .error error := rfl

theorem passed_gate {Error Value : Type} (tail : List (Except Error Unit)) (value : Value) :
    gates (.ok () :: tail) value = gates tail value := rfl

#print axioms admission_success_iff
#print axioms admission_failure
#print axioms admission_preserves
#print axioms input_zero_product
#print axioms differential_square_zero
#print axioms image_is_cycle
#print axioms failed_gate
#print axioms passed_gate

end TFQM.TwoStepComplex
