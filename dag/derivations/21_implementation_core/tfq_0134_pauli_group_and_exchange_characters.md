# [TFQ-0134] Pauli group and exchange characters

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `a891052f-5b77-5cd7-a56c-312d92953ecc`  
> **Parent Derivation**: [TFQ-0133](tfq_0133_observables_and_local_star_algebras.md)

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
- [`absent: no local lean twin located for lean4/quantum_mechanics`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:03d8dc44e2b48847afa8f562a899ee5d758f3ce9335af82270b755f921164401`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:2dc61f13ffcd3d6fe5a06c808077b268d82ae90da2f1473c34b8e099d0caf01a`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:8fa90b765b7795fe5d95b29b3bc96fac6a904e37527b90130df716de4bc389df`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:84f635fc4390806ffa803c0278afb28439dc5449aff1ea756d948db611384a5f`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:7b92d189c034dc6bb19e748fa9689912254a5b0b9a50a1f25d2566b9a4d4744f`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:4935d5a66cc832a33b76053028b8f74c320534cc433c51a33c468491c9348a31`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/pauli_spin_statistics_graph_control.py`](../../code/python/)
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/context_parity_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0135](tfq_0135_parity_contextuality_and_frame_functions.md)
- [TFQ-0136](tfq_0136_finite_chsh_boxes.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
