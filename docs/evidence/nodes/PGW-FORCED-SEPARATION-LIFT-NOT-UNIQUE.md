# PGW-FORCED-SEPARATION-LIFT-NOT-UNIQUE

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Suppose an external task requires \<a\> and \<ab\> to differ while the current regime has \<a\> ≈ₙ \<ab\>. Every operation f on the quotient S_n/≈ₙ gives f(\[\<a\>\]) = f(\[\<ab\>\]), so no operation on the current quotient answers the task on every input, and a refinement adding at least one observation o with o(\<a\>) ≠ o(\<ab\>) is forced; the analysis gives this as an argument with proof. The lift is not unique: under a supplied string decoder, 'payload has more than one position' and 'payload contains b' both separate \<a\> from \<ab\> but disagree on \<aa\> (true and false), and full inscription identity also separates the pair while carrying more than one bit. A canonical tower therefore needs a declared minimality or initiality policy, such as fewest new predicates, minimum description length, maximal preservation of old equivalences, a free or initial completion, or retention of every tied minimum branch.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Supplied string decoder for the payloads of \<a\>, \<ab\> and \<aa\>, used only by the non-uniqueness example (assumption)

## Bottleneck

The Lean declarations cover the quotient barrier; the non-uniqueness of the lift rests on the two-predicate example, and no selection policy, fixed ladder of quotients or minimal multiplicity lift is derived.

## Source status

000_oepregen 03_results_and_arguments.md section 5 (statement 5, argument with proof); 000_genesis_19l57g1 paper.md Proposition 1; Lean Paper000.separation_not_on_quotient

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Quot.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Quot.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Quot.lean)
- sha256 (`bytes`): `e2cbacdf63dc0fb91a57c1f02f2dff617353b1973e80d6c78225289d5e08868f`
- cited in: node.lean, record TFQ-0425
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Quot`): recorded sha256 `e2cbacdf63dc0fb91a57c1f02f2dff617353b1973e80d6c78225289d5e08868f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Quot.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `quotient_barrier` | yes | yes | yes | Quot.sound | `#print axioms quotient_barrier` |

- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Paper000.lean`

- file: [lean4/Imported/Genesis19l57g1/Paper000.lean](../../../lean4/Imported/Genesis19l57g1/Paper000.lean)
- sha256 (`bytes`): `1257bc7a308228f6d966fb493abe022f65123d4d5b0bdfeb49ed9dcd9722ce46`
- cited in: node.lean, record TFQ-0425
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.Genesis19l57g1.Paper000`): recorded sha256 `1257bc7a308228f6d966fb493abe022f65123d4d5b0bdfeb49ed9dcd9722ce46` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Paper000.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `separation_not_on_quotient` | yes | yes | yes | none | `#print axioms separation_not_on_quotient` |

- counts toward the grade: yes

### Lean: `lean4/Imported/PreGenesisToMssn/Observation.lean`

- file: [lean4/Imported/PreGenesisToMssn/Observation.lean](../../../lean4/Imported/PreGenesisToMssn/Observation.lean)
- sha256 (`bytes`): `cb6ccaec927d5bea865af8ae40f653a01f4b4301a4b022418e2a52e8df431d79`
- cited in: node.lean, record TFQ-0425
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.PreGenesisToMssn.Observation`): recorded sha256 `cb6ccaec927d5bea865af8ae40f653a01f4b4301a4b022418e2a52e8df431d79` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/PreGenesisToMssn/Observation.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsed_quotient_barrier` | yes | yes | yes | Quot.sound, propext | `#print axioms collapsed_quotient_barrier` |

- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/rust/src/main.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/rust/src/main.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0425_forced_separation_lift_not_unique.md`

- file: [dag/derivations/01_pregenesis/tfq_0425_forced_separation_lift_not_unique.md](../../../dag/derivations/01_pregenesis/tfq_0425_forced_separation_lift_not_unique.md)
- sha256 (`lf-normalised`): `58fc7c28bf72233b59572f7488989421e83b4299673e5492593883fe16b03c66`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0425
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`
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

- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/genesis_checks.py::quotient_factor`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/tests/test_genesis_checks.py::test_quotient_and_history_refuse_collapsed_answers`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/rust/src/main.rs::factor`

## Routes

Incoming (1):

- `PGW-R-FORCED-SEPARATION-LIFT-NOT-UNIQUE` `DERIVED_LEAN`: [PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION](PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION.md) (DEFINITION), [PG-COLLAPSE-BARRIER](PG-COLLAPSE-BARRIER.md) (PROVED_LEAN)

Outgoing (0):

