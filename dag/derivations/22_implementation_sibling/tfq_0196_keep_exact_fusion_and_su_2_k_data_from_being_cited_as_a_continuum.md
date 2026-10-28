# [TFQ-0196] Keep exact fusion and SU(2)_k data from being cited as a continuum

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `f795fdf8-a3d5-51b9-a2c2-ceb41ca284f8`  
> **Parent Derivation**: [TFQ-0166](tfq_0166_record_these_sibling_crates_as_controls_under_authorityeffect_none_not_as_completed.md)

---

## 1. Abstract & Formal Statement

Fusion data in tfqm_fusion_categories are exact ring controls, not a Hilbert anyon derivation. src/lib.rs requires nonnegative integer fusion coefficients and symbols in an exact number field, with no floating-point conversion and no tolerance, and it marks the crate Not PROVED. catalog.rs pins Ising, Fibonacci, and semion constructors and returns a typed field error when a needed root of unity is missing. su2_level.rs places algebraic Racah F-symbols in a cyclotomic field and says that gauge is not orthonormal. The obligation is to keep a pentagon or hexagon check from being cited as continuum SU(2).

### Governing Obligation
Keep exact fusion and SU(2)_k data from being cited as a continuum anyon or Hilbert derivation.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/wdp/lib.rs`](../../code/rust/src/)
- [`code/rust/src/fusion_categories/catalog.rs`](../../code/rust/src/)
- [`code/rust/src/fusion_categories/fusion_ring.rs`](../../code/rust/src/)
- [`code/rust/src/fusion_categories/su2_level.rs`](../../code/rust/src/)
- [`code/rust/src/fusion_categories/modular.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
