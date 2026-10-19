# [TFQ-0109] PPN endpoint checks do not discharge Regge calculus, the Einstein equation, or

> **Stage**: `FINITE_QG` | **Status**: `FINITE_MAP`  
> **UUID**: `9841b07e-7844-5fb9-aedf-8ac170fea68c`  
> **Parent Derivation**: [TFQ-0108](tfq_0108_gap_caller_supplied_lambda_is_not_the_physical_cosmological_constant_and_the_grid.md)

---

## 1. Abstract & Formal Statement

regge_gravity_ghz_chern_finite_map.md records rational identities: post-Newtonian factors, three-qubit eigenvalues, a four-tick history, and a Chern parity table. The same note says the Regge discretization named in the goal title is not implemented there, and the deflection factors are not obtained from a field equation. What is finite is arithmetic at declared inputs, with pi only as a rational interval for arcseconds. What is not discharged is Regge gravity, the Einstein equation, and quantum gravity. An enclosure is not a continuum law.

### Governing Obligation
PPN endpoint checks do not discharge Regge calculus, the Einstein equation, or a continuum limit.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/FiniteQFTAndGravity.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/regge_gravity_ghz_chern_finite_maps.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/regge_gravity_ghz_chern_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0110](tfq_0110_gap_on_continuum_limit_einstein_equation_physical_cosmological_constant_and_smooth_curvature.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
