# [TFQ-0147] Weighted Stinespring realizations

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `c1f4d519-618d-5bd2-80a2-104523b29be7`  
> **Parent Derivation**: [TFQ-0146](tfq_0146_kraus_channels_and_completely_positive_maps.md)

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
- [`absent: no local lean twin located for lean4/quantum_mechanics`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:7ecaf8b5a2fd5a4428b83ca6f579e8bda5323dd5ca0b2d87b0138227eb0e5cf3`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:3f6c8254db5f7f1cf34666bdcbabaca42db3715c6458f0d62c7e3fe7cf105cf9`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:ada3020191cd8fa36b0f4e9a76d9be86078a2e5854c9c395421126e118f9d73d`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:7b309464bfb77b31189268792f462650765f6d1a30cb1473cb2053a13fe3d861`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:f33c66ad847debef2c592483e63336b15c52ad19d9d543515d334e66806435ab`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:e69dc209e4b456a6f2777bd3fc921366f1e499b60106637ce01d9dde686de112`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/cptp_channels_stinespring.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0148](tfq_0148_population_and_spectral_entropy.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
