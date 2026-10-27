# [TFQ-0241] Projection postulate and Born pairing remain imported

> **Stage**: `FINITE_QM_DYNAMICS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `1f19289b-e4b8-52dc-89ee-c2f77bf93b64`  
> **Parent Derivation**: [TFQ-0239](tfq_0239_finite_path_sum_on_a_unique_intermediate_cut.md)

---

## 1. Abstract & Formal Statement

QM_030's ledger, as extracted in DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT, separates a finite descent reading of measurement from the projection postulate. Spectral projectors with E squared equal to E, and the observer pairing that turns weights into probabilities, are imported. The same node says an audit of several pairings does not select one Born rule. That matches Finite Quantum Mechanics section 1.1, rung 3, where positive states, effects, and a pairing are additional supplied structure, and the Born rule is not derived from difference.

### Governing Obligation
Do not read the finite path sum as having selected the projection postulate or a unique Born pairing.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `probability pairing and normalization (assumption)`
- **Admitted**: `projection postulate / spectral structure (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Overlaps L1_TO_L2 Born nodes (QM_020, other fragment).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/GleasonTheorem.lean::d2_binary_non_bornian_obstruction`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::born_pairing_boundary`](../../code/lean4/)
- [`sources/atlas/papers/finite_quantum_mechanics/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT` (`FINITE_QM_STRUCTURE` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-DS-PROJECTION-POSTULATE-BOUNDARY`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [170, -340, 255]`, `chord_potential = 255`, `holonomy_gamma2 = 340`
- **Finite Shadow Exact Witness (`M4`)**: `idempotent_repeat_stability: E(E(v)) == E(v) with trace 1 + 0 == 1` ($\text{value} = 1$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `sequential_order_sensitivity_defect: |(P_z P_x - P_x P_z)|_entry_sq == 4 (order sensitivity requires non-commuting projector algebra)` ($\text{value} = 4$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 2c867b3d2d5a91a4dc5e8116fad497573f2f6864492728764f1585f9d9216c7e`
