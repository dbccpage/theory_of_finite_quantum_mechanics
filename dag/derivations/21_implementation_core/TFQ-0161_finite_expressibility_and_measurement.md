# [TFQ-0161] Finite expressibility and measurement

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `7fad01dd-9631-5bcf-9194-1a76f07b70a5`  
> **Parent Derivation**: [TFQ-0160](TFQ-0160_import_finite_maps_qm-207_to_qm-215.md)

---

## 1. Abstract & Formal Statement

Covers quantum_import_finite_maps/finite_qm_expressibility_and_measurement.rs. The header names expressibility classification, Kraus measurement decoherence, a Wigner-friend obstruction, and a qutrit stabilizer-versus-magic boundary. The cited path lean4/quantum_mechanics was not found. Confirmed FiniteQM.lean Part VIII declares weyl_heisenberg_finite_trace_obstruction, lorentz_boost_non_unitary_in_finite_dim, and finite_clock_poincare_recurrence_vs_kraus_decoherence. A Python replay and a Lean 4 declaration would still have to match those three Rat identities where they overlap this file.

### Governing Obligation
Match the three confirmed Rat identities in FiniteQM.lean Part VIII where they overlap the expressibility control.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/finite_qm_expressibility_and_measurement.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/finite_qm_expressibility_and_measurement_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
