# [TFQ-0051] Keep the spin lift on declared flat complexes and off the Dirac

> **Stage**: `FINITE_TOPOLOGICAL` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `40f881b9-2e7f-583a-a395-3da4bbcdb36b`  
> **Parent Derivation**: [TFQ-0050](TFQ-0050_either_add_an_exact_su_3_fusion_file_or_leave_that_obligation_open.md)

---

## 1. Abstract & Formal Statement

spin_structure_obstruction.rs lifts a flat rational rotation transport on a declared finite 2-complex to SU(2) matrices, using omega_lie_theory::su2_matrix::matrix_spin_lift. A face is marked obstructed when the lifted holonomy is -I rather than I. Flat lifts are the sign patterns whose traversal parities match those obstruction bits, which the file describes as the cellular form of a vanishing second Stiefel-Whitney class on that declared complex only. This is a spin-structure control. It is not the lattice Dirac kernel, not a color fermion measure, and not a QCD composite.

### Governing Obligation
Keep the spin lift on declared flat complexes and off the Dirac and color controls.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: the Stiefel-Whitney sign search is not a FiniteQM theorem`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_lie_theory/src/su2.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/spin_structure_obstruction.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: spin-structure obstruction has no finite_qm use case`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
