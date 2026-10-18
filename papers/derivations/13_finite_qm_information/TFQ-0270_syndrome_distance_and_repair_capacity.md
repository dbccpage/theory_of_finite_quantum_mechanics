# [TFQ-0270] Syndrome distance and repair capacity

> **Stage**: `FINITE_QM_INFORMATION` | **Status**: `SOURCE_RECORD`  
> **UUID**: `7ebb99df-8e6f-5605-9a4a-54861e236f3a`  
> **Parent Derivation**: [TFQ-0269](TFQ-0269_threshold_theorems_read_as_repair-capacity_certificates.md)

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
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_majorana/src/repair_capacity.rs::repair_capacity`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0271](TFQ-0271_show-the-packet_protocol_for_a_finite_computation.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
