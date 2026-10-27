# [TFQ-0304] Lift capacity is not a dynamics derivation

> **Stage**: `L1_TO_L2` | **Status**: `SOURCE_RECORD`  
> **UUID**: `9765edbb-7887-51c5-a96f-e90bfa3f2eca`  
> **Parent Derivation**: [TFQ-0303](tfq_0303_linear_isometric_dynamics_are_an_import.md)

---

## 1. Abstract & Formal Statement

The section labeled Theorem 7 in qm_020_born_normalization_and_conditional_hilbert_lift.md says the Hilbert lift is redundant for sector probabilities and still able to host phase-sensitive dynamics. The finite obligation is that capacity remark: redundancy of the probability reading does not by itself delete interference or reversible linear updates from the representation. The paper says the capacity comes from the imported complex linear representation and unitary dynamics, and that it does not alter direct normalization.

### Governing Obligation
Keep probability redundancy separate from any claim that lifted dynamics have been selected.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `complex Hilbert space: assumption`
- **Admitted**: `linear isometric dynamics: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> No Lean located. The interference non-descent boundary is in the QM_122 nodes.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornRedundancy.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_thm7_and_qm121_ladder_rungs_2_to_6_separation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm020_thm7_representation_capacity`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:be048d5e98615cff70b3cdc1ebaa78a56395d67d55ca655cbb41494e307cde65`](../../code/rust/src/)
- [`external:sha256:d58eb2c1f4ae2ac65cc7145554cd2a5c955e096776c1f6d9daafb2065b14450e`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_l1_to_l2_bridges_and_ladder_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0305](tfq_0305_sector_weights_do_not_force_the_quadratic_form.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `external:sha256:ddbf8bad986fa5587b534c0f96f2c4ff370f95cb696c6245df0526d4bad32351`
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
  - `external:sha256:aa96a8bb76ae8bc4e83571f57783f369b645332421db0e1fdd8a7d9cf333aac9`
  - `external:sha256:eb788c5f48e4cc2ea2d3abdd7c4c0aaebe0b2b2edd084d6daf463e27df848c8b`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-QM020-THM7-REPRESENTATION-CAPACITY`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-QM020-THM7-REPRESENTATION-CAPACITY` (`L1_TO_L2` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-L1_TO_L2-L1-QM020-THM7-REPRESENTATION-CAPACITY`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [870, -1740, 1305]`, `chord_potential = 1305`, `holonomy_gamma2 = 1740`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-QM020-THM7-REPRESENTATION-CAPACITY): 4*idx(87) + 3*stage_rank(6) + route_degree(3) == 369` ($\text{value} = 369$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-QM020-THM7-REPRESENTATION-CAPACITY): R_raw(204) - G_cob(99) - S_decoy(6) == 99 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 99$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_thm7_and_qm121_ladder_rungs_2_to_6_separation`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = f5a2a2f391ad80e775183a1bc04c607b8a65a477d0367a0b867cf01109cfd9e4`
