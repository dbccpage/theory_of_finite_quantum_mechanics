# [TFQ-0542] wdp-graph-cochain-host

> **Stage**: `WDP` | **Status**: `DEFINITION`  
> **UUID**: `83837bdc-fae4-5eef-ad3c-a0e355a0d5e0`  
> **Parent Derivation**: [TFQ-0360](tfq_0360_supply_the_admitted_cut_x_e_tau_k_as_data_and_do.md)

---

## 1. Abstract & Formal Statement

On a finite oriented graph G = (V, E) with a normed coefficient space A, the host sets C⁰ = A^V, C¹ = A^E and (d₀f)(u, v) = f(v) − f(u); an edge field δ is exact when δ = d₀f. Q¹ = C¹/im d₀ records edge fields modulo vertex-potential repair, relative to the declared graph, coefficient space and repair map, and it is not the first cohomology group unless a next differential d₁ is supplied with d₁d₀ = 0. Worked cases: on the path 0 → 1 → 2, δ = (2, 3) = d₀(0, 2, 5) is exact; on the hollow cyclic triangle (01, 12, 20) every repair of δ = (1, 1, 1) still sums to 3, a quotient obstruction that is not contextuality without a measurement cover and an empirical model.

### Governing Obligation
Build C⁰, C¹ and d₀ from the declared oriented graph and coefficient space, treat Q¹ as a repair quotient, and withhold the name H¹ until a d₁ and a d₁d₀ = 0 certificate are supplied.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared finite oriented graph and normed coefficient space (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The graph, orientation and coefficients are declared inputs, not derived from Genesis admission (TFQ-0344); a repair-quotient class is not a cohomology class, and the host carries no measurement cover or empirical model.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean::Q1`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `omega_engine/crates_rs/omega_wdp/src/cochains.rs::FiniteComplex` (private upstream source, not in this repository)

### Python Oracles & Numerical Evaluators
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/cochains.py::FiniteComplex` (private upstream source, not in this repository)
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/cochains.py::d0` (private upstream source, not in this repository)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0543](tfq_0543_wdp_incidence_orientation_transport.md)
- [TFQ-0544](tfq_0544_wdp_phi_well_defined_l1_duality.md)
- [TFQ-0545](tfq_0545_wdp_closure_needs_degree.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md:894-919`
  - `omega_engine_education/documentation/006_oewdp/levels/level_03_discrete_complex_cochains.md:68-121`
