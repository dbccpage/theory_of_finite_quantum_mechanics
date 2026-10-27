# [TFQ-0226] Finite valuations stay on exact rationals

> **Stage**: `ENGINE_CUSTODY` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `3212695f-294e-5ee9-83e0-64f1303f0be8`  
> **Parent Derivation**: [TFQ-0225](tfq_0225_a_certifier_catalog_row_does_not_discharge_a_claim.md)

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
- [`lean4/ExactRatBasic.lean`](../../../lean4/ExactRatBasic.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/finite_probability/finite_valuation.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:70c158328f038a7c76fcacc04288b142250b1121803c1c0c511aa71943a83782`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0227](tfq_0227_pipeline_runtime_refuses_to_mint_authority.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F003.S000`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `external:git-tree:5d358f5062016c742016b891fa7891bb0f0e19ef`
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:aaf60017b237ab042d2a4f52cec36e21f4264b2f`
