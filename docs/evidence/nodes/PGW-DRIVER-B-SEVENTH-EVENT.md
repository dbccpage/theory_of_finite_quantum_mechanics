# PGW-DRIVER-B-SEVENTH-EVENT

Stage: [GENESIS](../stages/GENESIS.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Driver B, a lift that needs a new sealed Event kind, is retained as OPEN (AE-DRIVER-B-OPEN) and is successor research S3. The Alpha harness has exactly the six sealed Event kinds (Supply, AdmitDatum, AdmitForm, AdmitInst, AdmitRuleAll, Impose), and append_sealed_event refuses a seventh constructor (SeventhEventError), so no lift beyond the six kinds can be admitted through the slice.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 14
- distinct cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Open. The refusal of label 6 is the bound k \< 6 in this model, not a theorem that six kinds suffice, and the bound k \< 7 accepts 6. The Alpha harness, SeventhEventError, a seal amendment, and a factorization of every lift through the six kinds stay open.

## Source status

closeout.txt §2.1 retained OPEN and §4 S3; ALPHA_HANDOFF §9 typed outcomes

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwDriverBSeventhEvent.lean`

- file: [lean4/CampaignPgwDriverBSeventhEvent.lean](../../../lean4/CampaignPgwDriverBSeventhEvent.lean)
- sha256 (`bytes`): `a092f60ccc0db4a1a779de44480c0613c5573c749e3ddd49e393b48d21a5b222`
- cited in: node.lean, receipt dag/research/campaign_pgw-driver-b-seventh-event_lean_replay.json (CampaignPgwDriverBSeventhEvent), receipt dag/research/pr_355_review_replay.json (CampaignPgwDriverBSeventhEvent), record TFQ-0503
- replay: `verified`
  - receipt [dag/research/campaign_pgw-driver-b-seventh-event_lean_replay.json](../../../dag/research/campaign_pgw-driver-b-seventh-event_lean_replay.json) (module `CampaignPgwDriverBSeventhEvent`): recorded sha256 `a092f60ccc0db4a1a779de44480c0613c5573c749e3ddd49e393b48d21a5b222` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_355_review_replay.json](../../../dag/research/pr_355_review_replay.json) (module `CampaignPgwDriverBSeventhEvent`): recorded sha256 `a092f60ccc0db4a1a779de44480c0613c5573c749e3ddd49e393b48d21a5b222` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwDriverBSeventhEvent`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `amended_bound_accepts_seventh` | yes | yes | yes | none | `#print axioms amended_bound_accepts_seventh` |
| `index_roundtrip` | yes | yes | yes | Quot.sound, propext | `#print axioms index_roundtrip` |
| `ofIndex_roundtrip` | yes | yes | yes | propext | `#print axioms ofIndex_roundtrip` |
| `sealedIndex_admitDatum` | yes | yes | yes | propext | `#print axioms sealedIndex_admitDatum` |
| `sealedIndex_admitForm` | yes | yes | yes | propext | `#print axioms sealedIndex_admitForm` |
| `sealedIndex_admitInst` | yes | yes | yes | propext | `#print axioms sealedIndex_admitInst` |
| `sealedIndex_admitRuleAll` | yes | yes | yes | propext | `#print axioms sealedIndex_admitRuleAll` |
| `sealedIndex_impose` | yes | yes | yes | propext | `#print axioms sealedIndex_impose` |
| `sealedIndex_supply` | yes | yes | yes | propext | `#print axioms sealedIndex_supply` |
| `seventh_label_not_a_sealed_index` | yes | yes | yes | propext | `#print axioms seventh_label_not_a_sealed_index` |
| `seventh_label_refused` | yes | yes | yes | none | `#print axioms seventh_label_refused` |
| `six_labels_admitted` | yes | yes | yes | propext | `#print axioms six_labels_admitted` |

- counts toward the grade: yes

### Rust: `atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/event.rs`

- file: [atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/event.rs](../../../atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/event.rs)
- sha256 (`bytes`): `8c1184d6bcb255f44143e1a488ace12a3cee4ab6d894fd634ed25c12fa977237`
- cited in: node.rust, record TFQ-0503

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Event` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/pgw-driver-b-seventh-event.py`

- file: [checks/independent/pgw-driver-b-seventh-event.py](../../../checks/independent/pgw-driver-b-seventh-event.py)
- sha256 (`bytes`): `78c6bc5b20b0b5f413266d3eb6b4e5a814b7525e2f58776c4f6002de3f9fabe0`
- cited in: record TFQ-0503

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt`

- file: [atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt](../../../atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt)
- sha256 (`lf-normalised`): `c613e357809438876d1fcec34ea896548f17f4e9d4ea7f21048fafe9451651ac`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0503_driver_b_seventh_event.md`

- file: [dag/derivations/02_genesis/tfq_0503_driver_b_seventh_event.md](../../../dag/derivations/02_genesis/tfq_0503_driver_b_seventh_event.md)
- sha256 (`lf-normalised`): `cb52f42203db9d30ddad7dcf1ce79535e76567fdc66e1646df0ba3702aca516a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0503
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-driver-b-seventh-event.md`

- file: [dag/derivations/independent/pgw-driver-b-seventh-event.md](../../../dag/derivations/independent/pgw-driver-b-seventh-event.md)
- sha256 (`lf-normalised`): `5cf8772433966d0d788cdb8c7c02483f2ddbe642d97bfdf2ba0814f1364ea9a5`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-driver-b-seventh-event_lean_replay.json`

- file: [dag/research/campaign_pgw-driver-b-seventh-event_lean_replay.json](../../../dag/research/campaign_pgw-driver-b-seventh-event_lean_replay.json)
- sha256 (`lf-normalised`): `dfdb26bcdae26d1eb72174ff1f364b40056576ab5c051856c267b323e3a69f5d`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/docs/ALPHA_HANDOFF.md:179-192`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/alpha_engine/harness.py::append_sealed_event`

## Routes

Incoming (1):

- `PGW-R-DRIVER-B-SEVENTH-EVENT` `GAP_NO_DERIVATION`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (0):

