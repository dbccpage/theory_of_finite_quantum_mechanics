# L1-QM020-THM1-DIRECT-NORMALIZATION

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a list w of rationals with nonzero total W, the normalized list P = w/W sums to one and normalizing P again returns P. For two lists w, w' with positive totals, P(w) = P(w') iff w' = c w for some rational c \> 0. The ray criterion needs positive totals: with W \< 0 the lists w and -w have the same normalization.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Stated over List Rat in BornRedundancy.lean (listSum_normalize, normalize_idempotent, ray_quotient_classification). The source version, which asks only for a nonzero total in the ray criterion, is false for negative totals and is not claimed.

## Source status

Thm 1 \[PROVEN\]; ledger C1 one-line algebra

## Review

- PFP review: [dag/results/L1-QM020-THM1-DIRECT-NORMALIZATION/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM020-THM1-DIRECT-NORMALIZATION/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact idempotence, nonzero scaling and positive-ray-premise controls; general normalization algebra and a negative-ray counterexample in Lean.
  - does not support: Refine arbitrary lists and positive-mass ray classification to the source theorem. Do not claim positive-ray equivalence under nonzero totals alone.
  - next test: Refine arbitrary lists and positive-mass ray classification to the source theorem. Do not claim positive-ray equivalence under nonzero totals alone.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornNormalization.lean`

- file: [lean4/BornNormalization.lean](../../../lean4/BornNormalization.lean)
- sha256 (`bytes`): `83fdfac8a9b2d61cff987d7a8b8cd7acb809afd851d8d6d0369a3ae2b12004c8`
- cited in: record TFQ-0317 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `BornNormalization`): recorded sha256 `83fdfac8a9b2d61cff987d7a8b8cd7acb809afd851d8d6d0369a3ae2b12004c8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornNormalization`
- counts toward the grade: no

### Lean: `lean4/BornRedundancy.lean`

- file: [lean4/BornRedundancy.lean](../../../lean4/BornRedundancy.lean)
- sha256 (`bytes`): `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b`
- cited in: node.lean, record TFQ-0290 (shared), record TFQ-0317 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `BornRedundancy`): recorded sha256 `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornRedundancy`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `listSum_normalize` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms listSum_normalize` |
| `normalize_idempotent` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms normalize_idempotent` |
| `ray_quotient_classification` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ray_quotient_classification` |

- counts toward the grade: yes

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: record TFQ-0317 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`
- counts toward the grade: no

### Lean: `lean4/ProbabilitySimplex.lean`

- file: [lean4/ProbabilitySimplex.lean](../../../lean4/ProbabilitySimplex.lean)
- sha256 (`bytes`): `94547b50c80b02dfef733d5adb798e338d8a6feeebe02e82dade7f5ebe9f7f8a`
- cited in: record TFQ-0167 (shared)
- replay: `none`
- check: `cd lean4 && lake build ProbabilitySimplex`
- counts toward the grade: no

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
- sha256 (`bytes`): `c844d8c003be489580055a725155199cd38ae56ca2f0bbb2dc141f8da77e7c9d`
- cited in: record TFQ-0167 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0290_direct_normalization_of_sector_weights.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0290_direct_normalization_of_sector_weights.md](../../../dag/derivations/08_l1_to_l2/tfq_0290_direct_normalization_of_sector_weights.md)
- sha256 (`lf-normalised`): `9d91fd836966dc16496f2580af4a3b8876195958b350204a2726100c0d4a0007`
- generated view: listed, not counted
- cited in: record TFQ-0290 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/09_finite_hilbert/tfq_0317_three_lean_files_stay_on_a_narrow_carrier.md`

- file: [dag/derivations/09_finite_hilbert/tfq_0317_three_lean_files_stay_on_a_narrow_carrier.md](../../../dag/derivations/09_finite_hilbert/tfq_0317_three_lean_files_stay_on_a_narrow_carrier.md)
- sha256 (`lf-normalised`): `73a019cb7a67400109fee3dfd8fd8f694941b611ed3b2ede245ea82c97e97aca`
- generated view: listed, not counted
- cited in: record TFQ-0317 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/22_implementation_sibling/tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md`

- file: [dag/derivations/22_implementation_sibling/tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md](../../../dag/derivations/22_implementation_sibling/tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md)
- sha256 (`lf-normalised`): `41557758a7050c2588bc74805153b91fb9a233d4f895ea3a484d186cf3b0c2b1`
- generated view: listed, not counted
- cited in: record TFQ-0167 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:10accdc18b88414a6a931a9e7fc887c41090315925cc258605a210ae3a97c286::try_from_weights`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- `external:sha256:8534bf2948b65ab72605a33c219105f09458247c00aa57acc8beb275df568d27:123`
- `external:sha256:c061ef7e709a4bfb47b1bca1c4182aba033ca07cf550c24aac6d9efed6b9f41f#C1`

## Absences recorded by the TFQ records

- TFQ-0167 python: not located
- TFQ-0290 python: no local python twin located for sources/atlas/papers/quantum_foundations/_code/qm_020/code/qm_020_born_normalization_and_conditional_hilbert_lift_core.py
- TFQ-0290 rust: no local rust twin located for external:sha256:2367d7d43e194cf155298ace7054041ae444c67ab6cd71f51cc12cfacda6f3d4

## Routes

Incoming (1):

- `L1-R-THM1` `DERIVED_LEAN`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL)

Outgoing (5):

- `DS-R-MEASUREMENT-CONDITIONING` `COMPUTED`: [DS-QM021-IDEMPOTENT-CONDITIONING](DS-QM021-IDEMPOTENT-CONDITIONING.md) (COMPUTATIONALLY_CHECKED)
- `L1-R-LADDER` `COMPUTED`: [L1-QM121-LADDER-RUNGS-2-6](L1-QM121-LADDER-RUNGS-2-6.md) (COMPUTATIONALLY_CHECKED)
- `L1-R-THM4` `DERIVED_PROSE`: [L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY](L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY.md) (PROVED_PROSE)
- `L1-R-THM6-P1` `COMPUTED`: [L1-QM020-THM6-P1-SCOPE-FENCE](L1-QM020-THM6-P1-SCOPE-FENCE.md) (COMPUTATIONALLY_CHECKED)
- `X-R-BORN-REDUNDANCY-TO-FQ` `DERIVED_LEAN`: [FQ-BORN-NORMALIZATION-REDUNDANCY](FQ-BORN-NORMALIZATION-REDUNDANCY.md) (PROVED_LEAN)
