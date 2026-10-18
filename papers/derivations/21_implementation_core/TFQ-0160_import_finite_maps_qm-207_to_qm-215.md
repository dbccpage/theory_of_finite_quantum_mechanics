# [TFQ-0160] Import finite maps QM-207 to QM-215

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `512fb3b6-86bd-59d7-954b-da1426928162`  
> **Parent Derivation**: [TFQ-0131](TFQ-0131_density_operators_over_q_i.md)

---

## 1. Abstract & Formal Statement

Covers quantum_import_finite_maps.rs, quantum_import_finite_maps/algebraic_bound_state_spectra.rs, and quantum_import_finite_maps/foundational_derivation_closure.rs. The facade states exact finite-map controls for QM-207 through QM-215. algebraic_bound_state_spectra.rs is the QM-217 Kravchuk and so(4) hydrogen finite spectra. foundational_derivation_closure.rs is the 5 by 5 import-independence countermodel matrix and the Z[zeta_12] Sorkin readout class. Electroweak, QCD, and continuum-named siblings stay outside this node. A Python replay and a Lean 4 declaration would still have to match that 5 by 5 matrix.

### Governing Obligation
Match the 5 by 5 single-system import-independence countermodel matrix in the QM-219 closure.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/algebraic_bound_state_spectra.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/foundational_derivation_closure.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/algebraic_bound_state_spectra_control.py`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/foundational_derivation_closure_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0161](TFQ-0161_finite_expressibility_and_measurement.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
