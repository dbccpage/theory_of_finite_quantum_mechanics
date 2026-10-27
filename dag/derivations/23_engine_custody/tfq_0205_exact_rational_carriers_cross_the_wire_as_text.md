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
- [`lean4/ExactRatBasic.lean`](../../../lean4/ExactRatBasic.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:70c158328f038a7c76fcacc04288b142250b1121803c1c0c511aa71943a83782`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:d8a797c3e2b79dea816a3ec3cffb85eb0179b327e0ffd5f08789bd59d72829a6`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0206](tfq_0206_a_float_computation_cannot_authorize.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F003.S000`, `F003.S000:000_omega_engine_prime_algorithms_and_runtime`, `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:5d358f5062016c742016b891fa7891bb0f0e19ef`
  - `external:git-tree:e03ce30c258cf9ca164637ea387b5267bad58df9`
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
