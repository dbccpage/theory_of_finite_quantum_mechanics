# [TFQ-0334] Let one supplied binary tag separate one collapsed pair, and keep the

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `77a1f49d-0908-5bc6-a9e2-32824362fd30`  
> **Parent Derivation**: [TFQ-0333](TFQ-0333_account_finite_demand_by_s_next_s_-_d_b_only.md)

---

## 1. Abstract & Formal Statement

WDP-P001-004 records that a supplied binary tag can separate one collapsed pair and retain the old report. Finding tags and satisfying many conflicts are separate questions. The DAG node PG-REFINE-SEPARATES points at the same Pre-Genesis section and at Paper001.lean symbol supplied_tag_separates. WDP-P001-003 is a negative boundary: the displayed seven-entry survivor sequence is a chosen ledger example, not a native law. Grammar files sn.ebnf and mssn.ebnf sit under 001_sn_mssn/code/grammar, and WDP-P001-014 says the MSS grammar has 22 listed public starts, which is not 22 completed semantic adapters.

### Governing Obligation
Let one supplied binary tag separate one collapsed pair, and keep the seven-entry survivor sequence and the 22 grammar starts from becoming laws.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Supplied tag (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Tag supply is an input; no derivation of which tag to supply.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::refine_separates`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::supplied_tag_separates`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/code/sn_mssn_checks.py`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/code/tests/test_sn_mssn_checks.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0335](TFQ-0335_from_typed_old-image_recovery_record_injectivity_of_the_lift_only_and_refuse.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-REFINE-SEPARATES`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-REFINE-SEPARATES` (`PREGENESIS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-PREGENESIS-PG-REFINE-SEPARATES`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [450, -900, 675]`, `chord_potential = 675`, `holonomy_gamma2 = 900`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-REFINE-SEPARATES): 4*idx(45) + 3*stage_rank(1) + route_degree(3) == 186` ($\text{value} = 186$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-REFINE-SEPARATES): R_raw(95) - G_cob(47) - S_decoy(1) == 47 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 47$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = d646677fb63e9f149cb6739f71c15de3e971982274cf90950cbb892845e778e8`
