# [TFQ-0345] On a declared window with d1 d0 = 0, compute Q1, kappa1,

> **Stage**: `WDP` | **Status**: `SOURCE_RECORD`  
> **UUID**: `c4b0a474-e424-5bcc-b287-8b15bdb21de9`  
> **Parent Derivation**: [TFQ-0344](tfq_0344_do_not_derive_the_degree_1_window_c0_c1_c2_d0_d1_from.md)

---

## 1. Abstract & Formal Statement

WDP-CH04-D02, once a window and a norm J are declared, sets Q1 = C1/im(d0), kappa1 of a class to d1 h, H1 to the kernel of kappa1, Phi1 to the quotient defect, Gamma2 to the L1 norm of d1 h, and R_cl to Gamma2/Phi1 when Phi1 is positive. Diagnostic classes are ExactClass, ClosedResidual, and ActiveClosureFailure, with a typed NoRule refusal for missing or ill-typed window data. WDP-CH04-P03 states that if d1 d0 is zero then kappa1 is well defined and the sequence 0 to H1 to Q1 to im(d1) to 0 is exact, with no canonical splitting. The parent gap means this tuple is not a Genesis theorem.

### Governing Obligation
On a declared window with d1 d0 = 0, compute Q1, kappa1, H1, Phi1, Gamma2, and R_cl, and refuse a missing window with NoRule.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Norm hypothesis over R, C, or Q restricted from the real extension (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Ledger rows carry prose (P03) and prose plus computed (P04, P05) bindings, no L: binding. Lean symbols with matching names exist in Obstruction.lean (not checked against statements); they cover the exact sequence and ratio bounds at the symbols named, not necessarily every clause (claim_map.md not re-checked row by row).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::closure_ratio_le_opnorm`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::closure_ratio_nonneg`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::kappa_exact_sequence`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::kappa_well_defined`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_wdp_obligations_and_growth_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/cochains.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/obstruction.rs`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0346](tfq_0346_do_not_lower_phi1_by_passing_to_a_larger_complex_attaching_faces.md)
- [TFQ-0347](tfq_0347_keep_exactclass_closedresidual_and_activeclosurefailure_off_the_routing_terminal_and_leave.md)
- [TFQ-0348](tfq_0348_certify_a_rational_phi1_value_by_a_bounded_circulation_that_meets_a.md)
- [TFQ-0349](../07_l1_emergence/tfq_0349_compute_declared_phi1_and_gamma2_on_a_finite_window_and_do_not.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-WDP-QUOTIENT-EXACT-SEQUENCE`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-WDP-QUOTIENT-EXACT-SEQUENCE` (`WDP` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-WDP-PG-WDP-QUOTIENT-EXACT-SEQUENCE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [650, -1300, 975]`, `chord_potential = 975`, `holonomy_gamma2 = 1300`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-WDP-QUOTIENT-EXACT-SEQUENCE): 4*idx(65) + 3*stage_rank(4) + route_degree(5) == 277` ($\text{value} = 277$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-WDP-QUOTIENT-EXACT-SEQUENCE): R_raw(150) - G_cob(73) - S_decoy(4) == 73 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 73$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = fee8023c81762ae519473827c2e8202b27c86a4a6d901df1cfb03f8bf331c0c2`
