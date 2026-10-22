# AUTHF-MATHLIB-HALTING-BRIDGE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> With Computable as the allowed class on both sides, a source predicate with no computable total decider and a computable validity-preserving map give proposal validity with no computable total decider; for the source predicate that program c halts on input n this is Mathlib's ComputablePred.halting_problem.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Halting is the only source predicate instantiated; no Rice instance, no extensional property of encoded DTM0 programs and no computable reduction from DTM0 to Nat.Partrec.Code is given.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record no_computable_authorizer_of_computable_reduction claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/MathlibBridge.lean`

- file: [lean4/AuthIncompleteness/MathlibBridge.lean](../../../lean4/AuthIncompleteness/MathlibBridge.lean)
- sha256 (`bytes`): `ca675198cccf4d30999c8a63a6469ba0d63f2d6f6e0fc09f081069cc17ff9b49`
- cited in: node.lean, node.source, record TFQ-1348
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/MathlibBridge.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.MathlibBridge.computable_closed_under_computable_reduction` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.MathlibBridge.computable_closed_under_computable_reduction` |
| `AuthorizationIncompleteness.MathlibBridge.halting_has_no_computable_decider` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.MathlibBridge.halting_has_no_computable_decider` |
| `AuthorizationIncompleteness.MathlibBridge.halting_transport_instance` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.MathlibBridge.halting_transport_instance` |
| `AuthorizationIncompleteness.MathlibBridge.no_computable_authorizer_of_computable_reduction` | yes | yes | yes | - | `#print axioms AuthorizationIncompleteness.MathlibBridge.no_computable_authorizer_of_computable_reduction` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1348_authf_mathlib_halting_bridge.md`

- file: [dag/derivations/29_computation/tfq_1348_authf_mathlib_halting_bridge.md](../../../dag/derivations/29_computation/tfq_1348_authf_mathlib_halting_bridge.md)
- sha256 (`lf-normalised`): `549bdc0d6ec87752a5b13aa20794ea150615fe960755de49e04e74d06b02e4eb`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1348
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/FORMAL_RECOVERY_NOTES.md`

- file: [papers/foundations/authorization_incompleteness/FORMAL_RECOVERY_NOTES.md](../../../papers/foundations/authorization_incompleteness/FORMAL_RECOVERY_NOTES.md)
- sha256 (`lf-normalised`): `8b88ca59c0e6400660aea8712963d6beff9ec458036b5211ca6677f1e094dee5`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTHF-MATHLIB-HALTING-BRIDGE` `DERIVED_LEAN`: [AUTHF-CLASS-RELATIVE-TRANSPORT](AUTHF-CLASS-RELATIVE-TRANSPORT.md) (PROVED_LEAN)

Outgoing (0):

