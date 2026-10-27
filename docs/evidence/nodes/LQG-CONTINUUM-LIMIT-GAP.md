# LQG-CONTINUUM-LIMIT-GAP

Stage: [LOOP_QUANTUM_GRAVITY](../stages/LOOP_QUANTUM_GRAVITY.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No source read for this change derives a continuum limit, a semiclassical limit or a physical cosmological constant from the finite recoupling tables of the repository, or from the exact finite targets of this stage. The fences of TFQ-0104 and TFQ-0105 say so; this node records the gap so that the exact 6j, area and pentagon checks are not read as steps toward a limit. Separate conditional mathematical result: For a supplied finite discrete label alphabet and normalized nonnegative probability laws on every finite set of natural-number coordinates, compatibility under coordinate restriction is equivalent to existence of an infinite projective-limit measure. Under compatibility, that probability measure is unique. Every countable family of measurable finite-window constraints having mass one in its finite law holds almost everywhere simultaneously in the limit, and at least one satisfying infinite configuration exists. The theorem specializes to the three level-two spin labels Fin 3 and arbitrary predicates on their finite windows.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 9
- cited Lean, Rust or Python symbols found in their in-repo files: 21
- distinct cited Lean declarations covered by a current replay receipt: 21
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (3 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- supplied finite discrete label alphabet and product measurable structure
- normalized nonnegative finite laws compatible under all finite coordinate restrictions
- countably many supplied finite-window constraints with probability one

## Bottleneck

The alphabet, discrete topology, product measurable structure, compatible finite probability laws and full-mass constraint premises are supplied. Physical LQG or complex spin-foam amplitudes are not shown to satisfy them. No triangulation refinement, manifold, semiclassical geometry, Einstein dynamics or physical cosmological constant is derived; the original node and physical routes remain OPEN/GAP. Earlier finite-census boundary: The census and the two dimension identities do not discharge a continuum limit, a semiclassical limit, or a physical cosmological constant. No sequence of triangulations and no Einstein equation is constructed. Routes FRO-R-LQG-CONTINUUM-LIMIT-GAP and FRO-R-BACK-LQG-LIMIT-TO-TFQ0105 stay GAP_NO_DERIVATION. The broader audit sentence, that no source read for this change derives a limit, is not discharged in full.

## Source status

Finite census and Q(sqrt 2) dimension identities checked in Lean 4.35.0 on 2026-10-24. Node stays OPEN. No continuum limit, semiclassical limit, or physical cosmological constant is derived. Earlier audit against arXiv:1205.2019 Part V and TFQ-0104/TFQ-0105 was on 2026-10-22. The supplied-family projective probability extension is separately kernel-checked; no physical LQG continuum claim follows.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/LqgContinuumLimitGap.lean`

- file: [lean4/LqgContinuumLimitGap.lean](../../../lean4/LqgContinuumLimitGap.lean)
- sha256 (`bytes`): `4a79e5e6ae40dcc26affad9b69b7a7b061a105e3b3cbdbc44395fecb504e4a39`
- cited in: node.lean, node.source, receipt dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json (LqgContinuumLimitGap)
- replay: `verified`
  - receipt [dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json](../../../dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json) (module `LqgContinuumLimitGap`): recorded sha256 `4a79e5e6ae40dcc26affad9b69b7a7b061a105e3b3cbdbc44395fecb504e4a39` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build LqgContinuumLimitGap`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `LqgContinuumLimitGap.level2_admissible_count` | yes | yes | yes | none | `#print axioms LqgContinuumLimitGap.level2_admissible_count` |
| `LqgContinuumLimitGap.level2_counts_do_not_select_a_scale` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgContinuumLimitGap.level2_counts_do_not_select_a_scale` |
| `LqgContinuumLimitGap.level2_dimension_truncation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgContinuumLimitGap.level2_dimension_truncation` |
| `LqgContinuumLimitGap.level2_free_positive_scale` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgContinuumLimitGap.level2_free_positive_scale` |
| `LqgContinuumLimitGap.level2_tuple_census` | yes | yes | yes | none | `#print axioms LqgContinuumLimitGap.level2_tuple_census` |

- counts toward the grade: yes

### Lean: `lean4/LqgProjectiveLimit.lean`

- file: [lean4/LqgProjectiveLimit.lean](../../../lean4/LqgProjectiveLimit.lean)
- sha256 (`bytes`): `da2eeaf7235a9235d37adfabb167008dbd920d935f71a1d8bb862c142052b3ef`
- cited in: node.lean, node.source, receipt dag/research/campaign_lqg-projective-limit_lean_replay.json (LqgProjectiveLimit), record TFQ-2315
- replay: `verified`
  - receipt [dag/research/campaign_lqg-projective-limit_lean_replay.json](../../../dag/research/campaign_lqg-projective-limit_lean_replay.json) (module `LqgProjectiveLimit`): recorded sha256 `da2eeaf7235a9235d37adfabb167008dbd920d935f71a1d8bb862c142052b3ef` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build LqgProjectiveLimit`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `LqgProjectiveLimit.Config` | yes | yes | yes | none | `#print axioms LqgProjectiveLimit.Config` |
| `LqgProjectiveLimit.constraints_have_configuration` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgProjectiveLimit.constraints_have_configuration` |
| `LqgProjectiveLimit.content_sigma_subadditive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgProjectiveLimit.content_sigma_subadditive` |
| `LqgProjectiveLimit.content_tendsto_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgProjectiveLimit.content_tendsto_zero` |
| `LqgProjectiveLimit.countable_constraints` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgProjectiveLimit.countable_constraints` |
| `LqgProjectiveLimit.cylinder_closed` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgProjectiveLimit.cylinder_closed` |
| `LqgProjectiveLimit.empty_stage` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgProjectiveLimit.empty_stage` |
| `LqgProjectiveLimit.exists_limit_iff_projective` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgProjectiveLimit.exists_limit_iff_projective` |
| `LqgProjectiveLimit.exists_unique_limit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgProjectiveLimit.exists_unique_limit` |
| `LqgProjectiveLimit.limitMeasure` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgProjectiveLimit.limitMeasure` |
| `LqgProjectiveLimit.limit_marginals` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgProjectiveLimit.limit_marginals` |
| `LqgProjectiveLimit.limit_probability` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgProjectiveLimit.limit_probability` |
| `LqgProjectiveLimit.limit_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgProjectiveLimit.limit_unique` |
| `LqgProjectiveLimit.projective_of_limit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgProjectiveLimit.projective_of_limit` |
| `LqgProjectiveLimit.spin_constraints_ae` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgProjectiveLimit.spin_constraints_ae` |
| `LqgProjectiveLimit.spin_labels_extension` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LqgProjectiveLimit.spin_labels_extension` |

- counts toward the grade: yes

### Rust: `code/rust/src/general_relativity/spin_foam.rs`

- file: [code/rust/src/general_relativity/spin_foam.rs](../../../code/rust/src/general_relativity/spin_foam.rs)
- sha256 (`bytes`): `8ab22473e5ebc36ab2cb23247e2d6835664bab9ac0e9f0f26b6ab9b4fd63892e`
- cited in: node.source
- note: no test is cited for this symbol; its crate is tfqm_general_relativity
- counts toward the grade: yes

### Python: `checks/independent/lqg-continuum-limit-gap.py`

- file: [checks/independent/lqg-continuum-limit-gap.py](../../../checks/independent/lqg-continuum-limit-gap.py)
- sha256 (`bytes`): `7a81f17c2b4c021a84348b6eaa13951a111920f338fb3ffabcdf962f5433f52a`
- cited in: node.source
- counts toward the grade: yes

### Python: `checks/independent/lqg-projective-limit.py`

- file: [checks/independent/lqg-projective-limit.py](../../../checks/independent/lqg-projective-limit.py)
- sha256 (`bytes`): `92a2722ef79365d7e7ea13e60d613f3897e801a00878e6ef4d46b1cf613405d4`
- cited in: node.source, record TFQ-2315
- counts toward the grade: yes

### Documents and data: `dag/derivations/33_loop_quantum_gravity/tfq_2315_lqg_continuum_limit_gap.md`

- file: [dag/derivations/33_loop_quantum_gravity/tfq_2315_lqg_continuum_limit_gap.md](../../../dag/derivations/33_loop_quantum_gravity/tfq_2315_lqg_continuum_limit_gap.md)
- sha256 (`lf-normalised`): `9631012f80af4bf39f3145e7140638158effcc07c2da13120181de24a53540cd`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2315
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/lqg-continuum-limit-gap.md`

- file: [dag/derivations/independent/lqg-continuum-limit-gap.md](../../../dag/derivations/independent/lqg-continuum-limit-gap.md)
- sha256 (`lf-normalised`): `838971aee13396e955879ac3c0820840c4546365d5da622375f7193dc2a9ca16`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/independent/lqg-projective-limit.md`

- file: [dag/derivations/independent/lqg-projective-limit.md](../../../dag/derivations/independent/lqg-projective-limit.md)
- sha256 (`lf-normalised`): `e7fab74ded89375031cd49e4efd1655a41ea2a4ae28d28cf225893eba258d125`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json`

- file: [dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json](../../../dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json)
- sha256 (`lf-normalised`): `c14daa2b570129566d5e8bb15a74bb93a8a1baf38430e4bc639b974f8b7e947b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_lqg-projective-limit_lean_replay.json`

- file: [dag/research/campaign_lqg-projective-limit_lean_replay.json](../../../dag/research/campaign_lqg-projective-limit_lean_replay.json)
- sha256 (`lf-normalised`): `62932e8533a0c36d4d5b4de59c83fa3b9dba456c6e886243986d2a1467ccef34`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FRO-R-LQG-CONTINUUM-LIMIT-GAP` `GAP_NO_DERIVATION`: [LQG-EPRL-VERTEX-IMPORT](LQG-EPRL-VERTEX-IMPORT.md) (IMPORTED_ASSUMPTION), [LQG-TV-LEVEL2-PENTAGON-TARGET](LQG-TV-LEVEL2-PENTAGON-TARGET.md) (PROVED_LEAN)

Outgoing (1):

- `FRO-R-BACK-LQG-LIMIT-TO-TFQ0105` `GAP_NO_DERIVATION`: [TFQ-0105](TFQ-0105.md) (SOURCE_RECORD)
