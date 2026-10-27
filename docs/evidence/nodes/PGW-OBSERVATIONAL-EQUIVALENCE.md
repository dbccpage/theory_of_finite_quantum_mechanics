# PGW-OBSERVATIONAL-EQUIVALENCE

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Relative to the family O_n of internal observations available at stage n, x ≈ₙ y holds exactly when o(x) = o(y) for every o in O_n, with equality taken in each observation's codomain. If O_n is empty, every pair is equivalent vacuously, so with no observations \<a\> ≈ₙ \<ab\>. This is regime-relative equivalence: it does not make the strings equal and does not install an equality operator inside the regime.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- A declared carrier of inscriptions and a declared family O_n of observations on it (assumption)

## Bottleneck

The relation depends on the declared O_n and compares observation values in the metatheory; it is not literal string equality and does not say which observations a regime should have.

## Source status

genesis paper.md section 4 definition; v1 Formalization B; 000_oepregen rewriting Definition 2.3

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/PreGenesisToMssn/Observation.lean`

- file: [lean4/Imported/PreGenesisToMssn/Observation.lean](../../../lean4/Imported/PreGenesisToMssn/Observation.lean)
- sha256 (`bytes`): `ccbdc2919571c7267a4dc3697bf9b59bbbaa4e37481a731dd6649ebdefce12e1`
- cited in: node.lean, record TFQ-0421
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.PreGenesisToMssn.Observation`): recorded sha256 `ccbdc2919571c7267a4dc3697bf9b59bbbaa4e37481a731dd6649ebdefce12e1` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/PreGenesisToMssn/Observation.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `SameProfile` | yes | yes | yes | none | `#print axioms SameProfile` |
| `empty_profiles_equal` | yes | yes | yes | Quot.sound, propext | `#print axioms empty_profiles_equal` |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis/paper.md](../../../atlas/papers/finite_obstruction_calculus/genesis/paper.md)
- sha256 (`lf-normalised`): `0dde974e14ff1b54ff6e65705a1194aea38fad7e65bf77b159a07ea1b96bb9a5`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/01_pregenesis/tfq_0421_observational_equivalence.md`

- file: [dag/derivations/01_pregenesis/tfq_0421_observational_equivalence.md](../../../dag/derivations/01_pregenesis/tfq_0421_observational_equivalence.md)
- sha256 (`lf-normalised`): `e3ce1bea8448c27a8d11afd3904769745ad8243bac5d7cb298b08f80ac8f561e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0421
- counts toward the grade: no

### Documents and data: `education/pregenesis_empty_mark/sources/analysis_derivation_v1.md`

- file: [education/pregenesis_empty_mark/sources/analysis_derivation_v1.md](../../../education/pregenesis_empty_mark/sources/analysis_derivation_v1.md)
- sha256 (`lf-normalised`): `0a9068781f8c282418f8ae2933ae6502b1bef56df91c16758cf730de1e359149`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:1713d12cc07cce5f295bb69922c49e278be2277c31d4fecee6b41ecb87d639bb:64-70`

## Absences recorded by the TFQ records

- TFQ-0421 python: no Python ≈ₙ check over Pre-Genesis inscriptions; the Genesis profile instance is separable in genesis/code/derivation/observe.py
- TFQ-0421 rust: no Rust observation-family type for Pre-Genesis inscriptions; the Genesis profile instance is separable in genesis/code/rust/src/separability.rs

## Routes

Incoming (1):

- `PGW-R-OBSERVATIONAL-EQUIVALENCE` `DERIVED_PROSE`: [PG-INERT-DIAMOND](PG-INERT-DIAMOND.md) (DEFINITION)

Outgoing (1):

- `PGW-R-PRESENTATION-NOT-EXPRESSIVE-LIFT` `CONDITIONAL_ON_IMPORT`: [PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT](PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT.md) (CONDITIONAL)
