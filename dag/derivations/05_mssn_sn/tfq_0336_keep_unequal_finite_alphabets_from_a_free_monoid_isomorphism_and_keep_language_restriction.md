# [TFQ-0336] Keep unequal finite alphabets from a free-monoid isomorphism, and keep language restriction,

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `3deab1ba-5279-5d87-b278-5c762367033a`  
> **Parent Derivation**: [TFQ-0335](tfq_0335_from_typed_old_image_recovery_record_injectivity_of_the_lift_only_and_refuse.md)

---

## 1. Abstract & Formal Statement

WDP-P001-007 records that free monoids on different finite alphabet sizes are nonisomorphic. WDP-P001-008 records that discrete categories of different finite object counts are inequivalent, with isomorphism classes as singletons. WDP-P001-009 records that language restriction, partial word recovery, and total erasure have different types, and that no Ext calculation is included. The DAG node PG-FREE-MONOID-NONISO cites the Pre-Genesis lines and Paper001.lean symbols no_free_monoid_iso and no_discrete_equivalence.

### Governing Obligation
Keep unequal finite alphabets from a free-monoid isomorphism, and keep language restriction, partial recovery, and total erasure as different types.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> none (finite-cardinality argument).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/lean4/Paper.lean`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/lean4/Paper.lean::unequal_finite_alphabets_not_iso`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/lean4/Paper001.lean`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/lean4/Paper001.lean::no_discrete_equivalence`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/lean4/Paper001.lean::no_free_monoid_iso`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/code/sn_mssn_checks.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0337](tfq_0337_record_homology_injectivity_under_a_chain_map_retraction_and_record_that_the_two_point.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-FREE-MONOID-NONISO`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-FREE-MONOID-NONISO` (`PREGENESIS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-PREGENESIS-PG-FREE-MONOID-NONISO`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [480, -960, 720]`, `chord_potential = 720`, `holonomy_gamma2 = 960`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-FREE-MONOID-NONISO): 4*idx(48) + 3*stage_rank(1) + route_degree(3) == 198` ($\text{value} = 198$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-FREE-MONOID-NONISO): R_raw(101) - G_cob(50) - S_decoy(1) == 50 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 50$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 039e66b0acd4fa614b6d181eefbf88777842eb06f09187ee619680326c8e8c86`
