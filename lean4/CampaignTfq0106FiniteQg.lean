import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp

/-!
# Campaign: TFQ-0106 — Exact Rational Replay of `CosmologicalCoupling`, External Cell-Volume Calibration Underdetermination, and Scalar-vs-Tensor Einstein Fence

AuthorityEffect: None.

This module narrows `TFQ-0106` (stage `FINITE_QG`, status `OPEN`, backed by
`code/rust/src/general_relativity/cosmological_constant.rs`) into three exact rational components
and non-equivalence fences:

1. **Exact Rational Replay of `CosmologicalCoupling` (`cosmological_constant.rs`)**:
   - Replays `evaluate_action(K, V) = K / (2 * kappa) - lambda * V` and
     `effective_scalar_curvature = 2 * lambda * kappa` over `ℚ`, verifying the exact Rust unit test
     (`dimension = 4`, `lambda = 1/10`, `kappa = 1/2`, `K = 10`, `V = 20` -> `effective = 1/10`,
     `action = 8`, `rust_cosmological_action_unit_test_replay`).
   - Proves that `evaluateCosmologicalAction lambda kappa K V = 0` holds if and only if
     `K = effectiveScalarCurvature lambda kappa * V` (`cosmological_action_zero_iff_curvature_balance`),
     and establishes homogeneous scaling in `(K, V)` and reciprocal invariance of
     `effectiveScalarCurvature` under `(lambda / s, s * kappa)` (`cosmological_action_scaling_and_invariance`).

2. **External Cell-Volume Calibration Underdetermination Fence (`V_cell` Tautology)**:
   - For the Track B hinge-mean residual `lambdaResidual H Vcell = H / Vcell`, proves that rescaling
     the lattice length unit by `s ≠ 0` in 4D (`Vcell ↦ s^4 * Vcell`) scales `lambdaResidual` by
     `1 / s^4` (`cell_volume_4d_length_rescaling`).
   - Proves that for any nonzero finite hinge mean `H ≠ 0` and any nonzero target value
     `targetLambda ≠ 0`, choosing the external cell-volume parameter `Vcell = H / targetLambda`
     yields `lambdaResidual H (H / targetLambda) = targetLambda`
     (`any_target_lambda_achievable_by_cell_volume_calibration`), showing that matching a continuum
     cosmological-constant magnitude by calibrating `Vcell` is a 1-parameter rescaling identity
     rather than a derivation of physical `Λ`.
   - Proves joint `(gamma, Vcell)` scale degeneracy of the Immirzi-weighted residual
     `immirziLambdaResidual (c * gamma) (c * Vcell) H0 = immirziLambdaResidual gamma Vcell H0`
     for all `c ≠ 0` (`immirzi_and_cell_volume_scale_degeneracy`).

3. **Scalar Hinge Mean vs. Tensorial 4D Einstein Equation Fence (`1` Scalar vs. `10` Components)**:
   - In `d = 4` dimensions, a symmetric tensor equation `G_{μν} + Λ g_{μν} = 0` has
     `d * (d + 1) / 2 = 10` independent components (`9` trace-free components plus `1` trace),
     whereas `evaluate_action` and `lambdaResidual` constrain only `1` scalar summary
     (`four_dim_symmetric_tensor_component_counts`).
   - Exhibits an explicit 4-component anisotropic curvature family
     `(Λ + δ, Λ - δ, Λ, Λ)` (`δ ≠ 0`) whose scalar mean residual vanishes identically while its
     individual components violate `R_μ = Λ` (`anisotropic_curvature_vanishing_scalar_mean_fence`).
-/

namespace CampaignTfq0106FiniteQg

-- ============================================================================
-- 1. Exact Rational Replay of `CosmologicalCoupling` (`cosmological_constant.rs`)
-- ============================================================================

/-- Exact rational counterpart of `CosmologicalCoupling::effective_scalar_curvature` in
`code/rust/src/general_relativity/cosmological_constant.rs`: `2 * lambda * kappa`. -/
def effectiveScalarCurvature (lambda kappa : ℚ) : ℚ :=
  2 * lambda * kappa

/-- Exact rational counterpart of `CosmologicalCoupling::evaluate_action` in
`code/rust/src/general_relativity/cosmological_constant.rs`:
`total_hinge_curvature / (2 * kappa) - lambda * total_volume`. -/
def evaluateCosmologicalAction (lambda kappa totalHingeCurvature totalVolume : ℚ) : ℚ :=
  totalHingeCurvature / (2 * kappa) - lambda * totalVolume

/-- Theorem 1: Exact replay of `test_cosmological_action` in
`code/rust/src/general_relativity/cosmological_constant.rs` (`lambda = 1/10`, `kappa = 1/2`,
`total_hinge_curvature = 10`, `total_volume = 20`). -/
theorem rust_cosmological_action_unit_test_replay :
    effectiveScalarCurvature (1 / 10) (1 / 2) = 1 / 10 ∧
    evaluateCosmologicalAction (1 / 10) (1 / 2) 10 20 = 8 := by
  dsimp [effectiveScalarCurvature, evaluateCosmologicalAction]
  norm_num

/-- Theorem 2: For any nonzero gravitational coupling `kappa ≠ 0`, the discrete cosmological action
`evaluateCosmologicalAction lambda kappa K V` vanishes if and only if the total hinge curvature `K`
equals `effectiveScalarCurvature lambda kappa * V`. -/
theorem cosmological_action_zero_iff_curvature_balance
    (lambda kappa K V : ℚ) (hkappa : kappa ≠ 0) :
    evaluateCosmologicalAction lambda kappa K V = 0 ↔
      K = effectiveScalarCurvature lambda kappa * V := by
  dsimp [evaluateCosmologicalAction, effectiveScalarCurvature]
  constructor
  · intro h
    field_simp [hkappa] at h
    linarith
  · intro h
    rw [h]
    field_simp [hkappa]
    ring

/-- Theorem 3: Homogeneous linearity of `evaluateCosmologicalAction` under joint `(K, V)` scaling
and invariance of `effectiveScalarCurvature` under reciprocal `(lambda / s, s * kappa)` rescaling. -/
theorem cosmological_action_scaling_and_invariance
    (lambda kappa K V s : ℚ) (hs : s ≠ 0) :
    evaluateCosmologicalAction lambda kappa (s * K) (s * V) =
      s * evaluateCosmologicalAction lambda kappa K V ∧
    effectiveScalarCurvature (lambda / s) (s * kappa) =
      effectiveScalarCurvature lambda kappa := by
  refine ⟨?_, ?_⟩
  · dsimp [evaluateCosmologicalAction]
    ring
  · dsimp [effectiveScalarCurvature]
    field_simp [hs]

-- ============================================================================
-- 2. External Cell-Volume Calibration Underdetermination Fence (`V_cell`)
-- ============================================================================

/-- Track B cosmological-constant residual `H / Vcell` dividing a finite hinge mean `H` by an
external cell-volume calibration parameter `Vcell`. -/
def lambdaResidual (H Vcell : ℚ) : ℚ :=
  H / Vcell

/-- Immirzi-weighted hinge residual `(gamma * H0) / Vcell` with supplied Immirzi parameter `gamma`
and cell volume `Vcell`. -/
def immirziLambdaResidual (gamma Vcell H0 : ℚ) : ℚ :=
  (gamma * H0) / Vcell

/-- Theorem 4: Under a 4D lattice spacing rescaling `a ↦ s * a` (`Vcell ↦ s^4 * Vcell` with
`s ≠ 0`), `lambdaResidual H (s^4 * Vcell)` scales by `1 / s^4` with `s^4 ≠ 0`. -/
theorem cell_volume_4d_length_rescaling (H Vcell s : ℚ) (hs : s ≠ 0) :
    lambdaResidual H (s ^ 4 * Vcell) = (1 / s ^ 4) * lambdaResidual H Vcell ∧
    s ^ 4 ≠ 0 := by
  refine ⟨?_, pow_ne_zero 4 hs⟩
  dsimp [lambdaResidual]
  ring

/-- Theorem 5: For any nonzero finite hinge mean `H ≠ 0` and any nonzero target value
`targetLambda ≠ 0`, choosing the external cell-volume calibration `Vcell = H / targetLambda`
reproduces `lambdaResidual H Vcell = targetLambda`, and distinct positive cell volumes `V1 ≠ V2`
produce distinct residuals `lambdaResidual H V1 ≠ lambdaResidual H V2`. -/
theorem any_target_lambda_achievable_by_cell_volume_calibration
    (H targetLambda : ℚ) (hH : H ≠ 0) (htarget : targetLambda ≠ 0) :
    lambdaResidual H (H / targetLambda) = targetLambda ∧
    (H / targetLambda) ≠ 0 := by
  refine ⟨?_, div_ne_zero hH htarget⟩
  dsimp [lambdaResidual]
  field_simp [hH, htarget]

/-- Theorem 6: Distinct nonzero cell-volume calibrations `V1 ≠ V2` on a nonzero finite hinge mean
`H ≠ 0` always yield distinct cosmological-constant residuals `lambdaResidual H V1 ≠ lambdaResidual H V2`. -/
theorem cell_volume_calibration_injective
    (H V1 V2 : ℚ) (hH : H ≠ 0) (hV1 : V1 ≠ 0) (hV2 : V2 ≠ 0)
    (heq : lambdaResidual H V1 = lambdaResidual H V2) :
    V1 = V2 := by
  dsimp [lambdaResidual] at heq
  field_simp [hH, hV1, hV2] at heq
  linarith

/-- Theorem 7: Scaling both the supplied Immirzi parameter `gamma` and the cell volume `Vcell` by
the same nonzero factor `c ≠ 0` leaves `immirziLambdaResidual` identically unchanged. -/
theorem immirzi_and_cell_volume_scale_degeneracy
    (gamma Vcell H0 c : ℚ) (hc : c ≠ 0) :
    immirziLambdaResidual (c * gamma) (c * Vcell) H0 =
      immirziLambdaResidual gamma Vcell H0 := by
  dsimp [immirziLambdaResidual]
  field_simp [hc]

/-- Mean of a 4-hinge valency list `[v0, v1, v2, v3]`. -/
def fourHingeMean (v0 v1 v2 v3 : ℚ) : ℚ :=
  (v0 + v1 + v2 + v3) / 4

/-- Theorem 8: On the 4-hinge default valency scaffold `(3, 4, 5, 6)`, the exact mean is `9 / 2`,
and varying the uncalibrated cell volume `Vcell ∈ {1, 9/2, 9, 45}` shifts `lambdaResidual` across
`{9/2, 1, 1/2, 1/10}`. -/
theorem default_valency_scaffold_calibration_spread :
    fourHingeMean 3 4 5 6 = 9 / 2 ∧
    lambdaResidual (fourHingeMean 3 4 5 6) 1 = 9 / 2 ∧
    lambdaResidual (fourHingeMean 3 4 5 6) (9 / 2) = 1 ∧
    lambdaResidual (fourHingeMean 3 4 5 6) 9 = 1 / 2 ∧
    lambdaResidual (fourHingeMean 3 4 5 6) 45 = 1 / 10 := by
  dsimp [fourHingeMean, lambdaResidual]
  norm_num

-- ============================================================================
-- 3. Scalar Hinge Residual vs. 4D Tensorial Einstein Equation Fence
-- ============================================================================

/-- Number of independent components `d * (d + 1) / 2` of a symmetric rank-2 tensor in `d`
spacetime dimensions, and the number of trace-free components `d * (d + 1) / 2 - 1`. -/
def symTensorComponents (d : Nat) : Nat :=
  d * (d + 1) / 2

def traceFreeSymComponents (d : Nat) : Nat :=
  symTensorComponents d - 1

/-- Theorem 9: In `d = 4` spacetime dimensions, the symmetric Einstein tensor equation has `10`
independent components (`9` trace-free components plus `1` scalar trace), so a single scalar hinge
residual leaves `9` trace-free tensor components unconstrained. -/
theorem four_dim_symmetric_tensor_component_counts :
    symTensorComponents 4 = 10 ∧
    traceFreeSymComponents 4 = 9 ∧
    1 < symTensorComponents 4 := by
  decide

/-- Scalar mean residual `((R0 - lambda) + (R1 - lambda) + (R2 - lambda) + (R3 - lambda)) / 4` of a
4-component diagonal Ricci profile `(R0, R1, R2, R3)` against cosmological constant `lambda`. -/
def diagonalEinsteinMeanResidual (R0 R1 R2 R3 lambda : ℚ) : ℚ :=
  ((R0 - lambda) + (R1 - lambda) + (R2 - lambda) + (R3 - lambda)) / 4

/-- Sum of squared componentwise Einstein residuals `(R0 - lambda)^2 + ... + (R3 - lambda)^2`. -/
def diagonalEinsteinSqResidual (R0 R1 R2 R3 lambda : ℚ) : ℚ :=
  (R0 - lambda) ^ 2 + (R1 - lambda) ^ 2 + (R2 - lambda) ^ 2 + (R3 - lambda) ^ 2

/-- Theorem 10: For any cosmological constant `lambda` and any anisotropy parameter `delta`, the
anisotropic diagonal profile `(lambda + delta, lambda - delta, lambda, lambda)` has identically
zero scalar mean residual `diagonalEinsteinMeanResidual = 0` while its squared tensorial residual
is `2 * delta^2`. -/
theorem anisotropic_curvature_vanishing_scalar_mean_fence (lambda delta : ℚ) :
    diagonalEinsteinMeanResidual (lambda + delta) (lambda - delta) lambda lambda lambda = 0 ∧
    diagonalEinsteinSqResidual (lambda + delta) (lambda - delta) lambda lambda lambda =
      2 * delta ^ 2 := by
  refine ⟨?_, ?_⟩
  · dsimp [diagonalEinsteinMeanResidual]; ring
  · dsimp [diagonalEinsteinSqResidual]; ring

/-- Theorem 11: Whenever `delta ≠ 0`, the anisotropic profile
`(lambda + delta, lambda - delta, lambda, lambda)` has zero scalar mean residual but strictly
positive squared tensorial Einstein residual `0 < diagonalEinsteinSqResidual`, and violates the
componentwise Einstein equation `(lambda + delta) - lambda ≠ 0`. -/
theorem anisotropic_profile_violates_tensorial_einstein
    (lambda delta : ℚ) (hdelta : delta ≠ 0) :
    diagonalEinsteinMeanResidual (lambda + delta) (lambda - delta) lambda lambda lambda = 0 ∧
    0 < diagonalEinsteinSqResidual (lambda + delta) (lambda - delta) lambda lambda lambda ∧
    (lambda + delta) - lambda ≠ 0 := by
  have hsq : 0 < delta ^ 2 := sq_pos_of_ne_zero hdelta
  rcases anisotropic_curvature_vanishing_scalar_mean_fence lambda delta with ⟨hmean, hsum⟩
  refine ⟨hmean, ?_, ?_⟩
  · rw [hsum]
    linarith
  · intro h0
    apply hdelta
    linarith

/-- Theorem 12: A 4-component diagonal profile `(R0, R1, R2, R3)` satisfies the componentwise
Einstein equation `R0 = lambda ∧ R1 = lambda ∧ R2 = lambda ∧ R3 = lambda` if and only if its
squared tensorial residual `diagonalEinsteinSqResidual R0 R1 R2 R3 lambda` vanishes. -/
theorem diagonal_einstein_iff_sq_residual_zero (R0 R1 R2 R3 lambda : ℚ) :
    (R0 = lambda ∧ R1 = lambda ∧ R2 = lambda ∧ R3 = lambda) ↔
      diagonalEinsteinSqResidual R0 R1 R2 R3 lambda = 0 := by
  constructor
  · rintro ⟨rfl, rfl, rfl, rfl⟩
    dsimp [diagonalEinsteinSqResidual]
    ring
  · intro h
    dsimp [diagonalEinsteinSqResidual] at h
    have h0 : 0 ≤ (R0 - lambda) ^ 2 := sq_nonneg (R0 - lambda)
    have h1 : 0 ≤ (R1 - lambda) ^ 2 := sq_nonneg (R1 - lambda)
    have h2 : 0 ≤ (R2 - lambda) ^ 2 := sq_nonneg (R2 - lambda)
    have h3 : 0 ≤ (R3 - lambda) ^ 2 := sq_nonneg (R3 - lambda)
    have z0 : (R0 - lambda) ^ 2 = 0 := by linarith
    have z1 : (R1 - lambda) ^ 2 = 0 := by linarith
    have z2 : (R2 - lambda) ^ 2 = 0 := by linarith
    have z3 : (R3 - lambda) ^ 2 = 0 := by linarith
    refine ⟨?_, ?_, ?_, ?_⟩
    · have e0 := sq_eq_zero_iff.mp z0; linarith
    · have e1 := sq_eq_zero_iff.mp z1; linarith
    · have e2 := sq_eq_zero_iff.mp z2; linarith
    · have e3 := sq_eq_zero_iff.mp z3; linarith

end CampaignTfq0106FiniteQg

#print axioms CampaignTfq0106FiniteQg.rust_cosmological_action_unit_test_replay
#print axioms CampaignTfq0106FiniteQg.cosmological_action_zero_iff_curvature_balance
#print axioms CampaignTfq0106FiniteQg.cosmological_action_scaling_and_invariance
#print axioms CampaignTfq0106FiniteQg.cell_volume_4d_length_rescaling
#print axioms CampaignTfq0106FiniteQg.any_target_lambda_achievable_by_cell_volume_calibration
#print axioms CampaignTfq0106FiniteQg.cell_volume_calibration_injective
#print axioms CampaignTfq0106FiniteQg.immirzi_and_cell_volume_scale_degeneracy
#print axioms CampaignTfq0106FiniteQg.default_valency_scaffold_calibration_spread
#print axioms CampaignTfq0106FiniteQg.four_dim_symmetric_tensor_component_counts
#print axioms CampaignTfq0106FiniteQg.anisotropic_curvature_vanishing_scalar_mean_fence
#print axioms CampaignTfq0106FiniteQg.anisotropic_profile_violates_tensorial_einstein
#print axioms CampaignTfq0106FiniteQg.diagonal_einstein_iff_sq_residual_zero

private def l5aProvenance : String :=
  "Origin: lean4/CampaignTfq0106FiniteQg.lean Claim: TFQ-0106 AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
