# PGW-SN0-GROUND-INERTIA

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> S(0) supplies the literal \<\> as one opaque token: one presentation-token slot and two ASCII bytes, and neither count is the number of admitted data. In the sealed Genesis model nothing is derivable at genesis (genesis_underivable) and a bare supply leaves every regime unchanged (supply_no_op). The sealed Challenge 0 computation records admitted data empty in reading L and the single opaque datum in reading F, with no internal observables in either reading. The local S(n) Lean model has carrierCard 0 = 0 beside the two-character wire form of the ground token (ground_presentation_vs_carrier), and Carrier 0 has no inhabitant (ground_carrier_empty).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared S(n) example carrier table carrierCard in SnCarrier.lean, chosen and not derived from 19L57G1 (assumption)

## Bottleneck

Zero admitted data is the reading-L and initial-regime statement; in reading F the inscription \<\> is the single admitted datum after its admission event, so the education phrase does not cover reading F. ground_carrier_empty concerns the declared example carrier, not a source replay.

## Source status

genesis_source.txt section 4 (Challenge 0); 002_oesn level_00_ground.md; Lean SnTheorems and Derivation/Inertia

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)
- sha256 (`bytes`): `9386f41cf6bbefae8ccb8fdae47f69a33140a0c45b3e6ca9a08f1e9596a922a7`
- cited in: node.lean, record TFQ-0511
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Inertia`): recorded sha256 `9386f41cf6bbefae8ccb8fdae47f69a33140a0c45b3e6ca9a08f1e9596a922a7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `genesis_underivable` | yes | yes | yes | none | `#print axioms genesis_underivable` |
| `supply_no_op` | yes | yes | yes | propext | `#print axioms supply_no_op` |

- counts toward the grade: yes

### Lean: `lean4/Imported/OeSn/SnTheorems.lean`

- file: [lean4/Imported/OeSn/SnTheorems.lean](../../../lean4/Imported/OeSn/SnTheorems.lean)
- sha256 (`bytes`): `acbabe52a9557e71a1ca32cd81122a70859a1f25c7c4654ec78102c8fc1fcf81`
- cited in: node.lean, record TFQ-0511
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mssn_sn.json](../../../dag/research/lean_replay_campaign_mssn_sn.json) (module `Imported.OeSn.SnTheorems`): recorded sha256 `acbabe52a9557e71a1ca32cd81122a70859a1f25c7c4654ec78102c8fc1fcf81` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/OeSn/SnTheorems.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ground_carrier_empty` | yes | yes | yes | none | `#print axioms ground_carrier_empty` |
| `ground_presentation_vs_carrier` | yes | yes | yes | none | `#print axioms ground_presentation_vs_carrier` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0511_sn0_ground_inertia.md`

- file: [dag/derivations/05_mssn_sn/tfq_0511_sn0_ground_inertia.md](../../../dag/derivations/05_mssn_sn/tfq_0511_sn0_ground_inertia.md)
- sha256 (`lf-normalised`): `e134aa2ed7bc9275225d5f73e7f8f11ce025a5f4edcffaed9f7ee1da081b5323`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0511
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/levels/level_00_ground.md`

- file: `omega_engine_education/documentation/002_oesn/levels/level_00_ground.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/sn.md`

- file: `omega_engine_education/documentation/002_oesn/sn.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine_education/documentation/002_oesn/code/sn_core.py::S0Ground`

## Absences recorded by the TFQ records

- TFQ-0511 rust: no Rust check of the S(0) ground in the S(n) strand

## Routes

Incoming (1):

- `PGW-R-SN0-GROUND-INERTIA` `DERIVED_LEAN`: [PGW-SN-TWO-BOXED-LAWS](PGW-SN-TWO-BOXED-LAWS.md) (DEFINITION)

Outgoing (1):

- `PGW-R-SN1-SUPPLY-NOT-ADMISSION` `DERIVED_LEAN`: [PGW-SN1-SUPPLY-NOT-ADMISSION](PGW-SN1-SUPPLY-NOT-ADMISSION.md) (PROVED_LEAN)
