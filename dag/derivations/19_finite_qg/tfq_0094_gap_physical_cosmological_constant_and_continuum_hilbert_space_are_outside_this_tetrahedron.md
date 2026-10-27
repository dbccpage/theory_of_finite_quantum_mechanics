# [TFQ-0094] GAP: physical cosmological constant and continuum Hilbert space are outside this tetrahedron

> **Stage**: `FINITE_QG` | **Status**: `FINITE_GEOMETRY`  
> **UUID**: `59644faa-1e57-5d92-b882-da76760bb6f2`  
> **Parent Derivation**: [TFQ-0093](tfq_0093_imported_area_scale_and_casimir_stay_unpaid_the_einstein_equation_and_smooth.md)

---

## 1. Abstract & Formal Statement

loop_quantum_gravity.rs evaluates exact rational flux closure and squared volume for one oriented tetrahedron given rational vertex coordinates, and it refuses a degenerate volume. The module fence says this finite geometric face does not construct a continuum Hilbert space. What is finite is one tetrahedron and its Gram determinant over the rationals. What is not discharged is a spin-network space, a physical cosmological constant, dynamics, and the continuum limit. Four points are not quantum gravity and do not discharge the Einstein equation.

### Governing Obligation
GAP: physical cosmological constant and continuum Hilbert space are outside this tetrahedron certificate.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Hamiltonian constraint / Einstein equation (assumption)`
- **Admitted**: `SU(2) gauge group (assumption)`
- **Admitted**: `continuum manifold, metric, connection (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean names not checked by me; dynamics Q-held.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
*Formalization active. Proof obligations tracked under zero-sorry regime.*

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/general_relativity/loop_quantum_gravity.rs`](../../code/rust/src/)
- [`code/rust/src/wdp/lib.rs`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0095](tfq_0095_qm_111_c3_does_not_discharge_nabla_g_equals_zero_qm_111_c7_imports_the_continuum.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
