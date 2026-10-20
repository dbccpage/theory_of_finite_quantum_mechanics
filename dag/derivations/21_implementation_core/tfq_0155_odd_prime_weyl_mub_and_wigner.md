# [TFQ-0155] Odd-prime Weyl MUB and Wigner

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `eff7ffce-f9be-526d-8bc1-e8f4b5f4bc8a`  
> **Parent Derivation**: [TFQ-0154](tfq_0154_canonical_mub_inversion.md)

---

## 1. Abstract & Formal Statement

Covers mub/odd_prime.rs, mub/odd_prime_weyl.rs, mub/odd_prime_gauss_certificate_gate.rs, and wigner.rs. mub/odd_prime.rs constructs, for an odd prime p, the computational basis and p quadratic chirp bases, including four bases in dimension 3. The Weyl file records the finite-field schema, and the Gauss gate links declared odd-prime controls. wigner.rs computes exact odd-prime discrete Wigner values. A Python replay and a Lean 4 declaration would still have to match the chirp-basis formula and those Wigner values.

### Governing Obligation
Match the odd-prime computational basis plus p quadratic chirp bases, including four bases in dimension 3.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: no local lean twin located for lean4/quantum_mechanics`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/mub/odd_prime.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/mub/odd_prime_weyl.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/mub/odd_prime_gauss_certificate_gate.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/wigner.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: The python twin is not located for mub/odd_prime.rs. page_wootters_tsirelson_wigner_control.py is a different QM-218 control.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0156](tfq_0156_odd_prime_power_mub_controls.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
