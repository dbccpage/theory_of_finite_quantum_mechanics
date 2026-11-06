# AUTHF-MATHLIB-HALTING-BRIDGE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> With Computable as the allowed class on both sides, a source predicate with no computable total decider and a computable validity-preserving map give proposal validity with no computable total decider; for the source predicate that program c halts on input n this is Mathlib's ComputablePred.halting_problem.

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

Halting is the only source predicate instantiated; no Rice instance, no extensional property of encoded DTM0 programs and no computable reduction from DTM0 to Nat.Partrec.Code is given.

## Source status

dag/derivations/04_authorization/authorization_incompleteness/evidence/original/formal_binding_manifest.md record no_computable_authorizer_of_computable_reduction claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/MathlibBridge.lean`

- file: [lean4/AuthIncompleteness/MathlibBridge.lean](../../../lean4/AuthIncompleteness/MathlibBridge.lean)
- sha256 (`bytes`): `ca675198cccf4d30999c8a63a6469ba0d63f2d6f6e0fc09f081069cc17ff9b49`
- cited in: node.lean, node.source, record TFQ-1348
- replay: `verified`
  - receipt [evidence/lean_receipts/lean_replay_campaign_computation.json](../../../evidence/lean_receipts/lean_replay_campaign_computation.json) (module `AuthIncompleteness.MathlibBridge`): recorded sha256 `ca675198cccf4d30999c8a63a6469ba0d63f2d6f6e0fc09f081069cc17ff9b49` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/MathlibBridge.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.MathlibBridge.computable_closed_under_computable_reduction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AuthorizationIncompleteness.MathlibBridge.computable_closed_under_computable_reduction` |
| `AuthorizationIncompleteness.MathlibBridge.halting_has_no_computable_decider` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AuthorizationIncompleteness.MathlibBridge.halting_has_no_computable_decider` |
| `AuthorizationIncompleteness.MathlibBridge.halting_transport_instance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AuthorizationIncompleteness.MathlibBridge.halting_transport_instance` |
| `AuthorizationIncompleteness.MathlibBridge.no_computable_authorizer_of_computable_reduction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AuthorizationIncompleteness.MathlibBridge.no_computable_authorizer_of_computable_reduction` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/04_authorization/authorization_incompleteness/FORMAL_RECOVERY_NOTES.md`

- file: [dag/derivations/04_authorization/authorization_incompleteness/FORMAL_RECOVERY_NOTES.md](../../../dag/derivations/04_authorization/authorization_incompleteness/FORMAL_RECOVERY_NOTES.md)
- sha256 (`lf-normalised`): `b4f7baee0dd634505d7da70a920b9bbb3548666ec77244eb9d1c7fc3d0191a6c`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1348_authf_mathlib_halting_bridge.md`

- file: [dag/derivations/29_computation/tfq_1348_authf_mathlib_halting_bridge.md](../../../dag/derivations/29_computation/tfq_1348_authf_mathlib_halting_bridge.md)
- sha256 (`lf-normalised`): `e30894ae56f845f5fff6a50e2fb9589fcf26a8433555642ade4880e0f25c56f9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1348
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-AUTHF-MATHLIB-HALTING-BRIDGE` `DERIVED_LEAN`: [AUTHF-CLASS-RELATIVE-TRANSPORT](AUTHF-CLASS-RELATIVE-TRANSPORT.md) (PROVED_LEAN)

Outgoing (0):

