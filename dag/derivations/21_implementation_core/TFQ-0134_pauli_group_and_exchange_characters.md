# [TFQ-0134] Pauli group and exchange characters

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `a891052f-5b77-5cd7-a56c-312d92953ecc`  
> **Parent Derivation**: [TFQ-0133](TFQ-0133_observables_and_local_star_algebras.md)

---

## 1. Abstract & Formal Statement

Covers pauli.rs, pauli_context_table.rs, qubit_bloch_map.rs, parity_context_packet.rs, pauli_spin_statistics_graph.rs, and pair_exchange_characters.rs. pauli.rs states Pauli letters, phased n-qubit strings, the symplectic commutation form, and exact Q(i) matrices checked against products. The other files hold a 3 by 3 sign table, the affine Bloch map of a qubit Kraus map, F2 parity packets, graph spin-statistics, and scalar exchange characters. A Python replay and a Lean 4 declaration would still have to match the symplectic commutation rule.

### Governing Obligation
Match Pauli letter products, the symplectic commutation form, and the exact Q(i) matrices.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/pair_exchange_characters.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/parity_context_packet.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/pauli.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/pauli_context_table.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/pauli_spin_statistics_graph.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/qubit_bloch_map.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/context_parity_control.py`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/pauli_spin_statistics_graph_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0135](TFQ-0135_parity_contextuality_and_frame_functions.md)
- [TFQ-0136](TFQ-0136_finite_chsh_boxes.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
