# AUTHF-PD-EXTENSION-NONUNIQUE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Over the minimal Bool analogue of a primitive difference with two unequal marks, identityExtension and rejectingExtension give different validity and terminal values at the same carrier point.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The analogue is not the J011 interface and no naturality statement about all primitive differences follows.

## Source status

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record primitive_interface_has_distinct_authorization_extensions claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/PDModels.lean`

- file: [lean4/AuthIncompleteness/PDModels.lean](../../../lean4/AuthIncompleteness/PDModels.lean)
- sha256 (`bytes`): `6ae7afc020db9edcfcb842f7953ad85abb4838263e56a6078b2b91881c26a33d`
- cited in: node.lean, node.source, record TFQ-1359
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.PDModels`): recorded sha256 `6ae7afc020db9edcfcb842f7953ad85abb4838263e56a6078b2b91881c26a33d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/PDModels.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.PrimitiveDifferenceModels.boolPrimitive` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.PrimitiveDifferenceModels.boolPrimitive` |
| `AuthorizationIncompleteness.PrimitiveDifferenceModels.primitive_interface_has_distinct_authorization_extensions` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.PrimitiveDifferenceModels.primitive_interface_has_distinct_authorization_extensions` |
| `AuthorizationIncompleteness.PrimitiveDifferenceModels.same_primitive_extensions_split_policy` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.PrimitiveDifferenceModels.same_primitive_extensions_split_policy` |
| `AuthorizationIncompleteness.PrimitiveDifferenceModels.same_primitive_extensions_split_validity` | yes | yes | yes | none | `#print axioms AuthorizationIncompleteness.PrimitiveDifferenceModels.same_primitive_extensions_split_validity` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1359_authf_pd_extension_nonunique.md`

- file: [dag/derivations/29_computation/tfq_1359_authf_pd_extension_nonunique.md](../../../dag/derivations/29_computation/tfq_1359_authf_pd_extension_nonunique.md)
- sha256 (`lf-normalised`): `9a4488b48fa23c4bf52efbffdf7109da076bdfb5f97268eec1349503e0771670`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1359
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md`

- file: [papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md](../../../papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md)
- sha256 (`lf-normalised`): `50b2673ad6e6ce3e8f3cba55fbcc848fac64db21600db6e8d1a9e63e96b7f915`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTHF-PD-EXTENSION-NONUNIQUE` `DERIVED_LEAN`: [TFQ-0332](TFQ-0332.md) (OPEN)

Outgoing (0):

