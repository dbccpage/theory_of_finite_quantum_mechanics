# [TFQ-0154] Canonical MUB inversion

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `2e1d92b5-a2cf-5684-a92e-3899a559c0d0`  
> **Parent Derivation**: [TFQ-0131](tfq_0131_density_operators_over_q_i.md)

---

## 1. Abstract & Formal Statement

Covers mub.rs, mub/carrier.rs, mub/algebra.rs, mub/prime_controls.rs, and mub/dimension_stratification.rs. mub.rs states canonical finite exact MUB systems and Wootters-Fields linear inversion. The other files declare the clean-room carrier, verify projector algebra, construct supported prime controls, and separate prime-power consequences from tensor lower bounds. A Python replay and a Lean 4 declaration would still have to match that inversion layout and the stratification split.

### Governing Obligation
Match canonical finite MUB linear inversion and the split between prime-power controls and tensor lower bounds.

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
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/mub.rs`](../../code/rust/src/)
- [`code/rust/src/qm/campaigns/carrier.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/mub/algebra.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/mub/prime_controls.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/mub/dimension_stratification.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: The python twin is not located for mub.rs under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0155](tfq_0155_odd_prime_weyl_mub_and_wigner.md)
- [TFQ-0157](tfq_0157_characteristic_two_projector_mubs.md)
- [TFQ-0158](tfq_0158_composite_mub_tensor_lower_controls.md)
- [TFQ-0159](tfq_0159_mub_tomography_and_composition.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
