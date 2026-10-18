# [TFQ-0092] QM-110-C11 Hamiltonian constraint stays Q-held. Continuum SU(2) data in QM-110-C10 are imported,

> **Stage**: `FINITE_QG` | **Status**: `TOY_CARRIER`  
> **UUID**: `65a38ccf-82c8-586f-bf29-ef5a968453c9`  
> **Parent Derivation**: [TFQ-0091](TFQ-0091_finite_loop_words_stay_on_the_declared_graph_continuum_connection_and_the.md)

---

## 1. Abstract & Formal Statement

QM-110 records finite-descent shadows of selected loop-gravity motifs on toy carriers. Pure-gauge loops have trivial holonomy, the Q8 plaquette Wilson value differs from 1, abelian gauge sits in the image of d0, a single cycle has first-cohomology rank one, and flux fails to commute with holonomy on that finite group. Area labels use an imported eigenvalue. What is finite is Q8 with finite cycles. What is not discharged is SU(2) representation theory, the spin-network Hilbert space, the area scale, and the Hamiltonian constraint, left Q-held. Q8 is not SU(2), and this packet is not quantum gravity.

### Governing Obligation
QM-110-C11 Hamiltonian constraint stays Q-held. Continuum SU(2) data in QM-110-C10 are imported, not discharged.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/spin_area_spectrum.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_ds_qm_dynamics_structure_and_majorana_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0093](TFQ-0093_imported_area_scale_and_casimir_stay_unpaid_the_einstein_equation_and_smooth.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
