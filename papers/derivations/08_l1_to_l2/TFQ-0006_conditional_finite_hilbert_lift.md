# [TFQ-0006] Conditional finite Hilbert lift

> **Stage**: `L1_TO_L2` | **Status**: `GAP`  
> **UUID**: `c5fc9265-5e57-5684-b28d-3870cf71e931`  
> **Parent Derivation**: [TFQ-0005](../07_l1_emergence/TFQ-0005_declared_l1_sector_weights.md)

---

## 1. Abstract & Formal Statement

The pass from L1 weights to a finite Hilbert carrier imports structure the finite papers do not derive: a square-root field, a complex field, U(1) phases, an inner product, orthogonal additivity, Haar-independent phases, and linear isometric dynamics. QM_020 states that it does not derive quantum mechanics. QM_122 recovers matrices over the Gaussian integers and leaves ordinary matrix algebras over the complex numbers unrecovered. Python, Rust, and Lean 4 must name each import and keep it imported. A finite matrix calculation is not a discharge of the import list.

### Governing Obligation
List each imported structure the finite Hilbert lift still requires, and do not discharge them by naming quantum mechanics.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
*Formalization active. Proof obligations tracked under zero-sorry regime.*

### Sovereign Rust Certifiers
*Computational witness tracked under `theory_of_finite_qm` crate.*

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0007](../10_finite_qm_core/TFQ-0007_finite_quantum_mechanics_core_on_an_admitted_carrier.md)
- [TFQ-0234](../10_finite_qm_core/TFQ-0234_supplied_hilbert_carrier_after_the_conditional_lift.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
