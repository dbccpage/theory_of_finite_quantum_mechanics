# [TFQ-0308] Born-uniqueness band slot is still a stub

> **Stage**: `FINITE_HILBERT` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `462d8349-de7a-5c7a-b0d0-09e386b22fa7`  
> **Parent Derivation**: [TFQ-0307](tfq_0307_gleason_route_for_dimension_at_least_three.md)

---

## 1. Abstract & Formal Statement

qm_204_born_uniqueness_import_boundary.md and its claim ledger leave QM_204-C0 as a reserved band slot with stub status. The finite obligation is open: the boundary is named, and the slot does not yet carry a self-contained finite certificate separating redundant normalization from uniqueness. Until that slot is written, the working statement stays the conditional section in qm_020 and the leftover list in qm_122, not a new discharge. FiniteQM.lean separates five rational import predicates by countermodels, which is a different and narrower check than Gleason at n at least 3. AuthorityEffect is None.

### Governing Obligation
Leave the QM_204 slot open while it is only a reserved band, and do not promote it.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/FiniteQM.lean`](../../code/lean4/)

### Sovereign Rust Certifiers
*Computational witness tracked under `theory_of_finite_qm` crate.*

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0309](tfq_0309_ingredient_ladder_stops_before_the_imported_ceiling.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `external:sha256:ddbf8bad986fa5587b534c0f96f2c4ff370f95cb696c6245df0526d4bad32351`
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
  - `external:sha256:aa96a8bb76ae8bc4e83571f57783f369b645332421db0e1fdd8a7d9cf333aac9`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-FIVE-IMPORT-PROXY-SEPARATION`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-FIVE-IMPORT-PROXY-SEPARATION` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-FQ-FIVE-IMPORT-PROXY-SEPARATION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1050, -2100, 1575]`, `chord_potential = 1575`, `holonomy_gamma2 = 2100`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-FIVE-IMPORT-PROXY-SEPARATION): 4*idx(105) + 3*stage_rank(8) + route_degree(2) == 446` ($\text{value} = 446$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-FIVE-IMPORT-PROXY-SEPARATION): R_raw(250) - G_cob(121) - S_decoy(8) == 121 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 121$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 2a0d78d22e0ec9123838c87bde358aff8ff9aa3eeec116e276f54f44c707b450`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1520, -3040, 2280]`, `chord_potential = 2280`, `holonomy_gamma2 = 3040`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED): 4*idx(152) + 3*stage_rank(8) + route_degree(3) == 635` ($\text{value} = 635$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED): R_raw(344) - G_cob(168) - S_decoy(8) == 168 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 168$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `sources/atlas/papers/finite_quantum_mechanics/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm072_bit_shadow_q1_q4_obstruction_and_p7_c10_bloch_refutation`
- **Sovereign Rust Witness Anchor**: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs::verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 03529c7cea05de107b256ab9d02734a69f338c379a63d1085c416314eb593d1e`
