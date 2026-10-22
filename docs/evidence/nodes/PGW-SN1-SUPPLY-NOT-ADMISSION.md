# PGW-SN1-SUPPLY-NOT-ADMISSION

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> S(1) supplies \<a\>. Supply(\<a\>) alone leaves the admitted regime unchanged (supply_no_op), and AdmitDatum(\<a\>) is a separate event that may create one admitted datum. The sealed source records that whether \<a\> is admitted at Challenge 1 is underdetermined, and that the two sub-readings converge at Challenge 2 because admission deduplicates on presentation identity. With no admitted instances every pair of data is observationally collapsed, even with uniform rules present (collapsed_of_no_insts). The ledger value s₁ = 1 is chosen for the exercise that issues the demand obs_unconsumed_mark and is not inferred from singleton cardinality.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `proved_lean_below_e3`: grade E0; 2 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 2 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

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

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0512_sn1_supply_not_admission.md`

- file: [dag/derivations/05_mssn_sn/tfq_0512_sn1_supply_not_admission.md](../../../dag/derivations/05_mssn_sn/tfq_0512_sn1_supply_not_admission.md)
- sha256 (`lf-normalised`): `d13482e52878b3d4a663f3c6492572da7f85b643a7e0f2dcf0a9763df79c2f65`
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

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean::collapsed_of_no_insts`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean::supply_no_op`
- `external:the_symbol_game/omega_engine_education/documentation/002_oesn/code/sn_core.py::S1Supply`

## Absences recorded by the TFQ records

- TFQ-0512 rust: no Rust check of supply versus admission in the S(n) strand

## Routes

Incoming (1):

- `PGW-R-SN1-SUPPLY-NOT-ADMISSION` `DERIVED_LEAN`: [PGW-SN0-GROUND-INERTIA](PGW-SN0-GROUND-INERTIA.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-SN2-OPAQUE-COLLAPSE` `DERIVED_LEAN`: [PGW-SN2-OPAQUE-COLLAPSE](PGW-SN2-OPAQUE-COLLAPSE.md) (PROVED_LEAN)
