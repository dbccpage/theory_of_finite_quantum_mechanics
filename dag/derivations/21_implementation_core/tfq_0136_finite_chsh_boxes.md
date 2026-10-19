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
- [`lean4/quantum_mechanics`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/composition_quantum_bound.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/finite_bell_extension.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/finite_bell_preparation.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/finite_chsh_correlations.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_correlation.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/tensor_commuting_correlation_frontier.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/quantum_correlation.py`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/tensor_commuting_correlation_frontier.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
