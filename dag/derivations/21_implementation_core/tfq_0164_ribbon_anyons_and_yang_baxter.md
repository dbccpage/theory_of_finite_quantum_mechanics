# [TFQ-0164] Ribbon anyons and Yang-Baxter

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `54822c37-9195-5ec5-bf3a-6daf3751faaf`  
> **Parent Derivation**: [TFQ-0127](tfq_0127_hilbert_carriers_and_tensor_index.md)

---

## 1. Abstract & Formal Statement

Covers anyon_model.rs, anyon.rs, r_matrix.rs, yang_baxter_equation.rs, modular_tensor_category.rs, and topological_quantum_computing.rs. anyon_model.rs runs fusion and braiding on a multiplicity-free ribbon category inside an explicit pentagon and hexagon bound. The other files read simple charges, retain a Yang-Baxter residual, and say a finite closure bound does not establish density of a braid image. A Python replay and a Lean 4 declaration would still have to match the bounded replay and the retained residual.

### Governing Obligation
Match bounded ribbon fusion replay and retention of the Yang-Baxter residual matrix.

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
- [`absent: no local rust twin located for external:sha256:1b998e845c6cb87aacd3c80aea6dfeab4c89757dc8ae040a1e2ab8ef9fd87046`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:fc304d9ddd8e307e14c12aaab1d0538770b28760252cd7c07c933f3da0c78a27`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:3e7e56da3775a6e3d7e50ae1b02d5919f0e67701a37dd1af30f97919bd77a8d6`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:81cef7530a42b0fd9c77ebad734ec9001b102541d55b056c07911c1b8934d0c5`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:c5a468580a14418873219a21a9092c722a0eb690cc7178bebb7bbcf73bfa0dd4`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:2e8dae27ae2eb20bd4b748b6d4d44838b0b94b0f0ca60692ad0b01b8e0942b20`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: The python twin is not located for anyon_model.rs under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
