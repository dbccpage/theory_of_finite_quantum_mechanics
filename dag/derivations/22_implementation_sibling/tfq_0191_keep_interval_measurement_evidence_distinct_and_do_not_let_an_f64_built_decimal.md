# [TFQ-0191] Keep interval measurement evidence distinct, and do not let an f64-built decimal

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `GAP`  
> **UUID**: `a0cc0796-08ba-5bc0-8bcf-baa4803f1a66`  
> **Parent Derivation**: [TFQ-0189](tfq_0189_keep_exact_rational_measurement_evidence_distinct_and_free_of_float_authority.md)

---

## 1. Abstract & Formal Statement

Interval evidence is a third kind and is not yet a governance scalar. MeasurementValue::Interval stores lower and upper BigDecimal bounds, and MeasurementError::IntervalRequiresPolicy is the refusal when an interval is asked to decide. BigDecimal::from_f64_unchecked builds a decimal from an f64 with a fixed scale, which is not an exact rational. affine_calibration.rs, finite_response.rs, and finite_chain_clock.rs add further interval clocks and calibrations. The obligation is to keep interval evidence pending a policy decision and to stop that unchecked f64 constructor from authorizing a bound.

### Governing Obligation
Keep interval measurement evidence distinct, and do not let an f64-built decimal authorize a bound.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`not located`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_measurement/src/affine_calibration.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_measurement/src/finite_chain_clock.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_measurement/src/finite_response.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_measurement/src/measurement_kernel.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
