# [TFQ-0152] Shor code and stabilizer distance

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `4bb8efcd-9534-58a8-969b-8fbe13b8e0b1`  
> **Parent Derivation**: [TFQ-0151](tfq_0151_grover_reflections_and_quantum_walks.md)

---

## 1. Abstract & Formal Statement

Covers shor.rs, stabilizer_code_distance.rs, toric_code.rs, cochain_repair_code.rs, repair_capacity.rs, and threshold_repair_certificate.rs. shor.rs is the Shor nine-qubit code in exact binary Pauli algebra, with syndrome extraction and recovery of the 27 single-qubit Pauli errors. It is a code control, not a factoring procedure. The other files compute stabilizer distance, a rectangular toric CSS code with no asserted gap, and conditional repair bounds. A Python replay and a Lean 4 declaration would still have to match the nine-qubit syndrome table.

### Governing Obligation
Match the nine-qubit stabilizer syndrome table and recovery of the 27 single-qubit Pauli errors.

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
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/shor.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/stabilizer_code_distance.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/toric_code.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/cochain_repair_code.rs`](../../code/rust/src/)
- [`code/rust/src/majorana/repair_capacity.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/threshold_repair_certificate.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/stabilizer_codes.py`](../../code/python/)
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
