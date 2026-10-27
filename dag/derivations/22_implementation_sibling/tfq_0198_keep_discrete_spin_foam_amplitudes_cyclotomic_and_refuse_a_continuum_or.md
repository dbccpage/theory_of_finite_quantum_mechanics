# [TFQ-0198] Keep discrete spin-foam amplitudes cyclotomic and refuse a continuum or

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `a7a889b3-6aa4-5cb1-b822-4b45c4065748`  
> **Parent Derivation**: [TFQ-0197](tfq_0197_feed_finite_gravity_only_the_rational_regge_proxy_not_the_arccosine_deficit.md)

---

## 1. Abstract & Formal Statement

Finite spin-foam recoupling is a shadow amplitude, not continuum gravity. src/spin_foam.rs computes SU(2)_2 tetrahedral recoupling at q = exp(i pi/4) with labels 0, 1, 2 in Q(sqrt(2)), and its fence says no continuum admission. DiscreteSpinfoamAmplitudes.lean states tetrahedral amplitudes in Z[zeta_12] and excludes a continuous SU(2) or SL(2, C) and a continuous Haar measure. FourSimplexSpinfoamS4.lean stays in Z[zeta_12] for a 10j vertex. The obligation is to keep these cyclotomic amplitudes from being cited as a triangulation-invariant continuum spin foam.

### Governing Obligation
Keep discrete spin-foam amplitudes cyclotomic and refuse a continuum or triangulation-invariance admission.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/DiscreteSpinfoamAmplitudes.lean`](../../lean4/)
- [`lean4/FourSimplexSpinfoamS4.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/general_relativity/spin_foam.rs`](../../code/rust/src/)

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
