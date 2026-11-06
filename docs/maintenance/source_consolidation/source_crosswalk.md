# Source consolidation crosswalk

AuthorityEffect: None. Relocation is not evidence promotion.

The [short reading spine](FIRST_MARK_TO_QUANTUM_GRAVITY.md) combines the repeated arguments.
The [manifest](source_consolidation_manifest.json) records every file, original SHA-256, destination,
and the hash of any edited live copy. The versioned sources were under `papers/`;
the requested `atlas/` paths were an intermediate workspace location. The manifest
retains both paths and hashes. It excludes 217 local build/cache files from this PR.
Source-package interiors and verbatim reviews retain historical paths and bytes. Resolve a historical path through this table or the manifest.

## Package destinations

| Former package | Destination | Files |
|---|---|---:|
| `atlas/foundations/authorization_incompleteness` | [dag/derivations/04_authorization/authorization_incompleteness](04_authorization/authorization_incompleteness/) | 56 |
| `atlas/core/000_meron_sign_problem` | [dag/derivations/26_fsp/000_meron_sign_problem](26_fsp/000_meron_sign_problem/) | 74 |
| `atlas/core/001_hubbard_sign_problem` | [dag/derivations/26_fsp/001_hubbard_sign_problem](26_fsp/001_hubbard_sign_problem/) | 17 |
| `atlas/core/constraint_closure` | [dag/derivations/19_finite_qg/constraint_closure](19_finite_qg/constraint_closure/) | 137 |
| `atlas/core/fsp` | [dag/derivations/26_fsp/fsp](26_fsp/fsp/) | 100 |
| `atlas/core/majorana` | [dag/derivations/28_majorana/majorana](28_majorana/majorana/) | 25 |
| `atlas/core/mub6` | [dag/derivations/25_mub/mub6](25_mub/mub6/) | 693 |
| `atlas/core/tools` | [dag/derivations/10_finite_qm_core/tools](10_finite_qm_core/tools/) | 3 |
| `education/l1_to_many_worlds/codex_primitive_to_hamilton_noether` | [dag/derivations/11_finite_qm_dynamics/hamilton_noether_sources](11_finite_qm_dynamics/hamilton_noether_sources/) | 79 |
| `atlas/computation` | [atlas/computation_complexity_pvnp](../../atlas/computation_complexity_pvnp/) | 1 |
| `atlas/complexity` | [atlas/computation_complexity_pvnp](../../atlas/computation_complexity_pvnp/) | 2 |

## Individual manuscript assignments

Node matches below are cross-references by packet identifier or cited basename, not fresh proof audits.
A multi-topic monograph belongs to its principal stage and is used by several chapters.

| Former manuscript | Stage-aligned source | Related DAG nodes |
|---|---|---|
| `atlas/foundations/finite_quantum_foundations_proofs.md` | [finite_quantum_foundations_proofs.md](12_finite_qm_structure/sources/finite_quantum_foundations_proofs.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/foundations/qm_002_cofiber_to_banach_quotient_bridge.md` | [qm_002_cofiber_to_banach_quotient_bridge.md](07_l1_emergence/sources/qm_002_cofiber_to_banach_quotient_bridge.md) | `L1-QM002-O022A-PHI1-QUOTIENT` |
| `atlas/foundations/qm_003_residual_density_calculus_l1_l2_boundary.md` | [qm_003_residual_density_calculus_l1_l2_boundary.md](08_l1_to_l2/sources/qm_003_residual_density_calculus_l1_l2_boundary.md) | `L1-QM003-C17-COMPOSABLE-FACTORIZATION` |
| `atlas/foundations/qm_004_general_obstruction_management_calculus.md` | [qm_004_general_obstruction_management_calculus.md](03_finite_obstruction/sources/qm_004_general_obstruction_management_calculus.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/foundations/qm_005_finite_quantum_packet_theorem_m2.md` | [qm_005_finite_quantum_packet_theorem_m2.md](09_finite_hilbert/sources/qm_005_finite_quantum_packet_theorem_m2.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/foundations/qm_006_quantum_realization_requires_finite_descent.md` | [qm_006_quantum_realization_requires_finite_descent.md](09_finite_hilbert/sources/qm_006_quantum_realization_requires_finite_descent.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/foundations/qm_008_finite_descent_to_gtfoc_projection.md` | [qm_008_finite_descent_to_gtfoc_projection.md](04_authorization/sources/qm_008_finite_descent_to_gtfoc_projection.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/foundations/qm_010_hilbert_space_cochains_qm_cohomology.md` | [qm_010_hilbert_space_cochains_qm_cohomology.md](09_finite_hilbert/sources/qm_010_hilbert_space_cochains_qm_cohomology.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/foundations/qm_011_state_effect_pairing_audit.md` | [qm_011_state_effect_pairing_audit.md](09_finite_hilbert/sources/qm_011_state_effect_pairing_audit.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/foundations/qm_012_density_matrices_as_diagonal_residual_weights.md` | [qm_012_density_matrices_as_diagonal_residual_weights.md](10_finite_qm_core/sources/qm_012_density_matrices_as_diagonal_residual_weights.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/foundations/qm_020_born_normalization_and_conditional_hilbert_lift.md` | [qm_020_born_normalization_and_conditional_hilbert_lift.md](08_l1_to_l2/sources/qm_020_born_normalization_and_conditional_hilbert_lift.md) | `L1-QM020-THM1-DIRECT-NORMALIZATION`, `L1-QM020-THM2A-L1-ADDITIVITY-DEFECT`, `L1-QM020-THM2B-MINKOWSKI`, `L1-QM020-THM3-ROW-SPARSITY`, `L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY`, `L1-QM020-THM5-PHASE-AVERAGED-SHADOW`, `L1-QM020-THM6-P1-SCOPE-FENCE` (+3 in manifest) |
| `atlas/foundations/qm_021_measurement_update_as_idempotent_conditioning.md` | [qm_021_measurement_update_as_idempotent_conditioning.md](10_finite_qm_core/sources/qm_021_measurement_update_as_idempotent_conditioning.md) | `DS-QM021-IDEMPOTENT-CONDITIONING` |
| `atlas/foundations/qm_030_finite_weighted_transport_calculus.md` | [qm_030_finite_weighted_transport_calculus.md](11_finite_qm_dynamics/sources/qm_030_finite_weighted_transport_calculus.md) | `DS-QM030-GRADED-PATHSUM`, `DS-QM030-UNGRADED-OVERCOUNT`, `DS-QM030-TRANSFER-OPERATOR-SHADOW`, `DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT` |
| `atlas/foundations/qm_031_finite_path_sum_as_graded_transport.md` | [qm_031_finite_path_sum_as_graded_transport.md](11_finite_qm_dynamics/sources/qm_031_finite_path_sum_as_graded_transport.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/foundations/qm_032_gtta_feynman_finite_shadow_histories.md` | [qm_032_gtta_feynman_finite_shadow_histories.md](11_finite_qm_dynamics/sources/qm_032_gtta_feynman_finite_shadow_histories.md) | `DS-QM032-FINITE-FEYNMAN-SHADOW`, `DS-QM032-CONTINUUM-LIMIT-CONDITIONAL` |
| `atlas/foundations/qm_033_schrodinger_finite_shadow.md` | [qm_033_schrodinger_finite_shadow.md](11_finite_qm_dynamics/sources/qm_033_schrodinger_finite_shadow.md) | `DS-QM033-SCHRODINGER-DISCRETE-COCHAIN`, `DS-QM033-064-074-083-QHELD-CONTINUUM` |
| `atlas/foundations/qm_034_unitary_finite_shadow.md` | [qm_034_unitary_finite_shadow.md](11_finite_qm_dynamics/sources/qm_034_unitary_finite_shadow.md) | `DS-QM034-035-050-051-095-RESERVED-STUBS` |
| `atlas/foundations/qm_035_hamiltonian_generator_admission.md` | [qm_035_hamiltonian_generator_admission.md](11_finite_qm_dynamics/sources/qm_035_hamiltonian_generator_admission.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/foundations/qm_040_matrix_vs_diffeq_representation.md` | [qm_040_matrix_vs_diffeq_representation.md](11_finite_qm_dynamics/sources/qm_040_matrix_vs_diffeq_representation.md) | `DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS` |
| `atlas/foundations/qm_041_heisenberg_picture_shadow.md` | [qm_041_heisenberg_picture_shadow.md](11_finite_qm_dynamics/sources/qm_041_heisenberg_picture_shadow.md) | `DS-QM041-HEISENBERG-PICTURE-FINITE` |
| `atlas/foundations/qm_043_gellmann_hartle_cochain_decoherence.md` | [qm_043_gellmann_hartle_cochain_decoherence.md](12_finite_qm_structure/sources/qm_043_gellmann_hartle_cochain_decoherence.md) | `DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT`, `DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY` |
| `atlas/foundations/qm_060_superposition_as_the_quotient_fiber.md` | [qm_060_superposition_as_the_quotient_fiber.md](12_finite_qm_structure/sources/qm_060_superposition_as_the_quotient_fiber.md) | `DS-QM060-SUPERPOSITION-QUOTIENT-FIBER` |
| `atlas/foundations/qm_061_interference_as_the_non_l1_resource.md` | [qm_061_interference_as_the_non_l1_resource.md](12_finite_qm_structure/sources/qm_061_interference_as_the_non_l1_resource.md) | `DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE`, `DS-QM061-BUILDABILITY-SET-S` |
| `atlas/foundations/qm_062_the_u1_selector.md` | [qm_062_the_u1_selector.md](08_l1_to_l2/sources/qm_062_the_u1_selector.md) | `DS-QM062-U1-SELECTOR-LAYERS`, `DS-QM062-U1-RESIDUES-IMPORT` |
| `atlas/foundations/qm_063_holonomy_structured_superposition.md` | [qm_063_holonomy_structured_superposition.md](14_finite_gauge/sources/qm_063_holonomy_structured_superposition.md) | `DS-QM063-HOLONOMY-COHERENT-INTENSITY` |
| `atlas/foundations/qm_070_product_non_factorization_as_a_bipartite_obstruction.md` | [qm_070_product_non_factorization_as_a_bipartite_obstruction.md](27_tensor_composition/sources/qm_070_product_non_factorization_as_a_bipartite_obstruction.md) | `DS-QM070-PRODUCT-NONFACTORIZATION` |
| `atlas/foundations/qm_071_entanglement_as_a_separability_obstruction.md` | [qm_071_entanglement_as_a_separability_obstruction.md](27_tensor_composition/sources/qm_071_entanglement_as_a_separability_obstruction.md) | `DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS` |
| `atlas/foundations/qm_072_bit_shadow_and_qubit.md` | [qm_072_bit_shadow_and_qubit.md](09_finite_hilbert/sources/qm_072_bit_shadow_and_qubit.md) | `DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED` |
| `atlas/foundations/qm_073_correlation_separability_finite_bell.md` | [qm_073_correlation_separability_finite_bell.md](12_finite_qm_structure/sources/qm_073_correlation_separability_finite_bell.md) | `DS-QM073-FINITE-CHSH-AND-PR-BOX`, `DS-QM073-BELL-THEOREM-OBSTRUCTED` |
| `atlas/foundations/qm_080_cptp_trace_norm_geometry_and_quantum_dual_witnesses.md` | [qm_080_cptp_trace_norm_geometry_and_quantum_dual_witnesses.md](13_finite_qm_information/sources/qm_080_cptp_trace_norm_geometry_and_quantum_dual_witnesses.md) | `DS-QM080-IMPORT-FREE-TRACE-NORM-CORE`, `DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION` |
| `atlas/foundations/qm_081_trace_norm_cptp_transport_audit.md` | [qm_081_trace_norm_cptp_transport_audit.md](13_finite_qm_information/sources/qm_081_trace_norm_cptp_transport_audit.md) | `DS-QM081-CPTP-MONOTONE-NOT-SELECTING`, `DS-QM081-STOCHASTIC-L1-CONTRACTION` |
| `atlas/foundations/qm_082_channels_as_stochastic_kernels_and_the_cptp_lift.md` | [qm_082_channels_as_stochastic_kernels_and_the_cptp_lift.md](13_finite_qm_information/sources/qm_082_channels_as_stochastic_kernels_and_the_cptp_lift.md) | `DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL` |
| `atlas/foundations/qm_090_interpretations_as_authority_shadows.md` | [qm_090_interpretations_as_authority_shadows.md](12_finite_qm_structure/sources/qm_090_interpretations_as_authority_shadows.md) | `DS-QM090-092-AUTHORITY-FIREWALL`, `DS-QM090-093-O022-REGISTRY-RELATIVE-MINIMALITY`, `DS-QM090-093-QM-UNIQUENESS-TIER3` |
| `atlas/foundations/qm_091_deutsch_everett_wolfram_promotion_error.md` | [qm_091_deutsch_everett_wolfram_promotion_error.md](12_finite_qm_structure/sources/qm_091_deutsch_everett_wolfram_promotion_error.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/foundations/qm_093_from_q_to_gtfoc_finite_descent_of_quantum_structure.md` | [qm_093_from_q_to_gtfoc_finite_descent_of_quantum_structure.md](04_authorization/sources/qm_093_from_q_to_gtfoc_finite_descent_of_quantum_structure.md) | `DS-QM093-SURVIVAL-THEOREM`, `DS-QM093-QUANTUM-COCHAIN-D1D0-ZERO` |
| `atlas/foundations/qm_094_everettian_relative_state_contact.md` | [qm_094_everettian_relative_state_contact.md](12_finite_qm_structure/sources/qm_094_everettian_relative_state_contact.md) | `DS-QM094-EVERETT-RELATIVE-STATE-CONTACT` |
| `atlas/foundations/qm_095_copenhagen_as_authority_shadow.md` | [qm_095_copenhagen_as_authority_shadow.md](12_finite_qm_structure/sources/qm_095_copenhagen_as_authority_shadow.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/foundations/qm_101_threshold_theorems_as_repair_capacity_certificates.md` | [qm_101_threshold_theorems_as_repair_capacity_certificates.md](13_finite_qm_information/sources/qm_101_threshold_theorems_as_repair_capacity_certificates.md) | `DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE` |
| `atlas/foundations/qm_102_fault_tolerance_repair_capacity.md` | [qm_102_fault_tolerance_repair_capacity.md](13_finite_qm_information/sources/qm_102_fault_tolerance_repair_capacity.md) | `DS-QM102-SYNDROME-CAPACITY-BOUND` |
| `atlas/foundations/qm_103_packet_evidence_checklist.md` | [qm_103_packet_evidence_checklist.md](04_authorization/sources/qm_103_packet_evidence_checklist.md) | `DS-QM103-SHOW-THE-PACKET-PROTOCOL` |
| `atlas/foundations/qm_120_mermin_peres_contextuality_cochain_obstruction.md` | [qm_120_mermin_peres_contextuality_cochain_obstruction.md](12_finite_qm_structure/sources/qm_120_mermin_peres_contextuality_cochain_obstruction.md) | `DS-QM120-MERMIN-PERES-F2-OBSTRUCTION` |
| `atlas/foundations/qm_122_brought_readme.md` | [qm_122_brought_readme.md](09_finite_hilbert/sources/qm_122_brought_readme.md) | `L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE`, `L1-QM122-CIRCLE-SELECTOR-BOUNDARY`, `L1-QM122-BORN-PAIRING-NONUNIQUE`, `L1-QM122-LEFTOVER-MNC-NOT-RECOVERED` |
| `atlas/foundations/qm_122_finite_hilbert_boundary_from_primitive_difference.md` | [qm_122_finite_hilbert_boundary_from_primitive_difference.md](09_finite_hilbert/sources/qm_122_finite_hilbert_boundary_from_primitive_difference.md) | `L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE`, `L1-QM122-CIRCLE-SELECTOR-BOUNDARY`, `L1-QM122-BORN-PAIRING-NONUNIQUE`, `L1-QM122-LEFTOVER-MNC-NOT-RECOVERED`, `TFQ-0104`, `TFQ-0316` |
| `atlas/foundations/qm_212_microsoft_majorana_problem.md` | [qm_212_microsoft_majorana_problem.md](28_majorana/sources/qm_212_microsoft_majorana_problem.md) | `DS-QM212-MAJORANA-PROBLEM` |
| `atlas/foundations/README.md` | [README.md](08_l1_to_l2/sources/foundations_inventory.md) | `L1-IMP-COMPLEX-FIELD`, `L1-IMP-SECTOR-SYMMETRY-LAW`, `L1-IMP-LINEAR-ISOMETRIC-DYNAMICS`, `L1-IMP-TRANSITION-PROBABILITY-LAW`, `FQ-OPERATIONAL-LOCAL-TOMOGRAPHY`, `FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION`, `TFQ-0084` (+15 in manifest) |
| `atlas/foundations/theory_of_finite_quantum_foundations.md` | [theory_of_finite_quantum_foundations.md](08_l1_to_l2/sources/theory_of_finite_quantum_foundations.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/core/dressing_field_proofs.md` | [dressing_field_proofs.md](24_dressing_field/sources/dressing_field_proofs.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/core/fermion_sign_and_majorana_proofs.md` | [fermion_sign_and_majorana_proofs.md](26_fsp/sources/fermion_sign_and_majorana_proofs.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/core/finite_qm_guide_map.md` | [finite_qm_guide_map.md](10_finite_qm_core/sources/finite_qm_guide_map.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/core/finite_quantum_mechanics.md` | [finite_quantum_mechanics.md](10_finite_qm_core/sources/finite_quantum_mechanics.md) | `FQ-CARRIER-CONTRACT-V2`, `FQ-PRIMDIFF-QUOTIENT-KERNEL`, `FQ-POSITIVE-WEIGHTS-ADMITTED`, `FQ-DECLARED-QUANTUM-INTERFACE`, `FQ-PRIM-TO-QM-SELECTION-OPEN`, `FQ-PHASE-FIBER-QUOTIENT`, `FQ-PHASE-BLIND-DESCENT-ZERO-RETAINED` (+24 in manifest) |
| `atlas/core/finite_quantum_mechanics_change_log.md` | [finite_quantum_mechanics_change_log.md](10_finite_qm_core/sources/finite_quantum_mechanics_change_log.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/core/finite_quantum_mechanics_claim_ledger.md` | [finite_quantum_mechanics_claim_ledger.md](10_finite_qm_core/sources/finite_quantum_mechanics_claim_ledger.md) | `FQ-PRIMDIFF-QUOTIENT-KERNEL`, `FQ-PHASE-FIBER-QUOTIENT`, `FQ-BORN-NORMALIZATION-REDUNDANCY`, `FQ-INTERFERENCE-NONDESCENT`, `FQ-SORKIN-READOUT-CLASS-QM208`, `FQ-CABELLO-NO-INTEGER-FRAME`, `FQ-BUSCH-EFFECT-FRAME` |
| `atlas/core/finite_quantum_mechanics_proofs.md` | [finite_quantum_mechanics_proofs.md](10_finite_qm_core/sources/finite_quantum_mechanics_proofs.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/core/finite_quantum_mechanics_source_notes.md` | [finite_quantum_mechanics_source_notes.md](10_finite_qm_core/sources/finite_quantum_mechanics_source_notes.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/core/frontier_finite_targets_proofs.md` | [frontier_finite_targets_proofs.md](19_finite_qg/sources/frontier_finite_targets_proofs.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/core/master_derivation_ledger.md` | [master_derivation_ledger.md](10_finite_qm_core/sources/master_derivation_ledger.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/core/mub6_proofs.md` | [mub6_proofs.md](25_mub/sources/mub6_proofs.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/core/tensor_composition_proofs.md` | [tensor_composition_proofs.md](27_tensor_composition/sources/tensor_composition_proofs.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/computation/computation_proofs.md` | [computation_proofs.md](../../atlas/computation_complexity_pvnp/computation_proofs.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |
| `atlas/complexity/p_vs_np_and_eth_from_genesis.md` | [p_vs_np_and_eth_from_genesis.md](../../atlas/computation_complexity_pvnp/p_vs_np_and_eth_from_genesis.md) | See the stage chapter and TFQ index; no direct node attribution inferred. |

## Historical citations in custody-pinned TFQ papers

The operad-pinned TFQ papers retain their original bytes and therefore retain
older path spellings in their citation labels. Resolve those labels as follows:

| Historical label prefix | Current local file or directory |
|---|---|
| `lean4/quantum_mechanics/DerivationDagQMClosure.lean` | [DerivationDagQMClosure.lean](../../lean4/DerivationDagQMClosure.lean) |
| `lean4/quantum_mechanics/LggrFiniteResults.lean` | [LggrFiniteResults.lean](../../lean4/LggrFiniteResults.lean) |
| `atlas/papers/finite_obstruction_calculus/` | [finite_obstruction_calculus](../../atlas/finite_obstruction_calculus/) |

`atlas/...` labels in the observer-presheaf fragment name the
external source tree. They are provenance identifiers rather than links to
this checkout. These mappings repair navigation only; they do not verify a
Lean declaration or change the status of a claim.

## Consolidation policy

- The new chapters are the canonical short narrative; the TFQ papers define individual claims.
- Full proof texts and claim ledgers retain their source identity and author/license statements.
- Older PDF/TeX exports are historical artifacts, not regenerated editions of the new chapters.
- Teaching renderers depend on earlier versions, so all versions and review history stay together.
- Existing receipt hashes are not silently resealed after relocation.
- A source title match does not establish duplicate content. Unique source bytes were retained.

The former `atlas/core/master_derivation_ledger.md` is an older generated snapshot, now in
`10_finite_qm_core/sources/master_derivation_ledger.md`. The live ledger is
[MASTER_DERIVATION_LEDGER.md](MASTER_DERIVATION_LEDGER.md); its generator now writes only that file.
