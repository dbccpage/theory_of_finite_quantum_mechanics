import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Surjective fiber descent including Option-definedness
reflection and Boolean truth/falsity,composition and mixed-radix/prefix bounds.
Rust table/signature/map admission,first-error order/storage refinement separate. -/
namespace TFQM.PartialStructure

variable {X Y Z V W : Type}

def FiberConstant (q : X → Y) (value : X → V) : Prop :=
  ∀ x y, q x = q y → value x = value y

noncomputable def factor (q : X → Y) (onto : Function.Surjective q) (value : X → V) (y : Y) : V :=
  value (Classical.choose (onto y))

theorem factor_spec (q : X → Y) (onto : Function.Surjective q) (value : X → V)
    (constant : FiberConstant q value) (x : X) : factor q onto value (q x) = value x :=
  constant _ _ (Classical.choose_spec (onto (q x)))

theorem factor_unique (q : X → Y) (onto : Function.Surjective q) (value : X → V)
    (g h : Y → V) (left : ∀ x, g (q x) = value x) (right : ∀ x, h (q x) = value x) : g = h := by
  funext y
  obtain ⟨x, rfl⟩ := onto y
  exact (left x).trans (right x).symm

theorem exists_descent_iff (q : X → Y) (onto : Function.Surjective q) (value : X → V) :
    (∃ g : Y → V, ∀ x, g (q x) = value x) ↔ FiberConstant q value := by
  constructor
  · rintro ⟨g, law⟩ x y same
    exact (law x).symm.trans ((congrArg g same).trans (law y))
  · intro constant
    exact ⟨factor q onto value, factor_spec q onto value constant⟩

theorem conflict_refuses (q : X → Y) (value : X → V) (x y : X)
    (same : q x = q y) (different : value x ≠ value y) :
    ¬∃ g : Y → V, ∀ x, g (q x) = value x := by
  rintro ⟨g, law⟩
  exact different ((law x).symm.trans ((congrArg g same).trans (law y)))

theorem none_reflected (output : Z → W) (value : Option Z) :
    value.map output = none ↔ value = none := by cases value <;> simp

theorem none_some_conflict (output : Z → W) (value : Z) :
    (none : Option Z).map output ≠ (some value).map output := by simp

theorem collapsed_defined (output : Z → W) (left right : Z) (same : output left = output right) :
    (some left).map output = (some right).map output := congrArg some same

theorem false_true_conflict : (false : Bool) ≠ true := by decide

theorem output_map_composition (first : Y → Z) (second : Z → W) (value : Option Y) :
    (value.map first).map second = value.map (second ∘ first) := by cases value <;> rfl

theorem descent_composition (first : X → Y) (second : Y → Z)
    (value : X → V) (middle : Y → V) (target : Z → V)
    (left : ∀ x, middle (first x) = value x)
    (right : ∀ y, target (second y) = middle y) (x : X) :
    target ((second ∘ first) x) = value x := (right (first x)).trans (left x)

theorem coordinate_bound (row base : Nat) (positive : 0 < base) : row % base < base :=
  Nat.mod_lt row positive

theorem mixed_digit_bound (digit base suffix stride : Nat)
    (digitBound : digit < base) (suffixBound : suffix < stride) :
    digit * stride + suffix < base * stride := by
  calc
    digit * stride + suffix < digit * stride + stride := Nat.add_lt_add_left suffixBound _
    _ = (digit + 1) * stride := by simp [Nat.add_mul]
    _ ≤ base * stride := Nat.mul_le_mul_right stride (Nat.succ_le_of_lt digitBound)

theorem mixed_value_fits (value count maximum : Nat) (inside : value < count) (fits : count ≤ maximum) :
    value ≤ maximum := Nat.le_trans (Nat.le_of_lt inside) fits

def checkedProducts (maximum : Nat) : Nat → List Nat → Option Nat
  | n, [] => some n
  | n, size :: rest => if n * size ≤ maximum then checkedProducts maximum (n * size) rest else none

theorem nullary_product (maximum : Nat) : checkedProducts maximum 1 [] = some 1 := rfl

theorem prefix_refused (maximum n size : Nat) (rest : List Nat) (overflow : maximum < n * size) :
    checkedProducts maximum n (size :: rest) = none := by
  simp [checkedProducts, Nat.not_le.mpr overflow]

theorem zero_prefix (maximum : Nat) (rest : List Nat) : checkedProducts maximum 0 rest = some 0 := by
  induction rest with
  | nil => rfl
  | cons size rest ih => simpa [checkedProducts] using ih

theorem overflow_before_zero (maximum n size : Nat) (overflow : maximum < n * size) :
    checkedProducts maximum n [size, 0] = none := prefix_refused maximum n size [0] overflow

end TFQM.PartialStructure

#print axioms TFQM.PartialStructure.factor
#print axioms TFQM.PartialStructure.factor_spec
#print axioms TFQM.PartialStructure.factor_unique
#print axioms TFQM.PartialStructure.exists_descent_iff
#print axioms TFQM.PartialStructure.conflict_refuses
#print axioms TFQM.PartialStructure.none_reflected
#print axioms TFQM.PartialStructure.none_some_conflict
#print axioms TFQM.PartialStructure.collapsed_defined
#print axioms TFQM.PartialStructure.false_true_conflict
#print axioms TFQM.PartialStructure.output_map_composition
#print axioms TFQM.PartialStructure.descent_composition
#print axioms TFQM.PartialStructure.coordinate_bound
#print axioms TFQM.PartialStructure.mixed_digit_bound
#print axioms TFQM.PartialStructure.mixed_value_fits
#print axioms TFQM.PartialStructure.nullary_product
#print axioms TFQM.PartialStructure.prefix_refused
#print axioms TFQM.PartialStructure.zero_prefix
#print axioms TFQM.PartialStructure.overflow_before_zero
