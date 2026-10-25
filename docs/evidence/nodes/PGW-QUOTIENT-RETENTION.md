# PGW-QUOTIENT-RETENTION

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Let fine and coarse be equivalence relations on one set with every fine identification also a coarse one. The map \[x\]_fine ↦ \[x\]_coarse is well defined and surjective (collapseMap_surjective), injective exactly when every coarse identification also holds finely (collapseMap_injective_iff_reverse_refinement), and successive such maps compose without choosing representatives (collapseMap_compose). If a former identification fails in the finer relation, two distinct fine classes remain over one coarse class (failed_identification_retains_two_classes).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A theorem about supplied equivalence relations: no class is manufactured and no new primitive is inferred, and which identifications a later stage must retain is a declared task.

## Source status

paper.md section 10 (ledger WDP-P000-020); QuotientRetention.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/QuotientRetention.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/QuotientRetention.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/QuotientRetention.lean)
- sha256 (`bytes`): `21096d9353090ed454a70c74d01268b334e6a113a6adbb20a501aed8be9eb36c`
- cited in: node.lean, node.source, record TFQ-0457
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.QuotientRetention`): recorded sha256 `21096d9353090ed454a70c74d01268b334e6a113a6adbb20a501aed8be9eb36c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/QuotientRetention.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapseMap_compose` | yes | yes | yes | Quot.sound | `#print axioms collapseMap_compose` |
| `collapseMap_injective_iff_reverse_refinement` | yes | yes | yes | Quot.sound, propext | `#print axioms collapseMap_injective_iff_reverse_refinement` |
| `collapseMap_surjective` | yes | yes | yes | Quot.sound | `#print axioms collapseMap_surjective` |
| `failed_identification_retains_two_classes` | yes | yes | yes | Quot.sound, propext | `#print axioms failed_identification_retains_two_classes` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0457_quotient_retention.md`

- file: [dag/derivations/02_genesis/tfq_0457_quotient_retention.md](../../../dag/derivations/02_genesis/tfq_0457_quotient_retention.md)
- sha256 (`lf-normalised`): `b763b34d59183bd7c2cb31cbada440aa994a05201a1e6dd8c4b8a5d8e2bc3657`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0457
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/fixtures/historical_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/fixtures/historical_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0457 python: no Python check of quotient retention
- TFQ-0457 rust: no Rust check of quotient retention

## Routes

Incoming (1):

- `PGW-R-QUOTIENT-RETENTION` `DERIVED_LEAN`: [PGW-FIVE-PRESENTATION-QUESTIONS](PGW-FIVE-PRESENTATION-QUESTIONS.md) (DEFINITION)

Outgoing (1):

- `PGW-R-FAITHFUL-DESCENT-ROUND-TRIP` `DERIVED_LEAN`: [PGW-FAITHFUL-DESCENT-ROUND-TRIP](PGW-FAITHFUL-DESCENT-ROUND-TRIP.md) (PROVED_LEAN)
