# [TFQ-0270] Syndrome distance and repair capacity

> **Stage**: `FINITE_QM_INFORMATION` | **Status**: `SOURCE_RECORD`  
> **UUID**: `7ebb99df-8e6f-5605-9a4a-54861e236f3a`  
> **Parent Derivation**: [TFQ-0269](tfq_0269_threshold_theorems_read_as_repair_capacity_certificates.md)

---

## 1. Abstract & Formal Statement

QM_102 obliges cochain repair capacity on declared stabilizer packets. The derivation node DS-QM102-SYNDROME-CAPACITY-BOUND describes a syndrome as a coboundary defect and names the correctable weight by the usual floor expression in the distance. The node says the recorded argument supports the lower-bound direction, and that a matching upper-bound reading would be a different statement. Local vanishing of a syndrome does not by itself prevent a logical operator. The finite obligation is that lower-bound capacity statement on a declared code.

### Governing Obligation
Bound declared-code repair by the distance formula in the lower-bound direction, and do not convert a zero syndrome into logical protection.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `code distance d and error model (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Bound-direction caveat.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid`](../../code/lean4/)
- [`sources/atlas/papers/finite_quantum_mechanics/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:46de73c5a40726d0b5c25e6c7d2b90c639931cf1a5b130a6c5b422878b08bab1::repair_capacity`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`sources/atlas/papers/finite_quantum_mechanics/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0271](tfq_0271_show_the_packet_protocol_for_a_finite_computation.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM102-SYNDROME-CAPACITY-BOUND`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM102-SYNDROME-CAPACITY-BOUND` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM102-SYNDROME-CAPACITY-BOUND`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1680, -3360, 2520]`, `chord_potential = 2520`, `holonomy_gamma2 = 3360`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM102-SYNDROME-CAPACITY-BOUND): 4*idx(168) + 3*stage_rank(8) + route_degree(2) == 698` ($\text{value} = 698$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM102-SYNDROME-CAPACITY-BOUND): R_raw(376) - G_cob(184) - S_decoy(8) == 184 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 184$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = c1883d04d527bb7608a2160e652b6ca3a9679dad83298dd8c74acde1145587af`
