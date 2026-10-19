# [TFQ-0050] Either add an exact SU(3) fusion file or leave that obligation open

> **Stage**: `FINITE_TOPOLOGICAL` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `63c6efed-2e38-5a2c-a9d0-91e003055f72`  
> **Parent Derivation**: [TFQ-0049](tfq_0049_keep_frobenius_and_multiplicity_free_fusion_off_the_missing_color_hopf_algebra.md)

---

## 1. Abstract & Formal Statement

catalog.rs pins exact ribbon data for Ising, Fibonacci, semion, pointed braided categories, the toric code as D(Z_2), a three-fermion model, and quantum doubles D(Z_n). A coefficient field that lacks the needed root of unity is FusionError::FieldTooSmall, not an approximation. su2_level.rs is the SU(2) family in a Racah gauge. The file su3_level.rs is absent from omega_fusion_categories/src, so there is no fusion-category obligation already discharged for SU(3)_k. The catalog does not assert a material host. This absence is an open obligation, not a negative theorem about fusion categories.

### Governing Obligation
Either add an exact SU(3) fusion file or leave that obligation open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: no Lean SU(3)_k fusion file was located`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: omega_engine/crates_rs/omega_fusion_categories/src/su3_level.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_fusion_categories/src/catalog.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_fusion_categories/src/su2_level.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: catalog models have no QCD use case`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0051](tfq_0051_keep_the_spin_lift_on_declared_flat_complexes_and_off_the_dirac.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
