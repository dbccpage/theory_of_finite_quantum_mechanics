import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Ordered raw finite Cartesian witness products and
defined nonnegative raw-weight admission predicate. No profunctor action laws,
general coend,encoding injectivity or Rust storage/compiler extraction. -/
namespace TFQM.FiniteProfunctorInventory

variable {A B I : Type}

def product (left : List A) (right : List B) : List (A × B) :=
  left.flatMap fun x => right.map fun y => (x, y)

theorem product_empty_left (right : List B) : product ([] : List A) right = [] := rfl
theorem product_empty_right (left : List A) : product left ([] : List B) = [] := by
  simp [product]

theorem product_append (first second : List A) (right : List B) :
    product (first ++ second) right = product first right ++ product second right := by
  simp [product]

theorem product_length (left : List A) (right : List B) :
    (product left right).length = left.length * right.length := by
  induction left with
  | nil => simp [product]
  | cons x xs ih => simp [product, Nat.add_mul] at ih ⊢; omega

theorem product_member (left : List A) (right : List B) (x : A) (y : B) :
    (x, y) ∈ product left right ↔ x ∈ left ∧ y ∈ right := by
  simp [product]

def contributions (middle : List I) (left : I → List A) (right : I → List B) :
    List (A × B) := middle.flatMap fun i => product (left i) (right i)

theorem middle_empty (left : I → List A) (right : I → List B) :
    contributions [] left right = [] := rfl

theorem middle_append (first second : List I) (left : I → List A) (right : I → List B) :
    contributions (first ++ second) left right =
      contributions first left right ++ contributions second left right := by
  simp [contributions]

theorem middle_duplicate (i : I) (left : I → List A) (right : I → List B) :
    contributions [i, i] left right =
      product (left i) (right i) ++ product (left i) (right i) := by
  simp [contributions]

def admittedWeight (numerator denominator : Int) : Bool :=
  decide (0 < denominator ∧ 0 ≤ numerator)

theorem weight_iff (numerator denominator : Int) :
    admittedWeight numerator denominator = true ↔ 0 < denominator ∧ 0 ≤ numerator := by
  simp [admittedWeight]

theorem zero_denominator (numerator : Int) : admittedWeight numerator 0 = false := by
  simp [admittedWeight]

theorem negative_numerator (numerator denominator : Int) (negative : numerator < 0) :
    admittedWeight numerator denominator = false := by
  simp [admittedWeight, Int.not_le.mpr negative]

theorem zero_weight (denominator : Int) (positive : 0 < denominator) :
    admittedWeight 0 denominator = true := by simp [admittedWeight, positive]

end TFQM.FiniteProfunctorInventory

#print axioms TFQM.FiniteProfunctorInventory.product_empty_left
#print axioms TFQM.FiniteProfunctorInventory.product_empty_right
#print axioms TFQM.FiniteProfunctorInventory.product_append
#print axioms TFQM.FiniteProfunctorInventory.product_length
#print axioms TFQM.FiniteProfunctorInventory.product_member
#print axioms TFQM.FiniteProfunctorInventory.middle_empty
#print axioms TFQM.FiniteProfunctorInventory.middle_append
#print axioms TFQM.FiniteProfunctorInventory.middle_duplicate
#print axioms TFQM.FiniteProfunctorInventory.weight_iff
#print axioms TFQM.FiniteProfunctorInventory.zero_denominator
#print axioms TFQM.FiniteProfunctorInventory.negative_numerator
#print axioms TFQM.FiniteProfunctorInventory.zero_weight
