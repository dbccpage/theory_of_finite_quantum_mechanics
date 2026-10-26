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

### Lean: `lean4/CampaignLqgContinuumLimitGap.lean`

- file: [lean4/CampaignLqgContinuumLimitGap.lean](../../../lean4/CampaignLqgContinuumLimitGap.lean)
- sha256 (`bytes`): `a6adec8e3fe5ad9453a5a7ae74767860bd6794957da7dc9393242516b3d49d3d`
- cited in: node.lean, node.source, receipt dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json (CampaignLqgContinuumLimitGap)
- replay: `verified`
  - receipt [dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json](../../../dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json) (module `CampaignLqgContinuumLimitGap`): recorded sha256 `a6adec8e3fe5ad9453a5a7ae74767860bd6794957da7dc9393242516b3d49d3d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignLqgContinuumLimitGap`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignLqgContinuumLimitGap.level2_admissible_count` | yes | yes | yes | none | `#print axioms CampaignLqgContinuumLimitGap.level2_admissible_count` |
| `CampaignLqgContinuumLimitGap.level2_counts_do_not_select_a_scale` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgContinuumLimitGap.level2_counts_do_not_select_a_scale` |
| `CampaignLqgContinuumLimitGap.level2_dimension_truncation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgContinuumLimitGap.level2_dimension_truncation` |
| `CampaignLqgContinuumLimitGap.level2_free_positive_scale` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgContinuumLimitGap.level2_free_positive_scale` |
| `CampaignLqgContinuumLimitGap.level2_tuple_census` | yes | yes | yes | none | `#print axioms CampaignLqgContinuumLimitGap.level2_tuple_census` |

- counts toward the grade: yes

### Lean: `lean4/CampaignLqgProjectiveLimit.lean`

- file: [lean4/CampaignLqgProjectiveLimit.lean](../../../lean4/CampaignLqgProjectiveLimit.lean)
- sha256 (`bytes`): `44e21fe5531a266095edfbf5a78b818b9e2778dd96c8b4bccd4e800c1dac03a5`
- cited in: node.lean, node.source, receipt dag/research/campaign_lqg-projective-limit_lean_replay.json (CampaignLqgProjectiveLimit), record TFQ-2315
- replay: `verified`
  - receipt [dag/research/campaign_lqg-projective-limit_lean_replay.json](../../../dag/research/campaign_lqg-projective-limit_lean_replay.json) (module `CampaignLqgProjectiveLimit`): recorded sha256 `44e21fe5531a266095edfbf5a78b818b9e2778dd96c8b4bccd4e800c1dac03a5` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignLqgProjectiveLimit`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignLqgProjectiveLimit.Config` | yes | yes | yes | none | `#print axioms CampaignLqgProjectiveLimit.Config` |
| `CampaignLqgProjectiveLimit.constraints_have_configuration` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgProjectiveLimit.constraints_have_configuration` |
| `CampaignLqgProjectiveLimit.content_sigma_subadditive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgProjectiveLimit.content_sigma_subadditive` |
| `CampaignLqgProjectiveLimit.content_tendsto_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgProjectiveLimit.content_tendsto_zero` |
| `CampaignLqgProjectiveLimit.countable_constraints` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgProjectiveLimit.countable_constraints` |
| `CampaignLqgProjectiveLimit.cylinder_closed` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgProjectiveLimit.cylinder_closed` |
| `CampaignLqgProjectiveLimit.empty_stage` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgProjectiveLimit.empty_stage` |
| `CampaignLqgProjectiveLimit.exists_limit_iff_projective` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgProjectiveLimit.exists_limit_iff_projective` |
| `CampaignLqgProjectiveLimit.exists_unique_limit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgProjectiveLimit.exists_unique_limit` |
| `CampaignLqgProjectiveLimit.limitMeasure` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgProjectiveLimit.limitMeasure` |
| `CampaignLqgProjectiveLimit.limit_marginals` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgProjectiveLimit.limit_marginals` |
| `CampaignLqgProjectiveLimit.limit_probability` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgProjectiveLimit.limit_probability` |
| `CampaignLqgProjectiveLimit.limit_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgProjectiveLimit.limit_unique` |
| `CampaignLqgProjectiveLimit.projective_of_limit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgProjectiveLimit.projective_of_limit` |
| `CampaignLqgProjectiveLimit.spin_constraints_ae` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgProjectiveLimit.spin_constraints_ae` |
| `CampaignLqgProjectiveLimit.spin_labels_extension` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignLqgProjectiveLimit.spin_labels_extension` |

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
- sha256 (`lf-normalised`): `2aae847f97b286582b81aad805685c6031d848f11a143b00989179508f092f5f`
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
- sha256 (`lf-normalised`): `ffbd674cdda04065f9e14e28b924bad96660bccc0f589c03865994692803663b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json`

- file: [dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json](../../../dag/research/campaign_lqg-continuum-limit-gap_lean_replay.json)
- sha256 (`lf-normalised`): `1b9cfaf12cd195764cd17567b71c47010ae2ba2273cd361c9323c8326eb86239`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_lqg-projective-limit_lean_replay.json`

- file: [dag/research/campaign_lqg-projective-limit_lean_replay.json](../../../dag/research/campaign_lqg-projective-limit_lean_replay.json)
- sha256 (`lf-normalised`): `432d9dad3b30266bc1ea6036ac2c2cffdc27be7793f4a80bac4653e26c99e7f5`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FRO-R-LQG-CONTINUUM-LIMIT-GAP` `GAP_NO_DERIVATION`: [LQG-EPRL-VERTEX-IMPORT](LQG-EPRL-VERTEX-IMPORT.md) (IMPORTED_ASSUMPTION), [LQG-TV-LEVEL2-PENTAGON-TARGET](LQG-TV-LEVEL2-PENTAGON-TARGET.md) (PROVED_LEAN)

Outgoing (1):

- `FRO-R-BACK-LQG-LIMIT-TO-TFQ0105` `GAP_NO_DERIVATION`: [TFQ-0105](TFQ-0105.md) (SOURCE_RECORD)
