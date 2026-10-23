# [TFQ-0522] sn-e08-weighted-l1-duality

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `a8ebe4a6-bb20-5e89-af1f-5335d1c5dc93`  
> **Parent Derivation**: [TFQ-0516](tfq_0516_sn4_policy_closure_cycle_space.md)

---

## 1. Abstract & Formal Statement

Example E08 takes finite rational cochain spaces, d₀: C⁰ → C¹ and positive rational weights ω_e, and states that the minimum over g of Σ_e ω_e |c_e − (d₀g)_e| equals the maximum of cᵀy subject to d₀ᵀy = 0 and |y_e| ≤ ω_e, as finite linear-programming duality for the stated feasible bounded problem. Matching primal and dual feasible values certify optimality. An ℓ¹ minimizer need not be unique and is not in general the ℓ² harmonic residual. The page separately defines a categorical adjunction by functors, unit, counit and triangle identities, and says these maps are not the matrix pair d₀, d₀ᵀ.

### Governing Obligation
For a declared weighted ℓ¹ cochain problem, certify a value by a primal g and a dual y with d₀ᵀy = 0, |y_e| ≤ ω_e and equal objective values, and keep the categorical adjunction a separate construction.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> E08 is a declared mathematical construction that grammar cases do not verify; AdjunctionCochain implements only x ↦ (x,0) and first-coordinate projection, and no adjunction is claimed until objects, functors, naturality and triangle laws are supplied.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignSnE08WeightedL1Duality.lean::adjunctionCochain_not_cycD_transpose`](../../../lean4/CampaignSnE08WeightedL1Duality.lean)
- [`lean4/CampaignSnE08WeightedL1Duality.lean::certificate_optimal`](../../../lean4/CampaignSnE08WeightedL1Duality.lean)
- [`lean4/CampaignSnE08WeightedL1Duality.lean::cyc_harmonic`](../../../lean4/CampaignSnE08WeightedL1Duality.lean)
- [`lean4/CampaignSnE08WeightedL1Duality.lean::cyc_optimum`](../../../lean4/CampaignSnE08WeightedL1Duality.lean)
- [`lean4/CampaignSnE08WeightedL1Duality.lean::cyc_residuals_differ`](../../../lean4/CampaignSnE08WeightedL1Duality.lean)
- [`lean4/CampaignSnE08WeightedL1Duality.lean::e08_rational`](../../../lean4/CampaignSnE08WeightedL1Duality.lean)
- [`lean4/CampaignSnE08WeightedL1Duality.lean::farkas`](../../../lean4/CampaignSnE08WeightedL1Duality.lean)
- [`lean4/CampaignSnE08WeightedL1Duality.lean::lp_strong_duality`](../../../lean4/CampaignSnE08WeightedL1Duality.lean)
- [`lean4/CampaignSnE08WeightedL1Duality.lean::weighted_l1_strong_duality`](../../../lean4/CampaignSnE08WeightedL1Duality.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust LP solver in the S(n) strand; the page assigns evaluation to existing mathematics owners`

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-sn-e08-weighted-l1-duality.py::solve_dual`](../../../checks/independent/pgw-sn-e08-weighted-l1-duality.py)
- [`checks/independent/pgw-sn-e08-weighted-l1-duality.py::solve_primal`](../../../checks/independent/pgw-sn-e08-weighted-l1-duality.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0523](tfq_0523_sn_e12_circulation_functional.md)
- [TFQ-0524](tfq_0524_sn_e18_l1_ties_l2_center.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_education/documentation/002_oesn/levels/level_08_monadic_adjunction_cochains.md:19-29`
  - `omega_engine_education/documentation/002_oesn/levels/level_08_monadic_adjunction_cochains.md:40-44`
  - `omega_engine_education/documentation/002_oesn/levels/README.md:20`
  - `dag/derivations/independent/pgw-sn-e08-weighted-l1-duality.md:1-3`
