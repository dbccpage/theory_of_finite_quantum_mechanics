# [TFQ-0128] Declared U(1) connections

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `effc738e-d5e6-5d28-8319-7a96a0979ffd`  
> **Parent Derivation**: [TFQ-0127](TFQ-0127_hilbert_carriers_and_tensor_index.md)

---

## 1. Abstract & Formal Statement

Covers u1_graph_connection.rs, u1_gauge_triviality.rs, quaternion_gauge_shadow.rs, transport_isometry_orbits.rs, and spin_structure_obstruction.rs. u1_graph_connection.rs assigns a declared unit Gaussian-rational edge scalar and computes covariant difference, vertex gauge, and closed-walk holonomy. It states that this is not a Schrodinger equation. The other files decide pure gauge, test T-adjoint G T = G, and ask for a spin lift on a finite 2-complex. A Python replay and a Lean 4 declaration would still have to match those declared transport identities.

### Governing Obligation
Match declared U(1) covariant difference, gauge action, closed-walk holonomy, and the pure-gauge decision.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/quaternion_gauge_shadow.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/spin_structure_obstruction.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/transport_isometry_orbits.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/u1_gauge_triviality.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/u1_graph_connection.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/holonomy_bridge_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
