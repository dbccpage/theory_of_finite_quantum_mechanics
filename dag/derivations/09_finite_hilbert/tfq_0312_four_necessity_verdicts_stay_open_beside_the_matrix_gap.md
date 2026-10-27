# [TFQ-0312] Four necessity verdicts stay open beside the matrix gap

> **Stage**: `FINITE_HILBERT` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `791b42e4-6447-5e86-b8d6-44203ea1dad6`  
> **Parent Derivation**: [TFQ-0311](tfq_0311_ordinary_matrix_algebra_over_c_is_not_recovered.md)

---

## 1. Abstract & Formal Statement

qm_122_finite_hilbert_boundary_from_primitive_difference.md, in the drop-one census, still marks four necessity verdicts open after the matrix gap is stated: CPTP channels, uniqueness of a Hilbert tensor, the circle group, and a Python dual of the named Lean statements. Gleason uniqueness at n at least 3 is the separate gap already recorded. The finite obligation here is not to upgrade those four open verdicts because a later finish table pairs them with host facts. The paper says that finish table is not a necessity theorem.

### Governing Obligation
Leave CPTP, Hilbert-tensor uniqueness, the circle, and a Python dual as open necessity verdicts.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Gleason: assumption`
- **Admitted**: `circle group: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> A selector for C / U(1) is not derived here. Detail in QM_028 / QM_062 (other segment).

> [!WARNING]
> The file's own header says candidate only; the status PROVED_LEAN follows the ledger and the existence of named theorems, not a rebuild by me.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011Circle.lean::sign_excluded_circle_still_imported`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011Circle.lean::sign_fails_connectedness_shadow`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011U1SelectorBoundary.lean::selector_not_free`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011U1SelectorBoundary.lean::u1_selector_boundary`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::born_nonuniqueness_open`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::pairing_exists`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::quartic_rival`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::uniqueness_not_discharged`](../../code/lean4/)
- [`lean4/quantum_mechanics/H017Finish.lean::two_label_host_not_gleason_dimension`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:ddaee3d0d77722244a6451750ca1e5acf7a57b4f02e75ecec70e810976d57d9e`](../../code/rust/src/)
- [`external:sha256:c8f020f9abf33d6d86e8630fd8f9d3da0bb1db91835d6dfcbe56cfa4709cad7e`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`sources/atlas/papers/quantum_foundations/_code/qm_122/qm122_lib/qm122_dual.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0313](tfq_0313_operator_algebra_shadow_slot_is_still_a_stub.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `external:sha256:ddbf8bad986fa5587b534c0f96f2c4ff370f95cb696c6245df0526d4bad32351`
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
  - `external:sha256:aa96a8bb76ae8bc4e83571f57783f369b645332421db0e1fdd8a7d9cf333aac9`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`GP-DROP-ONE-CENSUS`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `GP-DROP-ONE-CENSUS` (`FINITE_QM_CORE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-GP-DROP-ONE-CENSUS`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1330, -2660, 1995]`, `chord_potential = 1995`, `holonomy_gamma2 = 2660`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(GP-DROP-ONE-CENSUS): 4*idx(133) + 3*stage_rank(7) + route_degree(2) == 555` ($\text{value} = 555$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(GP-DROP-ONE-CENSUS): R_raw(301) - G_cob(147) - S_decoy(7) == 147 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 147$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 374275e6a39595624f7d1018264f20c1e8169e991f1f5ec47e29f82d56564ac7`
