# PGW-REPLAY-NECESSITY

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Let H be the possible histories, σ(h) the state that history h produces and π(h) the part of h an auditor sees, for example only the last turn. If π(h₁) = π(h₂) but σ(h₁) ≠ σ(h₂), no auditor A that sees only π reports σ(h) for every h, because A(π(h₁)) = A(π(h₂)) would give σ(h₁) = σ(h₂). The trial failures motivate the theorem: the blind auditor flagged the licensed words 'We' (Trial 1) and 'rule' (Trial 2) as imports, so an audit needs two levels; in Trial 2, Prompt 14's false attribution was answered without objection, so claim provenance is a check separate from claim correctness, Result 15 lost the state, saying the regime contains only \<\> after \<a\> had been supplied; and the two-level auditor, shown only that turn, answered None. State certification therefore needs replay information that separates the relevant histories, and on a declared finite population a summary on which σ is constant per fiber of the view can stand in for the raw history.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

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

### Lean: `lean4/Imported/GenesisDerivation/Paper000.lean`

- file: [lean4/Imported/GenesisDerivation/Paper000.lean](../../../lean4/Imported/GenesisDerivation/Paper000.lean)
- sha256 (`bytes`): `9a0973383847018f21e8dbd13ceadda298a6cdbd10321d4bfa7eabf1a1e76d04`
- cited in: node.lean, record TFQ-0426
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.GenesisDerivation.Paper000`): recorded sha256 `9a0973383847018f21e8dbd13ceadda298a6cdbd10321d4bfa7eabf1a1e76d04` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Paper000.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `insufficient_history_view` | yes | yes | yes | none | `#print axioms insufficient_history_view` |
| `no_factor_through_common_view` | yes | yes | yes | none | `#print axioms no_factor_through_common_view` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/code/rust/src/main.rs`

- file: [atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/code/rust/src/main.rs](../../../atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/code/rust/src/main.rs)
- sha256 (`bytes`): `127c739edb34bb27c861a04090204049628934a3966c81bdbf1df33ab4a062dd`
- cited in: node.rust, record TFQ-0426

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `factor` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/genesis_checks.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/genesis_checks.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/genesis_checks.py)
- sha256 (`bytes`): `570c898692c070d22f655f96d74e0e468e1f4905ea52f917d28237056b7589c1`
- cited in: record TFQ-0426

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `history_auditor` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_genesis_checks.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_genesis_checks.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_genesis_checks.py)
- sha256 (`bytes`): `5bed3c5a8de7055ecba70dc88846ef73b3aed42cd7e713e08f6a3fd2e494d17e`
- cited in: record TFQ-0426
- check: `python -m pytest atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_genesis_checks.py::test_quotient_and_history_refuse_collapsed_answers`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_quotient_and_history_refuse_collapsed_answers` (python_test) | yes | yes | yes | - | `python -m pytest atlas/papers/finite_obstruction_calculus/genesis/code/tests/test_genesis_checks.py::test_quotient_and_history_refuse_collapsed_answers` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/01_pregenesis/tfq_0426_replay_necessity.md`

- file: [dag/derivations/01_pregenesis/tfq_0426_replay_necessity.md](../../../dag/derivations/01_pregenesis/tfq_0426_replay_necessity.md)
- sha256 (`lf-normalised`): `268f0893d65f09edc5ee8d18b9210d2b7731572d09c1ed5b121e0ab4e39112b7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0426
- counts toward the grade: no

### Documents and data: `education/pregenesis_empty_mark/sources/analysis_derivation_v1.md`

- file: [education/pregenesis_empty_mark/sources/analysis_derivation_v1.md](../../../education/pregenesis_empty_mark/sources/analysis_derivation_v1.md)
- sha256 (`lf-normalised`): `0a9068781f8c282418f8ae2933ae6502b1bef56df91c16758cf730de1e359149`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:1713d12cc07cce5f295bb69922c49e278be2277c31d4fecee6b41ecb87d639bb:100-106`
- `external:sha256:2e49c338376d7a78a6a89cdd340c9b3c351c485c20d4127e3c455b3fb1570428:101-111`

## Routes

Incoming (1):

- `PGW-R-REPLAY-NECESSITY` `DERIVED_LEAN`: [TFQ-0364](TFQ-0364.md) (SOURCE_RECORD), [PG-COLLAPSE-BARRIER](PG-COLLAPSE-BARRIER.md) (PROVED_LEAN), [PG-HISTORY-REPORT-CRITERION](PG-HISTORY-REPORT-CRITERION.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-CONTEXT-FIDELITY` `GAP_NO_DERIVATION`: [PGW-CONTEXT-FIDELITY](PGW-CONTEXT-FIDELITY.md) (OPEN)
