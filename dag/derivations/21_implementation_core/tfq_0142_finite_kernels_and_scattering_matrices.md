# [TFQ-0142] Finite kernels and scattering matrices

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `093c1aee-0e11-5daf-a942-9f2cafcbfd11`  
> **Parent Derivation**: [TFQ-0137](tfq_0137_unitary_steps_and_hamiltonians.md)

---

## 1. Abstract & Formal Statement

Covers path_integral.rs, time_sliced_action_shadow.rs, s_matrix.rs, scattering_amplitude.rs, and feynman_diagram.rs. path_integral.rs computes finite time-sliced kernels and says formal coefficients do not assert a continuum measure. s_matrix.rs builds S from a Hermitian reaction matrix over Q(i). scattering_amplitude.rs uses T = (S - I)/(2i) at a declared energy with no on-shell limit. The other files add a phase policy and finite Wick symmetry factors. A Python replay and a Lean 4 declaration would still have to match the reaction-matrix formula and that continuum refusal.

### Governing Obligation
Match S built from a Hermitian reaction matrix over Q(i) and the refusal to assert a continuum measure.

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
- [`absent: no local rust twin located for external:sha256:4b48c2e282a2ea334c8e4d0c1fca71cdf5555a374d1aebd974794cd6dd92b489`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:474ddf6dbc3e443dcb552a7cdefa247acdd30a2c373accc8a856001486418d0e`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:2d9da71f2a615ba2de86c6896030b306594bc1169d72e912cd6e525b06887b66`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:a4ca67769f0cdeae91bce65233c44b0a2b18deb921c5d4e4fabd22880ee84034`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:5750c8892fd61b580168841520e2dbb88c42dc9a2870654a5b5a13df5a7e3be1`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: The python twin is not located for path_integral.rs under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
