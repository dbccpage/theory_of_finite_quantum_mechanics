import CAQD.ErrorBound

namespace CAQD

/-- Single step bound evaluation (t = 1 step). -/
theorem single_step_rate
    (V : OperatorSpace)
    (lat : LatticeResiduals)
    (O : V.Carrier) :
    localCertificateBound V lat O 1 =
    V.op_norm O * sumEdgeRates lat.edge_rate 0 lat.num_edges := by
  dsimp [localCertificateBound, cumulativeLocalRateSum]
  rw [Nat.zero_add]

/-- Helper: sumEdgeRates equivalence under pointwise equal rates. -/
theorem sumEdgeRates_eq (r1 r2 : Nat → Nat → Nat) (k E : Nat)
    (h_eq : ∀ e, r1 e k = r2 e k) :
    sumEdgeRates r1 k E = sumEdgeRates r2 k E := by
  induction E with
  | zero =>
    dsimp [sumEdgeRates]
  | succ E' ih =>
    dsimp [sumEdgeRates]
    rw [ih, h_eq E']

/-- PO-000 Theorem 5.1 Short-time defect comparison:
    At short times, the leading linear coefficient of the certificate bound
    matches the sum of initial normal defect rates ∑_e ν_e(0). -/
theorem leading_linear_rate_matches_defect_sum
    (V : OperatorSpace)
    (lat : LatticeResiduals)
    (O : V.Carrier)
    (initial_rates : Nat → Nat)
    (h_init : ∀ e, lat.edge_rate e 0 = initial_rates e) :
    localCertificateBound V lat O 1 =
    V.op_norm O * sumEdgeRates (fun e _ => initial_rates e) 0 lat.num_edges := by
  rw [single_step_rate]
  have h_sum := sumEdgeRates_eq lat.edge_rate (fun e _ => initial_rates e) 0 lat.num_edges (fun e => h_init e)
  rw [h_sum]

end CAQD
