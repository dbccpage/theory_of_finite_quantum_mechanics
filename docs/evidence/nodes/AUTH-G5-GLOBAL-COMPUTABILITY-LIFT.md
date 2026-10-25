# AUTH-G5-GLOBAL-COMPUTABILITY-LIFT

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For an admitted program carrier and a nontrivial extensional property, a total computable sound and complete authorizer would decide that property; the lift is a stated target in the source and has no local theorem.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- admitted program carrier
- nontrivial extensional property

## Bottleneck

Choose the carrier, define the property by program behavior, give the satisfying and failing programs, prove the many-one reduction and the closure of the decision class, and cite rice₂ and halting_problem.

## Source status

papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md record AIT-G5 claims open; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/29_computation/tfq_1338_auth_g5_global_computability_lift.md`

- file: [dag/derivations/29_computation/tfq_1338_auth_g5_global_computability_lift.md](../../../dag/derivations/29_computation/tfq_1338_auth_g5_global_computability_lift.md)
- sha256 (`lf-normalised`): `99a2083d34843f2dc21b9b8833ea990c1248d155a2ab99188cb362040d9c950f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1338
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md`

- file: [papers/foundations/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md](../../../papers/foundations/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md)
- sha256 (`lf-normalised`): `28aa3a825d1b0296270b62f9a33a4a67b6c2a2d708028444a7f725ad46697feb`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/foundations/authorization_incompleteness/goals.yaml`

- file: [papers/foundations/authorization_incompleteness/goals.yaml](../../../papers/foundations/authorization_incompleteness/goals.yaml)
- sha256 (`lf-normalised`): `1968556bd399e43405dd7959cf6b093d9de580b8b01c6294ed8a8c5ffe81a990`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/foundations/authorization_incompleteness/proof_program.md`

- file: [papers/foundations/authorization_incompleteness/proof_program.md](../../../papers/foundations/authorization_incompleteness/proof_program.md)
- sha256 (`lf-normalised`): `e624d01a2371d6d8856a17c535ad1916abd8b1353450755c7281fe22e87b720f`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTH-G5-GLOBAL-COMPUTABILITY-LIFT` `GAP_NO_DERIVATION`: [AUTH-RICE-THEOREM-IMPORT](AUTH-RICE-THEOREM-IMPORT.md) (IMPORTED_ASSUMPTION), [AUTH-G5A-CLASS-RELATIVE-TRANSPORT](AUTH-G5A-CLASS-RELATIVE-TRANSPORT.md) (PROVED_LEAN), [AUTH-G5B-CARRIER-ADMISSION-GATE](AUTH-G5B-CARRIER-ADMISSION-GATE.md) (DEFINITION)

Outgoing (0):

