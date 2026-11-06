



import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring

namespace GR002.LinearEnergy

theorem norm_scal_homogeneity (c : ℝ) (v_norm : ℝ) (h_nonneg : v_norm ≥ 0) :
    |c * v_norm| = |c| * v_norm := by
  rw [abs_mul, abs_of_nonneg h_nonneg]

theorem linear_energy_scaling (c : ℝ) (Phi1 : ℝ) (_hP : Phi1 ≥ 0) :
    |c| * Phi1 = if c ≥ 0 then c * Phi1 else -c * Phi1 := by
  split_ifs with h
  · rw [abs_of_nonneg h]
  · rw [abs_of_neg (not_le.mp h)]

def l1_3 (v : ℝ × ℝ × ℝ) : ℝ :=
  |v.1| + |v.2.1| + |v.2.2|

def smul_3 (t : ℝ) (v : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  (t * v.1, t * v.2.1, t * v.2.2)

def sub_3 (u v : ℝ × ℝ × ℝ) : ℝ × ℝ × ℝ :=
  (u.1 - v.1, u.2.1 - v.2.1, u.2.2 - v.2.2)

theorem l1_3_homogeneity (t : ℝ) (v : ℝ × ℝ × ℝ) :
    l1_3 (smul_3 t v) = |t| * l1_3 v := by
  dsimp [l1_3, smul_3]
  rw [abs_mul, abs_mul, abs_mul]
  ring

theorem residual_candidate_scaling (t : ℝ) (omega D_alpha : ℝ × ℝ × ℝ) :
    sub_3 (smul_3 t omega) (smul_3 t D_alpha) = smul_3 t (sub_3 omega D_alpha) := by
  dsimp [sub_3, smul_3]
  apply Prod.ext
  · ring
  · apply Prod.ext <;> ring

theorem quotient_candidate_homogeneity (t : ℝ) (omega D_alpha : ℝ × ℝ × ℝ) :
    l1_3 (sub_3 (smul_3 t omega) (smul_3 t D_alpha)) = |t| * l1_3 (sub_3 omega D_alpha) := by
  rw [residual_candidate_scaling, l1_3_homogeneity]

theorem fixed_carrier_quotient_homogeneity (t : ℝ) (Phi_omega : ℝ) (h_nonneg : Phi_omega ≥ 0) :
    |t| * Phi_omega = if t ≥ 0 then t * Phi_omega else -t * Phi_omega := by
  exact linear_energy_scaling t Phi_omega h_nonneg

theorem linear_energy_has_origin_minimum (t : ℝ) (Phi_omega : ℝ) (h_pos : Phi_omega > 0) :
    |t| * Phi_omega ≥ 0 ∧ (|t| * Phi_omega = 0 ↔ t = 0) := by
  constructor
  · exact mul_nonneg (abs_nonneg t) (le_of_lt h_pos)
  · rw [mul_eq_zero, or_iff_left (ne_of_gt h_pos), abs_eq_zero]

#print axioms norm_scal_homogeneity
#print axioms linear_energy_scaling
#print axioms l1_3_homogeneity
#print axioms residual_candidate_scaling
#print axioms quotient_candidate_homogeneity
#print axioms fixed_carrier_quotient_homogeneity
#print axioms linear_energy_has_origin_minimum

end GR002.LinearEnergy
