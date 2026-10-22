# PGW-STAGE-CHANGE-CONTRACT-PROPOSAL-RECORD

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The sealed GraphGenesis.ProposalRecord s is a represented growth proposal at state s whose fields are exactly: a block proved to be a member of the complete family upFamily s (branch-local, with no canonicality or uniqueness claim); an embedding and a retraction with retract (embed x) = x for every represented position x \< s.occ.length; freshness of every token the block admits; preservation of every old asserted, retained and protected pair and of every pair the declared observation separates, transported along embed; a new pair equal to (parentPos, freshPos) with the parent represented and the fresh position the next one; and a declared cost : Nat. It has no license, execution or activation field: on a halted state its block replays to the same state (proposal_confers_no_execution), and upProposal inhabits the record with the identity embedding on a store-bounded live state. The education audit reads this record as the stage-change contract for S(n).

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

- `proved_lean_below_e3`: grade E0; 3 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 3 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

None recorded.

## Bottleneck

The record is one sufficient schema with no minimality or initiality property, it confers no authority, and its cost is a Nat-valued declared resource demand, not the exact rational cost accounting the education audit describes.

## Source status

Derivation/GraphGenesis.lean Part 2 (ProposalRecord, upProposal, proposal_confers_no_execution); education archive §2 stage-change contract

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/GraphGenesis.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/GraphGenesis.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0494_stage_change_contract_proposal_record.md`

- file: [dag/derivations/02_genesis/tfq_0494_stage_change_contract_proposal_record.md](../../../dag/derivations/02_genesis/tfq_0494_stage_change_contract_proposal_record.md)
- sha256 (`lf-normalised`): `d4fe7ca328a88ebfe4bedd2131d477029af2cd21ad3d0ea1d374ecb940b36ce5`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0494
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`

- file: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/graph_genesis.py::ProposalRecord`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/graph_genesis.py::carries_no_authority`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/GraphGenesis.lean::ProposalRecord`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/GraphGenesis.lean::proposal_confers_no_execution`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/GraphGenesis.lean::upProposal`

## Absences recorded by the TFQ records

- TFQ-0494 rust: no Rust port of ProposalRecord

## Routes

Incoming (1):

- `PGW-R-STAGE-CHANGE-CONTRACT-PROPOSAL-RECORD` `DERIVED_LEAN`: [PGW-FOUR-GATE-ACTIVE-OBSTRUCTION](PGW-FOUR-GATE-ACTIVE-OBSTRUCTION.md) (DEFINITION)

Outgoing (1):

- `PGW-R-GENESIS-TO-SN-CROSSWALK` `DERIVED_PROSE`: [PGW-GENESIS-TO-SN-CROSSWALK](PGW-GENESIS-TO-SN-CROSSWALK.md) (DEFINITION)
