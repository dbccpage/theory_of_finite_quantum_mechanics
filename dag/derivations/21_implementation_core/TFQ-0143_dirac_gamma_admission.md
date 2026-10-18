# [TFQ-0143] Dirac gamma admission

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `869fbe5e-cb6f-57b7-99fa-34382943c729`  
> **Parent Derivation**: [TFQ-0137](TFQ-0137_unitary_steps_and_hamiltonians.md)

---

## 1. Abstract & Formal Statement

Covers dirac_gamma_admission.rs, lattice_dirac_doubling.rs, atomic_dirac_lamb_hartree_fock.rs, and quantum_import_finite_maps/vacuum_polarization_lamb_shift.rs. dirac_gamma_admission.rs admits gamma matrices over Q(i) only when their anticommutators match a declared diagonal sign metric. lattice_dirac_doubling.rs compares naive and Wilson operators on a periodic lattice. The atomic and vacuum-polarization files are finite Lamb-shift maps, not the excluded continuum slices. A Python replay and a Lean 4 declaration would still have to match the anticommutator admission test.

### Governing Obligation
Match Clifford anticommutator admission for a declared diagonal sign metric over Q(i).

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/atomic_dirac_lamb_hartree_fock.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/dirac_gamma_admission.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/lattice_dirac_doubling.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/vacuum_polarization_lamb_shift.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/atomic_dirac_lamb_hartree_fock_control.py`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/vacuum_polarization_lamb_shift_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
