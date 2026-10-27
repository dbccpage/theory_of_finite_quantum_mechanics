# [TFQ-0063] Each language must carry: at every rational loop momentum, q contracted into

> **Stage**: `FINITE_QED` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `6ef373b6-c200-54bf-88eb-ae66c2c63942`  
> **Parent Derivation**: [TFQ-0062](tfq_0062_each_language_must_carry_a_truncated_intermediate_normalization_series_a.md)

---

## 1. Abstract & Formal Statement

The Ward finite shadow is an integrand identity in M_4(Q(i)), not an integrated continuum Ward identity. one_loop_vertex_integrand and the self-energy integrand in quantum_import_finite_maps.rs contract gamma matrices and rational Dirac propagators at a declared loop momentum k. dirac_ward_takahashi_finite_map.md states that q_mu times the vertex integrand at (p+q, p; k) equals the self-energy integrand at p minus the same integrand at p+q, at every rational k, before any integration.

### Governing Obligation
Each language must carry: at every rational loop momentum, q contracted into the one-loop vertex integrand equals the difference of self-energy integrands, and the zero-momentum subtractions therefore match with Z1/Z2 = 1 in Q.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `completion to R/C, Stone, period integrals (lift)`
- **Admitted**: `each row s5.2 "Residual import" column (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> All finite rational/integer control theorems for QM-207..231 are mechanized; continuum completions in QM-207..211 remain priced as explicit imports.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:376085dc410bbb86117c8efb40f2280ed15cb5734a22d050f6e1718aef3be579`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/dirac_ward_takahashi_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0064](tfq_0064_each_language_must_carry_exact_cancellation_of_the_declared_infrared_cutoff_between.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`
