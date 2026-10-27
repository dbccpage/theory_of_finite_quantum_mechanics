# [TFQ-0260] Bell theorem not derived from the finite tables

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `GAP`  
> **UUID**: `f73024e7-7f58-5804-ba23-688556c84148`  
> **Parent Derivation**: [TFQ-0259](tfq_0259_finite_chsh_ceiling_on_one_global_joint_table.md)

---

## 1. Abstract & Formal Statement

QM_073 states that Bell's theorem proper, with locality, measurement independence, and continuum observables, is obstructed clause by clause, and that no quantum nonlocality or Tsirelson bound is derived there. DS-QM073-BELL-THEOREM-OBSTRUCTED says there is no derivation of quantum violation or of the Tsirelson bound from the finite tables, and the reading note names this Bell-theorem node as a gap. Ledger rows FQM-B3 and FQM-B4 record a scoped sum-of-squares certificate and a static real witness under stated premises, while FQM-B5 fences the Bell endpoint as using supplied composition, an entangled state.

### Governing Obligation
Do not derive a Bell theorem or a Tsirelson bound from the finite joint tables; scoped certificates stay conditional on their stated inputs.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Hilbert tensor structure and quantum states (assumption)`
- **Admitted**: `bipartite tensor carrier (assumption)`
- **Admitted**: `entangled state (assumption)`
- **Admitted**: `tensor composition, entangled preparation, trace/Born pairing (assumption)`
- **Admitted**: `trace/Born pairing (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Four-tier CHSH squared separation (100 < 196 < 200 < 400) is mechanized; physical Bell nonlocality remains conditional on measurement independence and locality admissions.

> [!WARNING]
> Lean theorem is the attainment (existential over Z[sqrt2] vectors), not the operator SOS bound; SOS certificate is in the Rust QM-218 control.

> [!WARNING]
> Scaled CHSH value 70 = 25 * (14/5) > 50 = 2 * 25 and the non-existence of any non-negative joint weight list of mass 25 achieving 70 are mechanized in DerivationDagQMClosure.lean.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm073_bell_chsh_pythagorean_tsirelson_vs_pr_box_and_local_bound`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_bell_rational_violation_14_5_no_joint_law`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition`](../../code/lean4/)
- [`lean4/quantum_mechanics/H053EverettForkingTree.lean::chsh_pythagorean_quantum_value`](../../code/lean4/)
- [`lean4/quantum_mechanics/H064ContextualityThresholds.lean::conductor_24_contains_sqrt2`](../../code/lean4/)
- [`lean4/quantum_mechanics/QuantumCorrelation.lean::q1_violates_classical_bound`](../../code/lean4/)
- [`lean4/quantum_mechanics/QuantumCorrelation.lean::q2_tsirelson_attainment`](../../code/lean4/)
- [`sources/atlas/papers/finite_quantum_mechanics/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:436c024d77fc3479e5ac42ac8b0fc5e0884fa46295d995abb94d20d477c5c9cc::FiniteBellProblem`](../../code/rust/src/)
- [`external:sha256:3aa68d6116ce374efc50eed1e23d148aaae1be854b3bf16be67d8d1ab42dceb4`](../../code/rust/src/)
- [`external:sha256:3aa68d6116ce374efc50eed1e23d148aaae1be854b3bf16be67d8d1ab42dceb4::chsh_witness`](../../code/rust/src/)
- [`external:sha256:24f64c814749a499091a6ff28d77985d0a958f2c7d61551981693687b67f45a9::evaluate_qm218_page_wootters_tsirelson_wigner`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-BELL-RATIONAL-VIOLATION-14-5`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-BELL-RATIONAL-VIOLATION-14-5` (`FINITE_QM_CORE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_CORE-FQ-BELL-RATIONAL-VIOLATION-14-5`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1150, -2300, 1725]`, `chord_potential = 1725`, `holonomy_gamma2 = 2300`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-BELL-RATIONAL-VIOLATION-14-5): 4*idx(115) + 3*stage_rank(7) + route_degree(3) == 484` ($\text{value} = 484$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-BELL-RATIONAL-VIOLATION-14-5): R_raw(265) - G_cob(129) - S_decoy(7) == 129 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 129$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_bell_rational_violation_14_5_no_joint_law`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 4193e1dc12f0a1729fb73556178c8e423405d88ba671738b100f7163766b191f`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM073-BELL-THEOREM-OBSTRUCTED`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM073-BELL-THEOREM-OBSTRUCTED` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM073-BELL-THEOREM-OBSTRUCTED`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1540, -3080, 2310]`, `chord_potential = 2310`, `holonomy_gamma2 = 3080`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM073-BELL-THEOREM-OBSTRUCTED): 4*idx(154) + 3*stage_rank(8) + route_degree(2) == 642` ($\text{value} = 642$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM073-BELL-THEOREM-OBSTRUCTED): R_raw(348) - G_cob(170) - S_decoy(8) == 170 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 170$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `sources/atlas/papers/finite_quantum_mechanics/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm073_diagonal_exchange_suppression_and_bell_three_clause_obstruction`
- **Sovereign Rust Witness Anchor**: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs::verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 9a9512e080757f9c8d5380614c90c2568f417326b35f29a7a8acc4f434f5b059`
