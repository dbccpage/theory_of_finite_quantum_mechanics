# [TFQ-0315] Exact density, ray, and population shadow

> **Stage**: `FINITE_HILBERT` | **Status**: `SOURCE_RECORD`  
> **UUID**: `8d7a2934-8da6-5f6c-928a-c9d458c40a40`  
> **Parent Derivation**: [TFQ-0314](tfq_0314_cochain_lift_still_prices_the_born_law_as_an_import.md)

---

## 1. Abstract & Formal Statement

density_matrix.rs accepts an exact density over Gaussian rationals only when it is Hermitian, positive semidefinite by an exact test, and of trace one, and it separates that operator from the population shadow of its diagonal. The finite obligation is that split. The shadow of a pure projector and the shadow of a classical mixture can agree while the coherences differ, and the module says those coherences are reported rather than dropped. quantum_state.rs keeps unnormalized rays and applies a declared squared-modulus rule for computational-basis weights.

### Governing Obligation
Validate exact finite densities separately from their classical population shadows.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`external:sha256:b9218b94925f1a0b29dd010fe92d0351a6dba3190f5884676143cad625c44950`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:a9858061f68a9165aeb743a82864df532a5026453c94ca6eed5b5a7b4a704499`](../../code/rust/src/)
- [`external:sha256:904a09d9ca4b18f97838457416046361842e537e895afce0374f8b6c670a1ef1`](../../code/rust/src/)
- [`external:sha256:d58eb2c1f4ae2ac65cc7145554cd2a5c955e096776c1f6d9daafb2065b14450e`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`external:sha256:a2fd773252896051c9094d2d97692ddce4a9bd1a4cfe95f7e562909e5645b203`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0316](tfq_0316_package_chapter_states_a_conditional_lift.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`, `F003`
- **Primary Source Paths**:
  - `external:sha256:ddbf8bad986fa5587b534c0f96f2c4ff370f95cb696c6245df0526d4bad32351`
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
  - `external:sha256:aa96a8bb76ae8bc4e83571f57783f369b645332421db0e1fdd8a7d9cf333aac9`
  - `external:sha256:6d05310cee22614dcc62f1aa7f05a62186726cfb8fb84bbeae794d914805dc33`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1650, -3300, 2475]`, `chord_potential = 2475`, `holonomy_gamma2 = 3300`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO): 4*idx(165) + 3*stage_rank(8) + route_degree(4) == 688` ($\text{value} = 688$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO): R_raw(370) - G_cob(181) - S_decoy(8) == 181 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 181$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = fc38fab549fd80bc5007cbd459114755a0c90b7d36be7ae5fe20e79413026c70`
