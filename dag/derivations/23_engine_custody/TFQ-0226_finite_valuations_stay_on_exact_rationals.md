# [TFQ-0226] Finite valuations stay on exact rationals

> **Stage**: `ENGINE_CUSTODY` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `3212695f-294e-5ee9-83e0-64f1303f0be8`  
> **Parent Derivation**: [TFQ-0225](TFQ-0225_a_certifier_catalog_row_does_not_discharge_a_claim.md)

---

## 1. Abstract & Formal Statement

Finite valuations that accompany a quantum derivation stay on exact rationals. finite_valuation.rs uses Rational values, rejects a negative mass or a nonzero mass on the empty event. It separates this unnormalized layer from a nonempty probability carrier, so an empty carrier is representable without being presented as a density. ExactOperator and the kernel Exact type remain the neighboring rational hosts. A NumPy probability on the quantum shelf is not a substitute valuation. The runtime stores the rational map beside the finite statement and does not normalize it by a float division.

### Governing Obligation
Store accompanying valuations as exact rationals and do not normalize them in float.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/ExactRat/Basic.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_finite_probability/src/finite_valuation.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_kernel/src/exact.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/python/src/finite_quantum/density_matrix.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0227](TFQ-0227_pipeline_runtime_refuses_to_mint_authority.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F003.S000`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F003_omega_engine/S000_prime_algorithms_and_runtime`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics`
