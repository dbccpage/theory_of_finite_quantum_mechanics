# AUTHF-LOGICAL-EXTERNALITY

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For the presentation with identity report and equal source and evaluator sites, a report-only authorization exists; for the presentation with a Unit report and distinct sites, none exists.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Site is an unused finite label; the statement carries no custody, security or independence content.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record physical_separation_neither_needed_nor_sufficient_for_toy_authorization claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/Externality.lean`

- file: [lean4/AuthIncompleteness/Externality.lean](../../../lean4/AuthIncompleteness/Externality.lean)
- sha256 (`bytes`): `dbd4af95185200d0b103354ef2282b29bf78ba4f3548a8bfcd76417f4328c90f`
- cited in: node.lean, node.source, record TFQ-1358
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/Externality.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.LogicalExternalityModels.coLocatedComplete_can_authorize` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.LogicalExternalityModels.coLocatedComplete_can_authorize` |
| `AuthorizationIncompleteness.LogicalExternalityModels.physical_separation_neither_needed_nor_sufficient_for_toy_authorization` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.LogicalExternalityModels.physical_separation_neither_needed_nor_sufficient_for_toy_authorization` |
| `AuthorizationIncompleteness.LogicalExternalityModels.separatedCollapsed_cannot_authorize` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.LogicalExternalityModels.separatedCollapsed_cannot_authorize` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1358_authf_logical_externality.md`

- file: [dag/derivations/29_computation/tfq_1358_authf_logical_externality.md](../../../dag/derivations/29_computation/tfq_1358_authf_logical_externality.md)
- sha256 (`lf-normalised`): `ce41742c0478ff1a3fa3d8fd1c33dea0e5e47a0c2201022e98eb84c778e7d79f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1358
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md`

- file: [papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md](../../../papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md)
- sha256 (`lf-normalised`): `50b2673ad6e6ce3e8f3cba55fbcc848fac64db21600db6e8d1a9e63e96b7f915`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTHF-LOGICAL-EXTERNALITY` `DERIVED_LEAN`: [PGW-WDP-BRIDGE-REPORT-FIBER-OBSERVER](PGW-WDP-BRIDGE-REPORT-FIBER-OBSERVER.md) (CONDITIONAL)

Outgoing (0):

