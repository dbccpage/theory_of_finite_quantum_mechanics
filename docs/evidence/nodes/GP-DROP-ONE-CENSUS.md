# GP-DROP-ONE-CENSUS

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Eight extras (field C, spectral theorem, Gleason at n\>=3, CPTP, tensor uniqueness, circle group, continuous time, Python dual) are listed with no duplicates; field C, spectral and continuous time are classified lost on this host with obstruction evidence; necessity of the others is OPEN. A census, not a necessity theorem.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Necessity of Gleason, CPTP, tensor uniqueness and circle: OPEN.

## Source status

declared census at merge dba1434b; later finish table

## Review

- PFP review: [dag/results/GP-DROP-ONE-CENSUS/reviews/20261019_structure_audit/review_result.json](../../../dag/results/GP-DROP-ONE-CENSUS/reviews/20261019_structure_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: The actual source-declared eight-entry import census has no duplicates and partitions into three lost labels and five open labels. Counts and partition are recomputed without promoting labels to necessity theorems.
  - does not support: Necessity of the five open extras requires mathematical constructions or countermodels. Source labels and this census alone cannot supply those arguments.
  - next test: Necessity of the five open extras requires mathematical constructions or countermodels. Source labels and this census alone cannot supply those arguments.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/HilbertWalkGleasonExtrasDropOne.lean`

- file: [lean4/HilbertWalkGleasonExtrasDropOne.lean](../../../lean4/HilbertWalkGleasonExtrasDropOne.lean)
- sha256 (`bytes`): `1775f5c8d4c99a99d01cc3465fa8e0abaa7c66f0c1f546da02be6a54d911d11d`
- cited in: node.lean, record TFQ-1038
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `HilbertWalkGleasonExtrasDropOne`): recorded sha256 `1775f5c8d4c99a99d01cc3465fa8e0abaa7c66f0c1f546da02be6a54d911d11d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertWalkGleasonExtrasDropOne`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `drop_one_count` | yes | yes | yes | Quot.sound, propext | `#print axioms drop_one_count` |

- counts toward the grade: yes

### Lean: `lean4/HilbertWalkGleasonFinish.lean`

- file: [lean4/HilbertWalkGleasonFinish.lean](../../../lean4/HilbertWalkGleasonFinish.lean)
- sha256 (`bytes`): `d17eada69f37e9abb28ebc93122facd32716683618eed2c8e19e2b952b84daeb`
- cited in: node.lean, record TFQ-1038
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `HilbertWalkGleasonFinish`): recorded sha256 `d17eada69f37e9abb28ebc93122facd32716683618eed2c8e19e2b952b84daeb` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertWalkGleasonFinish`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `remaining_import_list` | yes | yes | yes | Quot.sound, propext | `#print axioms remaining_import_list` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1038
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1038_gp_drop_one_census.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1038_gp_drop_one_census.md](../../../dag/derivations/10_finite_qm_core/tfq_1038_gp_drop_one_census.md)
- sha256 (`lf-normalised`): `560b599c836af8bea77eccaa13a29c9e38c5d457dc0e53516915ddb22247fd3d`
- generated view: listed, not counted
- cited in: record TFQ-1038
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/finite_hilbert_boundary_from_primitive_difference.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/finite_hilbert_boundary_from_primitive_difference.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `X-R-DROP-ONE-CENSUS` `DERIVED_LEAN`: [GP-IMPORT-COMPLEX-FIELD](GP-IMPORT-COMPLEX-FIELD.md) (IMPORTED_ASSUMPTION), [GP-IMPORT-CIRCLE-U1](GP-IMPORT-CIRCLE-U1.md) (IMPORTED_ASSUMPTION), [GP-IMPORT-GLEASON](GP-IMPORT-GLEASON.md) (IMPORTED_ASSUMPTION), [GP-IMPORT-TENSOR-PRODUCT](GP-IMPORT-TENSOR-PRODUCT.md) (IMPORTED_ASSUMPTION), [GP-IMPORT-CPTP-CLASS](GP-IMPORT-CPTP-CLASS.md) (IMPORTED_ASSUMPTION), [GP-IMPORT-CONTINUOUS-TIME](GP-IMPORT-CONTINUOUS-TIME.md) (IMPORTED_ASSUMPTION), [GP-GAP-EXACT-DUALITY](GP-GAP-EXACT-DUALITY.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

