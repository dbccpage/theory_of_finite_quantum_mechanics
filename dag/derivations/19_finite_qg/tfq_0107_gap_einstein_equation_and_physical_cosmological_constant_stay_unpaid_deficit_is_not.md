# [TFQ-0107] GAP: Einstein equation and physical cosmological constant stay unpaid; deficit is not

> **Stage**: `FINITE_QG` | **Status**: `GAP`  
> **UUID**: `5a31525e-8d87-55bd-89b1-a4252574d09e`  
> **Parent Derivation**: [TFQ-0106](tfq_0106_gap_the_physical_cosmological_constant_is_not_discharged_the_rust_carrier_is.md)

---

## 1. Abstract & Formal Statement

field_equation.rs and hamiltonian_constraint.rs write discrete Einstein-Regge and Wheeler-DeWitt formulae, including a Lambda term, over floating edge lengths and dihedral angles. Those comments describe algebraic scaffolds and a vanishing condition for a discrete operator. They do not discharge the Einstein equation, which remains GAP, and they do not select a physical cosmological constant. What is finite is a triangulation with floating edge data when a caller supplies one. What is not discharged is a continuum field equation and any claim that a deficit equals smooth curvature. AuthorityEffect is None.

### Governing Obligation
GAP: Einstein equation and physical cosmological constant stay unpaid; deficit is not smooth curvature.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
*Formalization active. Proof obligations tracked under zero-sorry regime.*

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_general_relativity/src/field_equation.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_general_relativity/src/hamiltonian_constraint.rs`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0108](tfq_0108_gap_caller_supplied_lambda_is_not_the_physical_cosmological_constant_and_the_grid.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
