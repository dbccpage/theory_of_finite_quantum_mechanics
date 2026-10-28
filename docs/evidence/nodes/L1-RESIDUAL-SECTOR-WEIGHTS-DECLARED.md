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

Conditional. L1ResidualSectorWeights records the pairs (2, 0) and (0, 2) at coordinate sum 2, and the two length-4 holonomy checks. The weighted form and the general n-cycle stay open.

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

### Lean: `lean4/L1ResidualSectorWeights.lean`

- file: [lean4/L1ResidualSectorWeights.lean](../../../lean4/L1ResidualSectorWeights.lean)
- sha256 (`bytes`): `0ff32175a547b3980ee5e681ad23ee54264be5fcab12be66cab8e95d8b757e40`
- cited in: node.lean, node.source, receipt dag/research/campaign_l1-residual-sector-weights-declared_lean_replay.json (L1ResidualSectorWeights), receipt dag/research/pr_364_review_replay.json (L1ResidualSectorWeights)
- replay: `verified`
  - receipt [dag/research/campaign_l1-residual-sector-weights-declared_lean_replay.json](../../../dag/research/campaign_l1-residual-sector-weights-declared_lean_replay.json) (module `L1ResidualSectorWeights`): recorded sha256 `0ff32175a547b3980ee5e681ad23ee54264be5fcab12be66cab8e95d8b757e40` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_364_review_replay.json](../../../dag/research/pr_364_review_replay.json) (module `L1ResidualSectorWeights`): recorded sha256 `0ff32175a547b3980ee5e681ad23ee54264be5fcab12be66cab8e95d8b757e40` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build L1ResidualSectorWeights`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `holonomy_four_divisible` | yes | yes | yes | none | `#print axioms holonomy_four_divisible` |
| `holonomy_two_not_divisible` | yes | yes | yes | Quot.sound, propext | `#print axioms holonomy_two_not_divisible` |
| `same_phi1` | yes | yes | yes | none | `#print axioms same_phi1` |
| `weights_differ` | yes | yes | yes | none | `#print axioms weights_differ` |

- counts toward the grade: yes

### Lean: `lean4/ProbabilitySimplex.lean`

- file: [lean4/ProbabilitySimplex.lean](../../../lean4/ProbabilitySimplex.lean)
- sha256 (`bytes`): `94547b50c80b02dfef733d5adb798e338d8a6feeebe02e82dade7f5ebe9f7f8a`
- cited in: record TFQ-0167 (shared)
- replay: `none`
- check: `cd lean4 && lake build ProbabilitySimplex`
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
- sha256 (`bytes`): `96b602326544a81692b2d2b21ca3e555434715918df271de6957c835b91db39d`
- cited in: record TFQ-0167 (shared)
- note: no test is cited for this symbol; its crate is tfqm_finite_probability
- counts toward the grade: no

### Rust: `code/rust/src/wdp/lib.rs`

- file: [code/rust/src/wdp/lib.rs](../../../code/rust/src/wdp/lib.rs)
- sha256 (`bytes`): `9111d9c82247cc2f1e8176b0a0285a788fcd1d2bc6cd2c1d3be81f84f431d235`
- cited in: record TFQ-0167 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

### Rust: `code/rust/src/wdp/obstruction.rs`

- file: [code/rust/src/wdp/obstruction.rs](../../../code/rust/src/wdp/obstruction.rs)
- sha256 (`bytes`): `54a2d6c70adcbfb8ef7203785769515f17ab69b375f47f8f9eca1fb4eaa0bcb7`
- cited in: record TFQ-0354 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

### Rust: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs)
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
- sha256 (`lf-normalised`): `d255cffef32b803ce6549caa29704991ed67cc4af150509a091d4bf4efb72705`
- generated view: listed, not counted
- cited in: record TFQ-0005
- counts toward the grade: no

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0354_do_not_derive_declared_l1_sector_weights_from_the_phi1_and_gamma2.md`

- file: [dag/derivations/07_l1_emergence/tfq_0354_do_not_derive_declared_l1_sector_weights_from_the_phi1_and_gamma2.md](../../../dag/derivations/07_l1_emergence/tfq_0354_do_not_derive_declared_l1_sector_weights_from_the_phi1_and_gamma2.md)
- sha256 (`lf-normalised`): `d4531de0213a9426dd4e3025c034634a7373aed0a94d9b8eb21bcf4f662e1e65`
- generated view: listed, not counted
- cited in: record TFQ-0354 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md](../../../dag/derivations/22_implementation_sibling/tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md)
- sha256 (`lf-normalised`): `41557758a7050c2588bc74805153b91fb9a233d4f895ea3a484d186cf3b0c2b1`
- generated view: listed, not counted
- cited in: record TFQ-0167 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/l1-residual-sector-weights-declared.md`

- file: [dag/derivations/independent/l1-residual-sector-weights-declared.md](../../../dag/derivations/independent/l1-residual-sector-weights-declared.md)
- sha256 (`lf-normalised`): `827599c17b41765fa96d5cedc22708c9255ba217d4afd3eab6130b5416e2cdd1`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_l1-residual-sector-weights-declared_lean_replay.json`

- file: [dag/research/campaign_l1-residual-sector-weights-declared_lean_replay.json](../../../dag/research/campaign_l1-residual-sector-weights-declared_lean_replay.json)
- sha256 (`lf-normalised`): `82c34c8dfe215f0d8d7ed5280d9e06fa16a567267ff62bf35e1aba4a2988b357`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml`

- file: [sources/atlas/papers/quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml](../../../sources/atlas/papers/quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml)
- sha256 (`lf-normalised`): `bb38e1e763dba36d1194fde3c597b73c19f651ec9b4137eeb694fd92fed6f8fb`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:10accdc18b88414a6a931a9e7fc887c41090315925cc258605a210ae3a97c286::try_from_weights`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_l1_sector_weights_and_density_lift_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche21_pg_wdp_bridge_sector_weights_qm122_finish_embedding_and_baker_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche7_wdp_bridge_o03_o05_sector_orbit_and_gleason_rival_witness`
- `external:sha256:8534bf2948b65ab72605a33c219105f09458247c00aa57acc8beb275df568d27:103`
- `external:sha256:91902ad0b3daed220b6cb851493f83faf8fe90131ef5b3e5e3260cc721968c14`
- `external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`
- `external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche21_pg_wdp_bridge_sector_weights_qm122_finish_embedding_and_baker_witness`
- `external:sha256:d89349da5e7fff8fcf0114de9fa43655b5204edb2d0f59b97acd124730751df4#C1`
- `external:sha256:e3c1fb4d47cc71d77c93d54d3e25ddefd4cfd203d33b327084ad5d0426656e6e#RDB-1`

## Absences recorded by the TFQ records

- TFQ-0167 python: not located

## Routes

Incoming (2):

- `L1-R-DECLARED-MASS-TO-WEIGHTS` `CONDITIONAL_ON_IMPORT`: [L1-WDP-WITNESS-MASS](L1-WDP-WITNESS-MASS.md) (DEFINITION)
- `L1-R-RESIDUAL-TO-WEIGHTS` `CONDITIONAL_ON_IMPORT`: [L1-WDP-WINDOW-PHI1-GAMMA2](L1-WDP-WINDOW-PHI1-GAMMA2.md) (DEFINITION), [L1-GS000-EDGEWISE-L1](L1-GS000-EDGEWISE-L1.md) (COMPUTATIONALLY_CHECKED)

Outgoing (13):

- `DS-R-IDEMPOTENT-FROM-WEIGHTS` `COMPUTED`: [DS-QM021-IDEMPOTENT-CONDITIONING](DS-QM021-IDEMPOTENT-CONDITIONING.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-KERNEL-FROM-WEIGHTS` `COMPUTED`: [DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL](DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-OVERCOUNT-WITNESS` `COMPUTED`: [DS-QM030-UNGRADED-OVERCOUNT](DS-QM030-UNGRADED-OVERCOUNT.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-PRODUCT-FROM-WEIGHTS` `COMPUTED`: [DS-QM070-PRODUCT-NONFACTORIZATION](DS-QM070-PRODUCT-NONFACTORIZATION.md) (COMPUTATIONALLY_CHECKED)
- `L1-R-COMPLEX-GAP` `GAP_NO_DERIVATION`: [L1-IMP-COMPLEX-FIELD](L1-IMP-COMPLEX-FIELD.md) (CONDITIONAL)
- `L1-R-SQRT-GAP` `GAP_NO_DERIVATION`: [L1-IMP-SQRT-FIELD](L1-IMP-SQRT-FIELD.md) (IMPORTED_ASSUMPTION)
- `L1-R-THM1` `DERIVED_LEAN`: [L1-QM020-THM1-DIRECT-NORMALIZATION](L1-QM020-THM1-DIRECT-NORMALIZATION.md) (PROVED_LEAN)
- `L1-R-THM2A` `DERIVED_LEAN`: [L1-QM020-THM2A-L1-ADDITIVITY-DEFECT](L1-QM020-THM2A-L1-ADDITIVITY-DEFECT.md) (PROVED_LEAN)
- `L1-R-THM3` `COMPUTED`: [L1-QM020-THM3-ROW-SPARSITY](L1-QM020-THM3-ROW-SPARSITY.md) (COMPUTATIONALLY_CHECKED)
- `L1-R-TRACE-EMBED` `COMPUTED`: [L1-OPERATOR-LIFT-TRACE-EMBED-013](L1-OPERATOR-LIFT-TRACE-EMBED-013.md) (COMPUTATIONALLY_CHECKED)
- `UDG-R-TFQ-0006` `GAP_NO_DERIVATION`: [TFQ-0006](TFQ-0006.md) (OPEN)
- `UDG-R-TFQ-0279` `RECORD_PARENT`: [TFQ-0279](TFQ-0279.md) (SOURCE_RECORD)
- `X-R-WEIGHTS-DECLARED-TO-FQ-POSITIVE-WEIGHTS` `CONDITIONAL_ON_IMPORT`: [FQ-POSITIVE-WEIGHTS-ADMITTED](FQ-POSITIVE-WEIGHTS-ADMITTED.md) (IMPORTED_ASSUMPTION)
