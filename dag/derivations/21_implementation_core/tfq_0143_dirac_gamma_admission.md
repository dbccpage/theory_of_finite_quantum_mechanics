# [TFQ-0143] Dirac gamma admission

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `869fbe5e-cb6f-57b7-99fa-34382943c729`  
> **Parent Derivation**: [TFQ-0137](tfq_0137_unitary_steps_and_hamiltonians.md)

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
- [`absent: no local lean twin located for lean4/quantum_mechanics`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:6d09fe3d269514b28dde4a6f6dec6760ac77e87653e9f18c490226f9f26bb231`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:c3411f0605765fdcb49501e624ef950e733ec66459057bb8b89d9df1c9c7bfb2`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:dee13d74d257e960c55d1b3da0a35f7276c33ede91adba5203a17a7bb91cb34f`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:ac46ba7dd3e8763a1c8f6bf42bc9e263b13e63bcc8783cdaf598f6ec34d4c9e3`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/atomic_dirac_lamb_hartree_fock_control.py`](../../code/python/)
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/vacuum_polarization_lamb_shift_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
