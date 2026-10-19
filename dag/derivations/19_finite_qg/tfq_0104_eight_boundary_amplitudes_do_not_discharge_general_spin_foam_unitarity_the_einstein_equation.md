# [TFQ-0104] Eight-boundary amplitudes do not discharge general spin-foam unitarity, the Einstein equation,

> **Stage**: `FINITE_QG` | **Status**: `FINITE_MODEL`  
> **UUID**: `aed444d3-2cce-536c-9b38-92694c8ffb15`  
> **Parent Derivation**: [TFQ-0103](tfq_0103_finite_spin_label_bounds_do_not_discharge_the_einstein_equation_or_a_physical.md)

---

## 1. Abstract & Formal Statement

finite_spinfoam.rs holds two finite cyclotomic models of boundary amplitudes and a Pachner constraint. On eight admissible binary boundaries the published transition is a scalar times the all-ones matrix and is never unitary; the corrected transition is that scalar times the identity, unitary only when the scalar is a unit. The corrected partition is read as a Hermitian norm in a quadratic field. What is finite is this eight-boundary arithmetic. What is not discharged is spin-foam unitarity in general, triangulation independence, and quantum gravity. The amplitude is not a continuum path integral.

### Governing Obligation
Eight-boundary amplitudes do not discharge general spin-foam unitarity, the Einstein equation, or a continuum limit.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
*Formalization active. Proof obligations tracked under zero-sorry regime.*

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/finite_spinfoam.rs`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0105](tfq_0105_gap_no_continuum_limit_and_no_physical_cosmological_constant_are_discharged_by.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
