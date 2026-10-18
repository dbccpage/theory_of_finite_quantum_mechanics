# [TFQ-0095] QM-111-C3 does not discharge nabla G equals zero. QM-111-C7 imports the continuum

> **Stage**: `FINITE_QG` | **Status**: `TOY_CARRIER`  
> **UUID**: `a935deca-fb19-58fd-ae63-66b076aa149c`  
> **Parent Derivation**: [TFQ-0094](TFQ-0094_gap_physical_cosmological_constant_and_continuum_hilbert_space_are_outside_this_tetrahedron.md)

---

## 1. Abstract & Formal Statement

QM-111 places curvature, a Bianchi shape, metric compatibility, and parallel transport on toy carriers. The finite Bianchi row is the composition of d1 with d0 vanishing on a filled triangle, which makes a cohomology group definable and does not yield a contracted Bianchi identity for a smooth Einstein tensor. Isometries preserve a declared pairing; which pairing is physical stays imported. What is finite is Q8, a finite simplicial complex, and finite groups. What is not discharged is Levi-Civita uniqueness, the Riemann tensor, and the Einstein equation. These shadows are not quantum gravity.

### Governing Obligation
QM-111-C3 does not discharge nabla G equals zero. QM-111-C7 imports the continuum metric and connection.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Hamiltonian constraint / Einstein equation (assumption)`
- **Admitted**: `SU(2) gauge group (assumption)`
- **Admitted**: `continuum manifold, metric, connection (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean names not checked by me; dynamics Q-held.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm110_111_lqg_gr_kinematical_witness`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_ds_qm_dynamics_structure_and_majorana_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0096](TFQ-0096_gap_einstein_equation_stays_q-held_for_this_finite-descent_program_and_is_not.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F000.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction`
