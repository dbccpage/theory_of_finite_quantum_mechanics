# [TFQ-0014] Do not cite the M_2 packet complex or the groupoid algebra as

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `3747dd2d-29af-5d11-9220-e05990daab78`  
> **Parent Derivation**: [TFQ-0013](tfq_0013_use_cyclotomic_character_tables_only_as_labels_of_a_declared_finite_group.md)

---

## 1. Abstract & Formal Statement

finite_groupoid_algebra.rs linearizes a ValidatedFiniteGroupoid as convolution over Q(i). The module states that the associated complex C*-algebra is a mathematical extension, not a native finite computation. gauge_cochain_complex.rs is a different object: an exact complex on packets in M_2(Q(i)), with d0 sending anti-Hermitian generators to commutators on effects and states. Neither file is a Hopf gauge theory, and neither file stores SU(3) link variables. The obligation is to keep the groupoid convolution and the qubit packet complex from being cited as the color connection used later in the QCD control.

### Governing Obligation
Do not cite the M_2 packet complex or the groupoid algebra as the color connection.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: packet gauge complex is not a FiniteQM QCD theorem`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_lie_theory/src`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_lie_theory/src/finite_groupoid_algebra.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/gauge_cochain_complex.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no groupoid-algebra QCD use case`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0015](tfq_0015_keep_the_substantial_versus_artificial_split_on_b_2_q_not_on_su_3.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
