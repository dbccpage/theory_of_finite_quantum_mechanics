# [TFQ-0131] Density operators over Q(i)

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `cad05840-f131-5526-a70e-978ef2e0bbcb`  
> **Parent Derivation**: [TFQ-0129](TFQ-0129_exact_rays_and_pure_states.md)

---

## 1. Abstract & Formal Statement

Covers density_matrix.rs, exact_hermitian.rs, packed_hermitian.rs, residual_density_calculus.rs, and exact_operator.rs. density_matrix.rs admits ExactDensityMatrix only when the Q(i) matrix is Hermitian, positive semidefinite by exact LDL, and of trace 1. Mixtures, partial traces, and channel actions are revalidated. The population shadow is the diagonal, not the state. The other files carry Hermitian admission, packed physical storage, pointer-sector updates, and the exact real spectrum. A Python replay and a Lean 4 declaration would still have to match that admission gate and the shadow split.

### Governing Obligation
Match Hermitian, exact-LDL, trace-one admission and the split between a density and its population shadow.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/density_matrix.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/exact_hermitian.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/exact_operator.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/packed_hermitian.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/residual_density_calculus.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/density_matrix.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0132](TFQ-0132_trace-norm_certificates.md)
- [TFQ-0133](TFQ-0133_observables_and_local_star_algebras.md)
- [TFQ-0154](TFQ-0154_canonical_mub_inversion.md)
- [TFQ-0160](TFQ-0160_import_finite_maps_qm-207_to_qm-215.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
