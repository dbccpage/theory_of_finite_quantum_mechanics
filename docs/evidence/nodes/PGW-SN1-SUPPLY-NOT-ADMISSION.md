# PGW-SN1-SUPPLY-NOT-ADMISSION

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> S(1) supplies \<a\>. Supply(\<a\>) alone leaves the admitted regime unchanged (supply_no_op), and AdmitDatum(\<a\>) is a separate event that may create one admitted datum. The sealed source records that whether \<a\> is admitted at Challenge 1 is underdetermined, and that the two sub-readings converge at Challenge 2 because admission deduplicates on presentation identity. With no admitted instances every pair of data is observationally collapsed, even with uniform rules present (collapsed_of_no_insts). The ledger value s₁ = 1 is chosen for the exercise that issues the demand obs_unconsumed_mark and is not inferred from singleton cardinality.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Ledger value s₁ = 1 and demand label obs_unconsumed_mark, declared by the S(n) exercise (assumption)

## Bottleneck

The arrival of a mark does not issue a demand for context; S1Supply checks a declared count field, and its admit_mark returns a singleton by construction rather than by a source replay.

## Source status

genesis_source.txt section 5 (Challenge 1); 002_oesn level_01_symbol_genesis.md; Lean Derivation/Inertia

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)
- sha256 (`bytes`): `9386f41cf6bbefae8ccb8fdae47f69a33140a0c45b3e6ca9a08f1e9596a922a7`
- cited in: node.lean, record TFQ-0512
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Inertia`): recorded sha256 `9386f41cf6bbefae8ccb8fdae47f69a33140a0c45b3e6ca9a08f1e9596a922a7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsed_of_no_insts` | yes | yes | yes | propext | `#print axioms collapsed_of_no_insts` |
| `supply_no_op` | yes | yes | yes | propext | `#print axioms supply_no_op` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0512_sn1_supply_not_admission.md`

- file: [dag/derivations/05_mssn_sn/tfq_0512_sn1_supply_not_admission.md](../../../dag/derivations/05_mssn_sn/tfq_0512_sn1_supply_not_admission.md)
- sha256 (`lf-normalised`): `0d58b581f2014d91fa45869b424d053073c294b56295d979acdf8118f6a3d216`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0512
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/levels/level_01_symbol_genesis.md`

- file: `omega_engine_education/documentation/002_oesn/levels/level_01_symbol_genesis.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_education/documentation/002_oesn/code/sn_core.py::S1Supply`

## Absences recorded by the TFQ records

- TFQ-0512 rust: no Rust check of supply versus admission in the S(n) strand

## Routes

Incoming (1):

- `PGW-R-SN1-SUPPLY-NOT-ADMISSION` `DERIVED_LEAN`: [PGW-SN0-GROUND-INERTIA](PGW-SN0-GROUND-INERTIA.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-SN2-OPAQUE-COLLAPSE` `DERIVED_LEAN`: [PGW-SN2-OPAQUE-COLLAPSE](PGW-SN2-OPAQUE-COLLAPSE.md) (PROVED_LEAN)
