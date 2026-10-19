# [TFQ-0205] Exact rational carriers cross the wire as text

> **Stage**: `ENGINE_CUSTODY` | **Status**: `SOURCE_RECORD`  
> **UUID**: `090b5b10-6a94-5f16-bbc7-6e6565b1d538`  
> **Parent Derivation**: [TFQ-0204](tfq_0204_finite_floor_binding_for_a_quantum_carrier.md)

---

## 1. Abstract & Formal Statement

Exact rational carriers are the values a finite derivation may transport. omega_kernel defines Exact as BigRational and writes canonical text such as 3/4, refusing a JSON number because many readers treat that token as a float. parse_exact accepts only lowest terms with a positive denominator. Lean ExactRat.Frac is an integer numerator over a positive natural denominator, with equality by cross-multiplication, under AuthorityEffect None. ExactOperator builds matrices over Gaussian rationals and states that nothing there is floating point. The derivation folder stores these objects, not a rounded substitute.

### Governing Obligation
Transport authorizing carriers as exact rationals or canonical rational text.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/ExactRat/Basic.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_kernel/src/exact.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/exact_operator.rs`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0206](tfq_0206_a_float_computation_cannot_authorize.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F003.S000`, `F003.S000:000_omega_engine_prime_algorithms_and_runtime`, `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime`
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime/000_omega_engine_prime_algorithms_and_runtime`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
