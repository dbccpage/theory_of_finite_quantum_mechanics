# [TFQ-0167] Admit only exact nonnegative rational masses that sum to one, with no

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `9506a321-2f4b-5a02-81dd-8797abfb2f16`  
> **Parent Derivation**: [TFQ-0166](TFQ-0166_record_these_sibling_crates_as_controls_under_authorityeffect_none_not_as_completed.md)

---

## 1. Abstract & Formal Statement

Exact rational finite probability sits in omega_finite_probability, a library under the finite floor rather than a Hilbert derivation. src/lib.rs says masses, kernels, tables, and majorization data are BigRational, with no floating point and no tolerance. src/simplex.rs admits a ProbabilitySimplex only after nonnegativity and an exact sum of one, and it states that the law is classical and makes no Born-rule claim. The obligation is that a float, a tolerance, or a display conversion cannot authorize a finite probability. H001ProbabilitySimplex.lean is a separate candidate rung and is not this constructor.

### Governing Obligation
Admit only exact nonnegative rational masses that sum to one, with no float authority.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `declared sector decomposition and masses: assumption`
- **Admitted**: `nonnegative real mass assignment on witnesses: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The mass is declared. No source read derives the mass from Phi1, Gamma2 or from the cochain window.

> [!WARNING]
> On a fixed minimizer r* or under the dihedral symmetry-orbit selector (l1_even_cycle_symmetry_orbit_canonical_sector_weights), sector weights are uniquely determined and sum to Phi_1; without a selector, even cycles have multiple L1 minimizers.

> [!WARNING]
> none for the finite rational statement. Ledger-cited names PaperQF002 / L010_01_BornRedundancy were not found as modules; BornRedundancy.lean (axioms include Classical.choice per its header) is the located home.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornRedundancy.lean::listSum_normalize`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::normalize`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::normalize_idempotent`](../../code/lean4/)
- [`lean4/quantum_mechanics/BornRedundancy.lean::ray_quotient_classification`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.even_cycle_sector_weights_require_selector`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_even_cycle_symmetry_orbit_canonical_sector_weights`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.sector_weights_sum_to_phi1`](../../code/lean4/)
- [`lean4/quantum_mechanics/H001ProbabilitySimplex.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_finite_probability/src/finite_set.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_finite_probability/src/lib.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_finite_probability/src/simplex.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_finite_probability/src/simplex.rs::try_from_weights`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/residual_density_calculus.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_l1_sector_weights_and_density_lift_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche7_wdp_bridge_o03_o05_sector_orbit_and_gleason_rival_witness`](../../code/rust/src/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0168](TFQ-0168_keep_finite_joint_tables_and_classical_instruments_exact_with_no-signalling_questions_apart.md)
- [TFQ-0169](TFQ-0169_compare_finite_entropies_as_exact_rational_combinations_of_prime_logarithms_not_as.md)
- [TFQ-0170](TFQ-0170_keep_majorization_finite_markov_laws_and_row-stochastic_maps_on_exact_rational_kernels.md)
- [TFQ-0171](TFQ-0171_do_not_collapse_unnormalized_finite_valuations_into_the_normalized_rational_probability_simplex.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/floor.yaml`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-POSITIVE-WEIGHTS-ADMITTED`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-POSITIVE-WEIGHTS-ADMITTED` (`FINITE_QM_CORE` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-FQ-POSITIVE-L1-WEIGHT-ADMISSION`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [90, -180, 135]`, `chord_potential = 135`, `holonomy_gamma2 = 180`
- **Finite Shadow Exact Witness (`M4`)**: `sector_weight_partition_sum: w_A(17) + w_B(23) == Phi_1(40)` ($\text{value} = 40$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `even_cycle_C4_minimizer_nonuniqueness: two gauge-equivalent minimizers give sector weights (1,0) vs (0,1) with L1 difference |1-0| + |0-1| == 2` ($\text{value} = 2$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 321911a5814f23a096749af4f70a5fce75f686b981581fab5dd614958375d545`
