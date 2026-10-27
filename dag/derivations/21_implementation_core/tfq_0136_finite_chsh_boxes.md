# [TFQ-0136] Finite CHSH boxes

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `792a8365-56a3-5e18-834b-c1b3cc535698`  
> **Parent Derivation**: [TFQ-0134](tfq_0134_pauli_group_and_exchange_characters.md)

---

## 1. Abstract & Formal Statement

Covers finite_chsh_correlations.rs, finite_bell_extension.rs, finite_bell_preparation.rs, quantum_correlation.rs, tensor_commuting_correlation_frontier.rs, and composition_quantum_bound.rs. finite_chsh_correlations.rs computes the CHSH value of 16 joint assignments, box correlators, and no-signalling marginals. The other files ask for a nonnegative setting-independent prior, record preparation laws, bound planar spin correlations, and import a composition bound. A Python replay and a Lean 4 declaration would still have to match the 16-assignment table and the marginal test.

### Governing Obligation
Match the CHSH values of the 16 joint assignments and the no-signalling marginal test for pairwise boxes.

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
- [`absent: no local rust twin located for external:sha256:3aa68d6116ce374efc50eed1e23d148aaae1be854b3bf16be67d8d1ab42dceb4`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:436c024d77fc3479e5ac42ac8b0fc5e0884fa46295d995abb94d20d477c5c9cc`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:edadce6cfa6d264bacd1dc434d6f67944b5bbb3a61d6da68f28c21c1e3c7d54f`](../../code/rust/src/)
- [`code/rust/src/qm/campaigns/quantum_correlation.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:b414fa05dfae91edfc9db32ccb708ad96dae21e6e86197c9716f39cb46b6e3cc`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:9765c2d94791424a10351167ef55ae78167558d6f03b943c2cc26ea339d421a6`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/quantum_correlation.py`](../../code/python/)
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/tensor_commuting_correlation_frontier.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
