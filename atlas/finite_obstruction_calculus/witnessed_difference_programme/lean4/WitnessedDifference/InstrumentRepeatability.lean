import Std

/-!
# Exact finite zero detection behind Kraus outcome repeatability

A Gaussian rational entry can be written `(a + i b) / d` with signed integer
numerators and a strictly positive common denominator. Its norm vanishes iff
`a² + b²` vanishes. A finite sum of these nonnegative norm terms vanishes iff
every entry of every cross-outcome product is zero.

This standalone core formalization proves the finite zero-separation step used
by the Rust arbitrary-dimensional criterion. It does not formalize matrix
multiplication, density-operator trace positivity, or the entire Kraus theorem;
those algebraic steps are stated in the derivation note and executed by the
existing exact matrix/channel owners. No physical measurement rule is derived.
-/

namespace WitnessedDifference.InstrumentRepeatability

structure GaussianFraction where
  realNumerator : Int
  imaginaryNumerator : Int
  denominator : Nat
  denominator_positive : 0 < denominator

def IsZero (z : GaussianFraction) : Prop :=
  z.realNumerator = 0 ∧ z.imaginaryNumerator = 0

def normNumerator (z : GaussianFraction) : Nat :=
  z.realNumerator.natAbs * z.realNumerator.natAbs +
    z.imaginaryNumerator.natAbs * z.imaginaryNumerator.natAbs

theorem normNumerator_eq_zero_iff (z : GaussianFraction) :
    normNumerator z = 0 ↔ IsZero z := by
  simp [normNumerator, IsZero, Nat.mul_eq_zero,
    Int.natAbs_eq_zero]

theorem finite_nonnegative_sum_zero_iff
    {α : Type} (terms : List α) (f : α → Nat) :
    (terms.map f).sum = 0 ↔ ∀ x ∈ terms, f x = 0 := by
  induction terms with
  | nil => simp
  | cons head tail ih =>
    simp only [List.map_cons, List.sum_cons, Nat.add_eq_zero_iff,
      List.forall_mem_cons, ih]

def matrixNumerator (entries : List GaussianFraction) : Nat :=
  (entries.map normNumerator).sum

theorem matrixNumerator_eq_zero_iff (entries : List GaussianFraction) :
    matrixNumerator entries = 0 ↔ ∀ entry ∈ entries, IsZero entry := by
  simp [matrixNumerator, finite_nonnegative_sum_zero_iff,
    normNumerator_eq_zero_iff]

structure CrossOutcomeProduct where
  firstOutcome : Nat
  secondOutcome : Nat
  distinct_outcomes : firstOutcome ≠ secondOutcome
  firstKraus : Nat
  secondKraus : Nat
  entries : List GaussianFraction

def switchingNumerator (products : List CrossOutcomeProduct) : Nat :=
  (products.map fun product => matrixNumerator product.entries).sum

/-- Finite exhaustive zero detection, rather than checking selected states. -/
theorem all_cross_products_zero_iff
    (products : List CrossOutcomeProduct) :
    switchingNumerator products = 0 ↔
      ∀ product ∈ products, ∀ entry ∈ product.entries, IsZero entry := by
  simp [switchingNumerator, finite_nonnegative_sum_zero_iff,
    matrixNumerator_eq_zero_iff]

theorem positive_switching_witness_iff
    (products : List CrossOutcomeProduct) :
    0 < switchingNumerator products ↔
      ¬ (∀ product ∈ products, ∀ entry ∈ product.entries, IsZero entry) := by
  rw [← all_cross_products_zero_iff]
  omega

/-- Missing cross-products are not silently supplied: a separate completeness
obligation must relate this finite encoding to the full declared Kraus family. -/
def ExhaustiveEncoding
    (required : Nat → Nat → Nat → Nat → Prop)
    (products : List CrossOutcomeProduct) : Prop :=
  ∀ first second a b, required first second a b →
    ∃ product ∈ products,
      product.firstOutcome = first ∧ product.secondOutcome = second ∧
      product.firstKraus = a ∧ product.secondKraus = b

theorem exhaustive_zero_criterion_covers_required_products
    (required : Nat → Nat → Nat → Nat → Prop)
    (products : List CrossOutcomeProduct)
    (hexhaustive : ExhaustiveEncoding required products)
    (hzero : switchingNumerator products = 0) :
    ∀ first second a b, required first second a b →
      ∃ product ∈ products,
        product.firstOutcome = first ∧ product.secondOutcome = second ∧
        product.firstKraus = a ∧ product.secondKraus = b ∧
        ∀ entry ∈ product.entries, IsZero entry := by
  intro first second a b hrequired
  obtain ⟨product, hmem, hfirst, hsecond, ha, hb⟩ :=
    hexhaustive first second a b hrequired
  exact ⟨product, hmem, hfirst, hsecond, ha, hb,
    (all_cross_products_zero_iff products).mp hzero product hmem⟩

#print axioms normNumerator_eq_zero_iff
#print axioms finite_nonnegative_sum_zero_iff
#print axioms matrixNumerator_eq_zero_iff
#print axioms all_cross_products_zero_iff
#print axioms positive_switching_witness_iff
#print axioms exhaustive_zero_criterion_covers_required_products

end WitnessedDifference.InstrumentRepeatability
