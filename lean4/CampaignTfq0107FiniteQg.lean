import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp

/-!
# Campaign Formalization: `TFQ-0107` (`FINITE_QG`)
## Exact Rational Replay and Scope Fences for `field_equation.rs` and `hamiltonian_constraint.rs`

This module formalizes the exact rational counterpart and non-equivalence scope fences for
DAG node `TFQ-0107` (`GAP: Einstein equation and physical cosmological constant stay unpaid;
deficit is not smooth curvature`):

1. **Exact Rational Replay of Discrete 4D Regge Field Equations (`field_equation.rs`)**:
   - Models `cosmoGrad`, `reggeEdgeResidual`, `discreteEinsteinTensor`, and `reggeRelaxationStepSq`
     from `code/rust/src/general_relativity/field_equation.rs`.
   - Proves the vanishing characterization `reggeEdgeResidual C lambda Vgrad = 0 ↔ C = lambda * Vgrad`
     (`regge_edge_residual_zero_iff`), the flat-interior identity
     `reggeEdgeResidual 0 lambda Vgrad = -cosmoGrad lambda Vgrad` replaying the two Rust unit tests
     (`flat_interior_regge_residual_replay`), and the gradient-relaxation fixed-point equivalence
     `reggeRelaxationStepSq L2 lr res = L2 ↔ res = 0` for `lr ≠ 0`
     (`regge_relaxation_fixed_point_iff`).

2. **Exact Rational Replay of Simplicial Wheeler-DeWitt / Hamiltonian Constraint (`hamiltonian_constraint.rs`)**:
   - Models `vertexDualVolumeShare`, `vertexKineticTerm`, `vertexCurvaturePotential`,
     `vertexCosmologicalPotential`, and `vertexHamiltonianResidual` from
     `code/rust/src/general_relativity/hamiltonian_constraint.rs`.
   - Proves the 4-vertex tetrahedral volume partition `4 * vertexDualVolumeShare V3 = V3` and
     zero-momentum kinetic vanishing (`single_tetrahedron_zero_momentum_replay`, replaying
     `test_hamiltonian_constraint_evaluation_single_tetrahedron`).
   - Proves the indefinite-signature property of the discrete DeWitt kinetic quadratic form
     `∑ π_e^2 - (1/2)(∑ π_e)^2`: it vanishes identically on 2 equal nonzero edge momenta `(p, p)`
     and is strictly negative `-(3/2) * p^2 / V < 0` on 3 equal nonzero edge momenta `(p, p, p)`
     (`dewitt_kinetic_null_and_negative_modes`).

3. **Scope Fences: $\Lambda$ Underdetermination, Scaling Mismatch, and Multi-Hinge Kernel**:
   - **$\Lambda$ Underdetermination (`hamiltonian_lambda_underdetermination`, `regge_edge_lambda_underdetermination`)**:
     For any vertex volume `V ≠ 0` (or nonzero volume gradient `Vgrad ≠ 0`), the discrete
     Hamiltonian constraint (or Regge edge equation) vanishes at the caller-supplied value
     `lambda = (curv - kin) / (2 * V)` (or `lambda = C / Vgrad`), so neither equation selects a
     unique physical cosmological constant $\Lambda$.
   - **3D Spatial Rescaling Mismatch (`static_hamiltonian_scaling_mismatch`)**:
     Under uniform edge rescaling `L ↦ s * L`, `curv` scales as `s^1` while 3D volume `V` scales
     as `s^3`, so a balanced static state `curv = 2 * lambda * V ≠ 0` at `s = 1` acquires residual
     `curv * s * (s^2 - 1) ≠ 0` for `s > 1` unless `lambda` is externally rescaled by `1 / s^2`.
   - **Two-Hinge Cancellation Kernel (`two_hinge_curvature_grad_cancellation_fence`)**:
     Two hinges sharing an edge with equal area derivatives `dA ≠ 0` and opposite nonzero deficits
     `(+delta, -delta)` (`delta ≠ 0`) yield `curvature_grad = 0` and vanishing Regge edge residual
     at `lambda = 0` despite strictly positive squared deficit `2 * delta^2 > 0`.
-/

namespace CampaignTfq0107FiniteQg

-- ============================================================================
-- 1. Exact Rational Replay of `field_equation.rs`
-- ============================================================================

/-- Cosmological volume-gradient term `lambda * volGrad` in `compute_regge_field_equations_4d`
(`code/rust/src/general_relativity/field_equation.rs` line 87). -/
def cosmoGrad (lambda volGrad : ℚ) : ℚ :=
  lambda * volGrad

/-- Discrete Regge edge residual `curvatureGrad - lambda * volGrad` in
`compute_regge_field_equations_4d` (`field_equation.rs` line 88). -/
def reggeEdgeResidual (curvatureGrad lambda volGrad : ℚ) : ℚ :=
  curvatureGrad - cosmoGrad lambda volGrad

/-- Discrete edge Einstein quotient `curvatureGrad / dualVolume` (`field_equation.rs` line 91). -/
def discreteEinsteinTensor (curvatureGrad dualVolume : ℚ) : ℚ :=
  curvatureGrad / dualVolume

/-- Squared edge-length relaxation update `currentSq - learningRate * res` in
`solve_regge_field_equations_relaxation` (`field_equation.rs` lines 160-161). -/
def reggeRelaxationStepSq (currentSq learningRate res : ℚ) : ℚ :=
  currentSq - learningRate * res

/-- Theorem 1: The discrete Regge edge residual vanishes if and only if `curvatureGrad` equals
`lambda * volGrad`. -/
theorem regge_edge_residual_zero_iff (curvatureGrad lambda volGrad : ℚ) :
    reggeEdgeResidual curvatureGrad lambda volGrad = 0 ↔
      curvatureGrad = cosmoGrad lambda volGrad := by
  dsimp [reggeEdgeResidual, cosmoGrad]
  constructor <;> intro h <;> linarith

/-- Theorem 2: Exact rational replay of the two unit tests in `field_equation.rs`
(`test_flat_fan_regge_field_equations_vanish_for_zero_lambda` and
`test_cosmological_term_nonzero_when_lambda_positive`): on a flat interior (`curvatureGrad = 0`),
the residual vanishes for `lambda = 0`, equals `-cosmoGrad lambda volGrad` for all `lambda`, and is
nonzero whenever `lambda ≠ 0` and `volGrad ≠ 0`. -/
theorem flat_interior_regge_residual_replay
    (lambda volGrad : ℚ) (hlambda : lambda ≠ 0) (hvol : volGrad ≠ 0) :
    reggeEdgeResidual 0 0 volGrad = 0 ∧
    reggeEdgeResidual 0 lambda volGrad = -cosmoGrad lambda volGrad ∧
    cosmoGrad lambda volGrad ≠ 0 := by
  refine ⟨?_, ?_, mul_ne_zero hlambda hvol⟩
  · dsimp [reggeEdgeResidual, cosmoGrad]; ring
  · dsimp [reggeEdgeResidual, cosmoGrad]; ring

/-- Theorem 3: For any nonzero learning rate `lr ≠ 0`, a squared edge length `L2` is a fixed point
of `reggeRelaxationStepSq` if and only if its edge residual `res` vanishes. -/
theorem regge_relaxation_fixed_point_iff
    (L2 lr res : ℚ) (hlr : lr ≠ 0) :
    reggeRelaxationStepSq L2 lr res = L2 ↔ res = 0 := by
  dsimp [reggeRelaxationStepSq]
  constructor
  · intro h
    have hmul : lr * res = 0 := by linarith
    exact (mul_eq_zero.mp hmul).resolve_left hlr
  · intro h
    rw [h]
    ring

-- ============================================================================
-- 2. Exact Rational Replay of `hamiltonian_constraint.rs`
-- ============================================================================

/-- Vertex share `(1 / 4) * vol3` of a 3D tetrahedron's volume in `compute_vertex_volumes`
(`code/rust/src/general_relativity/hamiltonian_constraint.rs` line 55). -/
def vertexDualVolumeShare (vol3 : ℚ) : ℚ :=
  (1 / 4) * vol3

/-- Simplicial DeWitt kinetic term `(1 / vVol) * (sumPiSq - (1 / 2) * sumPi^2)` in
`evaluate_vertex_constraint` (`hamiltonian_constraint.rs` line 129). -/
def vertexKineticTerm (vVol sumPiSq sumPi : ℚ) : ℚ :=
  (1 / vVol) * (sumPiSq - (1 / 2) * sumPi ^ 2)

/-- Simplicial curvature potential `(1 / 2) * sumLenEps` (`hamiltonian_constraint.rs` line 135). -/
def vertexCurvaturePotential (sumLenEps : ℚ) : ℚ :=
  (1 / 2) * sumLenEps

/-- Simplicial cosmological potential `2 * lambda * vVol` (`hamiltonian_constraint.rs` line 138). -/
def vertexCosmologicalPotential (lambda vVol : ℚ) : ℚ :=
  2 * lambda * vVol

/-- Vertex Hamiltonian constraint residual `kinetic - curv + 2 * lambda * vVol`
(`hamiltonian_constraint.rs` line 139). -/
def vertexHamiltonianResidual (kinetic curv lambda vVol : ℚ) : ℚ :=
  kinetic - curv + vertexCosmologicalPotential lambda vVol

/-- Theorem 4: Exact rational replay of `test_hamiltonian_constraint_evaluation_single_tetrahedron`
in `hamiltonian_constraint.rs`: the 4 vertex dual-volume shares sum to `vol3`, and zero edge
momenta (`sumPiSq = 0, sumPi = 0`) yield identically zero vertex kinetic energy. -/
theorem single_tetrahedron_zero_momentum_replay (vol3 vVol : ℚ) :
    4 * vertexDualVolumeShare vol3 = vol3 ∧
    vertexKineticTerm vVol 0 0 = 0 := by
  refine ⟨?_, ?_⟩
  · dsimp [vertexDualVolumeShare]; ring
  · dsimp [vertexKineticTerm]; ring

/-- Theorem 5: Indefinite signature of the discrete DeWitt kinetic term `vertexKineticTerm`:
(1) on 2 incident edges with equal momenta `(p, p)` (`sumPiSq = 2*p^2, sumPi = 2*p`), the kinetic
term vanishes identically even for `p ≠ 0`;
(2) on 3 incident edges with equal momenta `(p, p, p)` (`sumPiSq = 3*p^2, sumPi = 3*p`), the kinetic
term equals `-(3 / 2) * p^2 / vVol`, which is strictly negative for `vVol > 0` and `p ≠ 0`. -/
theorem dewitt_kinetic_null_and_negative_modes
    (vVol p : ℚ) (hv : 0 < vVol) (hp : p ≠ 0) :
    vertexKineticTerm vVol (p ^ 2 + p ^ 2) (p + p) = 0 ∧
    vertexKineticTerm vVol (p ^ 2 + p ^ 2 + p ^ 2) (p + p + p) =
      -(3 / 2) * p ^ 2 / vVol ∧
    vertexKineticTerm vVol (p ^ 2 + p ^ 2 + p ^ 2) (p + p + p) < 0 := by
  have hp2 : 0 < p ^ 2 := sq_pos_of_ne_zero hp
  have hquot : 0 < p ^ 2 / vVol := div_pos hp2 hv
  refine ⟨?_, ?_, ?_⟩
  · dsimp [vertexKineticTerm]; ring
  · dsimp [vertexKineticTerm]; ring
  · have heq : vertexKineticTerm vVol (p ^ 2 + p ^ 2 + p ^ 2) (p + p + p) =
        -(3 / 2) * (p ^ 2 / vVol) := by
      dsimp [vertexKineticTerm]; ring
    rw [heq]
    linarith

-- ============================================================================
-- 3. Scope Fences: Lambda Underdetermination, Scaling Mismatch, & Hinge Kernel
-- ============================================================================

/-- Theorem 6 (`Lambda` Underdetermination in `hamiltonian_constraint.rs`): For any nonzero vertex
dual volume `vVol ≠ 0` and any kinetic and curvature terms `(kin, curv)`, choosing the caller-supplied
cosmological constant `lambda = (curv - kin) / (2 * vVol)` makes `vertexHamiltonianResidual` vanish,
and any `lambda` satisfying the constraint must equal `(curv - kin) / (2 * vVol)`. -/
theorem hamiltonian_lambda_underdetermination
    (kin curv lambda vVol : ℚ) (hv : vVol ≠ 0) :
    vertexHamiltonianResidual kin curv lambda vVol = 0 ↔
      lambda = (curv - kin) / (2 * vVol) := by
  dsimp [vertexHamiltonianResidual, vertexCosmologicalPotential]
  constructor
  · intro h
    have h1 : 2 * lambda * vVol = curv - kin := by linarith
    rw [← h1]
    field_simp [hv]
  · intro h
    rw [h]
    field_simp [hv]
    ring

/-- Theorem 7 (`Lambda` Underdetermination in `field_equation.rs`): For any nonzero volume gradient
`volGrad ≠ 0` and any curvature gradient `curvatureGrad`, choosing `lambda = curvatureGrad / volGrad`
makes `reggeEdgeResidual` vanish, and any `lambda` with zero residual equals `curvatureGrad / volGrad`. -/
theorem regge_edge_lambda_underdetermination
    (curvatureGrad lambda volGrad : ℚ) (hvol : volGrad ≠ 0) :
    reggeEdgeResidual curvatureGrad lambda volGrad = 0 ↔
      lambda = curvatureGrad / volGrad := by
  dsimp [reggeEdgeResidual, cosmoGrad]
  constructor
  · intro h
    have h1 : curvatureGrad = lambda * volGrad := by linarith
    rw [h1]
    field_simp [hvol]
  · intro h
    rw [h]
    field_simp [hvol]
    ring

/-- Theorem 8 (3D Spatial Rescaling Mismatch Fence): On a static slice (`kin = 0`) where the
unscaled Hamiltonian constraint holds (`curv = 2 * lambda * vVol`), uniform edge rescaling `L ↦ s * L`
scales `curv` by `s` and 3D volume `vVol` by `s^3`, producing residual
`vertexHamiltonianResidual 0 (s * curv) lambda (s^3 * vVol) = curv * s * (s^2 - 1)`, while rescaling
`lambda ↦ lambda / s^2` (`s ≠ 0`) restores balance. -/
theorem static_hamiltonian_scaling_mismatch
    (curv lambda vVol s : ℚ) (hs : s ≠ 0)
    (hbal : vertexHamiltonianResidual 0 curv lambda vVol = 0) :
    vertexHamiltonianResidual 0 (s * curv) lambda (s ^ 3 * vVol) =
      curv * s * (s ^ 2 - 1) ∧
    vertexHamiltonianResidual 0 (s * curv) (lambda / s ^ 2) (s ^ 3 * vVol) = 0 ∧
    s ^ 2 ≠ 0 := by
  dsimp [vertexHamiltonianResidual, vertexCosmologicalPotential] at hbal ⊢
  have hcurv : curv = 2 * lambda * vVol := by linarith
  refine ⟨?_, ?_, pow_ne_zero 2 hs⟩
  · rw [hcurv]; ring
  · rw [hcurv]
    field_simp [hs]
    ring

/-- Curvature gradient `eps1 * dA1 + eps2 * dA2` of two hinges sharing an edge (`field_equation.rs`
line 70) and their squared hinge-deficit norm `eps1^2 + eps2^2`. -/
def twoHingeCurvatureGrad (eps1 dA1 eps2 dA2 : ℚ) : ℚ :=
  eps1 * dA1 + eps2 * dA2

def twoHingeDeficitSqNorm (eps1 eps2 : ℚ) : ℚ :=
  eps1 ^ 2 + eps2 ^ 2

/-- Theorem 9 (Two-Hinge Cancellation Kernel Fence): If two hinges incident to edge `(u, v)` have
equal area derivatives `dA` and opposite deficits `(+delta, -delta)` with `delta ≠ 0`, then
`twoHingeCurvatureGrad` and `reggeEdgeResidual` at `lambda = 0` both vanish (`= 0`), whereas the
squared hinge-deficit norm `twoHingeDeficitSqNorm delta (-delta) = 2 * delta^2` is strictly positive. -/
theorem two_hinge_curvature_grad_cancellation_fence
    (delta dA volGrad : ℚ) (hdelta : delta ≠ 0) :
    twoHingeCurvatureGrad delta dA (-delta) dA = 0 ∧
    reggeEdgeResidual (twoHingeCurvatureGrad delta dA (-delta) dA) 0 volGrad = 0 ∧
    twoHingeDeficitSqNorm delta (-delta) = 2 * delta ^ 2 ∧
    0 < twoHingeDeficitSqNorm delta (-delta) := by
  have hsq : 0 < delta ^ 2 := sq_pos_of_ne_zero hdelta
  refine ⟨?_, ?_, ?_, ?_⟩
  · dsimp [twoHingeCurvatureGrad]; ring
  · dsimp [reggeEdgeResidual, cosmoGrad, twoHingeCurvatureGrad]; ring
  · dsimp [twoHingeDeficitSqNorm]; ring
  · dsimp [twoHingeDeficitSqNorm]; linarith

/-- Theorem 10: Two hinge deficits `(eps1, eps2)` vanish individually (`eps1 = 0 ∧ eps2 = 0`) if
and only if `twoHingeDeficitSqNorm eps1 eps2 = 0`. -/
theorem two_hinge_deficit_zero_iff_sq_norm_zero (eps1 eps2 : ℚ) :
    (eps1 = 0 ∧ eps2 = 0) ↔ twoHingeDeficitSqNorm eps1 eps2 = 0 := by
  constructor
  · rintro ⟨rfl, rfl⟩
    dsimp [twoHingeDeficitSqNorm]; ring
  · intro h
    dsimp [twoHingeDeficitSqNorm] at h
    have h1 : 0 ≤ eps1 ^ 2 := sq_nonneg eps1
    have h2 : 0 ≤ eps2 ^ 2 := sq_nonneg eps2
    have z1 : eps1 ^ 2 = 0 := by linarith
    have z2 : eps2 ^ 2 = 0 := by linarith
    exact ⟨sq_eq_zero_iff.mp z1, sq_eq_zero_iff.mp z2⟩

end CampaignTfq0107FiniteQg

#print axioms CampaignTfq0107FiniteQg.regge_edge_residual_zero_iff
#print axioms CampaignTfq0107FiniteQg.flat_interior_regge_residual_replay
#print axioms CampaignTfq0107FiniteQg.regge_relaxation_fixed_point_iff
#print axioms CampaignTfq0107FiniteQg.single_tetrahedron_zero_momentum_replay
#print axioms CampaignTfq0107FiniteQg.dewitt_kinetic_null_and_negative_modes
#print axioms CampaignTfq0107FiniteQg.hamiltonian_lambda_underdetermination
#print axioms CampaignTfq0107FiniteQg.regge_edge_lambda_underdetermination
#print axioms CampaignTfq0107FiniteQg.static_hamiltonian_scaling_mismatch
#print axioms CampaignTfq0107FiniteQg.two_hinge_curvature_grad_cancellation_fence
#print axioms CampaignTfq0107FiniteQg.two_hinge_deficit_zero_iff_sq_norm_zero

private def l5aProvenance : String :=
  "Origin: lean4/CampaignTfq0107FiniteQg.lean Claim: TFQ-0107 AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
