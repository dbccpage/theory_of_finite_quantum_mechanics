# [TFQ-0108] GAP: caller-supplied Lambda is not the physical cosmological constant, and the grid

> **Stage**: `FINITE_QG` | **Status**: `GAP`  
> **UUID**: `2b681202-ff3f-5cfd-822b-34f570bca06a`  
> **Parent Derivation**: [TFQ-0107](TFQ-0107_gap_einstein_equation_and_physical_cosmological_constant_stay_unpaid_deficit_is_not.md)

---

## 1. Abstract & Formal Statement

quantum_regge_bridge.rs joins exact rational area-square eigenvalues to an integer Ponzano-Regge style weight and to a floating mini-superspace Wheeler-DeWitt grid. The grid potential uses caller-supplied curvature and Lambda parameters. A residual norm scores a supplied wave array; it does not solve cosmology. What is finite is the rational area map and a finite-difference stencil on a declared grid. What is not discharged is the Einstein equation, the physical cosmological constant, and the continuum limit. The toy grid is not quantum gravity and is not the rational proxy.

### Governing Obligation
GAP: caller-supplied Lambda is not the physical cosmological constant, and the grid does not discharge the Einstein equation.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_regge_bridge.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/spin_area_spectrum.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_ds_qm_dynamics_structure_and_majorana_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0109](TFQ-0109_ppn_endpoint_checks_do_not_discharge_regge_calculus_the_einstein_equation_or.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
