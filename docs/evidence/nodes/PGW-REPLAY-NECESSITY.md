# PGW-REPLAY-NECESSITY

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Let H be the possible histories, σ(h) the state that history h produces and π(h) the part of h an auditor sees, for example only the last turn. If π(h₁) = π(h₂) but σ(h₁) ≠ σ(h₂), no auditor A that sees only π reports σ(h) for every h, because A(π(h₁)) = A(π(h₂)) would give σ(h₁) = σ(h₂). The trial failures motivate the theorem: the blind auditor flagged the licensed words 'We' (Trial 1) and 'rule' (Trial 2) as imports, so an audit needs two levels; in Trial 2, Prompt 14's false attribution was answered without objection, so claim provenance is a check separate from claim correctness, Result 15 lost the state, saying the regime contains only \<\> after \<a\> had been supplied; and the two-level auditor, shown only that turn, answered None. State certification therefore needs replay information that separates the relevant histories, and on a declared finite population a summary on which σ is constant per fiber of the view can stand in for the raw history.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declaration references covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The trial contrasts motivate the theorem and do not instantiate it: the truncated window and the full replay received different inputs, so they are not a checked pair with equal auditor views; raw history retention is a provenance policy, and task-sufficient reconstruction is the mathematical requirement.

## Source status

000_oepregen 03_results_and_arguments.md section 6 (statement 6, theorem with proof); v1 Derivation 4; Lean Paper000.insufficient_history_view

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Paper000.lean`

- file: [lean4/Imported/Genesis19l57g1/Paper000.lean](../../../lean4/Imported/Genesis19l57g1/Paper000.lean)
- sha256 (`bytes`): `1257bc7a308228f6d966fb493abe022f65123d4d5b0bdfeb49ed9dcd9722ce46`
- cited in: node.lean, record TFQ-0426
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.Genesis19l57g1.Paper000`): recorded sha256 `1257bc7a308228f6d966fb493abe022f65123d4d5b0bdfeb49ed9dcd9722ce46` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Paper000.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `insufficient_history_view` | yes | yes | yes | none | `#print axioms insufficient_history_view` |
| `no_factor_through_common_view` | yes | yes | yes | none | `#print axioms no_factor_through_common_view` |

- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/rust/src/main.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/rust/src/main.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0426_replay_necessity.md`

- file: [dag/derivations/01_pregenesis/tfq_0426_replay_necessity.md](../../../dag/derivations/01_pregenesis/tfq_0426_replay_necessity.md)
- sha256 (`lf-normalised`): `1cd54de9a136459e4957fda0e6b41448d05f07996af651fae5689296c9ce971b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0426
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/000_oepregen/02_trial_record.md`

- file: `omega_engine_education/documentation/000_oepregen/02_trial_record.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/000_oepregen/03_results_and_arguments.md`

- file: `omega_engine_education/documentation/000_oepregen/03_results_and_arguments.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/000_oepregen/sources/analysis_derivation_v1.md`

- file: `omega_engine_education/documentation/000_oepregen/sources/analysis_derivation_v1.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/genesis_checks.py::history_auditor`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/tests/test_genesis_checks.py::test_quotient_and_history_refuse_collapsed_answers`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/rust/src/main.rs::factor`

## Routes

Incoming (1):

- `PGW-R-REPLAY-NECESSITY` `DERIVED_LEAN`: [TFQ-0364](TFQ-0364.md) (SOURCE_RECORD), [PG-COLLAPSE-BARRIER](PG-COLLAPSE-BARRIER.md) (PROVED_LEAN), [PG-HISTORY-REPORT-CRITERION](PG-HISTORY-REPORT-CRITERION.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-CONTEXT-FIDELITY` `GAP_NO_DERIVATION`: [PGW-CONTEXT-FIDELITY](PGW-CONTEXT-FIDELITY.md) (OPEN)
