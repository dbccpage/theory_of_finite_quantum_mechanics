# [TFQ-0370] supplied-binary-refinement

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `c3d238af-7743-5a39-808f-065c7ebe6750`  
> **Parent Derivation**: [TFQ-0369](tfq_0369_finite_demand_count.md)

---

## 1. Abstract & Formal Statement

PG-REFINE-SEPARATES and ledger row WDP-P001-004 say a supplied binary tag can separate one collapsed pair while the old report is retained. Opened Paper.lean declares refine_separates, and preservation.refine pairs reports with tags. The tag is an input. Pre-Genesis paper.md section 9 is the heading. The finite statement still required is that finding which tag to supply, and satisfying many conflicts at once, stay separate questions and are not discharged by one pair. Chapter 3 says a comparison regime is declared data, not something read off two marks.

### Governing Obligation
One supplied binary tag may separate one collapsed pair and retain the old report; tag search and many conflicts stay open.

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
- [`declaration obligation: refine_separates, one supplied tag, one collapsed pair`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::refine_separates`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::supplied_tag_separates`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: a supplied-tag splitter in crate pre_mssn_preservation with the tag passed in, not chosen inside the function`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: preservation.refine must take the tag as an argument and must not search for a tag`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/preservation.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0371](tfq_0371_old_image_injective_lift.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch03_marks_presentations_and_declared_comparisons.md`

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
