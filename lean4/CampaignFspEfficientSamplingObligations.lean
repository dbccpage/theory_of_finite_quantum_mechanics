import Mathlib.Tactic

/-!
# CampaignFspEfficientSamplingObligations: Sampling Cost, Variance, Mixing, and Normal-Form Scope Fences (TFQ-0409)

Formalizes the narrowed local mathematical witnesses and scope fences for
`FSP-EFFICIENT-SAMPLING-OBLIGATIONS` (`TFQ-0409`, stage `FERMION_SIGN`,
status `OPEN` preserved):

1. **Exhaustive SQL enumeration vs. cubic matrix cost (`sql_exhaustive_orbit_size_exponential_vs_polynomial`)**:
   Full spinful Fock space dimension `4^L` strictly exceeds `L^3` for `L ∈ {3, 4, 5, 6}`,
   separating finite SQL orbit enumeration (`O(4^L)`) from polynomial-in-`L` linear algebra.
2. **Meron orbit cancellation and survivor sign restoration (`meron_orbit_cancellation_preserves_partition_and_observable`)**:
   Cancelling a zero-sum meron pair `(+w_m, -w_m)` preserves the signed partition sum
   `Z = w1 + w2` while reducing `Z_abs` from `w1 + w2 + 2 * w_m` to `w1 + w2`, raising
   the average sign from `(w1 + w2) / (w1 + w2 + 2 * w_m) < 1` to `1`.
3. **Scope Fence 1 — Nonnegative weights do not bound observable variance (`nonnegative_weights_do_not_bound_observable_variance_fence`)**:
   In a strictly positive probability distribution `(p, 1 - p)` (`0 < p < 1`), an
   observable taking value `1 / p` on state 1 and `0` on state 2 has unit mean `1`
   but variance `1 / p - 1`, which grows without bound as `p` decreases (`0 < p1 < p2 < 1 → 1/p2 - 1 < 1/p1 - 1`).
4. **Scope Fence 2 — Nonnegative weights do not imply rapid mixing (`bimodal_energy_barrier_conductance_bottleneck_fence`)**:
   For two positive-weight wells `W_well > 0` separated by a positive barrier weight
   `0 < b1 < b2`, the inverse-conductance mixing lower bound `W_well / (2 * b)` grows
   strictly as the barrier weight decreases (`W_well / (2 * b2) < W_well / (2 * b1)`).
5. **DQMC per-update vs. stabilization sweep cost (`determinant_weight_evaluation_and_update_cost_accounting`)**:
   For spatial site count `Ns ≥ 2` and positive cost factor `c > 0`, rank-1 update cost
   `c * Ns^2` is strictly less than full QR/SVD stabilization cost `c * Ns^3`.
6. **Sign-reweighted sample complexity amplification (`sign_reweighted_sample_complexity_amplification`)**:
   For average signs `0 < s1 < s2 ≤ 1` and target error `eps > 0`, the required sample
   scale `1 / (s^2 * eps^2)` satisfies `1 / (s2^2 * eps^2) < 1 / (s1^2 * eps^2)`.
7. **RREF canonical section is not an L1 minimizer (`rref_canonical_section_not_l1_minimizer_witness`)**:
   For `d0 = (1, 1, 1)` and `c = (0, 1, 1)`, the RREF pivot-zero canonical representative
   is `c = (0, 1, 1)` with L1 norm `|0| + |1| + |1| = 2`, whereas `c - d0 = (-1, 0, 0)`
   lies in the same `im(d0)` coset with strictly smaller L1 norm `|-1| + |0| + |0| = 1 < 2`.
8. **Scope Fence 3 — Configuration-graph size blowup (`exponential_configuration_graph_sign_switching_cost_fence`)**:
   The half-filled configuration vertex count `Nat.choose (2 * m) m` grows rapidly
   (`choose 2 1 = 2 < choose 4 2 = 6 < choose 6 3 = 20 < choose 8 4 = 70`), so polynomial
   time in configuration-graph size is exponential in lattice site count `2 * m`.
9. **Scope Fence 4 — Protected Hubbard boundary (`bipartite_hubbard_protection_broken_by_doping_or_frustration_fence`)**:
   Equal spin determinants `det_up = det_dn` give `det_up * det_dn ≥ 0`, whereas
   asymmetric doped/frustrated determinants `det_up = 2, det_dn = -1` give `2 * (-1) = -2 < 0`.
10. **Scope Fence 5 — Four-tier epistemic separation (`four_tier_fsp_epistemic_separation_obligations`)**:
    Exhibits a concrete capability packet where `exactFiniteIdentity = true` and
    `nonnegativeProtectedWeights = true` while `polynomialMixingAndVarianceBound = false`
    and `unrestrictedFspSolution = false`, keeping `FSP-EFFICIENT-SAMPLING-OBLIGATIONS` `OPEN`.
-/

namespace CampaignFspEfficientSamplingObligations

/-- L1 norm of a 3-component integer cochain `(a, b, c)`. -/
def cochainL1Norm3 (a b c : ℤ) : ℤ :=
  |a| + |b| + |c|

/-- Four-tier epistemic capability record for a fermion sign representation (`TFQ-0409`). -/
structure SamplingObligationPacket where
  exactFiniteIdentity : Bool
  nonnegativeProtectedWeights : Bool
  polynomialMixingAndVarianceBound : Bool
  unrestrictedFspSolution : Bool
  deriving DecidableEq, Repr

/-- Theorem 1: Full spinful Hubbard Fock space dimension `4^L` strictly exceeds `L^3`
    for `L ∈ {3, 4, 5, 6}`, separating exhaustive SQL enumeration from cubic linear algebra. -/
theorem sql_exhaustive_orbit_size_exponential_vs_polynomial :
    (3 : ℕ) ^ 3 < 4 ^ 3 ∧
    (4 : ℕ) ^ 3 < 4 ^ 4 ∧
    (5 : ℕ) ^ 3 < 4 ^ 5 ∧
    (6 : ℕ) ^ 3 < 4 ^ 6 ∧
    (4 : ℕ) ^ 6 = 4096 := by
  decide

/-- Theorem 2: Cancelling a zero-sum meron pair `(+w_m, -w_m)` (`w_m > 0`) preserves
    the signed partition sum `w1 + w2` while strictly reducing the absolute partition sum
    from `w1 + w2 + 2 * w_m` to `w1 + w2`, raising the average sign from `< 1` to `1`. -/
theorem meron_orbit_cancellation_preserves_partition_and_observable
    (w1 w2 wm : ℚ) (hw1 : 0 < w1) (hw2 : 0 < w2) (hwm : 0 < wm) :
    (w1 + w2 + wm - wm = w1 + w2) ∧
    (w1 + w2 < w1 + w2 + 2 * wm) ∧
    ((w1 + w2) / (w1 + w2 + 2 * wm) < 1) ∧
    ((w1 + w2) / (w1 + w2) = 1) := by
  have h_sum_pos : 0 < w1 + w2 := by linarith
  have h_abs_pos : 0 < w1 + w2 + 2 * wm := by linarith
  refine ⟨by ring, by linarith, ?_, div_self (ne_of_gt h_sum_pos)⟩
  rw [div_lt_iff₀ h_abs_pos]
  linarith

/-- Theorem 3 (Scope Fence 1): Even when all configuration probabilities `p` and `1 - p`
    are strictly positive (`0 < p1 < p2 < 1`), an observable with value `1 / p` on state 1
    and `0` on state 2 has mean `1` and variance `1 / p - 1`, which strictly increases as
    `p` decreases (`1 / p2 - 1 < 1 / p1 - 1`). -/
theorem nonnegative_weights_do_not_bound_observable_variance_fence
    (p1 p2 : ℚ) (hp1 : 0 < p1) (hp12 : p1 < p2) (hp2 : p2 < 1) :
    p1 * (1 / p1) + (1 - p1) * 0 = 1 ∧
    0 < 1 / p2 - 1 ∧
    1 / p2 - 1 < 1 / p1 - 1 := by
  have hp2_pos : 0 < p2 := lt_trans hp1 hp12
  refine ⟨?_, ?_, ?_⟩
  · have hp1_ne : p1 ≠ 0 := ne_of_gt hp1
    calc
      p1 * (1 / p1) + (1 - p1) * 0 = p1 / p1 := by ring
      _ = 1 := div_self hp1_ne
  · have h_gt : 1 < 1 / p2 := (one_lt_div hp2_pos).mpr hp2
    linarith
  · have h_lt : 1 / p2 < 1 / p1 := div_lt_div_of_pos_left one_pos hp1 hp12
    linarith

/-- Theorem 4 (Scope Fence 2): Even when all configuration weights are positive, two wells
    of weight `W_well > 0` separated by a barrier of weight `0 < b1 < b2` have inverse-conductance
    mixing lower bound `W_well / (2 * b)` that grows strictly as the barrier weight decreases:
    `W_well / (2 * b2) < W_well / (2 * b1)`. -/
theorem bimodal_energy_barrier_conductance_bottleneck_fence
    (W_well b1 b2 : ℚ) (hW : 0 < W_well) (hb1 : 0 < b1) (hb12 : b1 < b2) :
    0 < W_well / (2 * b2) ∧
    W_well / (2 * b2) < W_well / (2 * b1) := by
  have hb2 : 0 < b2 := lt_trans hb1 hb12
  have h2b1 : 0 < 2 * b1 := by linarith
  have h2b2 : 0 < 2 * b2 := by linarith
  have h2b_lt : 2 * b1 < 2 * b2 := by linarith
  exact ⟨div_pos hW h2b2, div_lt_div_of_pos_left hW h2b1 h2b_lt⟩

/-- Theorem 5: In Determinant Quantum Monte Carlo on `Ns ≥ 2` spatial sites with cost
    coefficient `c > 0`, rank-1 update cost `c * Ns^2` is strictly smaller than full
    QR/SVD numerical stabilization cost `c * Ns^3`. -/
theorem determinant_weight_evaluation_and_update_cost_accounting
    (c Ns : ℕ) (hc : 0 < c) (hNs : 2 ≤ Ns) :
    c * (Ns ^ 2) < c * (Ns ^ 3) := by
  have h_pow : Ns ^ 2 < Ns ^ 3 := by nlinarith
  exact Nat.mul_lt_mul_of_pos_left h_pow hc

/-- Theorem 6: For average signs `0 < s1 < s2 ≤ 1` and target accuracy `eps > 0`,
    the sign-reweighted sample complexity scale `1 / (s^2 * eps^2)` is strictly larger
    at smaller average sign: `1 / (s2^2 * eps^2) < 1 / (s1^2 * eps^2)`. -/
theorem sign_reweighted_sample_complexity_amplification
    (s1 s2 eps : ℚ) (hs1 : 0 < s1) (hs12 : s1 < s2) (heps : 0 < eps) :
    1 / (s2 ^ 2 * eps ^ 2) < 1 / (s1 ^ 2 * eps ^ 2) := by
  have h_s_sq : s1 ^ 2 < s2 ^ 2 := by nlinarith
  have h_eps_sq : 0 < eps ^ 2 := by positivity
  have h_d1 : 0 < s1 ^ 2 * eps ^ 2 := by positivity
  have h_denom_lt : s1 ^ 2 * eps ^ 2 < s2 ^ 2 * eps ^ 2 :=
    mul_lt_mul_of_pos_right h_s_sq h_eps_sq
  exact div_lt_div_of_pos_left one_pos h_d1 h_denom_lt

/-- Theorem 7: Matching `BQNFSignEvaluator.normalize_cochain` vs `solve_quotient_distance`:
    for `d0 = (1, 1, 1)` and `c = (0, 1, 1)`, the RREF pivot-zero representative `c` has
    `cochainL1Norm3 0 1 1 = 2`, whereas the gauge-equivalent cochain `c - d0 = (-1, 0, 0)`
    has strictly smaller L1 norm `cochainL1Norm3 (-1) 0 0 = 1 < 2`. -/
theorem rref_canonical_section_not_l1_minimizer_witness :
    (0 - 1 = -1 ∧ 1 - 1 = 0 ∧ 1 - 1 = 0) ∧
    cochainL1Norm3 0 1 1 = 2 ∧
    cochainL1Norm3 (-1) 0 0 = 1 ∧
    cochainL1Norm3 (-1) 0 0 < cochainL1Norm3 0 1 1 := by
  decide

/-- Theorem 8 (Scope Fence 3): The half-filled configuration vertex count `Nat.choose (2 * m) m`
    grows strictly from `2` to `6`, `20`, and `70` for `m = 1, 2, 3, 4`, showing that
    polynomial time in configuration-graph size is not polynomial in site count `2 * m`. -/
theorem exponential_configuration_graph_sign_switching_cost_fence :
    Nat.choose 2 1 = 2 ∧
    Nat.choose 4 2 = 6 ∧
    Nat.choose 6 3 = 20 ∧
    Nat.choose 8 4 = 70 ∧
    Nat.choose 2 1 < Nat.choose 4 2 ∧
    Nat.choose 4 2 < Nat.choose 6 3 ∧
    Nat.choose 6 3 < Nat.choose 8 4 := by
  decide

/-- Theorem 9 (Scope Fence 4): When spin-up and spin-down determinants match (`det_up = det_dn`),
    the 2-spin determinant product is non-negative (`det_up * det_up ≥ 0`), whereas for doped
    or frustrated determinants `det_up = 2` and `det_dn = -1`, the product `2 * (-1) = -2 < 0`
    is negative. -/
theorem bipartite_hubbard_protection_broken_by_doping_or_frustration_fence (det_up : ℚ) :
    0 ≤ det_up * det_up ∧
    ((2 : ℚ) * (-1 : ℚ) = -2) ∧
    ((2 : ℚ) * (-1 : ℚ) < 0) := by
  refine ⟨mul_self_nonneg det_up, by norm_num, by norm_num⟩

/-- Theorem 10 (Scope Fence 5): The local FSP package capability packet satisfies
    `exactFiniteIdentity = true` and `nonnegativeProtectedWeights = true` while leaving
    `polynomialMixingAndVarianceBound = false` and `unrestrictedFspSolution = false`. -/
theorem four_tier_fsp_epistemic_separation_obligations :
    let pkg : SamplingObligationPacket := {
      exactFiniteIdentity := true
      nonnegativeProtectedWeights := true
      polynomialMixingAndVarianceBound := false
      unrestrictedFspSolution := false
    }
    pkg.exactFiniteIdentity = true ∧
    pkg.nonnegativeProtectedWeights = true ∧
    pkg.polynomialMixingAndVarianceBound = false ∧
    pkg.unrestrictedFspSolution = false := by
  decide

end CampaignFspEfficientSamplingObligations
