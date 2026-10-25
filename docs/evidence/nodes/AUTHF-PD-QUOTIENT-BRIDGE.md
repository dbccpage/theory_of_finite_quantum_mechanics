# AUTHF-PD-QUOTIENT-BRIDGE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a primitive difference P and a Bool validity that differs on some ZeroRel P class, no function on the canonical quotient report pdProj P agrees with validity everywhere; a ZeroRel-constant validity has a quotient decision.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- J011 candidate quotient interface: PrimitiveDifference, ZeroRel, ResidualQuotient, pdSetoid, pdProj, collapsePD

## Bottleneck

Not built here: the file imports J011_minimal_publication, whose source is absent from this repository, so the recorded proof is unreplayed.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record pd_quotient_split_blocks_report_only_authorization claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/PDBridge.lean`

- file: [lean4/AuthIncompleteness/PDBridge.lean](../../../lean4/AuthIncompleteness/PDBridge.lean)
- sha256 (`bytes`): `660b990da5b35b9d764737e6b2f0effd5db1751fa4fd8783697c83508923ca2f`
- cited in: node.lean, node.source, record TFQ-1360
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/PDBridge.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.PrimitiveDifferenceP0Bridge.collapse_pd_blocks_report_only_authorization` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.PrimitiveDifferenceP0Bridge.collapse_pd_blocks_report_only_authorization` |
| `AuthorizationIncompleteness.PrimitiveDifferenceP0Bridge.pdQuotientDecision` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.PrimitiveDifferenceP0Bridge.pdQuotientDecision` |
| `AuthorizationIncompleteness.PrimitiveDifferenceP0Bridge.pd_quotient_decision_if_zeroRel_constant` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.PrimitiveDifferenceP0Bridge.pd_quotient_decision_if_zeroRel_constant` |
| `AuthorizationIncompleteness.PrimitiveDifferenceP0Bridge.pd_quotient_split_blocks_report_only_authorization` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.PrimitiveDifferenceP0Bridge.pd_quotient_split_blocks_report_only_authorization` |
| `AuthorizationIncompleteness.PrimitiveDifferenceP0Bridge.pd_quotient_total_decision_requires_zeroRel_constancy` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.PrimitiveDifferenceP0Bridge.pd_quotient_total_decision_requires_zeroRel_constancy` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1360_authf_pd_quotient_bridge.md`

- file: [dag/derivations/29_computation/tfq_1360_authf_pd_quotient_bridge.md](../../../dag/derivations/29_computation/tfq_1360_authf_pd_quotient_bridge.md)
- sha256 (`lf-normalised`): `d30b493bff90266d5884a896d51e03ac910bb6b6a0fc2402ca308588d8546a07`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1360
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md`

- file: [papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md](../../../papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md)
- sha256 (`lf-normalised`): `50b2673ad6e6ce3e8f3cba55fbcc848fac64db21600db6e8d1a9e63e96b7f915`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTHF-PD-QUOTIENT-BRIDGE` `GAP_NO_DERIVATION`: [TFQ-0332](TFQ-0332.md) (OPEN)

Outgoing (0):

