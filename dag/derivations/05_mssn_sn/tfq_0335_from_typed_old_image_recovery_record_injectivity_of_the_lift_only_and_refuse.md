# [TFQ-0335] From typed old-image recovery, record injectivity of the lift only, and refuse

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `e5f79f78-4df5-5d3d-9750-460ba2d2e7d9`  
> **Parent Derivation**: [TFQ-0334](tfq_0334_let_one_supplied_binary_tag_separate_one_collapsed_pair_and_keep_the.md)

---

## 1. Abstract & Formal Statement

WDP-P001-005 records that typed old-image recovery implies injectivity of the lift, and that off-image rejection is not this row. WDP-P001-006 is the negative boundary: term recovery alone implies neither off-image rejection, observation preservation, nor obstruction repair. The DAG node PG-OLD-IMAGE-INJECTIVE carries the same split, including the negative symbols for off-image, observation, and repair. PG-SN-OFF-IMAGE-REFUSAL is a separate node for the domain-restriction half of WDP-P001-019. This slice does not promote either row. AuthorityEffect is None.

### Governing Obligation
From typed old-image recovery, record injectivity of the lift only, and refuse off-image rejection, observation preservation, and obstruction repair as consequences.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Domain-restriction (off-image refusal) half is separate; see PG-SN-OFF-IMAGE-REFUSAL.

> [!WARNING]
> Closes the domain-restriction half of WDP-P001-019; off-image points are refused by section-retraction roundtrip.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean::old_image_injective`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::off_image_not_implied`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean::old_image_injective`](../../code/lean4/)
- [`omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean::SnOffImage.accepted_only_from_section`](../../code/lean4/)
- [`omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean::SnOffImage.nonDescent_iff_off_image`](../../code/lean4/)
- [`omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean::SnOffImage.old_image_base'`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_sn_off_image_refusal_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/code/sn_mssn_checks.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0336](tfq_0336_keep_unequal_finite_alphabets_from_a_free_monoid_isomorphism_and_keep_language_restriction.md)
- [TFQ-0341](tfq_0341_refuse_unrestricted_old_image_recovery_and_the_advertised_sncarrier_cardinalities_until_a.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-OLD-IMAGE-INJECTIVE`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-OLD-IMAGE-INJECTIVE` (`PREGENESIS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-PREGENESIS-PG-OLD-IMAGE-INJECTIVE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [460, -920, 690]`, `chord_potential = 690`, `holonomy_gamma2 = 920`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-OLD-IMAGE-INJECTIVE): 4*idx(46) + 3*stage_rank(1) + route_degree(4) == 191` ($\text{value} = 191$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-OLD-IMAGE-INJECTIVE): R_raw(97) - G_cob(48) - S_decoy(1) == 48 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 48$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 06ae5b3d7f1f8a00988232f7d62bc4b9fdee5993cd638d56aee37078a2d6604c`
