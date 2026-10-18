# [TFQ-0147] Weighted Stinespring realizations

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `c1f4d519-618d-5bd2-80a2-104523b29be7`  
> **Parent Derivation**: [TFQ-0146](TFQ-0146_kraus_channels_and_completely_positive_maps.md)

---

## 1. Abstract & Formal Statement

Covers cptp_channels_stinespring.rs, stinespring_dilation.rs, cptp_trajectory_verifier.rs, population_shadow.rs, difference_transport_channel.rs, and qddc.rs. cptp_channels_stinespring.rs realizes a weighted Kraus channel by an isometry against a declared diagonal environment metric. The other files build a complementary channel, check exact-rational trajectories with no floating types, record population shadows, and keep operator-valued cochains distinct from densities. A Python replay and a Lean 4 declaration would still have to match the weighted isometry identity.

### Governing Obligation
Match the weighted isometry identity V adjoint (I tensor G) V = I for a declared diagonal environment metric.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/cptp_channels_stinespring.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/cptp_trajectory_verifier.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/difference_transport_channel.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/population_shadow.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/qddc.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/stinespring_dilation.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/cptp_channels_stinespring.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0148](TFQ-0148_population_and_spectral_entropy.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
