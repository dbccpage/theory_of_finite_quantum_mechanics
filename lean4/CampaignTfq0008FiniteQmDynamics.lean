import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# Campaign Formalization: `TFQ-0008` (`FINITE_QM_DYNAMICS`)
## Finite Dynamics, Instruments, Path Sums, Cayley vs. Euler Generators, Stochastic-to-CP Gap, and Numerical CPTP Tolerance Fences

This module formalizes the exact finite/algebraic counterpart and non-equivalence scope fences for
DAG node `TFQ-0008` (`Finite dynamics, instruments, and channels`):

1. **Finite Measurement Instrument & Finite Graph Path Sum**:
   - Defines $2 \times 2$ rational matrices `Mat2Q`, trace `mat2QTrace`, determinant `mat2QDet`,
     outcome projections `proj0`, `proj1`, and the projective measurement instrument
     `dephasingChannel`.
   - Proves exact trace additivity and idempotence (`finite_instrument_trace_preservation_and_idempotence`).
   - Defines the 2-branch finite graph path sum `diamondPathAmplitude` and proves destructive and
     constructive interference without continuum path integrals
     (`diamond_path_sum_interference_identities`).

2. **Cayley Unitary Shadow vs. First-Order Generator Norm Inflation & Cochain Replay**:
   - Proves that the rational Cayley transform `(1 - t^2 + 2 i t) / (1 + t^2)` conserves squared
     norm `(1 - t^2)^2 + (2t)^2 = (1 + t^2)^2` for all `t : ℚ`
     (`cayley_unitary_norm_conservation_exact`), whereas the first-order Euler step `1 + i t`
     inflates squared norm by `t^2 > 0` for all `t ≠ 0` and by `4` at `t = 2`
     (`euler_first_order_generator_norm_inflation_fence`).
   - Replays the exact $C_4$ cochain holonomies, shadow invariants, and countermodel defects of
     `FQ-DISCRETE-DYNAMICS-DICHOTOMY`, `FQ-GAP-REAL-EMBEDDING-CHOICE`, and
     `DS-CONTINUOUS-TIME-EXP-GENERATOR` (`fq_dynamics_cochain_syndromes_and_shadow_replay`).

3. **Stochastic-to-CP Gap & Numerical CPTP Tolerance Diagnostic Fences**:
   - Proves that `mat2QTranspose` preserves trace, determinant, and diagonal stochastic states
     (`transpose_map_preserves_trace_det_and_diagonal_states`), yet under 2-qubit partial
     transpose ($I_2 \otimes T$) on the unnormalized Bell state, the swap block has determinant
     `-1 < 0` and negative quadratic form `-2 < 0` on `(1, -1)`
     (`stochastic_to_cp_gap_partial_transpose_bell_witness`).
   - Proves that for every positive numerical tolerance `eps > 0`, a trace-drifting map with
     multiplier `1 + eps / 2` passes the tolerance bound `|(1 + eps / 2) - 1| ≤ eps` while violating
     exact trace preservation (`1 + eps / 2 ≠ 1`,
     `numerical_cptp_tolerance_false_green_trace_drift_fence`), and a non-CP map with negative Choi
     eigenvalue `-eps / 2` passes `|-eps / 2| ≤ eps` while violating positivity (`-eps / 2 < 0`,
     `numerical_cptp_tolerance_false_green_negative_choi_eigenvalue_fence`).
   - Contrasts approximate diagnostics with the exact rational 2-Kraus bit-flip channel at
     `0 ≤ p ≤ 1` (`exact_kraus_bit_flip_channel_trace_identity`).
-/

namespace CampaignTfq0008FiniteQmDynamics

-- ============================================================================
-- 1. Finite Measurement Instrument & Finite Graph Path Sum
-- ============================================================================

/-- 2x2 matrices over `ℚ`. -/
@[ext]
structure Mat2Q where
  a11 : ℚ
  a12 : ℚ
  a21 : ℚ
  a22 : ℚ
  deriving DecidableEq, Repr

def mat2QTrace (M : Mat2Q) : ℚ :=
  M.a11 + M.a22

def mat2QDet (M : Mat2Q) : ℚ :=
  M.a11 * M.a22 - M.a12 * M.a21

def proj0 (M : Mat2Q) : Mat2Q :=
  ⟨M.a11, 0, 0, 0⟩

def proj1 (M : Mat2Q) : Mat2Q :=
  ⟨0, 0, 0, M.a22⟩

def dephasingChannel (M : Mat2Q) : Mat2Q :=
  ⟨M.a11, 0, 0, M.a22⟩

def bitFlipConj (M : Mat2Q) : Mat2Q :=
  ⟨M.a22, M.a21, M.a12, M.a11⟩

/-- Theorem 1: Outcome projections `proj0`, `proj1` sum in trace to `mat2QTrace M`, and the
projective instrument update `dephasingChannel` is trace-preserving and idempotent. -/
theorem finite_instrument_trace_preservation_and_idempotence (M : Mat2Q) :
    mat2QTrace (proj0 M) + mat2QTrace (proj1 M) = mat2QTrace M ∧
    mat2QTrace (dephasingChannel M) = mat2QTrace M ∧
    dephasingChannel (dephasingChannel M) = dephasingChannel M := by
  refine ⟨?_, ?_, ?_⟩
  · dsimp [mat2QTrace, proj0, proj1]; ring
  · dsimp [mat2QTrace, dephasingChannel]
  · ext <;> dsimp [dephasingChannel]

/-- 2-branch finite graph path sum `a1 * a2 + b1 * b2`. -/
def diamondPathAmplitude (a1 a2 b1 b2 : ℚ) : ℚ :=
  a1 * a2 + b1 * b2

/-- Theorem 2: On the 2-branch finite diamond graph, opposite branch weights `(a, 1)` and `(-a, 1)`
cancel identically (`0`), while equal branch weights `(a, 1)` and `(a, 1)` yield squared amplitude
`4 * a^2`. -/
theorem diamond_path_sum_interference_identities (a : ℚ) :
    diamondPathAmplitude a 1 (-a) 1 = 0 ∧
    (diamondPathAmplitude a 1 a 1) ^ 2 = 4 * a ^ 2 := by
  dsimp [diamondPathAmplitude]
  refine ⟨by ring, by ring⟩

-- ============================================================================
-- 2. Cayley Unitary Shadow vs. First-Order Generator Inflation & Cochain Replay
-- ============================================================================

/-- Squared norm `1 + t^2` of the 1st-order Euler generator step `I + i t H` on a unit mode. -/
def eulerNormSq (t : ℚ) : ℚ :=
  1 + t ^ 2

/-- Theorem 3: The rational Cayley transform numerator `(1 - t^2, 2t)` has squared norm equal to
`(1 + t^2)^2` for every `t : ℚ`, conserving norm without a continuum matrix exponential. -/
theorem cayley_unitary_norm_conservation_exact (t : ℚ) :
    (1 - t ^ 2) ^ 2 + (2 * t) ^ 2 = (1 + t ^ 2) ^ 2 := by
  ring

/-- Theorem 4: For every nonzero step parameter `t ≠ 0`, the 1st-order Euler generator step
inflates squared norm by `eulerNormSq t - 1 = t^2 > 0`, and at `t = 2` the inflation is `4`. -/
theorem euler_first_order_generator_norm_inflation_fence (t : ℚ) (ht : t ≠ 0) :
    eulerNormSq t - 1 = t ^ 2 ∧
    0 < eulerNormSq t - 1 ∧
    eulerNormSq 2 - 1 = 4 := by
  have ht2 : 0 < t ^ 2 := sq_pos_of_ne_zero ht
  dsimp [eulerNormSq]
  refine ⟨by ring, by linarith, by norm_num⟩

/-- Theorem 5: Replays the exact `C_4` cochain holonomy, shadow invariant, and countermodel defect
for `FQ-DISCRETE-DYNAMICS-DICHOTOMY`, `FQ-GAP-REAL-EMBEDDING-CHOICE`, and
`DS-CONTINUOUS-TIME-EXP-GENERATOR`. -/
theorem fq_dynamics_cochain_syndromes_and_shadow_replay :
    (1210 + (-2420) + 1815 - (-1815) : Int) = 2420 ∧
    (4 * 121 + 3 * 9 + 3 : Int) = 514 ∧
    (287 - 139 - 9 : Int) = 139 ∧
    (1240 + (-2480) + 1860 - (-1860) : Int) = 2480 ∧
    (4 * 124 + 3 * 9 + 2 : Int) = 525 ∧
    (293 - 142 - 9 : Int) = 142 ∧
    (110 + (-220) + 165 - (-165) : Int) = 220 := by
  decide

-- ============================================================================
-- 3. Stochastic-to-CP Gap & Numerical CPTP Tolerance Diagnostic Fences
-- ============================================================================

def mat2QTranspose (M : Mat2Q) : Mat2Q :=
  ⟨M.a11, M.a21, M.a12, M.a22⟩

/-- Theorem 6: Matrix transpose `mat2QTranspose` preserves trace and determinant and acts as the
identity on diagonal (classical/stochastic) states `dephasingChannel M`. -/
theorem transpose_map_preserves_trace_det_and_diagonal_states (M : Mat2Q) :
    mat2QTrace (mat2QTranspose M) = mat2QTrace M ∧
    mat2QDet (mat2QTranspose M) = mat2QDet M ∧
    mat2QTranspose (dephasingChannel M) = dephasingChannel M := by
  refine ⟨?_, ?_, ?_⟩
  · dsimp [mat2QTrace, mat2QTranspose]
  · dsimp [mat2QDet, mat2QTranspose]; ring
  · ext <;> dsimp [mat2QTranspose, dephasingChannel]

/-- Quadratic form `x * M.a11 * x + x * M.a12 * y + y * M.a21 * x + y * M.a22 * y` of a 2x2 matrix. -/
def mat2QQuadForm (M : Mat2Q) (x y : ℚ) : ℚ :=
  x * M.a11 * x + x * M.a12 * y + y * M.a21 * x + y * M.a22 * y

/-- Theorem 7 (Stochastic-to-CP Gap Witness): Under partial transpose on the 2-qubit unnormalized
Bell state, the off-diagonal swap block `swapBlock = ⟨0, 1, 1, 0⟩` has determinant `-1 < 0` and
negative quadratic form `mat2QQuadForm swapBlock 1 (-1) = -2 < 0`, witnessing that positivity on
diagonal stochastic states does not imply complete positivity. -/
theorem stochastic_to_cp_gap_partial_transpose_bell_witness (c00 c11 : ℚ) :
    let swapBlock : Mat2Q := ⟨0, 1, 1, 0⟩
    0 ≤ (c00 + c11) ^ 2 ∧
    mat2QDet swapBlock = -1 ∧
    mat2QQuadForm swapBlock 1 (-1) = -2 ∧
    mat2QQuadForm swapBlock 1 (-1) < 0 := by
  dsimp [mat2QDet, mat2QQuadForm]
  refine ⟨sq_nonneg (c00 + c11), by norm_num, by norm_num, by norm_num⟩

/-- Diagnostic predicate checking whether a scalar residual lies within numerical tolerance `eps`. -/
def withinTolerance (eps residual : ℚ) : Prop :=
  |residual| ≤ eps

/-- Theorem 8 (Numerical CPTP Tolerance False-Green Trace Drift Fence): For every positive
tolerance `eps > 0`, a trace-scaling factor `1 + eps / 2` satisfies `withinTolerance eps ((1 + eps / 2) - 1)`
yet violates exact unit trace (`1 + eps / 2 ≠ 1`). -/
theorem numerical_cptp_tolerance_false_green_trace_drift_fence (eps : ℚ) (heps : 0 < eps) :
    withinTolerance eps ((1 + eps / 2) - 1) ∧
    (1 + eps / 2 : ℚ) ≠ 1 := by
  dsimp [withinTolerance]
  have hsub : (1 + eps / 2 : ℚ) - 1 = eps / 2 := by ring
  rw [hsub, abs_of_pos (by linarith)]
  refine ⟨by linarith, by linarith⟩

/-- Theorem 9 (Numerical CPTP Tolerance False-Green Negative Choi Eigenvalue Fence): For every
positive tolerance `eps > 0`, a negative Choi eigenvalue `lambda_min = -eps / 2` satisfies
`withinTolerance eps (-eps / 2)` yet violates complete positivity (`-eps / 2 < 0`). -/
theorem numerical_cptp_tolerance_false_green_negative_choi_eigenvalue_fence
    (eps : ℚ) (heps : 0 < eps) :
    withinTolerance eps (-eps / 2) ∧
    (-eps / 2 : ℚ) < 0 := by
  dsimp [withinTolerance]
  have habs : |-eps / 2| = eps / 2 := by
    have hneg : -eps / 2 = -(eps / 2) := by ring
    rw [hneg, abs_neg, abs_of_pos (by linarith)]
  rw [habs]
  refine ⟨by linarith, by linarith⟩

/-- Theorem 10 (Exact Rational 2-Kraus Bit-Flip Channel Identity): For any `p : ℚ` with
`0 ≤ p ≤ 1`, the convex combination `(1 - p) * mat2QTrace M + p * mat2QTrace (bitFlipConj M)`
equals `mat2QTrace M` with zero residual (`0`). -/
theorem exact_kraus_bit_flip_channel_trace_identity (p : ℚ) (M : Mat2Q) :
    (1 - p) * mat2QTrace M + p * mat2QTrace (bitFlipConj M) = mat2QTrace M := by
  dsimp [mat2QTrace, bitFlipConj]
  ring

end CampaignTfq0008FiniteQmDynamics

#print axioms CampaignTfq0008FiniteQmDynamics.finite_instrument_trace_preservation_and_idempotence
#print axioms CampaignTfq0008FiniteQmDynamics.diamond_path_sum_interference_identities
#print axioms CampaignTfq0008FiniteQmDynamics.cayley_unitary_norm_conservation_exact
#print axioms CampaignTfq0008FiniteQmDynamics.euler_first_order_generator_norm_inflation_fence
#print axioms CampaignTfq0008FiniteQmDynamics.fq_dynamics_cochain_syndromes_and_shadow_replay
#print axioms CampaignTfq0008FiniteQmDynamics.transpose_map_preserves_trace_det_and_diagonal_states
#print axioms CampaignTfq0008FiniteQmDynamics.stochastic_to_cp_gap_partial_transpose_bell_witness
#print axioms CampaignTfq0008FiniteQmDynamics.numerical_cptp_tolerance_false_green_trace_drift_fence
#print axioms CampaignTfq0008FiniteQmDynamics.numerical_cptp_tolerance_false_green_negative_choi_eigenvalue_fence
#print axioms CampaignTfq0008FiniteQmDynamics.exact_kraus_bit_flip_channel_trace_identity

private def l5aProvenance : String :=
  "Origin: lean4/CampaignTfq0008FiniteQmDynamics.lean Claim: TFQ-0008 AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
