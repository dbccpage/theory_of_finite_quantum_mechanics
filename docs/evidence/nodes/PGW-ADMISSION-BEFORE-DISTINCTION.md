# PGW-ADMISSION-BEFORE-DISTINCTION

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Given the corrected state, the full replay answered that the task of making \<a\> and \<ab\> internally distinguishable cannot be evaluated until \<ab\> is brought into the regime. The first addition can supply \<ab\> as data or write it into a rule pattern; the two are equally minimal and neither is uniquely forced. After Prompt 19 admitted \<ab\> beside \<a\> with no comparison, counting or matching, nothing in the regime reacts to them differently, so admission alone distinguishes nothing and no unique continuation is dictated. The requirement recorded is an order: the regime must admit inscriptions, retain them across turns and replay the current state before a separation task on them can be posed.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A recorded requirement drawn from model replies that no host checker evaluated; the two-flag Lean and Python models encode admission acts and separation by declaration and do not choose a first addition.

## Source status

recorded requirement: 000_oepregen 02_trial_record.md Prompts 18 and 19; curriculum Lesson 8; v1 Trial 2 main result

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisDerivation/Paper000.lean`

- file: [lean4/Imported/GenesisDerivation/Paper000.lean](../../../lean4/Imported/GenesisDerivation/Paper000.lean)
- sha256 (`bytes`): `9a0973383847018f21e8dbd13ceadda298a6cdbd10321d4bfa7eabf1a1e76d04`
- cited in: node.lean, record TFQ-0428
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.GenesisDerivation.Paper000`): recorded sha256 `9a0973383847018f21e8dbd13ceadda298a6cdbd10321d4bfa7eabf1a1e76d04` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Paper000.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `single_admission_does_not_separate` | yes | yes | yes | none | `#print axioms single_admission_does_not_separate` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/genesis_checks.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/genesis_checks.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/genesis_checks.py)
- sha256 (`bytes`): `570c898692c070d22f655f96d74e0e468e1f4905ea52f917d28237056b7589c1`
- cited in: record TFQ-0428

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `single_admission_report` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/01_pregenesis/tfq_0428_admission_before_distinction.md`

- file: [dag/derivations/01_pregenesis/tfq_0428_admission_before_distinction.md](../../../dag/derivations/01_pregenesis/tfq_0428_admission_before_distinction.md)
- sha256 (`lf-normalised`): `bb2c8598c36b124f99d8f730d1fadcf1735a780d1f6e6dc3c14dd64b508b136a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0428
- counts toward the grade: no

### Documents and data: `education/pregenesis_empty_mark/sources/analysis_derivation_v1.md`

- file: [education/pregenesis_empty_mark/sources/analysis_derivation_v1.md](../../../education/pregenesis_empty_mark/sources/analysis_derivation_v1.md)
- sha256 (`lf-normalised`): `0a9068781f8c282418f8ae2933ae6502b1bef56df91c16758cf730de1e359149`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:2e49c338376d7a78a6a89cdd340c9b3c351c485c20d4127e3c455b3fb1570428:132-149`
- `external:sha256:e15c1002c287921ce12959d4de7d7a313402443ec53dcb1d8159a017eb8c0b0d:179-194`

## Absences recorded by the TFQ records

- TFQ-0428 rust: no Rust two-flag admission model; Genesis admission events are step in genesis/code/rust/src/admission.rs

## Routes

Incoming (1):

- `PGW-R-ADMISSION-BEFORE-DISTINCTION` `DERIVED_PROSE`: [TFQ-0364](TFQ-0364.md) (SOURCE_RECORD), [PG-SIX-OPERATIONS](PG-SIX-OPERATIONS.md) (DEFINITION)

Outgoing (1):

- `UDG-R-TFQ-0429` `RECORD_PARENT`: [TFQ-0429](TFQ-0429.md) (SOURCE_RECORD)
