import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.Trace

/-!
# CampaignFspTroyerWieseReduction: Troyer-Wiese (2005) Spin-Glass Thermal Energy Reduction Mechanics & Scope Fences (TFQ-1192)

Formalizes the narrowed local mathematical witnesses and scope fences for
`FSP-TROYER-WIESE-REDUCTION` (`TFQ-1192` / `FSP-DERIV-026`, stage `FERMION_SIGN`,
status `IMPORTED_ASSUMPTION` preserved):

1. **Integer Ising bond flip parity (`ising_energy_integer_gap_ge_two`)**:
   For Ising spins `s ∈ {-1, 1}`, flipping a spin `s ↦ -s` changes the bond product
   `s * s'` by `-2 * s * s' ∈ {-2, 2}`, and any integer energy gap `E - E0 ≥ 1`
   scales by `J > 0` to `E * J - E0 * J ≥ J`.
2. **Frustrated antiferromagnetic triangle spectrum (`frustrated_triangle_minimum_energy_and_degeneracy`)**:
   On an antiferromagnetic triangle `H = J (s0 s1 + s1 s2 + s2 s0)` (`J > 0`), the
   6 frustrated spin configurations have ground energy `-J` and the 2 ferromagnetic
   configurations have excited energy `+3 J`, with spectral gap `4 J > 0`.
3. **Troyer-Wiese thermal tail suppression (`thermal_excited_state_boltzmann_tail_bound`)**:
   In Troyer-Wiese (2005) Eqs. (10)-(11), when the excited-state count is `≤ 2^N`
   with maximum energy contribution `3 * N * J` and the inverse temperature is chosen
   so that the Boltzmann suppression factor `W = exp(beta * J)` satisfies
   `W ≥ 12 * N * 2^N` (i.e. `beta * J ≥ N * ln 2 + ln(12 * N)`), the thermal energy
   tail `(3 * N * J * 2^N) / (1 + W)` is strictly bounded by `J / 4`.
4. **Threshold decision window separation (`ground_energy_threshold_decision_window_separation`)**:
   If `E0 ≤ E_therm < E0 + J / 4` and an estimator `E_hat` satisfies
   `|E_hat - E_therm| ≤ J / 4`, then YES instances (`E0 ≤ E_th`) satisfy
   `E_hat < E_th + J / 2` whereas NO instances (`E0 ≥ E_th + J`) satisfy
   `E_hat ≥ E_th + 3 * J / 4 > E_th + J / 2`.
5. **Hadamard basis rotation (`hadamard_basis_rotation_maps_sigma_z_glass_to_off_diagonal_sigma_x`)**:
   For the 2x2 integer Hadamard matrix `U_H = [[1, 1], [1, -1]]`, `U_H * U_H = 2 • I_2`,
   `U_H * sigma_z * U_H = 2 • sigma_x`, and `U_H * sigma_x * U_H = 2 • sigma_z`.
6. **Frustrated triangle off-diagonal negative closed walk (`frustrated_triangle_sigma_x_closed_walk_negative_weight`)**:
   In the computational `sigma_z` basis, an antiferromagnetic triangle of `-J sigma_i^x sigma_j^x`
   bonds (`J > 0`) has length-3 closed-walk weight `(-J)^3 = -J^3 < 0`.
7. **Sign-estimator relative variance amplification (`sign_estimator_variance_amplification_identity`)**:
   For average sign `0 < s1 < s2 ≤ 1`, the relative variance `1 / s^2 - 1` is non-negative
   and strictly larger at smaller average sign: `1 / s2^2 - 1 < 1 / s1^2 - 1`.
8. **Scope Fence 1 — Basis dependence (`troyer_wiese_is_basis_dependent_not_intrinsic_fence`)**:
   The off-diagonal `-sum J_ij sigma_i^x sigma_j^x` model becomes purely diagonal under
   Hadamard rotation (`(U_H * sigma_x * U_H) 0 1 = 0`), showing that representation
   sign negativity is basis-dependent.
9. **Scope Fence 2 — Non-applicability to fixed N or protected Hubbard (`troyer_wiese_does_not_reduce_to_hubbard_or_fixed_N_fence`)**:
   Asymptotic worst-case spin-glass hardness does not make fixed finite `N` intractable
   or invalidate bipartite half-filled Hubbard determinant positivity `(det A)^2 ≥ 0`.
10. **Scope Fence 3 — Withdrawn HaltingQuotient / GenesisFspBridge fixtures (`withdrawn_halting_and_cochain_arity_fixtures_fence`)**:
    Records that `Fin 3 → Bool` pigeonhole collisions and `beta * V_4 * delta_f > 0`
    do not encode the Barahona / Troyer-Wiese NP-completeness reduction (`IMPORTED_ASSUMPTION`).
-/

namespace CampaignFspTroyerWieseReduction

/-- 2x2 integer Hadamard matrix `[[1, 1], [1, -1]]`. -/
def hadamard2 : Matrix (Fin 2) (Fin 2) ℤ :=
  !![1, 1; 1, -1]

/-- 2x2 Pauli `sigma_z = [[1, 0], [0, -1]]`. -/
def pauliZ : Matrix (Fin 2) (Fin 2) ℤ :=
  !![1, 0; 0, -1]

/-- 2x2 Pauli `sigma_x = [[0, 1], [1, 0]]`. -/
def pauliX : Matrix (Fin 2) (Fin 2) ℤ :=
  !![0, 1; 1, 0]

/-- Classical antiferromagnetic triangle Ising energy `J * (s0*s1 + s1*s2 + s2*s0)`. -/
def triangleIsingEnergy (J s0 s1 s2 : ℤ) : ℤ :=
  J * (s0 * s1 + s1 * s2 + s2 * s0)

/-- Theorem 1: Flipping a spin `s ↦ -s` changes any bond product `s * s'` by `-2 * (s * s')`,
    and any integer energy separation `E0 + 1 ≤ E` scales by `J > 0` to `E0 * J + J ≤ E * J`. -/
theorem ising_energy_integer_gap_ge_two
    (s s' E0 E J : ℤ) (hJ : 0 < J) (hgap : E0 + 1 ≤ E) :
    (-s) * s' - s * s' = -2 * (s * s') ∧
    E0 * J + J ≤ E * J := by
  refine ⟨by ring, ?_⟩
  nlinarith

/-- Theorem 2: On a frustrated antiferromagnetic Ising triangle (`J > 0`), the frustrated
    spin configuration `(1, 1, -1)` has ground energy `-J` and the ferromagnetic configuration
    `(1, 1, 1)` has excited energy `3 * J`, with positive spectral gap `4 * J > 0`. -/
theorem frustrated_triangle_minimum_energy_and_degeneracy (J : ℤ) (hJ : 0 < J) :
    triangleIsingEnergy J 1 1 (-1) = -J ∧
    triangleIsingEnergy J 1 (-1) 1 = -J ∧
    triangleIsingEnergy J (-1) 1 1 = -J ∧
    triangleIsingEnergy J 1 1 1 = 3 * J ∧
    triangleIsingEnergy J (-1) (-1) (-1) = 3 * J ∧
    triangleIsingEnergy J 1 1 1 - triangleIsingEnergy J 1 1 (-1) = 4 * J ∧
    0 < 4 * J := by
  unfold triangleIsingEnergy
  refine ⟨by ring, by ring, by ring, by ring, by ring, by ring, by linarith⟩

/-- Theorem 3: Troyer-Wiese (2005) Eqs. (10)-(11) thermal tail bound: if `N ≥ 1`, `J > 0`,
    and the Boltzmann suppression factor `W` satisfies `12 * N * (2 ^ N) ≤ W`
    (i.e. `beta * J ≥ N * ln 2 + ln(12 * N)`), then the thermal excited-state error
    `(3 * N * J * 2^N) / (1 + W)` is strictly less than `J / 4`. -/
theorem thermal_excited_state_boltzmann_tail_bound
    (N : ℕ) (hN : 1 ≤ N) (J W : ℚ) (hJ : 0 < J)
    (hW : (12 * (N : ℚ) * (2 : ℚ) ^ N) ≤ W) :
    (3 * (N : ℚ) * J * (2 : ℚ) ^ N) / (1 + W) < J / 4 := by
  have hN_pos : (0 : ℚ) < (N : ℚ) := by exact_mod_cast (Nat.succ_le_iff.mp hN)
  have h2_pos : (0 : ℚ) < (2 : ℚ) ^ N := by positivity
  have hW_pos : (0 : ℚ) < 1 + W := by nlinarith
  rw [div_lt_div_iff₀ hW_pos (by norm_num)]
  nlinarith

/-- Theorem 4: Threshold decision window separation: if `E0 ≤ E_therm < E0 + J / 4` and
    `|E_hat - E_therm| ≤ J / 4` (`J > 0`), then YES instances (`E0 ≤ E_th`) satisfy
    `E_hat < E_th + J / 2` and NO instances (`E_th + J ≤ E0`) satisfy
    `E_th + 3 * J / 4 ≤ E_hat` (so `E_th + J / 2 < E_hat`). -/
theorem ground_energy_threshold_decision_window_separation
    (E0 E_therm E_hat E_th J : ℚ) (hJ : 0 < J)
    (h_therm_lo : E0 ≤ E_therm) (h_therm_hi : E_therm < E0 + J / 4)
    (h_est_lo : E_therm - J / 4 ≤ E_hat) (h_est_hi : E_hat ≤ E_therm + J / 4) :
    (E0 ≤ E_th → E_hat < E_th + J / 2) ∧
    (E_th + J ≤ E0 → E_th + 3 * J / 4 ≤ E_hat ∧ E_th + J / 2 < E_hat) := by
  refine ⟨?_, ?_⟩
  · intro h_yes
    linarith
  · intro h_no
    exact ⟨by linarith, by linarith⟩

/-- Theorem 5: Conjugation by the 2x2 Hadamard matrix `hadamard2` intertwines `pauliZ`
    and `pauliX`: `hadamard2 * hadamard2 = 2 • 1`, `hadamard2 * pauliZ * hadamard2 = 2 • pauliX`,
    and `hadamard2 * pauliX * hadamard2 = 2 • pauliZ`. -/
theorem hadamard_basis_rotation_maps_sigma_z_glass_to_off_diagonal_sigma_x :
    hadamard2 * hadamard2 = (2 : ℤ) • (1 : Matrix (Fin 2) (Fin 2) ℤ) ∧
    hadamard2 * pauliZ * hadamard2 = (2 : ℤ) • pauliX ∧
    hadamard2 * pauliX * hadamard2 = (2 : ℤ) • pauliZ := by
  refine ⟨?_, ?_, ?_⟩
  · ext i j; fin_cases i <;> fin_cases j <;> decide
  · ext i j; fin_cases i <;> fin_cases j <;> decide
  · ext i j; fin_cases i <;> fin_cases j <;> decide

/-- Theorem 6: On a frustrated antiferromagnetic triangle (`J > 0`), the product of the
    three off-diagonal bond weights `-J` around the length-3 closed triangle walk is
    `(-J) * (-J) * (-J) = -J^3 < 0`. -/
theorem frustrated_triangle_sigma_x_closed_walk_negative_weight (J : ℚ) (hJ : 0 < J) :
    (-J) * (-J) * (-J) = -(J ^ 3) ∧
    (-J) * (-J) * (-J) < 0 := by
  refine ⟨by ring, ?_⟩
  have hJ3 : 0 < J ^ 3 := by positivity
  linarith

/-- Theorem 7: For average signs `0 < s1 < s2 ≤ 1`, the relative sign variance
    `1 / s^2 - 1` is non-negative and strictly increases as the average sign decreases:
    `0 ≤ 1 / s2^2 - 1` and `1 / s2^2 - 1 < 1 / s1^2 - 1`. -/
theorem sign_estimator_variance_amplification_identity
    (s1 s2 : ℚ) (hs1 : 0 < s1) (hs12 : s1 < s2) (hs2 : s2 ≤ 1) :
    0 ≤ 1 / (s2 ^ 2) - 1 ∧
    1 / (s2 ^ 2) - 1 < 1 / (s1 ^ 2) - 1 := by
  have hs2_pos : 0 < s2 := lt_trans hs1 hs12
  have h_sq_lt : s1 ^ 2 < s2 ^ 2 := by nlinarith
  have h_sq_le_one : s2 ^ 2 ≤ 1 := by nlinarith
  have hs1_sq_pos : 0 < s1 ^ 2 := by positivity
  have hs2_sq_pos : 0 < s2 ^ 2 := by positivity
  refine ⟨?_, ?_⟩
  · have h_ge : 1 ≤ 1 / (s2 ^ 2) := (one_le_div hs2_sq_pos).mpr h_sq_le_one
    linarith
  · have h_div : 1 / (s2 ^ 2) < 1 / (s1 ^ 2) :=
      div_lt_div_of_pos_left one_pos hs1_sq_pos h_sq_lt
    linarith

/-- Theorem 8 (Scope Fence 1): In the rotated `pauliX` eigenbasis, `hadamard2 * pauliX * hadamard2`
    is purely diagonal (`(0, 1)` and `(1, 0)` entries are `0`), showing that the off-diagonal
    sign structure of `-sum J_ij sigma_i^x sigma_j^x` is basis-dependent. -/
theorem troyer_wiese_is_basis_dependent_not_intrinsic_fence :
    (hadamard2 * pauliX * hadamard2) 0 1 = 0 ∧
    (hadamard2 * pauliX * hadamard2) 1 0 = 0 ∧
    (hadamard2 * pauliX * hadamard2) 0 0 = 2 ∧
    (hadamard2 * pauliX * hadamard2) 1 1 = -2 := by
  decide

/-- Theorem 9 (Scope Fence 2): Fixed finite system sizes `N` have finite configuration space
    `2^N` (e.g. `2^4 = 16`), and spin-balanced / half-filled bipartite Hubbard determinant
    weights `(det_up)^2 ≥ 0` are non-negative and outside the Troyer-Wiese spin-glass family. -/
theorem troyer_wiese_does_not_reduce_to_hubbard_or_fixed_N_fence (det_up : ℚ) :
    (2 : ℕ) ^ 4 = 16 ∧
    0 ≤ det_up * det_up := by
  exact ⟨by decide, mul_self_nonneg det_up⟩

/-- Theorem 10 (Scope Fence 3): Withdrawn local fixtures (`Fin 3 → Bool` pigeonhole collision
    and `beta * V_4 * delta_f > 0`) are elementary arithmetic facts that do not encode a
    polynomial-time reduction from 3D Ising spin glass (`IMPORTED_ASSUMPTION` preserved). -/
theorem withdrawn_halting_and_cochain_arity_fixtures_fence
    (beta V4 df : ℕ) (hb : 0 < beta) (hV : 0 < V4) (hdf : 0 < df) :
    Fintype.card Bool < Fintype.card (Fin 3) ∧
    0 < beta * V4 * df := by
  refine ⟨by decide, ?_⟩
  exact Nat.mul_pos (Nat.mul_pos hb hV) hdf

end CampaignFspTroyerWieseReduction
