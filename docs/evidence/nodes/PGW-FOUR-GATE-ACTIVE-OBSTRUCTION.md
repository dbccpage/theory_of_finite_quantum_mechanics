# PGW-FOUR-GATE-ACTIVE-OBSTRUCTION

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Declared here as the test a residual must pass before it counts as an active obstruction: obstP = retainedP ∧ protectedP ∧ declaredP ∧ zeroDeclP, that is, the pair is retained in the witness store, carries a protected demand, an observation is declared, and the declared observation does not separate the pair. In the sealed passage system this is an identity of Bool-valued functions at every state and pair (PrimitivePassage.obstP_factors), with sufficiency obst_of_gates and necessity gates_of_obst; the source calls the factorization near-definitional, gives the four-way reading content through the four gate_*_independent theorems, and refutes joint freedom of the gates (obs_gates_not_both_false). zeroDeclP answers true before any observation by a declared convention that never makes anything obstructed (obst_requires_observation). The education module MssnObstructionDetector restates the factorization over supplied observation columns.

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

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Necessity is relative to this predicate, not to any notion of obstruction, and the decomposition is not claimed unique; the education archive's label apnf does not match the current nf.derivation.apnf.yaml, which is the apartness normal form.

## Source status

declared here; Derivation/PrimitivePassage.lean four gates (obstP_factors, obst_of_gates, gates_of_obst); education archive §6 normal-form table

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PrimitivePassage.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PrimitivePassage.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Lean: `omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean`

- file: `omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0493_four_gate_active_obstruction.md`

- file: [dag/derivations/02_genesis/tfq_0493_four_gate_active_obstruction.md](../../../dag/derivations/02_genesis/tfq_0493_four_gate_active_obstruction.md)
- sha256 (`lf-normalised`): `715358696c3bfefec027b2d87100fe2bab6daedd217598c7e94785381999dceb`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0493
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`

- file: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/primitive_passage.py::obst_p`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PrimitivePassage.lean::gates_of_obst`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PrimitivePassage.lean::obstP_factors`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PrimitivePassage.lean::obst_of_gates`
- `external:the_symbol_game/omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean::obstP_factors`

## Absences recorded by the TFQ records

- TFQ-0493 rust: no Rust port of the passage-system obstP; obstruction.rs::obstructed is the kernel's exhausted-menu notion, a different predicate

## Routes

Incoming (1):

- `PGW-R-FOUR-GATE-ACTIVE-OBSTRUCTION` `DERIVED_PROSE`: [PGW-CANDIDATE-EXTENSION-GENERATOR](PGW-CANDIDATE-EXTENSION-GENERATOR.md) (DEFINITION)

Outgoing (1):

- `PGW-R-STAGE-CHANGE-CONTRACT-PROPOSAL-RECORD` `DERIVED_LEAN`: [PGW-STAGE-CHANGE-CONTRACT-PROPOSAL-RECORD](PGW-STAGE-CHANGE-CONTRACT-PROPOSAL-RECORD.md) (PROVED_LEAN)
