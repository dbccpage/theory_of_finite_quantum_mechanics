# FQCD-STRONG-COUPLING-AREA-LAW

Stage: [FINITE_QCD](../stages/FINITE_QCD.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Target: in an explicitly justified non-screening regime for a finite gauge group G and nontrivial irreducible unitary representation R in dimension d \>= 2, construct the finite periodic-lattice Wilson expectation and derive explicit beta_0 \> 0, K and sigma \> 0 such that |\<W_R(C)\>| \<= K exp(-sigma Area(C)) for rectangular loops C and 0 \<= beta \< beta_0 on lattices with stated size and boundary conditions. Current Lean lemmas establish the bound only for abstract expectations supplied with the cluster bounds; arbitrary higher-dimensional representations are not covered.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 36
- distinct cited Lean declarations covered by a current replay receipt: 34
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- AbelianWilsonExpectation.cluster_expansion_bound
- NonAbelianWilsonExpectation.center_protected_bound
- CenterProtectedHypothesis.spanning_minimality
- Identification of exact2DDecimationValue with the finite Wilson measure

## Bottleneck

Define the actual finite Wilson configuration sum and normalization, derive its character expansion, and prove the cluster/animal estimates currently supplied as structure fields, including in the abelian case. Prove the identification of the 2D decimation definition with an integrated expectation under explicit boundary conditions. Derive the non-screening and spanning-minimality premises for the claimed regime; a zero cubic character sum alone is insufficient. This would replace the declared formula in TFQ-0024 by a derived strong-coupling inequality, with no weak-coupling or continuum claim.

## Source status

Lean establishes geometric bound consequences for abstract expectation structures: the abelian case assumes AbelianWilsonExpectation.cluster_expansion_bound; the nonabelian case assumes NonAbelianWilsonExpectation.center_protected_bound and spanning minimality. The 2D decimation theorem unfolds a prescribed formula. Neither constructs the finite lattice Wilson measure or derives its cluster expansion. Rust/Python examples do not discharge these general premises. Status remains CONDITIONAL.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FQCD/StrongCouplingAreaLaw.lean`

- file: [lean4/FQCD/StrongCouplingAreaLaw.lean](../../../lean4/FQCD/StrongCouplingAreaLaw.lean)
- sha256 (`bytes`): `9f32c0851eac5b2326999627e68f6d35da1f73bb1f05cd001a998cc971d8108b`
- cited in: node.lean, receipt dag/research/campaign_tfq-1052_lean_replay.json (FQCD.StrongCouplingAreaLaw), record TFQ-1052
- replay: `verified`
  - receipt [dag/research/campaign_tfq-1050_lean_replay.json](../../../dag/research/campaign_tfq-1050_lean_replay.json) (module `FQCD.StrongCouplingAreaLaw`): recorded sha256 `9f32c0851eac5b2326999627e68f6d35da1f73bb1f05cd001a998cc971d8108b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/campaign_tfq-1052_lean_replay.json](../../../dag/research/campaign_tfq-1052_lean_replay.json) (module `FQCD.StrongCouplingAreaLaw`): recorded sha256 `9f32c0851eac5b2326999627e68f6d35da1f73bb1f05cd001a998cc971d8108b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/FQCD/StrongCouplingAreaLaw.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FQCD.a5_cubic_invariants_exact` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.a5_cubic_invariants_exact` |
| `FQCD.abelian_strong_coupling_area_law` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.abelian_strong_coupling_area_law` |
| `FQCD.assembledWilsonDiracChemPotMatrix_intertwining_and_phase_quenched_positivity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.assembledWilsonDiracChemPotMatrix_intertwining_and_phase_quenched_positivity` |
| `FQCD.assembledWilsonDirac_composes_fermionSignWilsonDiracGamma5_det_positivity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.assembledWilsonDirac_composes_fermionSignWilsonDiracGamma5_det_positivity` |
| `FQCD.baryon_vs_gluon_screening_casimir_ratios_and_mednykh_2d_towers` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.baryon_vs_gluon_screening_casimir_ratios_and_mednykh_2d_towers` |
| `FQCD.binary_icosahedral_2i_invariants_and_protection` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.binary_icosahedral_2i_invariants_and_protection` |
| `FQCD.center_protected_3d_strong_coupling_area_law` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.center_protected_3d_strong_coupling_area_law` |
| `FQCD.complete_blichfeldt_ffk_su3_crystal_hierarchy_and_halving_laws` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.complete_blichfeldt_ffk_su3_crystal_hierarchy_and_halving_laws` |
| `FQCD.cubic_invariant_screening_perimeter_receipt` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.cubic_invariant_screening_perimeter_receipt` |
| `FQCD.d4_multi_plaquette_collar_contraction_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.d4_multi_plaquette_collar_contraction_bound` |
| `FQCD.finite_coupling_galois_conjugate_suppression_and_heat_kernel_damping` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.finite_coupling_galois_conjugate_suppression_and_heat_kernel_damping` |
| `FQCD.finite_group_2d_character_decimation_area_law` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.finite_group_2d_character_decimation_area_law` |
| `FQCD.finite_lattice_assembled_wilson_dirac_gamma5_hermiticity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.finite_lattice_assembled_wilson_dirac_gamma5_hermiticity` |
| `FQCD.finite_lattice_wilson_dirac_operator_gamma5_hermiticity_identity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.finite_lattice_wilson_dirac_operator_gamma5_hermiticity_identity` |
| `FQCD.ginsparg_wilson_overlap_relation_and_luscher_index_across_doubler_shells` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.ginsparg_wilson_overlap_relation_and_luscher_index_across_doubler_shells` |
| `FQCD.hessian_subgroups_and_quartic_adjoint_casimir_obstruction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.hessian_subgroups_and_quartic_adjoint_casimir_obstruction` |
| `FQCD.higher_genus_mednykh_abelianization_asymptotics_and_genus3_bounds` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.higher_genus_mednykh_abelianization_asymptotics_and_genus3_bounds` |
| `FQCD.klarner_lattice_animal_geometric_sum` | yes | yes | yes | module-level | `#print axioms FQCD.klarner_lattice_animal_geometric_sum` |
| `FQCD.klein_sigma168_invariants_and_complete_su3_defect_chain` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.klein_sigma168_invariants_and_complete_su3_defect_chain` |
| `FQCD.overlap_modified_chirality_involution` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.overlap_modified_chirality_involution` |
| `FQCD.overlap_modified_chirality_matrix_square` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.overlap_modified_chirality_matrix_square` |
| `FQCD.petcher_weingarten_bhanot_rebbi_freezing_defect_bounds` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.petcher_weingarten_bhanot_rebbi_freezing_defect_bounds` |
| `FQCD.quartic_character_invariants_and_su3_continuum_matching` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.quartic_character_invariants_and_su3_continuum_matching` |
| `FQCD.s4_cubic_invariants_exact` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.s4_cubic_invariants_exact` |
| `FQCD.strong_coupling_to_freezing_regime_separation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.strong_coupling_to_freezing_regime_separation` |
| `FQCD.su2_binary_polyhedral_ade_tower_defects_and_invariants` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.su2_binary_polyhedral_ade_tower_defects_and_invariants` |
| `FQCD.su2_higher_spin_casimir_obstruction_and_hessian_defect_enclosure` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.su2_higher_spin_casimir_obstruction_and_hessian_defect_enclosure` |
| `FQCD.su3_subgroup_tower_defects_and_freezing_scales` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.su3_subgroup_tower_defects_and_freezing_scales` |
| `FQCD.temporal_gauge_perron_frobenius_gap_and_2d_pachner_mednykh_invariance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.temporal_gauge_perron_frobenius_gap_and_2d_pachner_mednykh_invariance` |
| `FQCD.theta_vacuum_cp_symmetry_and_luscher_sector_partition_sum` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.theta_vacuum_cp_symmetry_and_luscher_sector_partition_sum` |
| `FQCD.valentiner_sigma1080_invariants_exact` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.valentiner_sigma1080_invariants_exact` |
| `FQCD.wilsonDirac2x2Det_unit_r` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.wilsonDirac2x2Det_unit_r` |
| `FQCD.wilson_dirac_chemical_potential_asymmetry_and_nielsen_ninomiya_doublers` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.wilson_dirac_chemical_potential_asymmetry_and_nielsen_ninomiya_doublers` |
| `FQCD.wilson_dirac_gamma5_hermiticity_and_two_flavor_det_positivity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms FQCD.wilson_dirac_gamma5_hermiticity_and_two_flavor_det_positivity` |

- counts toward the grade: yes

### Rust: `code/rust/src/fqcd/strong_coupling_area_law.rs`

- file: [code/rust/src/fqcd/strong_coupling_area_law.rs](../../../code/rust/src/fqcd/strong_coupling_area_law.rs)
- sha256 (`bytes`): `77a4ad95936ec2877d60f2e822b5cff928dce88fde556c94e433e89f3f10d3c4`
- cited in: node.rust, record TFQ-1052

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `theta_vacuum_and_wilson_dirac_operator_identity` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/fqcd/strong_coupling_area_law.py`

- file: [code/python/src/fqcd/strong_coupling_area_law.py](../../../code/python/src/fqcd/strong_coupling_area_law.py)
- sha256 (`bytes`): `d4126f41b339972b44a93918d4357eac419ddb395f505be11bb0132e809d615b`
- cited in: record TFQ-1052

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `theta_vacuum_and_wilson_dirac_operator_identity_rational` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/17_finite_qcd/finite_lattice_gauge_theory_yang_mills_qcd.md`

- file: [dag/derivations/17_finite_qcd/finite_lattice_gauge_theory_yang_mills_qcd.md](../../../dag/derivations/17_finite_qcd/finite_lattice_gauge_theory_yang_mills_qcd.md)
- sha256 (`lf-normalised`): `8a802a811b96cbe022372b44d51b43396f36bc54c8f2302bb76716383ad5e11c`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/17_finite_qcd/tfq_1052_fqcd_strong_coupling_area_law.md`

- file: [dag/derivations/17_finite_qcd/tfq_1052_fqcd_strong_coupling_area_law.md](../../../dag/derivations/17_finite_qcd/tfq_1052_fqcd_strong_coupling_area_law.md)
- sha256 (`lf-normalised`): `59b15614363a4c6de5c9d75281879d230648657bd59ddc8c1a9f0880cfe5c938`
- generated view: listed, not counted
- cited in: record TFQ-1052
- counts toward the grade: no

## Routes

Incoming (1):

- `FQCD-R-STRONG-COUPLING-AREA-LAW` `GAP_NO_DERIVATION`: [TFQ-0030](TFQ-0030.md) (COMPUTATIONALLY_CHECKED), [TFQ-0024](TFQ-0024.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

