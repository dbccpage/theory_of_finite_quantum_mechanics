# [TFQ-0371] old-image-injective-lift

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `707d9ae7-10da-5964-ac23-973bd75471b7`  
> **Parent Derivation**: [TFQ-0370](tfq_0370_supplied_binary_refinement.md)

---

## 1. Abstract & Formal Statement

PG-OLD-IMAGE-INJECTIVE and ledger row WDP-P001-005 say that if a lift has a typed recovery of old terms on the old image, then the lift is injective. Opened Paper.lean declares old_image_injective. Ledger row WDP-P001-006 says term recovery alone yields neither off-image rejection, nor observation preservation, nor obstruction repair. Pre-Genesis paper.md section 10 is the heading. The finite statement still required is injectivity on that old image only, with the three negative boundaries left standing. Declaration ground_carrier_empty on Carrier 0 is a separate empty-ground fact.

### Governing Obligation
Typed recovery of old terms on the old image yields injectivity of that lift, and does not yield off-image rejection, observation preservation, or repair.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Domain-restriction (off-image refusal) half is separate; see PG-SN-OFF-IMAGE-REFUSAL.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`declaration obligation: old_image_injective, scoped to typed recovery on the old image`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/lean4/Paper.lean`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/lean4/Paper.lean::old_image_injective`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/lean4/Paper001.lean::off_image_not_implied`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/lean4/Paper001.lean::old_image_injective`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: old-image injectivity in crate pre_mssn_preservation, with the three negative boundaries as separate tests`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: an injectivity check for recover_word on the old alphabet that does not also claim off-image refusal`](../../code/python/)
- [`atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/code/preservation.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0372](tfq_0372_off_image_refusal_half.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `external:sha256:e9771151ef2b40fcf062ad0b03605ecdd55eb43a1deb26c90a245b012e93bf2a`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-SN-OFF-IMAGE-REFUSAL`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-SN-OFF-IMAGE-REFUSAL` (`PREGENESIS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-PREGENESIS-PG-SN-OFF-IMAGE-REFUSAL`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [470, -940, 705]`, `chord_potential = 705`, `holonomy_gamma2 = 940`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-SN-OFF-IMAGE-REFUSAL): 4*idx(47) + 3*stage_rank(1) + route_degree(2) == 193` ($\text{value} = 193$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-SN-OFF-IMAGE-REFUSAL): R_raw(99) - G_cob(49) - S_decoy(1) == 49 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 49$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `education/symmetric_group_presentations/lean4/SnOffImage.lean::SnOffImage.old_image_base'`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 8d6d5d053ab2b9a671bbc4aaf2a937bf15ec0d50223cd3bde06e0aed78422f65`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-OLD-IMAGE-INJECTIVE`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-OLD-IMAGE-INJECTIVE` (`PREGENESIS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-PREGENESIS-PG-OLD-IMAGE-INJECTIVE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [460, -920, 690]`, `chord_potential = 690`, `holonomy_gamma2 = 920`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-OLD-IMAGE-INJECTIVE): 4*idx(46) + 3*stage_rank(1) + route_degree(4) == 191` ($\text{value} = 191$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-OLD-IMAGE-INJECTIVE): R_raw(97) - G_cob(48) - S_decoy(1) == 48 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 48$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 06ae5b3d7f1f8a00988232f7d62bc4b9fdee5993cd638d56aee37078a2d6604c`
