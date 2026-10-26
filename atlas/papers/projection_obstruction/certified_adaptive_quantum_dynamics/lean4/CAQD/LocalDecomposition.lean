import CAQD.Duhamel

namespace CAQD

/-- Sum of edge rates at step k across E edges: ∑_{e=0}^{E-1} ν_e(k). -/
def sumEdgeRates (edge_rate : Nat → Nat → Nat) (k : Nat) : Nat → Nat
  | 0 => 0
  | e + 1 => sumEdgeRates edge_rate k e + edge_rate e k

/-- A spatial quantum lattice with local edge residuals. -/
structure LatticeResiduals where
  num_edges : Nat
  edge_rate : Nat → Nat → Nat -- edge_rate e k = ν_e(k)
  total_residual_bound : Nat → Nat -- upper bound on ||R_k||_1
  subadditivity : ∀ k,
    total_residual_bound k ≤ sumEdgeRates edge_rate k num_edges

/-- Cumulative local bound sum across all edges and time steps:
    ∑_{k=0}^{n-1} ∑_{e=0}^{E-1} ν_e(k). -/
def cumulativeLocalRateSum (lat : LatticeResiduals) : Nat → Nat
  | 0 => 0
  | k + 1 => cumulativeLocalRateSum lat k + sumEdgeRates lat.edge_rate k lat.num_edges

/-- Full edge-decomposed observable certificate bound:
    B_O(K) = ||O||_∞ * ∑_{k=0}^{K-1} ∑_{e} ν_e(k). -/
def localCertificateBound (V : OperatorSpace) (lat : LatticeResiduals) (O : V.Carrier) (steps : Nat) : Nat :=
  V.op_norm O * cumulativeLocalRateSum lat steps

/-- Theorem: Trajectory residual sum is bounded by edge rate sum. -/
theorem trajectory_residual_le_edge_sum
    (V : OperatorSpace)
    (traj : DiscreteTrajectory V)
    (lat : LatticeResiduals)
    (h_res : ∀ k, V.trace_norm (traj.residual k) ≤ lat.total_residual_bound k)
    (n : Nat) :
    sumResidualNorms V traj n ≤ cumulativeLocalRateSum lat n := by
  induction n with
  | zero =>
    dsimp [sumResidualNorms, cumulativeLocalRateSum]
    exact Nat.le_refl 0
  | succ m ih =>
    dsimp [sumResidualNorms, cumulativeLocalRateSum]
    have h_sub := lat.subadditivity m
    have h_k := h_res m
    omega

/-- Theorem: Certificate Honesty — The exact observable expectation error is bounded by
    the computable edge-decomposed certificate bound B_O. -/
theorem certificate_honesty
    (V : OperatorSpace)
    (traj : DiscreteTrajectory V)
    (lat : LatticeResiduals)
    (O : V.Carrier)
    (h_res : ∀ k, V.trace_norm (traj.residual k) ≤ lat.total_residual_bound k) :
    Int.natAbs (stepPairing V traj O traj.steps) ≤ localCertificateBound V lat O traj.steps := by
  have h_duhamel := duhamel_observable_bound V traj O
  dsimp [cumulativeBound] at h_duhamel
  dsimp [localCertificateBound]
  have h_traj_le := trajectory_residual_le_edge_sum V traj lat h_res traj.steps
  have h_mul_mono : V.op_norm O * sumResidualNorms V traj traj.steps ≤
                    V.op_norm O * cumulativeLocalRateSum lat traj.steps := by
    apply Nat.mul_le_mul_left
    exact h_traj_le
  omega

/-- Certificate Margin: Margin_O = B_O - |Tr(O * Δ)|. -/
def certificateMargin
    (V : OperatorSpace)
    (traj : DiscreteTrajectory V)
    (lat : LatticeResiduals)
    (O : V.Carrier) : Int :=
  (localCertificateBound V lat O traj.steps : Int) - (Int.natAbs (stepPairing V traj O traj.steps) : Int)

/-- Margin Non-Negativity Theorem: Margin_O ≥ 0.
    Asserts that the certificate bound never underestimates the exact error. -/
theorem margin_nonnegative
    (V : OperatorSpace)
    (traj : DiscreteTrajectory V)
    (lat : LatticeResiduals)
    (O : V.Carrier)
    (h_res : ∀ k, V.trace_norm (traj.residual k) ≤ lat.total_residual_bound k) :
    0 ≤ certificateMargin V traj lat O := by
  dsimp [certificateMargin]
  have h_honesty := certificate_honesty V traj lat O h_res
  omega

end CAQD
