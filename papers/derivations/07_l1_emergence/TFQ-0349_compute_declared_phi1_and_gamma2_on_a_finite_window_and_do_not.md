# [TFQ-0349] Compute declared Phi1 and Gamma2 on a finite window, and do not

> **Stage**: `L1_EMERGENCE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `7d92ecf2-0981-50ae-b43b-15af02bc16d9`  
> **Parent Derivation**: [TFQ-0345](../06_wdp/TFQ-0345_on_a_declared_window_with_d1_d0_0_compute_q1_kappa1.md)

---

## 1. Abstract & Formal Statement

DAG node L1-WDP-WINDOW-PHI1-GAMMA2 restates the declared window: Phi1 of a class is the quotient seminorm, the minimum of a weighted l1 norm of x minus d0 h, and Gamma2 is the l1 norm of d1 on a minimizer. The node says the weighted l1 form is declared, not derived from MSS-0 or from Difference, and it warns that WDP Gamma2 is a norm while a later QM note uses Gamma for a set of residual sectors. primitive_axiomatics.rs says Root P owns no arithmetic: d0 and d1 come from omega_homology, and Phi1, Gamma2, and the trichotomy come from omega_functional.

### Governing Obligation
Compute declared Phi1 and Gamma2 on a finite window, and do not treat the weighted l1 norm as derived from MSS-0.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Complex/chain structure d1 d0 = 0 (assumption: window hypothesis)`
- **Admitted**: `Finite-dimensional real/complex vector space and norm J (assumption: declared)`
- **Admitted**: `weighted l1 norm on C1 (declared, see L1-OBSERVER-AXIOMS-H1-H5): assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The weighted l1 form of the norm is declared in the window definition, not derived from MSS-0 or Difference. Upstream window construction is in the WDP fragment.

> [!WARNING]
> The window is declared, not derived from <> or Real_0 (PG-GAP-GENESIS-TO-WINDOW). Geometry derivation belongs to the L1 emergence fragment.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gs001_replica_and_phi1_quotient_invariance`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::Repair`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::kappa`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_functional/src/phi1.rs::Phi1Functional`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/obstruction.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/obstruction.rs::Cochain1`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/obstruction.rs::solve_exact_potential_weighted`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/phi1_coda_adapter.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs::TriadSignature`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0350](TFQ-0350_assume_d1_d0_0_only_by_a_declared_certificate_or_the.md)
- [TFQ-0352](TFQ-0352_admit_h1_through_h5_as_observer_hypotheses_on_a_finite_edge_projection.md)
- [TFQ-0357](TFQ-0357_record_replica_extensivity_as_a_reason_l1_appears_and_keep_squared_l2.md)
- [TFQ-0358](TFQ-0358_normalize_a_declared_positive_witness_mass_to_cell_values_that_are_nonnegative.md)
- [TFQ-0359](TFQ-0359_keep_the_phi1_banach-quotient_reading_on_a_finite-dimensional_repair_packet_and_leave.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
