# [TFQ-0139] Page-Wootters clock and Tsirelson

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `920b2b70-2991-5c62-8de3-5e037e1a5ae4`  
> **Parent Derivation**: [TFQ-0138](tfq_0138_heisenberg_picture_and_cayley_jet.md)

---

## 1. Abstract & Formal Statement

Covers quantum_import_finite_maps/page_wootters_tsirelson_wigner.rs and its cyclotomic_rings.rs helper. The header states QM-218 Page-Wootters clock dressing, a Tsirelson sum-of-squares check, and a (Z_3) squared Wigner function. The helper supplies cyclotomic matrix arithmetic. Report fields include a history-shift unitary of order 4 and an idempotent Hermitian constraint projector. A Python replay and a Lean 4 declaration would still have to match those clock-dressing flags, which FiniteQM.lean does not declare.

### Governing Obligation
Match the QM-218 history-shift unitary of order 4 and the idempotent Hermitian constraint projector.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/page_wootters_tsirelson_wigner.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/page_wootters_tsirelson_wigner/cyclotomic_rings.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/page_wootters_tsirelson_wigner_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
