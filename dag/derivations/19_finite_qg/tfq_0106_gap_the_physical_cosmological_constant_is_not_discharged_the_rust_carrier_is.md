# [TFQ-0106] GAP: the physical cosmological constant is not discharged. The Rust carrier is

> **Stage**: `FINITE_QG` | **Status**: `GAP`  
> **UUID**: `37e6c1a1-38a5-56fc-829b-b07e176cf4a3`  
> **Parent Derivation**: [TFQ-0105](tfq_0105_gap_no_continuum_limit_and_no_physical_cosmological_constant_are_discharged_by.md)

---

## 1. Abstract & Formal Statement

derive_cosmological_constant_residual builds a float mean of hinge terms that mix a deficit angle with a sine and a supplied Immirzi number, then divides by a cell-volume parameter. The function's Track B note says a continuum magnitude near the quoted dark-energy scale still needs an external lattice-volume calibration. What is finite is that floating residual on a default valency list. What is not discharged is the physical cosmological constant, which stays GAP, and the Einstein equation. A few hinges are not a measured Lambda and not quantum gravity.

Narrowed in Lean 4 (`lean4/CampaignTfq0106FiniteQg.lean`) and an independent Python verifier (`checks/independent/tfq-0106.py`) to three exact rational algebraic components and scope fences over $\mathbb{Q}$:
1. **Exact Rational Replay of `CosmologicalCoupling` (`code/rust/src/general_relativity/cosmological_constant.rs`)**: replays `effective_scalar_curvature(lambda, kappa) = 2 * lambda * kappa` and `evaluate_action(lambda, kappa, K, V) = K / (2 * kappa) - lambda * V`, verifying the Rust unit test `(lambda, kappa, K, V) = (1/10, 1/2, 10, 20) -> (1/10, 8)` (`rust_cosmological_action_unit_test_replay`), the zero-action iff $K = (2\lambda\kappa)V$ (`cosmological_action_zero_iff_curvature_balance`), and scaling/invariance identities (`cosmological_action_scaling_and_invariance`).
2. **External Cell-Volume Calibration Underdetermination Fence ($V_{\text{cell}}$)**: formalizes the Track B quotient $\Lambda_{\text{res}}(H, V_{\text{cell}}) = H / V_{\text{cell}}$, its $s^{-4}$ scaling under 4D length rescaling $a \mapsto s \cdot a$ (`cell_volume_4d_length_rescaling`), bijective calibration to any nonzero target $\Lambda_{\text{target}} \neq 0$ via $V_{\text{cell}} = H / \Lambda_{\text{target}}$ (`any_target_lambda_achievable_by_cell_volume_calibration`, `cell_volume_calibration_injective`), joint $(\gamma, V_{\text{cell}})$ scale degeneracy (`immirzi_and_cell_volume_scale_degeneracy`), and the exact rational spread across $V_{\text{cell}} \in \{1, 9/2, 9, 45\}$ on the default valency list $(3, 4, 5, 6)$ (`default_valency_scaffold_calibration_spread`).
3. **Scalar Hinge Mean vs. 4D Tensorial Einstein Equation Fence ($1$ Scalar vs. $10$ Components)**: verifies that a symmetric rank-2 tensor equation in $d = 4$ has $d(d+1)/2 = 10$ independent components ($9$ trace-free plus $1$ trace) (`four_dim_symmetric_tensor_component_counts`), and exhibits the anisotropic 4-component profile $(\Lambda + \delta, \Lambda - \delta, \Lambda, \Lambda)$ ($\delta \neq 0$) whose scalar mean residual vanishes while its squared componentwise Einstein residual is $2\delta^2 > 0$ (`anisotropic_curvature_vanishing_scalar_mean_fence`, `anisotropic_profile_violates_tensorial_einstein`, `diagonal_einstein_iff_sq_residual_zero`).

### Governing Obligation
GAP: the physical cosmological constant is not discharged. The Rust carrier is only a degree-and-label scaffold.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
- [`lean4/CampaignTfq0106FiniteQg.lean`](../../../lean4/CampaignTfq0106FiniteQg.lean):
  - `CampaignTfq0106FiniteQg.rust_cosmological_action_unit_test_replay`
  - `CampaignTfq0106FiniteQg.cosmological_action_zero_iff_curvature_balance`
  - `CampaignTfq0106FiniteQg.cosmological_action_scaling_and_invariance`
  - `CampaignTfq0106FiniteQg.cell_volume_4d_length_rescaling`
  - `CampaignTfq0106FiniteQg.any_target_lambda_achievable_by_cell_volume_calibration`
  - `CampaignTfq0106FiniteQg.cell_volume_calibration_injective`
  - `CampaignTfq0106FiniteQg.immirzi_and_cell_volume_scale_degeneracy`
  - `CampaignTfq0106FiniteQg.default_valency_scaffold_calibration_spread`
  - `CampaignTfq0106FiniteQg.four_dim_symmetric_tensor_component_counts`
  - `CampaignTfq0106FiniteQg.anisotropic_curvature_vanishing_scalar_mean_fence`
  - `CampaignTfq0106FiniteQg.anisotropic_profile_violates_tensorial_einstein`
  - `CampaignTfq0106FiniteQg.diagonal_einstein_iff_sq_residual_zero`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/general_relativity/cosmological_constant.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`checks/independent/tfq-0106.py`](../../../checks/independent/tfq-0106.py) (`checks=843 rust_replay=602 calibration=165 tensor_fence=76 failures=0`)
- [`dag/derivations/independent/tfq-0106.md`](../independent/tfq-0106.md)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0107](tfq_0107_gap_einstein_equation_and_physical_cosmological_constant_stay_unpaid_deficit_is_not.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction`
