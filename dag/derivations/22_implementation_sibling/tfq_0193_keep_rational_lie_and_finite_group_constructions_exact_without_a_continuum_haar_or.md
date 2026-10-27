# [TFQ-0193] Keep rational Lie and finite-group constructions exact, without a continuum Haar or

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `b3f706f3-3245-5f8a-bd46-625837ab6f33`  
> **Parent Derivation**: [TFQ-0166](tfq_0166_record_these_sibling_crates_as_controls_under_authorityeffect_none_not_as_completed.md)

---

## 1. Abstract & Formal Statement

omega_lie_theory is an exact finite-group and rational Lie library, not a completed continuum symmetry derivation. src/lib.rs says every quantity is rational, cyclotomic, or quadratic, with no floating point and no tolerance, and it marks the crate Not PROVED. Declared modules include finite_group.rs, cayley.rs, su2.rs, rotation.rs, lorentz.rs, finite_order.rs, and lie_algebra.rs. Lorentz boosts in lorentz.rs are rational points of a hyperboloid. The obligation is to use these matrices as finite exact controls. They do not install a continuous Haar measure or a Hilbert representation.

### Governing Obligation
Keep rational Lie and finite-group constructions exact, without a continuum Haar or Hilbert step.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/RationalLieSpan.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/wdp/lib.rs`](../../code/rust/src/)
- [`code/rust/src/lie_theory/finite_group.rs`](../../code/rust/src/)
- [`code/rust/src/lie_theory/lorentz.rs`](../../code/rust/src/)
- [`code/rust/src/lie_theory/su2.rs`](../../code/rust/src/)
- [`code/rust/src/lie_theory/lie_algebra.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0194](tfq_0194_keep_the_finite_weyl_relation_distinct_from_a_characteristic_zero_ccr_which_the.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
