# [TFQ-0287] Cohomology admission does not select Hilbert space

> **Stage**: `L1_TO_L2` | **Status**: `SOURCE_RECORD`  
> **UUID**: `6e10f8d0-3251-5aa0-a882-62b26de020f7`  
> **Parent Derivation**: [TFQ-0286](TFQ-0286_descent_census_and_an_open_conjecture.md)

---

## 1. Abstract & Formal Statement

qm_010_hilbert_space_cochains_qm_cohomology.md defines a four-side adapter whose quantum side is an imported finite realization: Hilbert carrier, states, effects, POVMs, Born pairing, channels, and phase data. The finite obligation is admission of a declared cochain, including the complex law that the image of the first differential sits in the kernel of the next, once that law is part of the declaration. The status box says the note does not derive quantum mechanics, Hilbert space, or Born uniqueness. The claim ledger leaves a Lean discharge of that image-in-kernel step open. Cohomology here diagnoses exactness.

### Governing Obligation
Import the Hilbert side of the adapter and leave the cochain Lean discharge open.

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

- [TFQ-0288](TFQ-0288_pairing_audit_does_not_select_the_born_row.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
