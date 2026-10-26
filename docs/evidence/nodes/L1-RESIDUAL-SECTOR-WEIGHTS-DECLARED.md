# L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Sectors are residual sectors with declared finite nonnegative masses mu(s), total M \> 0. The carrier is the weight vector w. No derivation of w from the Phi1 / Gamma2 residual is given in the sources read: w is an input to QM_003, QM_012 and QM_020.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 9
- cited Lean, Rust or Python symbols found in their in-repo files: 26
- distinct cited Lean declarations covered by a current replay receipt: 24
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/ResidualSectorWeights.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

None recorded.

## Bottleneck

The general n-cycle, the weighted L1 form with declared masses, the sum-of-squares reading of Gamma2, and any selector other than these two length-4 holonomy checks stay open. The pairs (2, 0) and (0, 2) are one witness that a common coordinate sum does not fix the pair.

## Source status

Conditional. CampaignL1ResidualSectorWeights records the pairs (2, 0) and (0, 2) at coordinate sum 2, and the two length-4 holonomy checks. The weighted form and the general n-cycle stay open.

## Review

- PFP review: [dag/results/L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED/reviews/20261021_batch01a_audit/delivery_review_result.json](../../../dag/results/L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED/reviews/20261021_batch01a_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: For the n-cycle with the unweighted L1 form, the set of minimizing residuals is the scaled simplex of sign-definite cochains with sum S (minimizer_iff); the sector weights are its block sums, which are not a function of (Phi1, Gamma2 = holonomy) for n \>= 2, S != 0 and at least two sectors (sector_weights_not_determined), because (Phi1, Gamma2) determine only the signed holonomy S (hence Phi1 = \|S\| and the sign pattern); any single choice, including the cyclically symmetric average S/n, is an extra declaration, and with unequal declared masses the minimizer concentrates on the minimal-mass edges (native rows) so the masses themselves are the declared input.
  - does not support: Any derivation of declared sector weights from Phi1 and Gamma2 in the setting of the node source: the result is specific to EQUAL edge masses; for a weighted L1 form with a unique minimal-mass edge the minimizer, hence the sector weights, are unique (native weighted rows), so non-derivability can fail in the weighted setting that the node source declares (the masses are then the declared input); a Lean proof of the weighted statement or of the sum-of-squares reading of Gamma2; connected graphs of cycle rank \> 1 (only two DISJOINT cycles are tabulated natively); the Hilbert lift, density matrices or any physical reading of the weights; that the dihedral or cyclic symmetry is itself available (it is an extra declared input).
  - next test: Prove in the kernel that for the weighted form sum_i m_i \|r_i\| with declared positive edge masses the minimizers on the n-cycle are exactly the sign-definite cochains of holonomy S supported on the edges of minimal mass, so that the weights are unique iff the minimal mass is attained once.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornRedundancy.lean`

- file: [lean4/BornRedundancy.lean](../../../lean4/BornRedundancy.lean)
- sha256 (`bytes`): `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `BornRedundancy`): recorded sha256 `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornRedundancy`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `normalize` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms normalize` |

- counts toward the grade: yes

### Lean: `lean4/CampaignL1ResidualSectorWeights.lean`

- file: [lean4/CampaignL1ResidualSectorWeights.lean](../../../lean4/CampaignL1ResidualSectorWeights.lean)
- sha256 (`bytes`): `f8b91f84cece66dcdc6e9423159d31ec17230dbf931a7117e2cb31c073b5275e`
- cited in: node.lean, node.source, receipt dag/research/campaign_l1-residual-sector-weights-declared_lean_replay.json (CampaignL1ResidualSectorWeights), receipt dag/research/pr_364_review_replay.json (CampaignL1ResidualSectorWeights)
- replay: `verified`
  - receipt [dag/research/campaign_l1-residual-sector-weights-declared_lean_replay.json](../../../dag/research/campaign_l1-residual-sector-weights-declared_lean_replay.json) (module `CampaignL1ResidualSectorWeights`): recorded sha256 `f8b91f84cece66dcdc6e9423159d31ec17230dbf931a7117e2cb31c073b5275e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_364_review_replay.json](../../../dag/research/pr_364_review_replay.json) (module `CampaignL1ResidualSectorWeights`): recorded sha256 `f8b91f84cece66dcdc6e9423159d31ec17230dbf931a7117e2cb31c073b5275e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignL1ResidualSectorWeights`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `holonomy_four_divisible` | yes | yes | yes | none | `#print axioms holonomy_four_divisible` |
| `holonomy_two_not_divisible` | yes | yes | yes | Quot.sound, propext | `#print axioms holonomy_two_not_divisible` |
| `same_phi1` | yes | yes | yes | none | `#print axioms same_phi1` |
| `weights_differ` | yes | yes | yes | none | `#print axioms weights_differ` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.even_cycle_sector_weights_require_selector` | yes | yes | yes | propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.even_cycle_sector_weights_require_selector` |
| `QuantumMechanics.DerivationDagQMClosure.l1_even_cycle_symmetry_orbit_canonical_sector_weights` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_even_cycle_symmetry_orbit_canonical_sector_weights` |
| `QuantumMechanics.DerivationDagQMClosure.l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure` |
| `QuantumMechanics.DerivationDagQMClosure.l1_residual_sector_weights_minimizer_nonuniqueness_and_dihedral_selector` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_residual_sector_weights_minimizer_nonuniqueness_and_dihedral_selector` |
| `QuantumMechanics.DerivationDagQMClosure.sector_weights_sum_to_phi1` | yes | yes | yes | propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.sector_weights_sum_to_phi1` |

- counts toward the grade: yes

### Lean: `lean4/H001ProbabilitySimplex.lean`

- file: [lean4/H001ProbabilitySimplex.lean](../../../lean4/H001ProbabilitySimplex.lean)
- sha256 (`bytes`): `a466cf99bcf45d5ba786f52361702a2988400bd210a234cf5f783366a8a47228`
- cited in: record TFQ-0167 (shared)
- replay: `none`
- check: `cd lean4 && lake build H001ProbabilitySimplex`
- counts toward the grade: no

### Lean: `lean4/ResidualSectorWeights.lean`

- file: [lean4/ResidualSectorWeights.lean](../../../lean4/ResidualSectorWeights.lean)
- sha256 (`bytes`): `0409bb9a215f19e3c5a8d30091e4ad25ec7a4e256721b21ae49a1ddc6e3c6dab`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (ResidualSectorWeights)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `ResidualSectorWeights`): recorded sha256 `0409bb9a215f19e3c5a8d30091e4ad25ec7a4e256721b21ae49a1ddc6e3c6dab` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ResidualSectorWeights`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ResidualSectorWeights.c4_instance_two_minimizers` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ResidualSectorWeights.c4_instance_two_minimizers` |
| `ResidualSectorWeights.c4_orbit_sum_not_minimizer` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ResidualSectorWeights.c4_orbit_sum_not_minimizer` |
| `ResidualSectorWeights.class_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ResidualSectorWeights.class_iff` |
| `ResidualSectorWeights.exists_d0_of_hol_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ResidualSectorWeights.exists_d0_of_hol_zero` |
| `ResidualSectorWeights.hol_d0` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ResidualSectorWeights.hol_d0` |
| `ResidualSectorWeights.minimizer_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ResidualSectorWeights.minimizer_iff` |
| `ResidualSectorWeights.minimizer_unique_of_hol_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ResidualSectorWeights.minimizer_unique_of_hol_zero` |
| `ResidualSectorWeights.minimizer_unique_of_one_edge` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ResidualSectorWeights.minimizer_unique_of_one_edge` |
| `ResidualSectorWeights.minimizers_not_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ResidualSectorWeights.minimizers_not_unique` |
| `ResidualSectorWeights.phi1_attained_and_lower_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ResidualSectorWeights.phi1_attained_and_lower_bound` |
| `ResidualSectorWeights.sector_weights_not_determined` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ResidualSectorWeights.sector_weights_not_determined` |
| `ResidualSectorWeights.sector_weights_sum_to_phi1` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ResidualSectorWeights.sector_weights_sum_to_phi1` |
| `ResidualSectorWeights.symmetric_integral_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ResidualSectorWeights.symmetric_integral_iff` |
| `ResidualSectorWeights.symmetric_selector` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ResidualSectorWeights.symmetric_selector` |

- counts toward the grade: yes

### Rust: `code/rust/src/category_theory/foundations/finite_set.rs`

- file: [code/rust/src/category_theory/foundations/finite_set.rs](../../../code/rust/src/category_theory/foundations/finite_set.rs)
- sha256 (`bytes`): `6c154362ed87f04513aa3e3f705ca79a7fbda10be3e797fccf805b6b6ac81f5d`
- cited in: record TFQ-0167 (shared)
- note: no test is cited for this symbol; its crate is tfqm_category_theory
- counts toward the grade: no

### Rust: `code/rust/src/finite_probability/simplex.rs`

- file: [code/rust/src/finite_probability/simplex.rs](../../../code/rust/src/finite_probability/simplex.rs)
- sha256 (`bytes`): `f806fa8ae31e1d13be6cfe1ba131d1ae33c5778f7448c58601e5f2ed6eb7791f`
- cited in: record TFQ-0167 (shared)
- note: no test is cited for this symbol; its crate is tfqm_finite_probability
- counts toward the grade: no

### Rust: `code/rust/src/wdp/lib.rs`

- file: [code/rust/src/wdp/lib.rs](../../../code/rust/src/wdp/lib.rs)
- sha256 (`bytes`): `aa868cc58a3c6fdf1eabfcdd46798329bf560389e83367c574259837d2d3ed4c`
- cited in: record TFQ-0167 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

### Rust: `code/rust/src/wdp/obstruction.rs`

- file: [code/rust/src/wdp/obstruction.rs](../../../code/rust/src/wdp/obstruction.rs)
- sha256 (`bytes`): `d4a9514b3ee22c73ac47193206838c49cd5d908485d2c38dd026cd3bd9416cf8`
- cited in: record TFQ-0354 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_finite_probability/src/simplex.rs`

- file: `omega_engine/crates_rs/omega_finite_probability/src/simplex.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/residual_density_calculus.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/residual_density_calculus.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness` (rust_symbol) | yes | yes | yes | - | - |
| `verify_tranche21_pg_wdp_bridge_sector_weights_qm122_finish_embedding_and_baker_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/l1-residual-sector-weights-declared.py`

- file: [checks/independent/l1-residual-sector-weights-declared.py](../../../checks/independent/l1-residual-sector-weights-declared.py)
- sha256 (`bytes`): `bec830d915f19bb5b74b7cc7347476fa217501aeb3c294d85178af1015c3b3e4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0005_declared_l1_sector_weights.md`

- file: [dag/derivations/07_l1_emergence/tfq_0005_declared_l1_sector_weights.md](../../../dag/derivations/07_l1_emergence/tfq_0005_declared_l1_sector_weights.md)
- sha256 (`lf-normalised`): `5bfcdd145ea360a5aba774afbf97d1ef099783bcb4a5fba0f1b93c741fc57e94`
- generated view: listed, not counted
- cited in: record TFQ-0005
- counts toward the grade: no

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0354_do_not_derive_declared_l1_sector_weights_from_the_phi1_and_gamma2.md`

- file: [dag/derivations/07_l1_emergence/tfq_0354_do_not_derive_declared_l1_sector_weights_from_the_phi1_and_gamma2.md](../../../dag/derivations/07_l1_emergence/tfq_0354_do_not_derive_declared_l1_sector_weights_from_the_phi1_and_gamma2.md)
- sha256 (`lf-normalised`): `18700eae8449b13f08c61fadbbcd7fb803c6f31ab445adda49326decd63e389b`
- generated view: listed, not counted
- cited in: record TFQ-0354 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md](../../../dag/derivations/22_implementation_sibling/tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md)
- sha256 (`lf-normalised`): `1b9b4d68b36532db18e1b689ae85fc7d4cdb38c1031f1712b8b8f64fb01530e6`
- generated view: listed, not counted
- cited in: record TFQ-0167 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/l1-residual-sector-weights-declared.md`

- file: [dag/derivations/independent/l1-residual-sector-weights-declared.md](../../../dag/derivations/independent/l1-residual-sector-weights-declared.md)
- sha256 (`lf-normalised`): `9fc6212bbcd925157cfec1b4ddbcbe51f47a16d6abdb01e925f0879f0403f752`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_l1-residual-sector-weights-declared_lean_replay.json`

- file: [dag/research/campaign_l1-residual-sector-weights-declared_lean_replay.json](../../../dag/research/campaign_l1-residual-sector-weights-declared_lean_replay.json)
- sha256 (`lf-normalised`): `68502bdec2e87341d7851db7c9352a73cd4d71d7ac7abcebe4b105a0a6062dc8`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/003_residual_density_calculus_l1_l2_boundary/qm_003_residual_density_calculus_l1_l2_boundary_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/003_residual_density_calculus_l1_l2_boundary/qm_003_residual_density_calculus_l1_l2_boundary_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/012_density_matrices_as_diagonal_residual_weights/qm_012_density_matrices_as_diagonal_residual_weights_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/012_density_matrices_as_diagonal_residual_weights/qm_012_density_matrices_as_diagonal_residual_weights_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml`

- file: [sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml](../../../sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml)
- sha256 (`lf-normalised`): `2bfb4441352c4206cbd84f3e500e4c3ba817364aff49623a001087ecf12df5a6`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0167 python: not located

## Routes

Incoming (2):

- `L1-R-DECLARED-MASS-TO-WEIGHTS` `CONDITIONAL_ON_IMPORT`: [L1-WDP-WITNESS-MASS](L1-WDP-WITNESS-MASS.md) (DEFINITION)
- `L1-R-RESIDUAL-TO-WEIGHTS` `CONDITIONAL_ON_IMPORT`: [L1-WDP-WINDOW-PHI1-GAMMA2](L1-WDP-WINDOW-PHI1-GAMMA2.md) (DEFINITION), [L1-GS000-EDGEWISE-L1](L1-GS000-EDGEWISE-L1.md) (PROVED_LEAN)

Outgoing (13):

- `DS-R-IDEMPOTENT-FROM-WEIGHTS` `COMPUTED`: [DS-QM021-IDEMPOTENT-CONDITIONING](DS-QM021-IDEMPOTENT-CONDITIONING.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-KERNEL-FROM-WEIGHTS` `DERIVED_LEAN`: [DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL](DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL.md) (PROVED_LEAN)
- `DS-R-OVERCOUNT-WITNESS` `COMPUTED`: [DS-QM030-UNGRADED-OVERCOUNT](DS-QM030-UNGRADED-OVERCOUNT.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-PRODUCT-FROM-WEIGHTS` `DERIVED_LEAN`: [DS-QM070-PRODUCT-NONFACTORIZATION](DS-QM070-PRODUCT-NONFACTORIZATION.md) (PROVED_LEAN)
- `L1-R-COMPLEX-GAP` `GAP_NO_DERIVATION`: [L1-IMP-COMPLEX-FIELD](L1-IMP-COMPLEX-FIELD.md) (CONDITIONAL)
- `L1-R-SQRT-GAP` `GAP_NO_DERIVATION`: [L1-IMP-SQRT-FIELD](L1-IMP-SQRT-FIELD.md) (IMPORTED_ASSUMPTION)
- `L1-R-THM1` `DERIVED_LEAN`: [L1-QM020-THM1-DIRECT-NORMALIZATION](L1-QM020-THM1-DIRECT-NORMALIZATION.md) (PROVED_LEAN)
- `L1-R-THM2A` `DERIVED_LEAN`: [L1-QM020-THM2A-L1-ADDITIVITY-DEFECT](L1-QM020-THM2A-L1-ADDITIVITY-DEFECT.md) (PROVED_LEAN)
- `L1-R-THM3` `DERIVED_LEAN`: [L1-QM020-THM3-ROW-SPARSITY](L1-QM020-THM3-ROW-SPARSITY.md) (PROVED_LEAN)
- `L1-R-TRACE-EMBED` `DERIVED_LEAN`: [L1-OPERATOR-LIFT-TRACE-EMBED-013](L1-OPERATOR-LIFT-TRACE-EMBED-013.md) (PROVED_LEAN)
- `UDG-R-TFQ-0006` `GAP_NO_DERIVATION`: [TFQ-0006](TFQ-0006.md) (OPEN)
- `UDG-R-TFQ-0279` `RECORD_PARENT`: [TFQ-0279](TFQ-0279.md) (SOURCE_RECORD)
- `X-R-WEIGHTS-DECLARED-TO-FQ-POSITIVE-WEIGHTS` `CONDITIONAL_ON_IMPORT`: [FQ-POSITIVE-WEIGHTS-ADMITTED](FQ-POSITIVE-WEIGHTS-ADMITTED.md) (IMPORTED_ASSUMPTION)
