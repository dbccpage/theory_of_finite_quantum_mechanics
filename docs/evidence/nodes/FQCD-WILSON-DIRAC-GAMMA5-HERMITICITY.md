# FQCD-WILSON-DIRAC-GAMMA5-HERMITICITY

Stage: [FINITE_QCD](../stages/FINITE_QCD.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On a finite periodic hypercubic lattice in dimension 2 or 4 with arbitrary unitary link matrices U_mu(x), Hermitian Euclidean gamma matrices and gamma5 anticommuting with each gamma_mu, the Wilson-Dirac operator D_W = m + sum_mu \[gamma_mu (nabla_mu + nabla*_mu)/2 - (r/2) nabla*_mu nabla_mu\] with real m and r satisfies gamma5 D_W gamma5 = D_W^dagger.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 38
- distinct cited Lean declarations covered by a current replay receipt: 33
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (3 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Prove the operator identity in Lean for the finite lattice. A proof would supply the hypothesis that FSP-WILSON-DIRAC-GAMMA5 now imports; lean4/FermionSignWilsonDiracGamma5.lean states only the Clifford and determinant lemmas, not this identity.

## Source status

Lean formalizes the explicit four-component/four-direction rational kernel, its Matrix wrapper, and real/nonnegative two-flavor determinant under backward-kernel adjointness. The original dimension-2/4 periodic-lattice and arbitrary-Clifford-representation target remains OPEN pending its carrier/Clifford/refinement bridge. Python independently checks a complete colored periodic fixture and rational block examples.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/FQCD/StrongCouplingAreaLaw.lean`

- file: [lean4/FQCD/StrongCouplingAreaLaw.lean](../../../lean4/FQCD/StrongCouplingAreaLaw.lean)
- sha256 (`bytes`): `9f32c0851eac5b2326999627e68f6d35da1f73bb1f05cd001a998cc971d8108b`
- cited in: node.lean, receipt dag/research/campaign_tfq-1050_lean_replay.json (FQCD.StrongCouplingAreaLaw), record TFQ-1050
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

### Lean: `lean4/FermionSignWilsonDiracGamma5.lean`

- file: [lean4/FermionSignWilsonDiracGamma5.lean](../../../lean4/FermionSignWilsonDiracGamma5.lean)
- sha256 (`bytes`): `ff846e497a572038d084022f188dfb1ec05affba46ff2c8c652a2c4f1cd3664e`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/campaign_fsp-wilson-dirac-gamma5_lean_replay.json](../../../dag/research/campaign_fsp-wilson-dirac-gamma5_lean_replay.json) (module `FermionSignWilsonDiracGamma5`): recorded sha256 `ff846e497a572038d084022f188dfb1ec05affba46ff2c8c652a2c4f1cd3664e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FermionSignWilsonDiracGamma5`
- counts toward the grade: yes

### Rust: `code/rust/src/fqcd/strong_coupling_area_law.rs`

- file: [code/rust/src/fqcd/strong_coupling_area_law.rs](../../../code/rust/src/fqcd/strong_coupling_area_law.rs)
- sha256 (`bytes`): `77a4ad95936ec2877d60f2e822b5cff928dce88fde556c94e433e89f3f10d3c4`
- cited in: node.rust, record TFQ-1050

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `theta_vacuum_and_wilson_dirac_operator_identity` (rust_symbol) | yes | yes | yes | - | - |
| `wilson_dirac_gamma5_and_two_flavor_positivity` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/check_tfq_1050_fqcd_wilson_dirac_gamma5_hermiticity.py`

- file: [checks/independent/check_tfq_1050_fqcd_wilson_dirac_gamma5_hermiticity.py](../../../checks/independent/check_tfq_1050_fqcd_wilson_dirac_gamma5_hermiticity.py)
- sha256 (`bytes`): `7c124b96e870da0e88958ff76b1c84cc95e36957864906c510ca154527e82606`
- cited in: node.source, record TFQ-1050

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `check` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/fqcd/strong_coupling_area_law.py`

- file: [code/python/src/fqcd/strong_coupling_area_law.py](../../../code/python/src/fqcd/strong_coupling_area_law.py)
- sha256 (`bytes`): `d4126f41b339972b44a93918d4357eac419ddb395f505be11bb0132e809d615b`
- cited in: record TFQ-1050

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `theta_vacuum_and_wilson_dirac_operator_identity_rational` (python_symbol) | yes | yes | yes | - | - |
| `wilson_dirac_gamma5_and_two_flavor_positivity_rational` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/17_finite_qcd/tfq_1050_fqcd_wilson_dirac_gamma5_hermiticity.md`

- file: [dag/derivations/17_finite_qcd/tfq_1050_fqcd_wilson_dirac_gamma5_hermiticity.md](../../../dag/derivations/17_finite_qcd/tfq_1050_fqcd_wilson_dirac_gamma5_hermiticity.md)
- sha256 (`lf-normalised`): `ea254951a81b50256dd872369b2ddec14d4ec92f5607f7d6e22140dbaef992cd`
- generated view: listed, not counted
- cited in: record TFQ-1050
- counts toward the grade: no

### Documents and data: `papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md`

- file: [papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md](../../../papers/drafts/finite_lattice_gauge_theory_yang_mills_qcd.md)
- sha256 (`lf-normalised`): `dc388eaf79ed91e73233db79e15204ea6d67ba06bc5c30867589d745af7ae5f6`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQCD-R-WILSON-DIRAC-GAMMA5-HERMITICITY` `GAP_NO_DERIVATION`: [TFQ-0026](TFQ-0026.md) (OPEN), [FSP-WILSON-DIRAC-GAMMA5](FSP-WILSON-DIRAC-GAMMA5.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

