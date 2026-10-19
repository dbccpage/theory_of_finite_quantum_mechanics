# [TFQ-0049] Keep Frobenius and multiplicity-free fusion off the missing color Hopf algebra

> **Stage**: `FINITE_TOPOLOGICAL` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `519e493b-3a50-5e77-a55d-5f413a41cc4f`  
> **Parent Derivation**: [TFQ-0048](tfq_0048_do_not_read_the_toric_code_s_withheld_hamiltonian_gap_as_the_qcd.md)

---

## 1. Abstract & Formal Statement

frobenius_algebra.rs asks both Frobenius identities, units, and counits to replay on matrices over Q(i), with dimension from 1 to 16, and it refuses a degenerate trace form. fusion_category.rs replays the pentagon and unit laws for multiplicity-free data and states that categorification for N greater than 1 is not provided. A special commutative Frobenius algebra can underlie a lattice anyon model. It is not the missing Hopf gauge algebra for color, and the dimension cap is a code bound rather than a statement about QCD composites. The obligation is to keep Frobenius replay on the topological side of the cut.

### Governing Obligation
Keep Frobenius and multiplicity-free fusion off the missing color Hopf algebra.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: the dimension-16 Frobenius check is not in FiniteQM.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_fusion_categories/src/fusion_category.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/frobenius_algebra.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: Frobenius replay has no QCD use case`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0050](tfq_0050_either_add_an_exact_su_3_fusion_file_or_leave_that_obligation_open.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
