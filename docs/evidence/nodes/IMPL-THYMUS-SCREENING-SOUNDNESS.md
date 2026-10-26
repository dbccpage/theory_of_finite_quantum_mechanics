# IMPL-THYMUS-SCREENING-SOUNDNESS

Stage: [IMPLEMENTATION](../stages/IMPLEMENTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a screening predicate d and a sealed panel, the screen admits the panel iff d holds on every panel member, and an admitted panel has no false positives under d.

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

Stated in ThymusScreening.lean (thymus_admit_iff, self_panel_soundness). It concerns the repository's screening tool, not quantum mechanics.

## Source status

MECHANIZED in ThymusScreening.lean (empty axiom report) with Rust witness

## Review

- PFP review: [dag/results/IMPL-THYMUS-SCREENING-SOUNDNESS/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/IMPL-THYMUS-SCREENING-SOUNDNESS/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Complete finite panel/predicate controls and mismatch witnesses are exact; zero in-panel false positives under the actual screened predicate is kernel checked.
  - does not support: Bind an actual production detector, executed code and authenticated self-panel to these predicates, and state any out-of-panel assumptions. No generalization beyond the sealed panel or physical immune-system theorem is claimed.
  - next test: Bind an actual production detector, executed code and authenticated self-panel to these predicates, and state any out-of-panel assumptions. No generalization beyond the sealed panel or physical immune-system theorem is claimed.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/OePfp/ThymusScreening.lean`

- file: [lean4/Imported/OePfp/ThymusScreening.lean](../../../lean4/Imported/OePfp/ThymusScreening.lean)
- sha256 (`bytes`): `e10cd45992cd38464dd24eee3e03b48f334726dc37ff010afb1d7dd027db8a74`
- cited in: node.lean, node.source, record TFQ-1045
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_implementation.json](../../../dag/research/lean_replay_campaign_implementation.json) (module `Imported.OePfp.ThymusScreening`): recorded sha256 `e10cd45992cd38464dd24eee3e03b48f334726dc37ff010afb1d7dd027db8a74` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/OePfp/ThymusScreening.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Oeeis.Thymus.self_panel_soundness` | yes | yes | yes | none | `#print axioms Oeeis.Thymus.self_panel_soundness` |
| `Oeeis.Thymus.thymus_admit_iff` | yes | yes | yes | none | `#print axioms Oeeis.Thymus.thymus_admit_iff` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1045
- counts toward the grade: no

### Documents and data: `dag/derivations/21_implementation_core/tfq_1045_impl_thymus_screening_soundness.md`

- file: [dag/derivations/21_implementation_core/tfq_1045_impl_thymus_screening_soundness.md](../../../dag/derivations/21_implementation_core/tfq_1045_impl_thymus_screening_soundness.md)
- sha256 (`lf-normalised`): `ee990b8004adb529a9d90647d3d041658c7003fa343c718ed8f323c58c14b5a4`
- generated view: listed, not counted
- cited in: record TFQ-1045
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml`

- file: [sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml](../../../sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml)
- sha256 (`lf-normalised`): `2bfb4441352c4206cbd84f3e500e4c3ba817364aff49623a001087ecf12df5a6`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `IMPL-R-THYMUS-SCREENING` `DERIVED_LEAN`: [PG-PREGEN-CONSTRUCTIVE-SUMMARY](PG-PREGEN-CONSTRUCTIVE-SUMMARY.md) (PROVED_LEAN)

Outgoing (0):

