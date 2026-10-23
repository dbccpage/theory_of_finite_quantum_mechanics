import CAQD.LocalDecomposition

namespace CAQD

/-- Tolerance Certification Theorem:
    Whenever the computable certificate bound satisfies B_O(K) ≤ ε,
    the true physical observable error |Tr(O(ρ - ρ̃))| is guaranteed to satisfy ≤ ε. -/
theorem certified_tolerance_satisfaction
    (V : OperatorSpace)
    (traj : DiscreteTrajectory V)
    (lat : LatticeResiduals)
    (O : V.Carrier)
    (tol : Nat)
    (h_res : ∀ k, V.trace_norm (traj.residual k) ≤ lat.total_residual_bound k)
    (h_bound : localCertificateBound V lat O traj.steps ≤ tol) :
    Int.natAbs (stepPairing V traj O traj.steps) ≤ tol := by
  have h_honesty := certificate_honesty V traj lat O h_res
  omega

/-- Helper: sumEdgeRates is monotonic in the edge rates. -/
theorem sumEdgeRates_le (r1 r2 : Nat → Nat → Nat) (k E : Nat)
    (h_le : ∀ e, r1 e k ≤ r2 e k) :
    sumEdgeRates r1 k E ≤ sumEdgeRates r2 k E := by
  induction E with
  | zero =>
    dsimp [sumEdgeRates]
    exact Nat.le_refl 0
  | succ E' ih =>
    dsimp [sumEdgeRates]
    have h_step := h_le E'
    omega

/-- Refinement Monotonicity:
    If a localized adaptation replaces edge rate ν_e with ν'_e ≤ ν_e,
    the resulting certificate bound is monotonically non-increasing. -/
theorem refinement_monotonicity
    (V : OperatorSpace)
    (lat lat' : LatticeResiduals)
    (O : V.Carrier)
    (steps : Nat)
    (h_edges : lat.num_edges = lat'.num_edges)
    (h_le : ∀ e k, lat'.edge_rate e k ≤ lat.edge_rate e k) :
    localCertificateBound V lat' O steps ≤ localCertificateBound V lat O steps := by
  dsimp [localCertificateBound]
  have h_sum_le : cumulativeLocalRateSum lat' steps ≤ cumulativeLocalRateSum lat steps := by
    induction steps with
    | zero =>
      dsimp [cumulativeLocalRateSum]
      exact Nat.le_refl 0
    | succ n ih =>
      dsimp [cumulativeLocalRateSum]
      have h_edge_le : sumEdgeRates lat'.edge_rate n lat'.num_edges ≤
                       sumEdgeRates lat.edge_rate n lat.num_edges := by
        rw [← h_edges]
        exact sumEdgeRates_le lat'.edge_rate lat.edge_rate n lat.num_edges (fun e => h_le e n)
      omega
  have h_mul := Nat.mul_le_mul_left (V.op_norm O) h_sum_le
  exact h_mul

end CAQD
