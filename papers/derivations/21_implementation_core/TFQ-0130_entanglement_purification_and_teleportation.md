# [TFQ-0130] Entanglement, purification, and teleportation

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `5a4935ea-8d39-569d-ad3f-f2766bc6ce42`  
> **Parent Derivation**: [TFQ-0129](TFQ-0129_exact_rays_and_pure_states.md)

---

## 1. Abstract & Formal Statement

Covers entanglement.rs, purification.rs, bipartite_operator.rs, relative_state_branching.rs, no_cloning.rs, and teleportation.rs. entanglement.rs decides Schmidt rank of a pure bipartite state exactly over Q(i), and it says a diagonal population entropy is not an entanglement measure for a general state. The other files lift a mixed state, give exact bipartite operators, expand relative states, evaluate the Wootters-Zurek obstruction, and lay out qubit teleportation. A Python replay and a Lean 4 declaration would still have to match the exact Schmidt-rank decision.

### Governing Obligation
Match exact Schmidt rank over Q(i), the warning on diagonal population entropy, and the three-qubit teleportation layout.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/bipartite_operator.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/entanglement.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/no_cloning.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/purification.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/relative_state_branching.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/teleportation.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/higher_dim_entanglement.py`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/quantum_protocols.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
