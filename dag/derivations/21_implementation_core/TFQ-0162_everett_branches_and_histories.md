# [TFQ-0162] Everett branches and histories

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `9a84983e-1ae0-53d3-a32e-d3234e4811d7`  
> **Parent Derivation**: [TFQ-0129](TFQ-0129_exact_rays_and_pure_states.md)

---

## 1. Abstract & Formal Statement

Covers everett.rs, branch_finegraining.rs, chain_histories.rs, and decoherence_functional.rs. everett.rs keeps a count weight apart from the Born weight on exact finite branches. branch_finegraining.rs counts rational Born branches and records a cyclotomic irrational-weight obstruction. chain_histories.rs prepares histories through declared projective partitions. decoherence_functional.rs is the exact finite decoherence functional. A Python replay and a Lean 4 declaration would still have to match the count-versus-Born split and the history class operator.

### Governing Obligation
Match the separation of count weight from Born weight and the class operator of a declared projective history.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/branch_finegraining.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/chain_histories.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/decoherence_functional.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/everett.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/branch_finegraining.py`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/everett_tree.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
