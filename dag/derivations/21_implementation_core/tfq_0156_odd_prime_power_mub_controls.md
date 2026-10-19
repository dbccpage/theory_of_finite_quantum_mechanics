# [TFQ-0156] Odd-prime-power MUB controls

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `6e38f7c2-54db-5175-9061-7de5a95fd506`  
> **Parent Derivation**: [TFQ-0155](tfq_0155_odd_prime_weyl_mub_and_wigner.md)

---

## 1. Abstract & Formal Statement

Covers mub/odd_prime_power_weyl.rs, mub/odd_prime_power_controls.rs, mub/odd_prime_power_field_theorem_gate.rs, mub/odd_prime_power_parametric_gate.rs, and mub/prime_power_gtmur_boundary.rs. odd_prime_power_controls.rs gives exact Hilbert controls for dimensions 9, 25, 27, and 49 in named cyclotomic fields, as positive controls rather than an all-dimension theorem. The other files organize trace and Gauss reductions and the prime-power boundary of a broader request. A Python replay and a Lean 4 declaration would still have to match those declared-dimension controls.

### Governing Obligation
Match the declared exact controls in dimensions 9, 25, 27, and 49 without treating them as an all-dimension theorem.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/odd_prime_power_controls.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/odd_prime_power_field_theorem_gate.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/odd_prime_power_parametric_gate.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/odd_prime_power_weyl.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mub/prime_power_gtmur_boundary.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`The python twin is not located for the odd-prime-power MUB controls under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
