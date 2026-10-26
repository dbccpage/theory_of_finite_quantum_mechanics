import WitnessedDifference.LocalObservationCompletion

/-! Exact finite pairing, quotient-adapter and strict-margin theorems.
    The analytic CAR product estimate and Lehmann positivity are written proofs;
    this module verifies their finite certificate consequences, not Python. -/
namespace WitnessedDifference.TrotterObservableFiltering

open WitnessedDifference.LocalObservationCompletion

def pairSum : List (Rat × Rat) → Rat
  | [] => 0
  | (a,b)::xs => a-b+pairSum xs

theorem paired_bound (xs : List (Rat × Rat)) (h : Rat)
    (bounds : ∀ p, p ∈ xs → (p.1-p.2).abs ≤ h) :
    (pairSum xs).abs ≤ (xs.length : Rat)*h := by
  induction xs with
  | nil => simp [pairSum]
  | cons p xs ih =>
    have hp := bounds p (by simp)
    have hs := ih (fun q hq => bounds q (by simp [hq]))
    have ht := abs_triangle (p.1-p.2) (pairSum xs)
    have length : ((p::xs).length : Rat) = (xs.length : Rat)+1 := by simp
    simp only [pairSum]
    rw [length]
    grind

theorem pair_normalization (pairs total average d : Rat)
    (hn : 0 < total) (twice : total = 2*pairs)
    (normalization : total*average = pairs*d/total) : average = d/(2*total) := by
  have ht : total ≠ 0 := Rat.ne_of_gt hn
  have hi := Rat.div_mul_cancel (a := pairs*d) ht
  have hj := Rat.div_mul_cancel (a := d) (Rat.ne_of_gt (show 0 < 2*total by grind))
  grind

theorem square_bound (a b : Rat) (hb : 0 ≤ b) (ha : a.abs ≤ b) : a*a ≤ b*b := by
  have bounds := (abs_le_iff a b).mp ha
  by_cases h : 0 ≤ a
  · have h1 := Rat.mul_le_mul_of_nonneg_right bounds.2 h
    have h2 := Rat.mul_le_mul_of_nonneg_left bounds.2 hb
    exact Rat.le_trans h1 h2
  · have hneg : 0 ≤ -a := by grind
    have hle : -a ≤ b := by grind
    have h1 := Rat.mul_le_mul_of_nonneg_right hle hneg
    have h2 := Rat.mul_le_mul_of_nonneg_left hle hb
    have he : (-a)*(-a) = a*a := by grind
    rw [he] at h1
    exact Rat.le_trans h1 h2

theorem energy_bound (lambda average bound : Rat) (hl : 0 ≤ lambda)
    (hb : 0 ≤ bound) (ha : average.abs ≤ bound) :
    lambda*(average*average) ≤ lambda*(bound*bound) :=
  Rat.mul_le_mul_of_nonneg_left (square_bound average bound hb ha) hl

theorem margin_positivity (approx limit err : Rat)
    (error : (approx-limit).abs ≤ err) (margin : err < limit) : 0 < approx := by
  have h := (abs_le_iff (approx-limit) err).mp error
  grind

theorem uniform_envelope_positive (approx limit numerator time : Rat)
    (ht : 0 < time) (error : (approx-limit).abs ≤ numerator/time)
    (strictThreshold : numerator < limit*time) : 0 < approx :=
  margin_positivity approx limit (numerator/time) error ((Rat.div_lt_iff ht).mpr strictThreshold)

theorem threshold_must_be_strict : (2 : Rat)-4/2 = 0 := by grind

theorem m1_value_cross_multiplication :
    (1 : Int)^4 * 706440 = 4*21*841*10 := by decide

theorem staggered_difference (a : Rat) : (-a/2)-(a/2) = -a := by grind

theorem subdivision_square (x k : Rat) (hk : k ≠ 0) : k*k*(x/k)*(x/k) = x*x := by
  have cancel := Rat.div_mul_cancel (a := x) hk
  grind

theorem quotient_adapter_iff {C R} (equiv : C → C → Prop) (adapter : C → R)
    (q : C → R) (hq : ∀ x y, q x = q y ↔ equiv x y) :
    (∀ x y, equiv x y → adapter x = adapter y) ↔
      ∀ x y, q x = q y → adapter x = adapter y := by
  constructor
  · exact fun h x y he => h x y ((hq x y).mp he)
  · exact fun h x y he => h x y ((hq x y).mpr he)

theorem kills_repairs_iff_translation_invariance {C R}
    (addC : C → C → C) (zeroC : C) (addR : R → R → R) (zeroR : R)
    (adapter : C → R) (repair : C → Prop)
    (unitC : ∀ b, addC zeroC b = b) (unitR : ∀ r, addR r zeroR = r)
    (linear : ∀ x y, adapter (addC x y) = addR (adapter x) (adapter y))
    (zero : adapter zeroC = zeroR) :
    (∀ b, repair b → adapter b = zeroR) ↔
      ∀ x b, repair b → adapter (addC x b) = adapter x := by
  constructor
  · intro h x b hb
    rw [linear, h b hb, unitR]
  · intro h b hb
    have he := h zeroC b hb
    rw [unitC, zero] at he
    exact he

theorem projector_adapter_kills_fixed_repairs (projector : Rat → Rat)
    (postprocess : Rat → Rat) (zero : postprocess 0 = 0)
    (b : Rat) (fixed : projector b = b) : postprocess (b-projector b) = 0 := by
  rw [fixed, Rat.sub_self, zero]

theorem exact_cochain_period (a b c d : Rat) : (b-a)+(c-b)+(d-c)+(a-d) = 0 := by grind

theorem constant_is_not_exact : (1 : Rat)+1+1+1 ≠ 0 := by grind

end WitnessedDifference.TrotterObservableFiltering

#print axioms WitnessedDifference.TrotterObservableFiltering.paired_bound
#print axioms WitnessedDifference.TrotterObservableFiltering.pair_normalization
#print axioms WitnessedDifference.TrotterObservableFiltering.square_bound
#print axioms WitnessedDifference.TrotterObservableFiltering.energy_bound
#print axioms WitnessedDifference.TrotterObservableFiltering.margin_positivity
#print axioms WitnessedDifference.TrotterObservableFiltering.uniform_envelope_positive
#print axioms WitnessedDifference.TrotterObservableFiltering.threshold_must_be_strict
#print axioms WitnessedDifference.TrotterObservableFiltering.m1_value_cross_multiplication
#print axioms WitnessedDifference.TrotterObservableFiltering.staggered_difference
#print axioms WitnessedDifference.TrotterObservableFiltering.subdivision_square
#print axioms WitnessedDifference.TrotterObservableFiltering.quotient_adapter_iff
#print axioms WitnessedDifference.TrotterObservableFiltering.kills_repairs_iff_translation_invariance
#print axioms WitnessedDifference.TrotterObservableFiltering.projector_adapter_kills_fixed_repairs
#print axioms WitnessedDifference.TrotterObservableFiltering.exact_cochain_period
#print axioms WitnessedDifference.TrotterObservableFiltering.constant_is_not_exact
