# AUTHF-MATHLIB-HALTING-BRIDGE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> With Computable as the allowed class on both sides, a source predicate with no computable total decider and a computable validity-preserving map give proposal validity with no computable total decider; for the source predicate that program c halts on input n this is Mathlib's ComputablePred.halting_problem.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declaration references covered by a current replay receipt: 4
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

papers/foundations/authorization_incompleteness/evidence/original/formal_binding_manifest.md record no_computable_authorizer_of_computable_reduction claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/AuthIncompleteness/MathlibBridge.lean`

- file: [lean4/AuthIncompleteness/MathlibBridge.lean](../../../lean4/AuthIncompleteness/MathlibBridge.lean)
- sha256 (`bytes`): `ca675198cccf4d30999c8a63a6469ba0d63f2d6f6e0fc09f081069cc17ff9b49`
- cited in: node.lean, node.source, record TFQ-1348
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `AuthIncompleteness.MathlibBridge`): recorded sha256 `ca675198cccf4d30999c8a63a6469ba0d63f2d6f6e0fc09f081069cc17ff9b49` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/AuthIncompleteness/MathlibBridge.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `AuthorizationIncompleteness.MathlibBridge.computable_closed_under_computable_reduction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AuthorizationIncompleteness.MathlibBridge.computable_closed_under_computable_reduction` |
| `AuthorizationIncompleteness.MathlibBridge.halting_has_no_computable_decider` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AuthorizationIncompleteness.MathlibBridge.halting_has_no_computable_decider` |
| `AuthorizationIncompleteness.MathlibBridge.halting_transport_instance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AuthorizationIncompleteness.MathlibBridge.halting_transport_instance` |
| `AuthorizationIncompleteness.MathlibBridge.no_computable_authorizer_of_computable_reduction` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms AuthorizationIncompleteness.MathlibBridge.no_computable_authorizer_of_computable_reduction` |

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

