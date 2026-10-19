# [TFQ-0017] Do not promote the SU(2) quaternion shadow to su(3)_c

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `6163e5c0-1c6d-5b8e-a35a-e9b6502da302`  
> **Parent Derivation**: [TFQ-0016](tfq_0016_add_a_lean_replay_of_the_two_stage_dressing_or_leave_qm_213_as.md)

---

## 1. Abstract & Formal Statement

quaternion_gauge_shadow.rs says each listed Q8 element lies in SU(2) by the special-unitary check, and it says explicitly that Q8 is a finite subgroup of SU(2), not SU(2) itself. su2.rs holds quaternions, the adjoint cover, spinor norms, and binary polyhedral groups. Those constructions give a finite non-abelian shadow with a two-dimensional carrier. They do not provide the three diagonal color labels used by the weighted Gell-Mann family. Promoting Q8 flux operators to a stand-in for su(3)_c would skip the separate generator control. The obligation is to keep this SU(2) shadow on the gauge side of the cut.

### Governing Obligation
Do not promote the SU(2) quaternion shadow to su(3)_c.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: Q8-versus-SU(3) separation is not a FiniteQM theorem`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_lie_theory/src/su2.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quaternion_gauge_shadow.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no use case promotes Q8 to color`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0018](tfq_0018_treat_c_n_as_a_declared_label_space_before_any_graph_attachment.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
