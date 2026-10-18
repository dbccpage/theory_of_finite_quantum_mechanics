import Mathlib

/-!
LT-M — classical stochastic maps contract the ℓ¹ distance.

Paper: `10_trace_norm_cptp_transport_audit.md` §3 (classical precursor);
`11_…` T5 support.

The division-algebra-free precursor to trace-norm contractivity: a finite
column-stochastic kernel `S` (nonnegative entries, each column summing to `1`) does
not increase the ℓ¹ norm, `‖S·x‖₁ ≤ ‖x‖₁`. This is the contractivity *shape* that the
quantum trace-distance data-processing inequality specialises; it selects no metric
and mints no authority (and, with LT-L, shows CPTP/contractivity alone does not pin
the trace norm). Over `ℚ`; Mathlib `Finset`/`abs`.
-/

namespace QM

open Finset

variable {n : Type*} [Fintype n]

/-- ℓ¹ norm of a finite vector. -/
def l1 (x : n → ℚ) : ℚ := ∑ i, |x i|

/-- A finite column-stochastic kernel: nonnegative, each column sums to one.
`S i j` is the weight transported from `j` to `i`. -/
def ColStochastic (S : n → n → ℚ) : Prop :=
  (∀ i j, 0 ≤ S i j) ∧ (∀ j, ∑ i, S i j = 1)

/-- The image of `x` under the kernel `S`. -/
def applyS (S : n → n → ℚ) (x : n → ℚ) (i : n) : ℚ := ∑ j, S i j * x j

/-- **ℓ¹ contractivity.** A column-stochastic kernel does not increase ℓ¹ distance. -/
theorem stochastic_l1_contraction (S : n → n → ℚ) (hS : ColStochastic S) (x : n → ℚ) :
    l1 (applyS S x) ≤ l1 x := by
  obtain ⟨hpos, hcol⟩ := hS
  simp only [l1, applyS]
  have step1 : (∑ i, |∑ j, S i j * x j|) ≤ ∑ i, ∑ j, S i j * |x j| := by
    apply Finset.sum_le_sum
    intro i _
    calc |∑ j, S i j * x j| ≤ ∑ j, |S i j * x j| := Finset.abs_sum_le_sum_abs _ _
      _ = ∑ j, S i j * |x j| := by
            apply Finset.sum_congr rfl
            intro j _
            rw [abs_mul, abs_of_nonneg (hpos i j)]
  have step2 : (∑ i, ∑ j, S i j * |x j|) = ∑ i, |x i| := by
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro j _
    rw [← Finset.sum_mul, hcol j, one_mul]
  exact le_of_le_of_eq step1 step2

end QM

#print axioms QM.stochastic_l1_contraction
