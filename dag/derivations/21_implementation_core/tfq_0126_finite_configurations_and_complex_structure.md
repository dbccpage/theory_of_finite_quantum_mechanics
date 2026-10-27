# [TFQ-0126] Finite configurations and complex structure

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `f9f2c565-a29a-56de-a764-1112cabe206a`  
> **Parent Derivation**: [TFQ-0125](tfq_0125_crate_index_and_derivation_witnesses.md)

---

## 1. Abstract & Formal Statement

Covers finite_geometry.rs, complex_realification.rs, complex_structure_selector.rs, tower.rs, and embedding_relativity.rs. finite_geometry.rs states exact QM_122 configurations whose enumerations keep explicit finite bounds. The other files realize a declared Q(i) complex structure, the finite U(1)-selector checks, the cyclotomic tower with Q(zeta_6)=Q(zeta_3), and positivity relative to a declared real embedding. A Python replay and a Lean 4 declaration would still have to match those bounded configurations and the embedding-dependent sign.

### Governing Obligation
Match bounded QM_122 configurations, the Q(i) complex-structure realization, the cyclotomic tower criterion, and embedding-dependent positivity.

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
- [`code/rust/src/combinatorics/finite_geometry.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:1ae9121daca3f6d1f5cb700a325bc1aaa0d5a6988db99eee907e24ca729e876e`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:ddaee3d0d77722244a6451750ca1e5acf7a57b4f02e75ecec70e810976d57d9e`](../../code/rust/src/)
- [`code/rust/src/qm/campaigns/tower.rs`](../../code/rust/src/)
- [`code/rust/src/qm/campaigns/embedding_relativity.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: The python twin is not located for finite_geometry.rs under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0127](tfq_0127_hilbert_carriers_and_tensor_index.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
