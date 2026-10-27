# [TFQ-0291] Disjoint aggregation and the real p>1 import

> **Stage**: `L1_TO_L2` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `d7832be5-6ffb-5b12-a45f-93bdb0319e30`  
> **Parent Derivation**: [TFQ-0290](tfq_0290_direct_normalization_of_sector_weights.md)

---

## 1. Abstract & Formal Statement

qm_020_born_normalization_and_conditional_hilbert_lift.md separates an l1 coordinate defect from a strict comparison for exponents above one on disjoint supports. The finite obligation on the rational side is the sign defect: the coordinate triangle defect vanishes when the two entries are not of opposite sign, which is the fragment BornRedundancy.lean actually states. The claim ledger says the real-exponent comparison is prose and that Lean hardens a rational defect plus natural-exponent cases.

### Governing Obligation
Keep the rational sign defect in the finite file and import real p>1 subadditivity.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `real analysis (Minkowski, strict convexity): assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Real-exponent p>1 is node L1-QM020-THM2B-MINKOWSKI. Lean covers integer D1 only.

> [!WARNING]
> Not mechanized.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornRedundancy.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::D1_zero_iff_mul_nonneg`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::D1_zero_iff_same_sign`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_minkowski_sqrt_decoherence_and_scoped_custody_witness`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0292](tfq_0292_square_root_field_for_amplitude_coordinates.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `external:sha256:ddbf8bad986fa5587b534c0f96f2c4ff370f95cb696c6245df0526d4bad32351`
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
  - `external:sha256:aa96a8bb76ae8bc4e83571f57783f369b645332421db0e1fdd8a7d9cf333aac9`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-QM020-THM2A-L1-ADDITIVITY-DEFECT`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-QM020-THM2A-L1-ADDITIVITY-DEFECT` (`L1_TO_L2` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-L1_TO_L2-L1-QM020-THM2A-L1-ADDITIVITY-DEFECT`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [820, -1640, 1230]`, `chord_potential = 1230`, `holonomy_gamma2 = 1640`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-QM020-THM2A-L1-ADDITIVITY-DEFECT): 4*idx(82) + 3*stage_rank(6) + route_degree(4) == 350` ($\text{value} = 350$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-QM020-THM2A-L1-ADDITIVITY-DEFECT): R_raw(194) - G_cob(94) - S_decoy(6) == 94 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 94$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 4fe72910799e415a738a75b2984783aed5f3f19afb445ddf31efcdf6a1a750da`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-QM020-THM2B-MINKOWSKI`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-QM020-THM2B-MINKOWSKI` (`L1_TO_L2` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-L1-MINKOWSKI-LP-SUBADDITIVITY`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [340, -680, 510]`, `chord_potential = 510`, `holonomy_gamma2 = 680`
- **Finite Shadow Exact Witness (`M4`)**: `l1_disjoint_support_exact_additivity: ||u+v||_1 = 3 + 4 == 7 == ||u||_1 + ||v||_1` ($\text{value} = 7$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `minkowski_l2_strict_subadditivity_gap: (||u||_2 + ||v||_2)^2 - ||u+v||_2^2 = (3+4)^2 - (9+16) = 49 - 25 == 24 > 0` ($\text{value} = 24$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = d4c7ab4348440b1e5e699cbc22ebad8945d9d932a82475e633277730ca2d28ac`
