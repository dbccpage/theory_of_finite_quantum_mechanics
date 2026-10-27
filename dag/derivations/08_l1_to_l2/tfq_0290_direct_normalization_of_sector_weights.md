# [TFQ-0290] Direct normalization of sector weights

> **Stage**: `L1_TO_L2` | **Status**: `SOURCE_RECORD`  
> **UUID**: `ab14bb13-d9d3-522a-929d-a2f72554c475`  
> **Parent Derivation**: [TFQ-0289](../09_finite_hilbert/tfq_0289_diagonal_density_with_coherences_unfixed.md)

---

## 1. Abstract & Formal Statement

In qm_020_born_normalization_and_conditional_hilbert_lift.md the section labeled Theorem 1 defines the unit-sum profile of a finite nonnegative weight vector with positive total by dividing by that total. The finite obligation is that profile: nonnegative coordinates summing to one, with a later probability reading treated as a separate adapter the paper says it does not supply. The claim ledger types this row as algebra that needs no Hilbert space. derivation_dag.json records the ids L1-QM020-THM1-DIRECT-NORMALIZATION and FQ-BORN-NORMALIZATION-REDUNDANCY beside it.

### Governing Obligation
Compute the unit-sum weight profile on a positive total without a Hilbert carrier.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Born/quadratic readout (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> none for the finite rational statement. Ledger-cited names PaperQF002 / L010_01_BornRedundancy were not found as modules; BornRedundancy.lean (axioms include Classical.choice per its header) is the located home.

> [!WARNING]
> The cited declarations live in lean4/original_lean_20260809/qm_l010_01_born_redundancy.lean (2,215 lines, Mathlib.Tactic import); repo-level lean4/quantum_mechanics copy is Mathlib-free but this extraction did not run a build. Zenodo 20683775 needs the narrowing erratum.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornRedundancy.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::listSum_normalize`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::normalize_idempotent`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::ray_quotient_classification`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:10accdc18b88414a6a931a9e7fc887c41090315925cc258605a210ae3a97c286::try_from_weights`](../../code/rust/src/)
- [`external:sha256:2367d7d43e194cf155298ace7054041ae444c67ab6cd71f51cc12cfacda6f3d4`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`sources/atlas/papers/quantum_foundations/_code/qm_020/code/qm_020_born_normalization_and_conditional_hilbert_lift_core.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0291](tfq_0291_disjoint_aggregation_and_the_real_p_1_import.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `external:sha256:ddbf8bad986fa5587b534c0f96f2c4ff370f95cb696c6245df0526d4bad32351`
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
  - `external:sha256:aa96a8bb76ae8bc4e83571f57783f369b645332421db0e1fdd8a7d9cf333aac9`
  - `external:sha256:eb788c5f48e4cc2ea2d3abdd7c4c0aaebe0b2b2edd084d6daf463e27df848c8b`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-QM020-THM1-DIRECT-NORMALIZATION`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-QM020-THM1-DIRECT-NORMALIZATION` (`L1_TO_L2` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-L1_TO_L2-L1-QM020-THM1-DIRECT-NORMALIZATION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [810, -1620, 1215]`, `chord_potential = 1215`, `holonomy_gamma2 = 1620`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-QM020-THM1-DIRECT-NORMALIZATION): 4*idx(81) + 3*stage_rank(6) + route_degree(7) == 349` ($\text{value} = 349$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-QM020-THM1-DIRECT-NORMALIZATION): R_raw(192) - G_cob(93) - S_decoy(6) == 93 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 93$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = c094685cfa33f2ef01e97ebdc58be439beae89a442c1037059eacd9b5d3fcadf`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-BORN-NORMALIZATION-REDUNDANCY`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-BORN-NORMALIZATION-REDUNDANCY` (`FINITE_QM_CORE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-FQ-BORN-NORMALIZATION-REDUNDANCY`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1010, -2020, 1515]`, `chord_potential = 1515`, `holonomy_gamma2 = 2020`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-BORN-NORMALIZATION-REDUNDANCY): 4*idx(101) + 3*stage_rank(7) + route_degree(4) == 429` ($\text{value} = 429$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-BORN-NORMALIZATION-REDUNDANCY): R_raw(237) - G_cob(115) - S_decoy(7) == 115 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 115$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = c52fa38dbe320d4d849d276768eeb99853785e707c1b023e853e20ccc34cd324`
