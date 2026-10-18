import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic

/-!
# BornQuadraticCountermodel — the OB-BORN ceiling (why the *square*?)

Mechanizes the countermodel direction of **ENC-0317 / pub-010 Theorem 6**: the quadratic Born
form `|c|²` is **not forced** by normalization. It is just one member of the power-normalization
family `Pₚ(c)ᵢ = (cᵢ)^p / Σⱼ (cⱼ)^p`; *every* `p` gives a valid (sums-to-one) probability rule, so
"valid normalization" alone does not single out `p = 2`.

What pins `p = 2` is the **imported** Gleason structure (a non-contextual frame function on a
complex Hilbert space of dimension ≥ 3) — see ENC-0317's conditional list. The **non-contextuality**
half of that import is exactly the contextuality QM_047 mechanizes as a PrimitiveDifference cochain
obstruction (Mermin–Peres). So OB-BORN is honestly: *the quadratic is not forced (mechanized here);
its selection is imported via Gleason, whose non-contextuality hypothesis QM_047 makes obstruction-
explicit.* Complements ENC-1070 (Born not selected by the pairing skeleton) with the orthogonal
form/exponent countermodel. Mathlib-light over `ℚ`; no Born rule derived, no authority minted.
-/

namespace QM
namespace BornQuadraticCountermodel

open Finset

variable {n : ℕ}

/-- Power-normalization probability rule `Pₚ(c)ᵢ = (cᵢ)^p / Σⱼ (cⱼ)^p`. `p = 2` is Born. -/
def powProb (p : ℕ) (c : Fin n → ℚ) (i : Fin n) : ℚ := (c i) ^ p / (∑ j, (c j) ^ p)

/-- **Generic validity.** For *any* `p`, when the denominator is nonzero the power rule sums to one
— a valid probability normalization. So normalization-validity does not single out `p = 2`. -/
theorem powProb_sums_to_one (p : ℕ) (c : Fin n → ℚ) (hS : (∑ j, (c j) ^ p) ≠ 0) :
    (∑ i, powProb p c i) = 1 := by
  unfold powProb
  rw [← Finset.sum_div, div_self hS]

/-- The Born rule (`p = 2`) and the quartic rule (`p = 4`) over `Fin 2`. -/
def bornProb (c : Fin 2 → ℚ) : Fin 2 → ℚ := powProb 2 c
def quarticProb (c : Fin 2 → ℚ) : Fin 2 → ℚ := powProb 4 c

/-- A nonzero amplitude witness `(1, 2)`. -/
def witness : Fin 2 → ℚ := ![1, 2]

/-- Born is a valid distribution on the witness: `(1/5, 4/5)` sums to one. -/
theorem born_valid : (∑ i, bornProb witness i) = 1 := by
  norm_num [bornProb, powProb, witness, Fin.sum_univ_two]

/-- Quartic is also a valid distribution on the witness: `(1/17, 16/17)` sums to one. -/
theorem quartic_valid : (∑ i, quarticProb witness i) = 1 := by
  norm_num [quarticProb, powProb, witness, Fin.sum_univ_two]

/-- **The countermodel.** Born (`p = 2`) and quartic (`p = 4`) are *distinct* valid probability
rules — they disagree on the witness (`1/5 ≠ 1/17`). Hence normalization-validity does **not** force
the quadratic; the selection of `p = 2` is imported (Gleason; cf. ENC-0317). -/
theorem born_not_forced_by_normalization : bornProb witness ≠ quarticProb witness := by
  intro h
  have h0 := congrFun h 0
  simp [bornProb, quarticProb, powProb, witness, Fin.sum_univ_two] at h0

/-! ## Firewall — derived ⇏ authority -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end BornQuadraticCountermodel
end QM

#print axioms QM.BornQuadraticCountermodel.powProb_sums_to_one
#print axioms QM.BornQuadraticCountermodel.born_valid
#print axioms QM.BornQuadraticCountermodel.quartic_valid
#print axioms QM.BornQuadraticCountermodel.born_not_forced_by_normalization
