import Mathlib.Data.Real.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Fintype.Basic

namespace QM.GOMC06

variable {E : Type} [Fintype E] [DecidableEq E]

-- A generic obstruction ledger is just a nonnegative mass assignment
structure ObstructionLedger (E : Type) [Fintype E] where
  mass : E → ℚ
  mass_nonneg : ∀ e, 0 ≤ mass e
  total_mass_pos : 0 < ∑ e, mass e

-- The diagonal density representation
def diagonalDensity (L : ObstructionLedger E) : Matrix E E ℚ :=
  fun i j => if i = j then (L.mass i) / (∑ e, L.mass e) else 0

-- Theorem: Every valid obstruction ledger universally admits a trace-one diagnostic representation
theorem universality_trace_one (L : ObstructionLedger E) :
    Matrix.trace (diagonalDensity L) = 1 := by
  dsimp [diagonalDensity, Matrix.trace, Matrix.diag]
  have h_sum : (∑ i : E, ite (i = i) (L.mass i / ∑ e, L.mass e) 0) = ∑ i : E, (L.mass i / ∑ e, L.mass e) := by
    apply Finset.sum_congr rfl
    intro x _
    simp only [if_true]
  rw [h_sum]
  have h_div : ∑ i : E, (L.mass i / ∑ e, L.mass e) = (∑ i : E, L.mass i) / ∑ e, L.mass e := by
    calc ∑ i : E, (L.mass i / ∑ e, L.mass e)
      _ = ∑ i : E, (L.mass i * (∑ e, L.mass e)⁻¹) := by simp_rw [div_eq_mul_inv]
      _ = (∑ i : E, L.mass i) * (∑ e, L.mass e)⁻¹ := by rw [← Finset.sum_mul]
      _ = (∑ i : E, L.mass i) / ∑ e, L.mass e := by rw [← div_eq_mul_inv]
  rw [h_div]
  have h_pos : ∑ e, L.mass e ≠ 0 := ne_of_gt L.total_mass_pos
  exact div_self h_pos

-- Theorem: The representation is PSD in the diagonal sense (all diagonal entries nonnegative)
theorem universality_psd_diag (L : ObstructionLedger E) (e : E) :
    0 ≤ diagonalDensity L e e := by
  dsimp [diagonalDensity]
  simp only [if_true]
  have h1 : 0 ≤ L.mass e := L.mass_nonneg e
  have h2 : 0 < ∑ x, L.mass x := L.total_mass_pos
  exact div_nonneg h1 (le_of_lt h2)

end QM.GOMC06
