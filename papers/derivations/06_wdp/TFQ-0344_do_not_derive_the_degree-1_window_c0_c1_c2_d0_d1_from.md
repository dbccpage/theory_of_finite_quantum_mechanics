# [TFQ-0344] Do not derive the degree-1 window (C0, C1, C2, d0, d1) from

> **Stage**: `WDP` | **Status**: `GAP`  
> **UUID**: `f17ca273-1ed3-5bd8-8529-76250c3b36b8`  
> **Parent Derivation**: [TFQ-0343](TFQ-0343_leave_gen-wdp-o01_through_o05_open_carrier_floor_preservation_maps_higher_fillers_hilbert.md)

---

## 1. Abstract & Formal Statement

WDP-CH04-D01 defines a degree-1 window as a declared tuple (C0, C1, C2, d0, d1) of finite-dimensional spaces, with a certificate that d1 composed with d0 is zero. That certificate is automatic on the simplicial nerve route and required otherwise. The pregenesis segment note says no opened source derives this window from Genesis admission. DAG node PG-WDP-DEGREE1-WINDOW says the window is declared, not derived from the inert inscription or from Real_0. Route PG-R-GAP-GENESIS-TO-WINDOW has a later conditional label that this slice does not adopt while O01 and O02 stay open.

### Governing Obligation
Do not derive the degree-1 window (C0, C1, C2, d0, d1) from Genesis admission; a declared window stays an extra datum while O01 and O02 are open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Complex/chain structure d1 d0 = 0 (assumption: window hypothesis)`
- **Admitted**: `Finite carrier items (assumption)`
- **Admitted**: `Finite-dimensional real/complex vector space and norm J (assumption: declared)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The window is declared, not derived from <> or Real_0 (PG-GAP-GENESIS-TO-WINDOW). Geometry derivation belongs to the L1 emergence fragment.

> [!WARNING]
> Bridge obligation GEN-WDP-O01 (justify or explicitly admit the primitive-to-witness carrier, signature, law and challenge-generation floor) is open; the explicit admission is done, the stronger derivation is not.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_six_operations_and_primdiff_admission_gate`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::Repair`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::kappa`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/obstruction.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/obstruction.rs::Cochain1`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs::GenesisAdmissionKernel`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs::PrimitiveDifferenceAxiom`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs::TriadSignature`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0345](TFQ-0345_on_a_declared_window_with_d1_d0_0_compute_q1_kappa1.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
