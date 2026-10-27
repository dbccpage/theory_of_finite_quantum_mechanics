# [TFQ-0037] Keep Slater, CAR, and shell capacities on the identical-particle side of the

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `91723989-4b4b-5318-8729-1b1510f7a922`  
> **Parent Derivation**: [TFQ-0036](tfq_0036_report_the_rust_and_lean_k5_torsion_rank_not_the_opening_paragraph_s.md)

---

## 1. Abstract & Formal Statement

The same QM-223 certificate sets the same-orbital Slater combination to 0, the fermion swap ratio to -1, the boson swap ratio to +1, and the Hanbury Brown-Twiss coincidence ratio to 2. It records Jordan-Wigner nilpotency and the CAR identity on a finite Fock space. Shell capacities 1..4 are 2, 8, 18, 32, and the closures are 2, 10, 18, 36, 54, 86, 118. Lean slater_determinant_pauli_exclusion_and_swap_antisymmetry covers the two-row identities over Rat. These are identical-particle controls on graphs and exterior algebra. They do not assign flavor or color to a three-quark state.

### Governing Obligation
Keep Slater, CAR, and shell capacities on the identical-particle side of the QCD cut.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/FiniteQM.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:7b92d189c034dc6bb19e748fa9689912254a5b0b9a50a1f25d2566b9a4d4744f`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/pauli_spin_statistics_graph_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0038](tfq_0038_reconcile_the_map_s_k5_ranks_with_the_rust_certificate_and_leave_the.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
