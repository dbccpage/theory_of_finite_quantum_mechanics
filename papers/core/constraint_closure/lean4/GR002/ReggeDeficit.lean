



import Lean.Elab.Tactic.Omega
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Push
import Mathlib.Tactic.Ring

namespace GR002.ReggeDeficit

noncomputable section

def corner_units : ℕ := 6 * 4

def edge_units (R : ℕ) : ℕ := 6 * (R - 1) * 3

def total_units (R : ℕ) : ℕ := corner_units + edge_units R

def total_deficit (R : ℕ) : ℝ := (total_units R : ℝ) * (Real.pi / 3)

theorem total_units_formula (R : ℕ) (hR : R ≥ 1) :
    total_units R = 6 + 18 * R := by
  dsimp [total_units, corner_units, edge_units]
  cases R with
  | zero => omega
  | succ n => omega

theorem total_units_strictly_increasing (R : ℕ) (hR : R ≥ 1) :
    total_units (R + 1) > total_units R := by
  rw [total_units_formula R hR,
    total_units_formula (R + 1) (by omega)]
  omega

theorem total_deficit_formula (R : ℕ) (hR : R ≥ 1) :
    total_deficit R = 2 * Real.pi + 6 * Real.pi * (R : ℝ) := by
  rw [total_deficit, total_units_formula R hR]
  push_cast
  ring

#print axioms total_units_formula
#print axioms total_units_strictly_increasing
#print axioms total_deficit_formula

end
end GR002.ReggeDeficit
