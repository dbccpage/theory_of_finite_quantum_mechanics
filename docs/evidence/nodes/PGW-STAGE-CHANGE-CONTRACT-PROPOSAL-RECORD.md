# PGW-STAGE-CHANGE-CONTRACT-PROPOSAL-RECORD

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The sealed GraphGenesis.ProposalRecord s is a represented growth proposal at state s whose fields are exactly: a block proved to be a member of the complete family upFamily s (branch-local, with no canonicality or uniqueness claim); an embedding and a retraction with retract (embed x) = x for every represented position x \< s.occ.length; freshness of every token the block admits; preservation of every old asserted, retained and protected pair and of every pair the declared observation separates, transported along embed; a new pair equal to (parentPos, freshPos) with the parent represented and the fresh position the next one; and a declared cost : Nat. It has no license, execution or activation field: on a halted state its block replays to the same state (proposal_confers_no_execution), and upProposal inhabits the record with the identity embedding on a store-bounded live state. The education audit reads this record as the stage-change contract for S(n).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

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

### Lean: `lean4/Imported/GenesisDerivation/Derivation/GraphGenesis.lean`

- file: [lean4/Imported/GenesisDerivation/Derivation/GraphGenesis.lean](../../../lean4/Imported/GenesisDerivation/Derivation/GraphGenesis.lean)
- sha256 (`bytes`): `dd2535c2e513ae346da495683120e3603b8e705b01e157fc159a971e41957337`
- cited in: node.lean, node.source, record TFQ-0494
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisDerivation.Derivation.GraphGenesis`): recorded sha256 `dd2535c2e513ae346da495683120e3603b8e705b01e157fc159a971e41957337` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisDerivation/Derivation/GraphGenesis.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ProposalRecord` | yes | yes | yes | Quot.sound, propext | `#print axioms ProposalRecord` |
| `proposal_confers_no_execution` | yes | yes | yes | Quot.sound, propext | `#print axioms proposal_confers_no_execution` |
| `upProposal` | yes | yes | yes | Quot.sound, propext | `#print axioms upProposal` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis/code/derivation/graph_genesis.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/derivation/graph_genesis.py](../../../atlas/papers/finite_obstruction_calculus/genesis/code/derivation/graph_genesis.py)
- sha256 (`bytes`): `47476354529b663f019deddcfd7e04ab66dc888c96bfcbcaba5ca181fe754f0c`
- cited in: record TFQ-0494

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ProposalRecord` (python_symbol) | yes | yes | yes | - | - |
| `carries_no_authority` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0494_stage_change_contract_proposal_record.md`

- file: [dag/derivations/02_genesis/tfq_0494_stage_change_contract_proposal_record.md](../../../dag/derivations/02_genesis/tfq_0494_stage_change_contract_proposal_record.md)
- sha256 (`lf-normalised`): `3b3b4fc6841dd8b92e381637b0da820abf3b286d7967654e2c5f4a8d901c95b5`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0494
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`

- file: `omega_engine_education/documentation/001_oegen/archive/genesis_pre_2026-10-09.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0494 rust: no Rust port of ProposalRecord

## Routes

Incoming (1):

- `PGW-R-STAGE-CHANGE-CONTRACT-PROPOSAL-RECORD` `DERIVED_LEAN`: [PGW-FOUR-GATE-ACTIVE-OBSTRUCTION](PGW-FOUR-GATE-ACTIVE-OBSTRUCTION.md) (DEFINITION)

Outgoing (1):

- `PGW-R-GENESIS-TO-SN-CROSSWALK` `DERIVED_PROSE`: [PGW-GENESIS-TO-SN-CROSSWALK](PGW-GENESIS-TO-SN-CROSSWALK.md) (DEFINITION)
