# AUTHF-SELF-RECEIPT-TOY

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For the one-bit Packet type with validity equal to its bit, no function from Unit to Bool satisfies authorize (receipt p) = valid p for all p, while the identity report admits such a function.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declaration references covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A toy instance of the split-fibre obstruction; it says nothing about receipts in general.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record self_receipt_blocks_authorization claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/Core.lean`

- file: [lean4/AuthIncompleteness/Core.lean](../../../lean4/AuthIncompleteness/Core.lean)
- sha256 (`bytes`): `28aba23d3c11dfe5847c72fe8fac86f4041ee5e979776f5ce0e6b3d81fdc29ce`
- cited in: node.lean, node.source, record TFQ-1346
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.Core`): recorded sha256 `28aba23d3c11dfe5847c72fe8fac86f4041ee5e979776f5ce0e6b3d81fdc29ce` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/Core.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.complete_receipt_decides_toy_contract` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.complete_receipt_decides_toy_contract` |
| `AuthorizationIncompleteness.self_receipt_blocks_authorization` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.self_receipt_blocks_authorization` |
| `AuthorizationIncompleteness.self_receipt_splits_validity` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.self_receipt_splits_validity` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1346_authf_self_receipt_toy.md`

- file: [dag/derivations/29_computation/tfq_1346_authf_self_receipt_toy.md](../../../dag/derivations/29_computation/tfq_1346_authf_self_receipt_toy.md)
- sha256 (`lf-normalised`): `c4653f526643c83609126b1c79ed59f1fbee85c90b897a8ab62c5a833773145c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1346
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md`

- file: [papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md](../../../papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md)
- sha256 (`lf-normalised`): `50b2673ad6e6ce3e8f3cba55fbcc848fac64db21600db6e8d1a9e63e96b7f915`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTHF-SELF-RECEIPT-TOY` `DERIVED_LEAN`: [PGW-WDP-BRIDGE-REPORT-FIBER-OBSERVER](PGW-WDP-BRIDGE-REPORT-FIBER-OBSERVER.md) (CONDITIONAL)

Outgoing (0):

