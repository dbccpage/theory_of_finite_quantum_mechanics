# PGW-DRIVER-B-SEVENTH-EVENT

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Narrowed boundary, status left OPEN. The sealed derivation Event has the six constructor names Supply, AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, and Impose. That name list has length 6 and no duplicates. Every event's constructor name is in the list, each of the six names is the name of an event, and the name Seventh is outside the list. Every event's constructor name differs from Seventh.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

These facts are the six constructor names of the sealed derivation Event. They are not a harness refusal and not a theorem that six kinds suffice for every lift. Status stays OPEN.

## Source status

closeout.txt §2.1 retained OPEN and §4 S3; ALPHA_HANDOFF §9 typed outcomes

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwDriverBSeventhEvent.lean`

- file: [lean4/CampaignPgwDriverBSeventhEvent.lean](../../../lean4/CampaignPgwDriverBSeventhEvent.lean)
- sha256 (`bytes`): `c564f055a6e8d1990a81c3100a1ddc8b0c1c70afe7cea1ab919db27d0619a19a`
- cited in: node.lean, receipt dag/research/campaign_pgw-driver-b-seventh-event_lean_replay.json (CampaignPgwDriverBSeventhEvent), record TFQ-0503
- replay: `verified`
  - receipt [dag/research/campaign_pgw-driver-b-seventh-event_lean_replay.json](../../../dag/research/campaign_pgw-driver-b-seventh-event_lean_replay.json) (module `CampaignPgwDriverBSeventhEvent`): recorded sha256 `c564f055a6e8d1990a81c3100a1ddc8b0c1c70afe7cea1ab919db27d0619a19a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwDriverBSeventhEvent`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pgwDrvB_kindName_mem` | yes | yes | yes | propext | `#print axioms pgwDrvB_kindName_mem` |
| `pgwDrvB_kind_count` | yes | yes | yes | none | `#print axioms pgwDrvB_kind_count` |
| `pgwDrvB_kind_nodup` | yes | yes | yes | none | `#print axioms pgwDrvB_kind_nodup` |
| `pgwDrvB_names_realized` | yes | yes | yes | none | `#print axioms pgwDrvB_names_realized` |
| `pgwDrvB_no_seventh_name` | yes | yes | yes | none | `#print axioms pgwDrvB_no_seventh_name` |
| `pgwDrvB_seventh_outside` | yes | yes | yes | propext | `#print axioms pgwDrvB_seventh_outside` |
- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/event.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/event.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `checks/independent/pgw-driver-b-seventh-event.py`

- file: [checks/independent/pgw-driver-b-seventh-event.py](../../../checks/independent/pgw-driver-b-seventh-event.py)
- sha256 (`bytes`): `6aef4bb82fc661fdc00174f0bc5ada5c30d007bfd6c74b5e02e92c7ffbbfb268`
- cited in: record TFQ-0503

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0503_driver_b_seventh_event.md`

- file: [dag/derivations/02_genesis/tfq_0503_driver_b_seventh_event.md](../../../dag/derivations/02_genesis/tfq_0503_driver_b_seventh_event.md)
- sha256 (`lf-normalised`): `a3f8614a9627546a97b5c08a88eb7600c3f6299020cad16e163f72b7f8d8946d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0503
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-driver-b-seventh-event.md`

- file: [dag/derivations/independent/pgw-driver-b-seventh-event.md](../../../dag/derivations/independent/pgw-driver-b-seventh-event.md)
- sha256 (`lf-normalised`): `82197cd08e75104bbbe2b8242584c97ef5bd6cb36e8ccdc6516016edc1dbfa4b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-driver-b-seventh-event_lean_replay.json`

- file: [dag/research/campaign_pgw-driver-b-seventh-event_lean_replay.json](../../../dag/research/campaign_pgw-driver-b-seventh-event_lean_replay.json)
- sha256 (`lf-normalised`): `e6d0ba2be1a1b87c8c5a34822f1cbefcdf7d5d9ad19be1a8bb0dedbb6b4ee452`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/docs/ALPHA_HANDOFF.md:179-192`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/alpha_engine/harness.py::append_sealed_event`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/event.rs::Event`

## Routes

Incoming (1):

- `PGW-R-DRIVER-B-SEVENTH-EVENT` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (0):

