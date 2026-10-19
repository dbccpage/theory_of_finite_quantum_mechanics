# [TFQ-0259] Finite CHSH ceiling on one global joint table

> **Stage**: `FINITE_QM_STRUCTURE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `ac7762b6-724e-5798-b685-a87c1426e2fa`  
> **Parent Derivation**: [TFQ-0256](tfq_0256_product_defect_on_a_bipartite_weight_table.md)

---

## 1. Abstract & Formal Statement

QM_073 obliges a finite CHSH ceiling when correlators come from one global joint table of sign-valued windows: the combination lies in the closed interval from minus two to two. The same pages say a Bell-state descent and a classical mixture can share a table, so the table grade does not exhibit entanglement. DS-QM073-FINITE-CHSH-AND-PR-BOX records bare-table separability, the ceiling two, and a PR-box value four with no joint extension. The load-bearing hypothesis is the single global table.

### Governing Obligation
Keep the finite CHSH ceiling attached to one global joint table, and keep any larger rational value on a separately supplied model.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `locality and setting independence for physical reading (assumption)`
- **Admitted**: `positive normalized joint law (assumption)`
- **Admitted**: `tensor composition, entangled preparation, trace/Born pairing (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> None (finite CHSH bound, bare-table separability, and PR-box non-extension mechanized in ds_qm073_bare_table_separability_single_joint_bound_and_pr_box_obstruction and ds_qm073_074_chsh_pr_box_and_no_signaling_marginal).

> [!WARNING]
> Both the 16 deterministic assignments in {-2, 2} and the inductive convexity step over arbitrary non-negative weight lists are mechanized in DerivationDagQMClosure.lean.

> [!WARNING]
> Scaled CHSH value 70 = 25 * (14/5) > 50 = 2 * 25 and the non-existence of any non-negative joint weight list of mass 25 achieving 70 are mechanized in DerivationDagQMClosure.lean.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/ContextualityObstruction.lean::x1_has_no_global_section`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm073_074_chsh_pr_box_and_no_signaling_marginal`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm073_bare_table_separability_single_joint_bound_and_pr_box_obstruction`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm073_bell_chsh_pythagorean_tsirelson_vs_pr_box_and_local_bound`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_bell_classical_joint_extension_convex_bound`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_bell_rational_violation_14_5_no_joint_law`](../../code/lean4/)
- [`lean4/quantum_mechanics/H053EverettForkingTree.lean::chsh_classical_bound`](../../code/lean4/)
- [`lean4/quantum_mechanics/H053EverettForkingTree.lean::chsh_pythagorean_quantum_value`](../../code/lean4/)
- [`lean4/quantum_mechanics/QuantumCorrelation.lean::classical_chsh_bound`](../../code/lean4/)
- [`lean4/quantum_mechanics/QuantumCorrelation.lean::q1_violates_classical_bound`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm073_bare_table_separability_single_joint_bound_and_pr_box_obstruction`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs::verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/finite_bell_extension.rs::FiniteBellProblem`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/finite_chsh_correlations.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/finite_chsh_correlations.rs::JointAssignment`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/finite_chsh_correlations.rs::chsh_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche4_edgewise_l1_u1_holonomy_chsh_and_cayley_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/tests/omega_quantum_physics/finite_bell_extension.rs::finite_bell_extension`](../../code/rust/src/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs::verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0260](tfq_0260_bell_theorem_not_derived_from_the_finite_tables.md)
- [TFQ-0261](tfq_0261_no_signalling_marginals_under_an_admitted_composition.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM073-FINITE-CHSH-AND-PR-BOX`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM073-FINITE-CHSH-AND-PR-BOX` (`FINITE_QM_STRUCTURE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM073-FINITE-CHSH-AND-PR-BOX`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1530, -3060, 2295]`, `chord_potential = 2295`, `holonomy_gamma2 = 3060`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM073-FINITE-CHSH-AND-PR-BOX): 4*idx(153) + 3*stage_rank(8) + route_degree(4) == 640` ($\text{value} = 640$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM073-FINITE-CHSH-AND-PR-BOX): R_raw(346) - G_cob(169) - S_decoy(8) == 169 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 169$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm073_bare_table_separability_single_joint_bound_and_pr_box_obstruction`
- **Sovereign Rust Witness Anchor**: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs::verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = c352cde616ae3f39af6f81ce4aae53e78a2a5cd8390e394a3bc752f046b08992`
