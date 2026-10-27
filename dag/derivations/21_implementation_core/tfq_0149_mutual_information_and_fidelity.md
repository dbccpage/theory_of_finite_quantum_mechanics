# [TFQ-0149] Mutual information and fidelity

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `1d85d481-14db-585d-b9f9-5e3f166e7bd6`  
> **Parent Derivation**: [TFQ-0148](tfq_0148_population_and_spectral_entropy.md)

---

## 1. Abstract & Formal Statement

Covers quantum_mutual_information.rs, quantum_entropy_cone.rs, fidelity.rs, simplicial_entropy_schedule.rs, and ancilla_capacity.rs. quantum_mutual_information.rs evaluates mutual information, conditional entropy, and coherent information from the entropy face. quantum_entropy_cone.rs treats monogamy as an optional constraint, not a law of every entropy vector. The other files are Uhlmann-Jozsa fidelity, a declared Page schedule, and ancilla extension-purity bounds. A Python replay and a Lean 4 declaration would still have to match those inequalities and the optional monogamy flag.

### Governing Obligation
Match mutual information from the entropy face and the optional status of monogamy on entropy vectors.

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
- [`absent: no local rust twin located for external:sha256:e02bba069865c9efd74ac9658f9e3040c5e6dc0b126e270a9f512c6dda65ec86`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:3e1d3e64a2206ec3c9f70d4969bc2fdd1c0e16e8aabd1f13a4487d63abb2c10e`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:176d2e422f34e1742ce3022824beffe63aa6032b51843a37266de7e369ebd575`](../../code/rust/src/)
- [`code/rust/src/qm/domain/simplicial_entropy_schedule.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:4447dc07da9857e72fdf961ed63fce285cebd4e0762f487974029267b988fe85`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/simplicial_complex_qm.py`](../../code/python/)
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0150](tfq_0150_discrete_phase_estimation.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
