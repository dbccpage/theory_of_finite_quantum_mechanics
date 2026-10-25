# PG-PREGEN-CONSTRUCTIVE-SUMMARY

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Constructive (no Classical.choice) Pre-Genesis summary/history theorem for explicitly listed histories: choice-free first-match reconstruction recon satisfies recon_of_fiberConstant and fiberConstant_of_recon in ListedHistorySummary.lean.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 13
- cited Lean declaration references covered by a current replay receipt: 13
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/PregenConstructive.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

None recorded.

## Bottleneck

Applies to explicitly listed histories with decidable report equality; unlisted or infinite populations and report types without decidable equality (choice-free substitute, or unavoidability of choice) remain outside.

## Source status

MECHANIZED in ListedHistorySummary.lean (choice-free listed-history report criterion) with Rust witness

## Review

- PFP review: [dag/results/PG-PREGEN-CONSTRUCTIVE-SUMMARY/reviews/20261021_batch01b_audit/delivery_review_result.json](../../../dag/results/PG-PREGEN-CONSTRUCTIVE-SUMMARY/reviews/20261021_batch01b_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Over an explicit listing with decidable report equality, first-match reconstruction returns every listed answer iff the answer is constant on the listed report fibers, with no axiom in the kernel for the seven general theorems (relative to the supplied DecidableEq instance on reports); off the listing it refuses unreported values and can be wrong on unlisted histories; verified exhaustively on 11 non-degenerate small tuples.
  - does not support: Report types without decidable equality (only the classical instance is covered, its proof term uses Classical.choice, and necessity of choice there is not shown); infinite or unlisted populations beyond the explicit complete-listing hypothesis; the unconditional factorization for an arbitrary history type (node PG-HISTORY-REPORT-CRITERION); the external ListedHistorySummary.lean (not in this repository); any probability, measurement or physical reading of reports.
  - next test: Decide whether the listed criterion survives a report type without decidable equality by a choice-free substitute for the first-match search, or show that the Classical.propDecidable instance is unavoidable there (a choice-free model or an independence argument).

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/OePregen/ListedHistorySummary.lean`

- file: [lean4/Imported/OePregen/ListedHistorySummary.lean](../../../lean4/Imported/OePregen/ListedHistorySummary.lean)
- sha256 (`bytes`): `b3cb2fad54a60c4dc4cfdfd59a7b2c83bc7e3650efed6ded32ffe0b89fa1c4ac`
- cited in: node.lean, node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.OePregen.ListedHistorySummary`): recorded sha256 `b3cb2fad54a60c4dc4cfdfd59a7b2c83bc7e3650efed6ded32ffe0b89fa1c4ac` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/OePregen/ListedHistorySummary.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `PreMssnListed.fiberConstant_of_recon` | yes | yes | yes | none | `#print axioms PreMssnListed.fiberConstant_of_recon` |
| `PreMssnListed.listed_history_report_criterion` | yes | yes | yes | none | `#print axioms PreMssnListed.listed_history_report_criterion` |
| `PreMssnListed.recon_of_fiberConstant` | yes | yes | yes | none | `#print axioms PreMssnListed.recon_of_fiberConstant` |

- counts toward the grade: yes

### Lean: `lean4/PregenConstructive.lean`

- file: [lean4/PregenConstructive.lean](../../../lean4/PregenConstructive.lean)
- sha256 (`bytes`): `6b600af885a14319d1f3cca3afa4631bb388eb8b88aa9b4993d31643538d28d9`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (PregenConstructive)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `PregenConstructive`): recorded sha256 `6b600af885a14319d1f3cca3afa4631bb388eb8b88aa9b4993d31643538d28d9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build PregenConstructive`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `PregenConstructive.fiberConstantOn_of_recon` | yes | yes | yes | none | `#print axioms PregenConstructive.fiberConstantOn_of_recon` |
| `PregenConstructive.instance_reconstructs` | yes | yes | yes | none | `#print axioms PregenConstructive.instance_reconstructs` |
| `PregenConstructive.instance_wrong_off_list` | yes | yes | yes | propext | `#print axioms PregenConstructive.instance_wrong_off_list` |
| `PregenConstructive.listed_factor_exists` | yes | yes | yes | none | `#print axioms PregenConstructive.listed_factor_exists` |
| `PregenConstructive.listed_history_report_criterion` | yes | yes | yes | none | `#print axioms PregenConstructive.listed_history_report_criterion` |
| `PregenConstructive.listed_history_report_criterion_classical` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms PregenConstructive.listed_history_report_criterion_classical` |
| `PregenConstructive.recon_eq_none_iff` | yes | yes | yes | none | `#print axioms PregenConstructive.recon_eq_none_iff` |
| `PregenConstructive.recon_of_fiberConstant` | yes | yes | yes | none | `#print axioms PregenConstructive.recon_of_fiberConstant` |
| `PregenConstructive.recon_unique` | yes | yes | yes | none | `#print axioms PregenConstructive.recon_unique` |
| `PregenConstructive.recon_wrong_off_list` | yes | yes | yes | none | `#print axioms PregenConstructive.recon_wrong_off_list` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0367_listed_history_choice_free_summary.md`

- file: [dag/derivations/01_pregenesis/tfq_0367_listed_history_choice_free_summary.md](../../../dag/derivations/01_pregenesis/tfq_0367_listed_history_choice_free_summary.md)
- sha256 (`lf-normalised`): `02c8878992a584c356641d08a65ce6970dbcf06cf19a739694cac52ba2642557`
- generated view: listed, not counted
- cited in: record TFQ-0367
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml`

- file: [sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml](../../../sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml)
- sha256 (`lf-normalised`): `2bfb4441352c4206cbd84f3e500e4c3ba817364aff49623a001087ecf12df5a6`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:prompts/fable_theorems_2026-10-17/04_pregenesis_constructive_summary.md`

## Absences recorded by the TFQ records

- TFQ-0367 lean4: missing declaration obligation: a choice-free listed-history criterion inside 000_pre_genesis_to_mssn/lean4, where Paper.lean still mentions Classical.choice
- TFQ-0367 python: missing obligation: a first-match reconstructor on an explicit list in 000_pre_genesis_to_mssn/code/preservation.py, beside report_factor and not using an unlisted search
- TFQ-0367 rust: missing obligation: a listed-history reconstructor in crate pre_mssn_preservation whose input length is part of the statement

## Routes

Incoming (1):

- `PG-R-CONSTRUCTIVE-SUMMARY` `DERIVED_LEAN`: [PG-HISTORY-REPORT-CRITERION](PG-HISTORY-REPORT-CRITERION.md) (PROVED_LEAN)

Outgoing (2):

- `IMPL-R-THYMUS-SCREENING` `DERIVED_LEAN`: [IMPL-THYMUS-SCREENING-SOUNDNESS](IMPL-THYMUS-SCREENING-SOUNDNESS.md) (PROVED_LEAN)
- `UDG-R-TFQ-0368` `RECORD_PARENT`: [TFQ-0368](TFQ-0368.md) (SOURCE_RECORD)
