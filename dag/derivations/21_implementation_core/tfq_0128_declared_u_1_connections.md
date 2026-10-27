# [TFQ-0128] Declared U(1) connections

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `effc738e-d5e6-5d28-8319-7a96a0979ffd`  
> **Parent Derivation**: [TFQ-0127](tfq_0127_hilbert_carriers_and_tensor_index.md)

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
- [`absent: no local lean twin located for lean4/quantum_mechanics`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:c2b85e3d42e7b05c158b418cbf2a803bdc86262cde384177ac8264c9c67ef6fe`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:e86ad3309b090c78f09e92fa9833a87b325a0513396663cbf2bd5c2ea1fd0c7b`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:5cb64e2aaf7b93cf52ee87e8545c9f2b3de52d45c3e8339ca80abdafdb9cc505`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:756874830c8541053d5f4966f71c8e84d747232a4226034f3d3319e7c58f3ff6`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:c76c5bd187ff61baee99a622c5d512278ad22d2cb2f6e397642fc414a760c314`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/holonomy_bridge_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
