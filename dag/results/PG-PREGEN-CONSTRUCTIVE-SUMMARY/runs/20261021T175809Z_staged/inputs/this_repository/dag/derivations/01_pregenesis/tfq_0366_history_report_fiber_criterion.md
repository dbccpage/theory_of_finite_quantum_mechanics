# [TFQ-0366] history-report-fiber-criterion

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `a6075523-4bdf-5bde-987e-6b0cbaba4a64`  
> **Parent Derivation**: [TFQ-0365](tfq_0365_collapsed_observation_barrier.md)

---

## 1. Abstract & Formal Statement

Opened PreMssn.history_report_criterion in 000_pre_genesis_to_mssn/lean4/Paper.lean says a question factors through the report image exactly when it is constant on report fibers, and the file header says Classical.choice is used for arbitrary report images. history_factor_unique is the companion declaration. DAG node PG-HISTORY-REPORT-CRITERION and ledger rows WDP-P000-005 and WDP-P001-018 record that image-restricted criterion. The finite statement still required is to keep the choice-using direction for unlisted images separate from a listed population.

### Governing Obligation
A question over histories factors through the realized report image exactly when it is constant on report fibers, and the factor is unique on that image.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Classical.choice (assumption: in Paper.lean, per its header comment)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Constructive version for explicitly listed histories is the Fable 04 target (PG-PREGEN-CONSTRUCTIVE-SUMMARY).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`declaration obligation: history_report_criterion and history_factor_unique, with Classical.choice left visible on the unlisted direction`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::history_factor_unique`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::history_report_criterion`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Descent.lean::function_descends_iff_fiber_constant`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/ProposalAdmissionBridge.lean::factorization_iff_fiber_constancy`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::descent_unique`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::exists_descent_of_constant`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: a report-factor checker in crate pre_mssn_preservation that refuses answers outside the realized image`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_category_theory/src/finite_report_query.rs::FactorizationCertificate`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: preservation.report_factor must be checked against fiber constancy and must return no factor off the image`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/preservation.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0367](tfq_0367_listed_history_choice_free_summary.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch05_descent_versus_selected_representatives.md`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-PREGEN-CONSTRUCTIVE-SUMMARY`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-PREGEN-CONSTRUCTIVE-SUMMARY` (`PREGENESIS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-PREGENESIS-PG-PREGEN-CONSTRUCTIVE-SUMMARY`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [430, -860, 645]`, `chord_potential = 645`, `holonomy_gamma2 = 860`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-PREGEN-CONSTRUCTIVE-SUMMARY): 4*idx(43) + 3*stage_rank(1) + route_degree(3) == 178` ($\text{value} = 178$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-PREGEN-CONSTRUCTIVE-SUMMARY): R_raw(91) - G_cob(45) - S_decoy(1) == 45 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 45$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `omega_engine_education/documentation/000_oepregen/lean4/ListedHistorySummary.lean::PreMssnListed.fiberConstant_of_recon`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = fda142091b847ff0c9c4270c0e46dab4eb5e4c01a012932242a083aea2e01ed9`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-HISTORY-REPORT-CRITERION`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-HISTORY-REPORT-CRITERION` (`PREGENESIS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-PREGENESIS-PG-HISTORY-REPORT-CRITERION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [420, -840, 630]`, `chord_potential = 630`, `holonomy_gamma2 = 840`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-HISTORY-REPORT-CRITERION): 4*idx(42) + 3*stage_rank(1) + route_degree(4) == 175` ($\text{value} = 175$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-HISTORY-REPORT-CRITERION): R_raw(89) - G_cob(44) - S_decoy(1) == 44 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 44$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 372962f855ce75bf587cc6128526aa84366ad2436b7403c45dcf24c53a398c9d`
