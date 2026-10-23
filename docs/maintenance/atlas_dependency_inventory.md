# Atlas dependency inventory

**AuthorityEffect:** None. This page is a report. It changes no node status and copies no file out of the sibling tree.

Generated 2026-10-22 by [`dag/research/lean_replay_campaign/atlas_inventory.py`](../../dag/research/lean_replay_campaign/atlas_inventory.py) and `atlas_inventory_md.py` from this checkout, read-only against the sibling checkout `the_symbol_game` (the tree that holds `omega_engine*` and the atlas folders). The machine-readable list is [`atlas_dependency_inventory.json`](atlas_dependency_inventory.json): one entry per distinct path, with whether it exists in the atlas, its size, its kind and which kinds of file here cite it.

## What was scanned

- 103300 text files of this checkout (`.py .rs .toml .md .json .jsonl .yaml .lean .txt ...`), 9711 of which name a sibling-tree path. `lean4/Imported/` (provenance headers), the campaign tools and this page are not scanned.
- 3382 distinct paths: 1988 exist in the sibling working tree, 223 existed until sibling commit `3379759468` removed them (see the next section), and 1161 are not files of the sibling tree at any commit examined (historical names, moved files, directories, or prose fragments that look like paths).
- Reference classes: node fields (`source`, `rust`, `lean`) and record fields (`lean4`, `rust`, `python`) of `dag/derivation_dag.json`; the fragments that generate them; generated derivation papers and views; `dag/results/**` (sealed run artifacts that quote the paths of their inputs); `code/**`; `papers/**`; `scripts/**`; `lean4/**`; `docs/**`.
- Records also carry 1531 provenance strings (`f004_refs`, `coda_atlas_paths`) that name atlas files as the origin of a record. They are left as they are; they are history, not a dependency a tool resolves.

## The sibling tree changed while this was being done

Sibling commit `3379759468` ("Remove seven F004 paper families from the atlas tree", 2026-10-22 17:52 -0400, on the sibling branch `chore/remove-woland-digests`) deleted `003_quantum_foundations`, `004_general_relativity`, `006_finite_qm`, `007_finite_to_continuum`, `008_fsp`, `009_ms_majorana`, `010_mub6` under `omega_engine_atlas/coda_atlas/F004_papers/` from the working tree. 223 files that this checkout names existed there; 129 of them are cited by live files (3.5 MB). They are still in the sibling's git history (`git -C the_symbol_game show 3379759468^:<path>`). The Lean files this change imported all come from families that were not removed, so the import and the replay are unaffected; the references that now dangle are the `source`, `rust` and `python` citations of nodes and records that quote the removed families. The inventory below counts those as *removed*, not as missing.

## Where the references are

| Reference class | references | distinct paths |
|---|---|---|
| dag/results (sealed run artifacts) | 10829 | 764 |
| dag generated views and derivation papers | 2980 | 778 |
| dag other (operads, research, pfp, tools) | 2474 | 1577 |
| code/** | 1777 | 788 |
| papers/** | 938 | 555 |
| dag nodes/records/routes (derivation_dag.json) | 605 | 605 |
| dag provenance strings (history) | 308 | 308 |
| dag fragments (sync inputs) | 190 | 190 |
| other | 81 | 37 |
| docs/** | 6 | 6 |
| lean4/** | 4 | 4 |

*dag provenance strings (history)* are the `f004_refs`, `coda_atlas_paths` and `coda_atlas_ids` values of records and fragments. They say where a record came from and are excluded from every *live* count below.

A reference in a generated paper or view, or in a sealed run artifact, follows from a reference in `dag/derivation_dag.json`, its fragments or a sealed input and is not a separate dependency.

## What Part 1 imported

All 236 Lean files that DAG nodes and records cite outside this repository, together with their local (non-Mathlib) imports, were copied to `lean4/Imported/<package>/<path under the package root>.lean` and registered as the non-default library `ImportedAtlas` in `lean4/lakefile.lean`. 97 are cited directly; the others are dependencies. The package folder disambiguates files that share a stem in different atlas papers (`Paper.lean`, `Same.lean`, `SnTheorems.lean`, `Core.lean`). Every file carries a header with its original path, original sha256 and the import date. All 236 compile under Lean 4.35.0 with Mathlib `56a005855ea17e0b0958f73ec801ae140b0a1679`; 1 needed a port for version drift (`Imported/GenesisOngoing/Second/Rename.lean`), recorded in its header and in [`lean4/Imported/import_manifest.json`](../../lean4/Imported/import_manifest.json). None contains `sorry`, `admit`, `axiom`, `native_decide` or `unsafe`.

| Package (atlas path of the Lean root) | files |
|---|---|
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/029_the_anomalon_boundary/lean4` -> `lean4/Imported/AnomalonBoundary/` | 1 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/009_conditional_density_lift_and_dual_witness_xi_functional/lean4` -> `lean4/Imported/ConditionalDensityLift/` | 1 |
| `omega_engine_atlas/coda_atlas/F004_papers/002_projection_obstruction/009_coordinate_wise_additivity/lean4` -> `lean4/Imported/CoordinateWiseAdditivity/` | 2 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4` -> `lean4/Imported/Genesis19l57g1/` | 80 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4` -> `lean4/Imported/GenesisOngoing/` | 83 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4_core` -> `lean4/Imported/GenesisOngoingCore/` | 28 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/003_l1_obstruction_framework/lean4` -> `lean4/Imported/L1ObstructionFramework/` | 2 |
| `omega_engine_education/documentation/001_oegen/primitives/lean4` -> `lean4/Imported/OeGenPrimitives/` | 1 |
| `omega_engine_education/documentation/003_oemssn/lean4` -> `lean4/Imported/OeMssn/` | 1 |
| `omega_engine_education/documentation/004_oepfp/lean4` -> `lean4/Imported/OePfp/` | 2 |
| `omega_engine_education/documentation/000_oepregen/lean4` -> `lean4/Imported/OePregen/` | 1 |
| `omega_engine_education/documentation/002_oesn/lean4` -> `lean4/Imported/OeSn/` | 4 |
| `omega_engine_education/documentation/006_oewdp/lean4` -> `lean4/Imported/OeWdp/` | 1 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/013_operator_lifts_trace_metrics_and_representation_limits/lean4` -> `lean4/Imported/OperatorLifts/` | 1 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4` -> `lean4/Imported/PreGenesisToMssn/` | 10 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4` -> `lean4/Imported/SnMssn/` | 1 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4` -> `lean4/Imported/WitnessedDifference/` | 17 |

Three cited paths were not imported because this repository already holds a file whose cited declarations have the same statements; the references now name the in-repo file:

- `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean` -> `lean4/DerivationDagQMClosure.lean`
- `omega_engine_atlas/coda_atlas/proposals/008_fsp_switching_normal_form/SwitchingNormalForm.lean` -> `lean4/SwitchingNormalForm.lean`
- `lean4/quantum_mechanics/H016ContinuousDynamicsFork.lean` -> `lean4/H016ContinuousDynamicsFork.lean`

The two cited `omega_engine_education/.../inputs/the_symbol_game/...` copies under `dag/results/` are sealed run inputs and were not touched.

## What this repository would lose

The table lists each group of sibling-tree paths that this checkout cites. *live* counts references from files that are inputs of the DAG, code, papers, scripts, `lean4/` and docs; *gen.* from generated papers and views; *sealed* from `dag/results/**`. *nodes* is the number of DAG nodes that cite a file of the group in their `source`, `rust` or `lean` field (node count only; a node can cite several).

| Group | paths (exist/removed/missing) | live | gen. | sealed | nodes | files cited live (present; removed) |
|---|---|---|---|---|---|---|
| `.claude` | 2 (1/0/1) | 5 | 0 | 15 | 0 | 1 paper / document |
| `.venv` | 1 (1/0/0) | 1 | 0 | 0 | 0 | 1 other |
| `create_new_worktree` | 1 (0/0/1) | 1 | 0 | 0 | 0 | - |
| `lean4` | 12 (3/0/9) | 22 | 0 | 0 | 0 | 2 Lean |
| `omega_engine` | 2001 (1515/0/486) | 3073 | 961 | 5296 | 195 | 1257 Rust, 27 data (json/jsonl/csv) |
| `omega_engine_atlas` | 1 (1/0/0) | 6 | 0 | 0 | 0 | - |
| `omega_engine_atlas/.../000_witnessed_difference_programme` | 1 (0/0/1) | 2 | 0 | 48 | 0 | - |
| `omega_engine_atlas/.../001_authorization_an_incompleteness_theory` | 1 (0/0/1) | 1 | 1 | 0 | 0 | - |
| `omega_engine_atlas/.../F000_finite` | 1 (0/0/1) | 1 | 0 | 0 | 0 | - |
| `omega_engine_atlas/coda_atlas` | 1 (1/0/0) | 1 | 0 | 0 | 0 | - |
| `omega_engine_atlas/coda_atlas/F000_finite` | 61 (61/0/0) | 48 | 259 | 154 | 0 | 19 Lean, 19 Python |
| `omega_engine_atlas/coda_atlas/F001_quantum` | 10 (10/0/0) | 17 | 381 | 675 | 8 | 2 yaml claim register |
| `omega_engine_atlas/coda_atlas/F002_continuum` | 14 (14/0/0) | 6 | 115 | 46 | 0 | 3 Python, 2 Lean |
| `omega_engine_atlas/coda_atlas/F003_omega_engine` | 19 (19/0/0) | 14 | 137 | 64 | 0 | 4 Lean, 2 Python |
| `omega_engine_atlas/coda_atlas/F004_papers` | 8 (4/0/4) | 19 | 3 | 5 | 0 | 1 paper / document |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1` | 85 (85/0/0) | 312 | 267 | 155 | 82 | 36 Lean, 23 Rust, 13 Python, 7 paper / document |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn` | 14 (14/0/0) | 47 | 55 | 464 | 21 | 7 Lean, 2 Python, 1 Rust, 1 paper / document |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme` | 50 (50/0/0) | 139 | 100 | 282 | 38 | 24 Python, 15 Lean, 7 paper / document, 1 Rust |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf` | 52 (52/0/0) | 95 | 63 | 154 | 14 | 27 Lean, 13 paper / document, 11 Python |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn` | 9 (9/0/0) | 26 | 33 | 282 | 10 | 2 Python, 2 Lean, 2 paper / document |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/002_l1_native_cohomology` | 2 (2/0/0) | 0 | 2 | 0 | 0 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/003_l1_obstruction_framework` | 3 (3/0/0) | 4 | 3 | 21 | 2 | 1 paper / document, 1 Lean |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/009_conditional_density_lift_and_dual_witness_xi_functional` | 2 (2/0/0) | 3 | 1 | 16 | 1 | 1 paper / document, 1 Lean |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/013_operator_lifts_trace_metrics_and_representation_limits` | 2 (2/0/0) | 3 | 1 | 13 | 1 | 1 Lean, 1 paper / document |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/029_the_anomalon_boundary` | 2 (2/0/0) | 3 | 3 | 20 | 1 | 1 Lean, 1 paper / document |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/plans` | 1 (0/0/1) | 1 | 0 | 0 | 0 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/002_projection_obstruction` | 1 (1/0/0) | 2 | 1 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/002_projection_obstruction/000_projection_obstruction` | 1 (1/0/0) | 0 | 1 | 0 | 0 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/002_projection_obstruction/009_coordinate_wise_additivity` | 2 (2/0/0) | 4 | 1 | 15 | 2 | 1 paper / document, 1 Lean |
| `omega_engine_atlas/coda_atlas/F004_papers/002_projection_obstruction/035_zero_container_relational_spacetime_and_witness_holonomy` | 4 (4/0/0) | 2 | 7 | 3 | 0 | 2 Python |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations` | 77 (0/40/37) | 0 | 77 | 0 | 0 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/002_cofiber_to_banach_quotient_bridge` | 1 (0/0/1) | 2 | 0 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/003_residual_density_calculus_l1_l2_boundary` | 1 (0/0/1) | 3 | 1 | 10 | 2 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/012_density_matrices_as_diagonal_residual_weights` | 1 (0/0/1) | 2 | 0 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift` | 2 (0/0/2) | 18 | 1 | 80 | 14 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/021_measurement_update_as_idempotent_conditioning` | 1 (0/0/1) | 2 | 0 | 6 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/028_the_u1_selector` | 1 (0/0/1) | 2 | 0 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/030_finite_weighted_transport_calculus` | 1 (0/0/1) | 6 | 2 | 30 | 5 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/031_finite_path_sum_as_graded_transport` | 1 (0/0/1) | 4 | 1 | 17 | 3 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/032_gtta_feynman_finite_shadow_histories` | 1 (0/0/1) | 3 | 0 | 12 | 2 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/033_schrodinger_finite_shadow` | 2 (0/0/2) | 5 | 0 | 18 | 2 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/034_unitary_finite_shadow` | 1 (0/0/1) | 2 | 0 | 6 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/035_hamiltonian_generator_admission` | 1 (0/0/1) | 2 | 0 | 6 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/040_matrix_vs_diffeq_representation` | 1 (0/0/1) | 2 | 0 | 6 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/041_heisenberg_picture_shadow` | 1 (0/0/1) | 2 | 0 | 6 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/043_gellmann_hartle_cochain_decoherence` | 2 (0/0/2) | 7 | 0 | 12 | 2 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/050_dirac_equation_admission` | 1 (0/0/1) | 2 | 0 | 6 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/051_spinor_structure_admission` | 1 (0/0/1) | 2 | 0 | 6 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/060_superposition_as_the_quotient_fiber` | 1 (0/0/1) | 2 | 0 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/061_interference_as_the_non_l1_resource` | 1 (0/0/1) | 3 | 0 | 10 | 2 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/062_the_u1_selector` | 1 (0/0/1) | 3 | 0 | 10 | 2 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/063_holonomy_structured_superposition` | 2 (0/0/2) | 6 | 0 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/064_phase_gauge_residual` | 1 (0/0/1) | 3 | 0 | 11 | 2 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/070_product_non_factorization_as_a_bipartite_obstruction` | 1 (0/0/1) | 2 | 0 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/071_entanglement_as_a_separability_obstruction` | 1 (0/0/1) | 2 | 0 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/072_bit_shadow_and_qubit` | 2 (0/0/2) | 4 | 0 | 10 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/073_correlation_separability_finite_bell` | 1 (0/0/1) | 3 | 0 | 10 | 2 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/074_no_signaling_finite_shadow` | 1 (0/0/1) | 4 | 0 | 16 | 3 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/080_cptp_trace_norm_geometry_and_quantum_dual_witnesses` | 1 (0/0/1) | 3 | 0 | 10 | 2 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/081_trace_norm_cptp_transport_audit` | 1 (0/0/1) | 4 | 0 | 15 | 3 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/082_channels_as_stochastic_kernels_and_the_cptp_lift` | 1 (0/0/1) | 4 | 0 | 16 | 3 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/083_completely_positive_import_boundary` | 1 (0/0/1) | 4 | 0 | 17 | 3 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/090_interpretations_as_authority_shadows` | 1 (0/0/1) | 4 | 0 | 16 | 3 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/091_deutsch_everett_wolfram_promotion_error` | 1 (0/0/1) | 2 | 0 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/092_qm_typed_authority_boundary_suite` | 1 (0/0/1) | 4 | 0 | 16 | 3 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/093_from_q_to_gtfoc_finite_descent_of_quantum_structure` | 1 (0/0/1) | 5 | 0 | 21 | 4 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/094_everettian_relative_state_contact` | 1 (0/0/1) | 2 | 0 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/095_copenhagen_as_authority_shadow` | 1 (0/0/1) | 2 | 0 | 6 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/101_threshold_theorems_as_repair_capacity_certificates` | 1 (0/0/1) | 2 | 0 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/102_fault_tolerance_repair_capacity` | 1 (0/0/1) | 2 | 0 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/103_show_the_packet_protocol` | 1 (0/0/1) | 2 | 0 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/110_loop_quantum_gravity_kinematical_shadows` | 1 (0/0/1) | 2 | 0 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/111_general_relativity_kinematical_shadows` | 1 (0/0/1) | 2 | 0 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/120_mermin_peres_contextuality_cochain_obstruction` | 1 (0/0/1) | 2 | 0 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/121_the_finite_qm_ingredient_ladder` | 2 (0/0/2) | 5 | 1 | 15 | 2 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference` | 2 (0/0/2) | 19 | 9 | 85 | 16 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/202_operator_algebra_shadow` | 1 (0/0/1) | 2 | 0 | 6 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/203_measurement_problem_obstruction` | 1 (0/0/1) | 2 | 0 | 6 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/204_born_uniqueness_import_boundary` | 1 (0/0/1) | 2 | 1 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/205_pointer_basis_obstruction` | 1 (0/0/1) | 2 | 0 | 6 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/206_universal_boundary_synthesis_and_cochain_lift` | 1 (0/0/1) | 3 | 2 | 10 | 2 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/207_complex_phase_fiber_and_u1_transport_lift` | 1 (0/0/1) | 3 | 1 | 10 | 2 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/208_quadratic_l2_readout_and_interference_boundary` | 1 (0/0/1) | 2 | 1 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/209_non_commutative_operator_algebra_and_contextuality` | 1 (0/0/1) | 2 | 1 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/210_born_rule_postulate_and_state_effect_pairing` | 1 (0/0/1) | 3 | 2 | 10 | 2 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/211_continuous_unitary_dynamics_and_l1_to_qm_synthesis` | 1 (0/0/1) | 2 | 1 | 5 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/212_microsoft_majorana_problem` | 1 (0/0/1) | 2 | 0 | 9 | 1 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code` | 4 (0/2/2) | 7 | 14 | 29 | 0 | -; removed: 2 Python |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm` | 4 (0/4/0) | 10 | 7 | 269 | 8 | -; removed: 1 yaml (other), 1 Python |
| `omega_engine_atlas/coda_atlas/F004_papers/004_general_relativity/002_constraint_closure_and_the_l1structure_of_physical_law` | 13 (0/13/0) | 9 | 25 | 0 | 0 | -; removed: 6 Python, 3 Lean |
| `omega_engine_atlas/coda_atlas/F004_papers/004_general_relativity/003_relational_point_coincidence_and_witnessed_difference` | 4 (0/4/0) | 1 | 6 | 0 | 0 | -; removed: 1 Python |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm` | 5 (0/3/2) | 48 | 21 | 274 | 28 | -; removed: 2 paper / document |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/apps` | 1 (0/0/1) | 1 | 0 | 19 | 0 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/campaigns` | 28 (0/28/0) | 10 | 0 | 138 | 0 | -; removed: 10 data (json/jsonl/csv) |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/claims` | 3 (0/3/0) | 30 | 10 | 182 | 27 | -; removed: 3 yaml claim register |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/code` | 10 (0/0/10) | 10 | 0 | 190 | 0 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/evidence` | 13 (0/13/0) | 12 | 0 | 244 | 0 | -; removed: 11 data (json/jsonl/csv), 1 paper / document |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean` | 2 (0/2/0) | 25 | 52 | 285 | 0 | -; removed: 2 Lean |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean4` | 12 (0/0/12) | 22 | 0 | 190 | 0 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native` | 9 (0/9/0) | 28 | 32 | 258 | 24 | -; removed: 4 Rust |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python` | 23 (0/21/2) | 26 | 103 | 108 | 0 | -; removed: 19 Python |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/research` | 13 (0/13/0) | 0 | 13 | 0 | 0 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/tests` | 6 (0/4/2) | 6 | 2 | 0 | 0 | -; removed: 4 Python |
| `omega_engine_atlas/coda_atlas/F004_papers/007_finite_to_continuum` | 1 (0/1/0) | 0 | 1 | 0 | 0 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/007_finite_to_continuum/_docs` | 2 (0/2/0) | 0 | 2 | 0 | 0 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/007_finite_to_continuum/code` | 8 (0/8/0) | 8 | 16 | 3 | 0 | -; removed: 8 Python |
| `omega_engine_atlas/coda_atlas/F004_papers/007_finite_to_continuum/lean4` | 3 (0/3/0) | 3 | 8 | 3 | 0 | -; removed: 3 Lean |
| `omega_engine_atlas/coda_atlas/F004_papers/008_fsp` | 1 (0/0/1) | 1 | 0 | 0 | 0 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/008_fsp/code` | 26 (0/23/3) | 112 | 8 | 0 | 0 | -; removed: 23 Python |
| `omega_engine_atlas/coda_atlas/F004_papers/009_ms_majorana` | 1 (0/1/0) | 0 | 1 | 0 | 0 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/009_ms_majorana/code` | 2 (0/2/0) | 5 | 1 | 3 | 0 | -; removed: 2 Python |
| `omega_engine_atlas/coda_atlas/F004_papers/009_ms_majorana/lean4` | 1 (0/1/0) | 1 | 0 | 0 | 0 | -; removed: 1 Lean |
| `omega_engine_atlas/coda_atlas/F004_papers/010_mub6` | 3 (0/1/2) | 4 | 1 | 0 | 0 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/010_mub6/artifacts` | 15 (0/14/1) | 28 | 0 | 0 | 0 | -; removed: 14 data (json/jsonl/csv) |
| `omega_engine_atlas/coda_atlas/F004_papers/010_mub6/code` | 2 (0/2/0) | 4 | 0 | 0 | 0 | -; removed: 2 Python |
| `omega_engine_atlas/coda_atlas/F004_papers/010_mub6/research` | 5 (0/5/0) | 5 | 0 | 0 | 0 | -; removed: 4 Python, 1 data (json/jsonl/csv) |
| `omega_engine_atlas/coda_atlas/F004_papers/010_mub6/rust` | 1 (0/1/0) | 1 | 2 | 0 | 0 | -; removed: 1 Rust |
| `omega_engine_atlas/coda_atlas/F004_papers/013_trace_zero_quotient_duality` | 2 (2/0/0) | 0 | 2 | 0 | 0 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/013_trace_zero_quotient_duality/code` | 2 (2/0/0) | 2 | 5 | 3 | 0 | 2 Python |
| `omega_engine_atlas/coda_atlas/F004_papers/015_pfp/003_pfp_host_admitted_failure_detectors` | 1 (1/0/0) | 0 | 0 | 1 | 0 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/015_pfp/021_recreated_demos_and_proposal_fidelity_evidence` | 5 (5/0/0) | 0 | 0 | 5 | 0 | - |
| `omega_engine_atlas/coda_atlas/F004_papers/plans` | 1 (1/0/0) | 2 | 0 | 5 | 1 | 1 data (json/jsonl/csv) |
| `omega_engine_atlas/coda_atlas/omega_engine_finite_qm` | 1 (0/0/1) | 6 | 0 | 0 | 0 | - |
| `omega_engine_atlas/coda_atlas/prompts` | 3 (3/0/0) | 3 | 0 | 0 | 0 | 3 data (json/jsonl/csv) |
| `omega_engine_atlas/coda_atlas/proposals` | 1 (1/0/0) | 1 | 1 | 16 | 0 | 1 Lean |
| `omega_engine_core` | 1 (0/0/1) | 4 | 0 | 0 | 0 | - |
| `omega_engine_education` | 2 (2/0/0) | 2 | 0 | 0 | 0 | - |
| `omega_engine_education/documentation/000_oepregen` | 9 (9/0/0) | 39 | 34 | 34 | 10 | 6 paper / document, 2 Python, 1 Lean |
| `omega_engine_education/documentation/001_oegen` | 3 (3/0/0) | 17 | 12 | 13 | 11 | 2 paper / document, 1 Lean |
| `omega_engine_education/documentation/002_oesn` | 23 (23/0/0) | 74 | 38 | 42 | 18 | 18 paper / document, 2 Python, 2 Lean |
| `omega_engine_education/documentation/003_oemssn` | 15 (15/0/0) | 45 | 26 | 2 | 10 | 8 paper / document, 2 Python, 2 Rust, 1 Lean |
| `omega_engine_education/documentation/004_oepfp` | 7 (7/0/0) | 8 | 4 | 14 | 1 | 3 paper / document, 2 Lean |
| `omega_engine_education/documentation/005_oegenong` | 7 (7/0/0) | 21 | 7 | 0 | 7 | 7 paper / document |
| `omega_engine_education/documentation/006_oewdp` | 9 (9/0/0) | 34 | 15 | 0 | 15 | 8 paper / document, 1 Lean |
| `omega_engine_education/documentation/007_oelggr` | 2 (2/0/0) | 6 | 2 | 0 | 1 | 2 paper / document |
| `omega_engine_education/documentation/030` | 1 (0/0/1) | 2 | 0 | 0 | 0 | - |
| `omega_engine_governance` | 42 (4/0/38) | 109 | 0 | 5 | 1 | 1 yaml claim register, 1 Python |
| `omega_engine_library` | 4 (4/0/0) | 5 | 0 | 5 | 1 | 2 paper / document, 1 yaml (other) |
| `omega_engine_majorana` | 1 (0/0/1) | 1 | 0 | 0 | 0 | - |
| `omega_engine_operations` | 3 (3/0/0) | 4 | 0 | 22 | 1 | 1 data (json/jsonl/csv), 1 Python |
| `omega_engine_pfp` | 16 (15/0/1) | 23 | 12 | 68 | 2 | 8 Python, 2 data (json/jsonl/csv) |
| `omega_engine_product_planning_office` | 5 (3/0/2) | 8 | 1 | 5 | 2 | 1 paper / document, 1 data (json/jsonl/csv) |
| `omega_engine_projects` | 459 (0/0/459) | 1120 | 0 | 0 | 0 | - |
| `omega_engine_py` | 8 (0/0/8) | 14 | 0 | 0 | 0 | - |
| `omega_engine_woland` | 5 (4/0/1) | 6 | 0 | 0 | 0 | 1 Python, 1 paper / document |
| `omega_engines` | 2 (0/0/2) | 16 | 0 | 0 | 0 | - |
| `omega_simplex_cache` | 4 (4/0/0) | 0 | 0 | 4 | 0 | - |
| `research` | 11 (0/0/11) | 33 | 0 | 0 | 0 | - |
| `sync_with_remote_main` | 2 (0/0/2) | 2 | 0 | 0 | 0 | - |

### Nodes that depend on the atlas, by status

Counting nodes whose `source`, `rust` or `lean` field names an atlas file that exists, or existed until the removal commit (the provenance strings are not counted):

| Status | nodes |
|---|---|
| `PROVED_LEAN` | 143 |
| `DEFINITION` | 56 |
| `COMPUTATIONALLY_CHECKED` | 31 |
| `CONDITIONAL` | 27 |
| `OPEN` | 21 |
| `IMPORTED_ASSUMPTION` | 21 |
| `PROVED_PROSE` | 13 |
| `ADMITTED_PRIMITIVE` | 3 |

Lean: the Lean files that a node `lean` field or a record `lean4` field cites are all in `lean4/` now. 137 further atlas Lean files are still named by live files, but not as a citation the evidence map resolves: 125 appear only inside `dag/derivation_dag.json` in free text (`absent: no local lean twin located for ...` notes, statements, summaries), and 11 are named by `code/**` or `papers/**` (the `source_pin.json` hash pins of the QM code and two MUB6 test files). None of them backs a replay receipt, so they were not imported; the DAG already records them as absent twins.

## Files cited by live files, by kind

| Kind | files | size | of which removed from the working tree |
|---|---|---|---|
| Rust | 1289 | 19.3 MB | 5 |
| Python | 169 | 1.9 MB | 72 |
| Lean | 137 | 1.5 MB | 9 |
| paper / document | 98 | 4.3 MB | 3 |
| data (json/jsonl/csv) | 71 | 2.2 MB | 36 |
| yaml claim register | 6 | 636.3 KB | 3 |
| yaml (other) | 2 | 27.7 KB | 1 |
| other | 1 | 235.5 KB | 0 |

## Recommended copy list (not copied in this change)

The papers, claim registers and data files that DAG nodes and records cite as `source` come to 107 files, 6.0 MB. 7 of them (1.2 MB) are no longer in the sibling working tree and would be restored from its git history. That is over the 5 MB this change allows for non-Lean files, so **none of them was copied**. Recommended: copy them verbatim, keeping their atlas-relative path, to `sources/atlas/<atlas-relative path>` in one follow-up change, then rewrite the `source` fields with `dag/research/lean_replay_campaign/rewrite_refs.py` (extend its table; the files are byte-identical, so `:line` references stay valid). The complete list with sizes is in the JSON file (entries whose `kind` is a document, yaml or data file and that are cited from the DAG classes). The largest:

| File | size | references |
|---|---|---|
| `omega_engine_atlas/coda_atlas/F004_papers/plans/goal_dag.jsonl` | 1.1 MB | 7 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md` | 999.2 KB | 62 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md` | 898.0 KB | 72 |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/claims/claim_ledger.yaml` (removed) | 542.1 KB | 25 |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics_claim_ledger.md` (removed) | 410.7 KB | 60 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/CLAUDE.md` | 336.2 KB | 9 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/axiom_report.txt` | 172.0 KB | 6 |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md` (removed) | 152.8 KB | 226 |
| `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md` | 129.4 KB | 18 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt` | 81.2 KB | 56 |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/claims/gap_register.yaml` (removed) | 74.2 KB | 183 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt` | 57.6 KB | 72 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_bridge_register.md` | 57.3 KB | 28 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md` | 51.2 KB | 83 |
| `omega_engine_operations/use_cases/cicd/f64_contract.json` | 44.5 KB | 12 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt` | 39.0 KB | 30 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md` | 36.8 KB | 94 |
| `omega_engine_product_planning_office/plans/review_remediation/evidence/batch_13/c4_native_actual.json` | 34.0 KB | 4 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/fourth/claim_ledger.md` | 32.2 KB | 6 |
| `omega_engine_atlas/coda_atlas/F004_papers/010_mub6/research/derivation_dag_20261011.json` (removed) | 31.0 KB | 1 |
| `omega_engine_education/documentation/000_oepregen/sources/analysis_derivation_v1.md` | 30.0 KB | 20 |
| `omega_engine_education/documentation/006_oewdp/levels/level_09_behavioral_quotients_finite_states.md` | 30.0 KB | 4 |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/ninth/claim_ledger.md` | 29.5 KB | 6 |
| `omega_engine_product_planning_office/architecture_review/06_genesis_native_route.md` | 27.3 KB | 7 |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml` (removed) | 27.1 KB | 62 |

Rust and Python files cited from node `rust` fields and record fields: 400 files, 6.1 MB (273 Rust, 127 Python). Most live in `omega_engine/` (the Rust crates); this repository has its own `code/rust` and `code/python`, and the in-repo twins are what the evidence map counts. Copying a sibling-crate file in would not make it build here; the honest options are to cite the in-repo twin or to record the citation as external. These were not copied.

## Code that imports sibling packages

Python files here that `import` or `from ... import` a package of the sibling tree (not a path citation; the code would fail to import without the package):

| Package | files | import statements |
|---|---|---|
| `omega_engine` | 352 | 961 |
| `omega_engine_atlas` | 1 | 1 |
| `omega_engine_governance` | 40 | 68 |
| `omega_engine_operating_system` | 16 | 16 |
| `omega_engine_operations` | 18 | 18 |
| `omega_engine_pfp` | 61 | 150 |
| `omega_engine_projects` | 20 | 48 |
| `omega_engine_woland` | 7 | 11 |
| `omega_engine_workflows_agents_skills` | 8 | 13 |

These are in vendored governance contracts and test support (`code/python/governance/**`, `papers/core/**/tests/support/**`) and in tests; none is on the path that builds the DAG, the evidence map or the Lean replay.

`Cargo.toml` path dependencies (excluding sealed copies under `dag/results/**`): 79 entries, 1 leave the repository:

- `papers/core/mub6/code/Cargo.toml`: `path = "../../../../../omega_engine/crates_rs/omega_mub"`

Every other path dependency points inside `code/rust`. The sealed copies of crates under `dag/results/**` carry absolute `the_symbol_game` paths in their `Cargo.toml`; they are archives, not built.

336 files name an absolute `...\the_symbol_game\...` path in prose, scripts or receipts; they are listed in the JSON.

## Verdict per atlas folder

*SAFE TO DELETE* means: no live file of this repository cites an existing file of the folder, so deleting it changes nothing the DAG checks, the replay or the tests read. *ALREADY REMOVED* means the folder is gone from the sibling working tree and this repository still cites files that were in it. *NOT YET SAFE* names what would break. Sealed run artifacts under `dag/results/**` quote paths of their inputs; they carry their own copies of those inputs and are not a dependency.

By top-level folder of the sibling tree (the answer to "can this whole folder go"):

| Top-level folder | verdict | reason |
|---|---|---|
| `.claude` | **NOT YET SAFE** | 1 existing file(s) are cited by live files of this repo (1 paper / document; 7.2 KB) |
| `.venv` | **NOT YET SAFE** | 1 existing file(s) are cited by live files of this repo (1 other; 235.5 KB) |
| `create_new_worktree` | **SAFE TO DELETE** | every live reference names a path that is not in the atlas (already broken); nothing is lost |
| `lean4` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (2 Lean; 30.0 KB) |
| `omega_engine` | **NOT YET SAFE** | 1284 existing file(s) are cited by live files of this repo (1257 Rust, 27 data (json/jsonl/csv); 19.2 MB) |
| `omega_engine_atlas` | **NOT YET SAFE** | 265 existing file(s) are cited by live files of this repo (118 Lean, 80 Python, 36 paper / document, 25 Rust, 4 data (json/jsonl/csv), 2 yaml claim register; 6.1 MB); a further 129 cited file(s) are already gone from the working tree |
| `omega_engine_core` | **SAFE TO DELETE** | every live reference names a path that is not in the atlas (already broken); nothing is lost |
| `omega_engine_education` | **NOT YET SAFE** | 70 existing file(s) are cited by live files of this repo (54 paper / document, 8 Lean, 6 Python, 2 Rust; 737.6 KB) |
| `omega_engine_governance` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (1 yaml claim register, 1 Python; 10.0 KB) |
| `omega_engine_library` | **NOT YET SAFE** | 3 existing file(s) are cited by live files of this repo (2 paper / document, 1 yaml (other); 19.1 KB) |
| `omega_engine_majorana` | **SAFE TO DELETE** | every live reference names a path that is not in the atlas (already broken); nothing is lost |
| `omega_engine_operations` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (1 data (json/jsonl/csv), 1 Python; 66.2 KB) |
| `omega_engine_pfp` | **NOT YET SAFE** | 10 existing file(s) are cited by live files of this repo (8 Python, 2 data (json/jsonl/csv); 79.2 KB) |
| `omega_engine_product_planning_office` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (1 paper / document, 1 data (json/jsonl/csv); 61.3 KB) |
| `omega_engine_projects` | **SAFE TO DELETE** | every live reference names a path that is not in the atlas (already broken); nothing is lost |
| `omega_engine_py` | **SAFE TO DELETE** | every live reference names a path that is not in the atlas (already broken); nothing is lost |
| `omega_engine_woland` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (1 Python, 1 paper / document; 13.2 KB) |
| `omega_engines` | **SAFE TO DELETE** | every live reference names a path that is not in the atlas (already broken); nothing is lost |
| `omega_simplex_cache` | **SAFE TO DELETE** | no live reference (only sealed run artifacts or generated views, if any) |
| `research` | **SAFE TO DELETE** | every live reference names a path that is not in the atlas (already broken); nothing is lost |
| `sync_with_remote_main` | **SAFE TO DELETE** | every live reference names a path that is not in the atlas (already broken); nothing is lost |

Per paper or sub-folder (only folders with at least one path that resolves now or resolved before the removal commit; folders whose every cited path never resolved are left out, they hold nothing to lose):

| Folder | verdict | reason |
|---|---|---|
| `.claude` | **NOT YET SAFE** | 1 existing file(s) are cited by live files of this repo (1 paper / document; 7.2 KB) |
| `.venv` | **NOT YET SAFE** | 1 existing file(s) are cited by live files of this repo (1 other; 235.5 KB) |
| `lean4` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (2 Lean; 30.0 KB) |
| `omega_engine` | **NOT YET SAFE** | 1284 existing file(s) are cited by live files of this repo (1257 Rust, 27 data (json/jsonl/csv); 19.2 MB) |
| `omega_engine_atlas` | **SAFE TO DELETE** | every live reference names a path that is not in the atlas (already broken); nothing is lost |
| `omega_engine_atlas/coda_atlas` | **SAFE TO DELETE** | every live reference names a path that is not in the atlas (already broken); nothing is lost |
| `omega_engine_atlas/coda_atlas/F000_finite` | **NOT YET SAFE** | 38 existing file(s) are cited by live files of this repo (19 Lean, 19 Python; 201.0 KB) |
| `omega_engine_atlas/coda_atlas/F001_quantum` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (2 yaml claim register; 14.8 KB) |
| `omega_engine_atlas/coda_atlas/F002_continuum` | **NOT YET SAFE** | 5 existing file(s) are cited by live files of this repo (3 Python, 2 Lean; 5.5 KB) |
| `omega_engine_atlas/coda_atlas/F003_omega_engine` | **NOT YET SAFE** | 6 existing file(s) are cited by live files of this repo (4 Lean, 2 Python; 20.9 KB) |
| `omega_engine_atlas/coda_atlas/F004_papers` | **NOT YET SAFE** | 1 existing file(s) are cited by live files of this repo (1 paper / document; 38.1 KB) |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1` | **NOT YET SAFE** | 79 existing file(s) are cited by live files of this repo (36 Lean, 23 Rust, 13 Python, 7 paper / document; 1.1 MB) |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn` | **NOT YET SAFE** | 11 existing file(s) are cited by live files of this repo (7 Lean, 2 Python, 1 Rust, 1 paper / document; 133.8 KB) |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme` | **NOT YET SAFE** | 47 existing file(s) are cited by live files of this repo (24 Python, 15 Lean, 7 paper / document, 1 Rust; 2.3 MB) |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf` | **NOT YET SAFE** | 51 existing file(s) are cited by live files of this repo (27 Lean, 13 paper / document, 11 Python; 894.6 KB) |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn` | **NOT YET SAFE** | 6 existing file(s) are cited by live files of this repo (2 Python, 2 Lean, 2 paper / document; 55.0 KB) |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/002_l1_native_cohomology` | **SAFE TO DELETE** | no live reference (only sealed run artifacts or generated views, if any) |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/003_l1_obstruction_framework` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (1 paper / document, 1 Lean; 21.5 KB) |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/009_conditional_density_lift_and_dual_witness_xi_functional` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (1 paper / document, 1 Lean; 22.7 KB) |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/013_operator_lifts_trace_metrics_and_representation_limits` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (1 Lean, 1 paper / document; 12.2 KB) |
| `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/029_the_anomalon_boundary` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (1 Lean, 1 paper / document; 20.1 KB) |
| `omega_engine_atlas/coda_atlas/F004_papers/002_projection_obstruction` | **SAFE TO DELETE** | every live reference names a path that is not in the atlas (already broken); nothing is lost |
| `omega_engine_atlas/coda_atlas/F004_papers/002_projection_obstruction/000_projection_obstruction` | **SAFE TO DELETE** | no live reference (only sealed run artifacts or generated views, if any) |
| `omega_engine_atlas/coda_atlas/F004_papers/002_projection_obstruction/009_coordinate_wise_additivity` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (1 paper / document, 1 Lean; 61.4 KB) |
| `omega_engine_atlas/coda_atlas/F004_papers/002_projection_obstruction/035_zero_container_relational_spacetime_and_witness_holonomy` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (2 Python; 88.2 KB) |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations` | **SAFE TO DELETE** | no live reference (only sealed run artifacts or generated views, if any) |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code` | **ALREADY REMOVED** | 2 cited file(s) (2 Python; 5.9 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm` | **ALREADY REMOVED** | 2 cited file(s) (1 yaml (other), 1 Python; 39.1 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/004_general_relativity/002_constraint_closure_and_the_l1structure_of_physical_law` | **ALREADY REMOVED** | 9 cited file(s) (6 Python, 3 Lean; 40.2 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/004_general_relativity/003_relational_point_coincidence_and_witnessed_difference` | **ALREADY REMOVED** | 1 cited file(s) (1 Python; 8.9 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm` | **ALREADY REMOVED** | 2 cited file(s) (2 paper / document; 563.5 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/campaigns` | **ALREADY REMOVED** | 10 cited file(s) (10 data (json/jsonl/csv); 215.1 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/claims` | **ALREADY REMOVED** | 3 cited file(s) (3 yaml claim register; 618.1 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/evidence` | **ALREADY REMOVED** | 12 cited file(s) (11 data (json/jsonl/csv), 1 paper / document; 431.9 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean` | **ALREADY REMOVED** | 2 cited file(s) (2 Lean; 277.6 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native` | **ALREADY REMOVED** | 4 cited file(s) (4 Rust; 126.9 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python` | **ALREADY REMOVED** | 19 cited file(s) (19 Python; 445.5 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/research` | **SAFE TO DELETE** | no live reference (only sealed run artifacts or generated views, if any) |
| `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/tests` | **ALREADY REMOVED** | 4 cited file(s) (4 Python; 25.3 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/007_finite_to_continuum` | **SAFE TO DELETE** | no live reference (only sealed run artifacts or generated views, if any) |
| `omega_engine_atlas/coda_atlas/F004_papers/007_finite_to_continuum/_docs` | **SAFE TO DELETE** | no live reference (only sealed run artifacts or generated views, if any) |
| `omega_engine_atlas/coda_atlas/F004_papers/007_finite_to_continuum/code` | **ALREADY REMOVED** | 8 cited file(s) (8 Python; 92.3 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/007_finite_to_continuum/lean4` | **ALREADY REMOVED** | 3 cited file(s) (3 Lean; 10.5 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/008_fsp/code` | **ALREADY REMOVED** | 23 cited file(s) (23 Python; 327.8 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/009_ms_majorana` | **SAFE TO DELETE** | no live reference (only sealed run artifacts or generated views, if any) |
| `omega_engine_atlas/coda_atlas/F004_papers/009_ms_majorana/code` | **ALREADY REMOVED** | 2 cited file(s) (2 Python; 10.9 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/009_ms_majorana/lean4` | **ALREADY REMOVED** | 1 cited file(s) (1 Lean; 15.2 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/010_mub6` | **SAFE TO DELETE** | every live reference names a path that is not in the atlas (already broken); nothing is lost |
| `omega_engine_atlas/coda_atlas/F004_papers/010_mub6/artifacts` | **ALREADY REMOVED** | 14 cited file(s) (14 data (json/jsonl/csv); 188.9 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/010_mub6/code` | **ALREADY REMOVED** | 2 cited file(s) (2 Python; 104.2 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/010_mub6/research` | **ALREADY REMOVED** | 5 cited file(s) (4 Python, 1 data (json/jsonl/csv); 54.8 KB) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/010_mub6/rust` | **ALREADY REMOVED** | 1 cited file(s) (1 Rust; 258 B) were deleted by sibling commit 3379759468; this repo's references to them no longer resolve and the content is only in the sibling's git history |
| `omega_engine_atlas/coda_atlas/F004_papers/013_trace_zero_quotient_duality` | **SAFE TO DELETE** | no live reference (only sealed run artifacts or generated views, if any) |
| `omega_engine_atlas/coda_atlas/F004_papers/013_trace_zero_quotient_duality/code` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (2 Python; 9.6 KB) |
| `omega_engine_atlas/coda_atlas/F004_papers/015_pfp/003_pfp_host_admitted_failure_detectors` | **SAFE TO DELETE** | no live reference (only sealed run artifacts or generated views, if any) |
| `omega_engine_atlas/coda_atlas/F004_papers/015_pfp/021_recreated_demos_and_proposal_fidelity_evidence` | **SAFE TO DELETE** | no live reference (only sealed run artifacts or generated views, if any) |
| `omega_engine_atlas/coda_atlas/F004_papers/plans` | **NOT YET SAFE** | 1 existing file(s) are cited by live files of this repo (1 data (json/jsonl/csv); 1.1 MB) |
| `omega_engine_atlas/coda_atlas/prompts` | **NOT YET SAFE** | 3 existing file(s) are cited by live files of this repo (3 data (json/jsonl/csv); 10.2 KB) |
| `omega_engine_atlas/coda_atlas/proposals` | **NOT YET SAFE** | 1 existing file(s) are cited by live files of this repo (1 Lean; 48.6 KB) |
| `omega_engine_education` | **SAFE TO DELETE** | every live reference names a path that is not in the atlas (already broken); nothing is lost |
| `omega_engine_education/documentation/000_oepregen` | **NOT YET SAFE** | 9 existing file(s) are cited by live files of this repo (6 paper / document, 2 Python, 1 Lean; 91.5 KB) |
| `omega_engine_education/documentation/001_oegen` | **NOT YET SAFE** | 3 existing file(s) are cited by live files of this repo (2 paper / document, 1 Lean; 153.8 KB) |
| `omega_engine_education/documentation/002_oesn` | **NOT YET SAFE** | 22 existing file(s) are cited by live files of this repo (18 paper / document, 2 Python, 2 Lean; 124.2 KB) |
| `omega_engine_education/documentation/003_oemssn` | **NOT YET SAFE** | 13 existing file(s) are cited by live files of this repo (8 paper / document, 2 Python, 2 Rust, 1 Lean; 99.1 KB) |
| `omega_engine_education/documentation/004_oepfp` | **NOT YET SAFE** | 5 existing file(s) are cited by live files of this repo (3 paper / document, 2 Lean; 45.7 KB) |
| `omega_engine_education/documentation/005_oegenong` | **NOT YET SAFE** | 7 existing file(s) are cited by live files of this repo (7 paper / document; 45.7 KB) |
| `omega_engine_education/documentation/006_oewdp` | **NOT YET SAFE** | 9 existing file(s) are cited by live files of this repo (8 paper / document, 1 Lean; 152.9 KB) |
| `omega_engine_education/documentation/007_oelggr` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (2 paper / document; 24.8 KB) |
| `omega_engine_governance` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (1 yaml claim register, 1 Python; 10.0 KB) |
| `omega_engine_library` | **NOT YET SAFE** | 3 existing file(s) are cited by live files of this repo (2 paper / document, 1 yaml (other); 19.1 KB) |
| `omega_engine_operations` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (1 data (json/jsonl/csv), 1 Python; 66.2 KB) |
| `omega_engine_pfp` | **NOT YET SAFE** | 10 existing file(s) are cited by live files of this repo (8 Python, 2 data (json/jsonl/csv); 79.2 KB) |
| `omega_engine_product_planning_office` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (1 paper / document, 1 data (json/jsonl/csv); 61.3 KB) |
| `omega_engine_woland` | **NOT YET SAFE** | 2 existing file(s) are cited by live files of this repo (1 Python, 1 paper / document; 13.2 KB) |
| `omega_simplex_cache` | **SAFE TO DELETE** | no live reference (only sealed run artifacts or generated views, if any) |

Folders of the sibling tree that no file here cites are not listed; nothing in this repository depends on them.

### The QM and other papers (`omega_engine_atlas/coda_atlas/F004_papers/**`)

21 of the 108 paper folders listed above are ALREADY REMOVED (their cited files are in the sibling's git history only) and 14 are NOT YET SAFE; the blockers are documents, claim registers and data files that nodes cite as `source` (and the Rust and Python files the atlas holds), not Lean. After the follow-up copy to `sources/atlas/` and the matching `source` rewrite, the paper folders can be deleted. Until then, deleting them leaves the DAG internally consistent but makes `validate_derivation_dag.py` (with files) and the evidence map's document links report the sources as missing.

