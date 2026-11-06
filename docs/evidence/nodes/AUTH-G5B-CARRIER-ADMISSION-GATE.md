# AUTH-G5B-CARRIER-ADMISSION-GATE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A program carrier is admitted for a global undecidability claim only when syntax and encodings, execution semantics, a universality witness, an extensional property, positive and negative nontriviality witnesses, an effective reduction, the split between adequacy and authorization, and replay closure are all frozen in one record.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

None of the eight fields is closed by the source: DTM0 and DTM1 are partial on syntax, execution and replay only, and the candidate inventory records admission as open.

## Source status

dag/derivations/04_authorization/authorization_incompleteness/authorization_incompleteness_theory.md record AIT-G5b claims defined; open; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/04_authorization/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md`

- file: [dag/derivations/04_authorization/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md](../../../dag/derivations/04_authorization/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md)
- sha256 (`lf-normalised`): `28aa3a825d1b0296270b62f9a33a4a67b6c2a2d708028444a7f725ad46697feb`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/04_authorization/authorization_incompleteness/computability_lift_admission.md`

- file: [dag/derivations/04_authorization/authorization_incompleteness/computability_lift_admission.md](../../../dag/derivations/04_authorization/authorization_incompleteness/computability_lift_admission.md)
- sha256 (`lf-normalised`): `ca0576eab3751c4afcc3cb9ecf28d5010409cb014674317902a9b8cbb194b7fe`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/04_authorization/authorization_incompleteness/goals.yaml`

- file: [dag/derivations/04_authorization/authorization_incompleteness/goals.yaml](../../../dag/derivations/04_authorization/authorization_incompleteness/goals.yaml)
- sha256 (`lf-normalised`): `152c4e028f62066572a61a1c2feca2468a0e8670388c426114f1d2d60917bf17`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/04_authorization/authorization_incompleteness/proof_program.md`

- file: [dag/derivations/04_authorization/authorization_incompleteness/proof_program.md](../../../dag/derivations/04_authorization/authorization_incompleteness/proof_program.md)
- sha256 (`lf-normalised`): `e624d01a2371d6d8856a17c535ad1916abd8b1353450755c7281fe22e87b720f`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1336_auth_g5b_carrier_admission_gate.md`

- file: [dag/derivations/29_computation/tfq_1336_auth_g5b_carrier_admission_gate.md](../../../dag/derivations/29_computation/tfq_1336_auth_g5b_carrier_admission_gate.md)
- sha256 (`lf-normalised`): `2eca640d49d837a459a2e61333dc0e5f11fac6f9b58811549e2a7370ac2fdc05`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1336
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-AUTH-G5B-CARRIER-ADMISSION-GATE` `DERIVED_PROSE`: [AUTH-DTM1-TOKEN-CODE-ROUNDTRIP](AUTH-DTM1-TOKEN-CODE-ROUNDTRIP.md) (PROVED_LEAN), [AUTH-G5A-CLASS-RELATIVE-TRANSPORT](AUTH-G5A-CLASS-RELATIVE-TRANSPORT.md) (PROVED_LEAN)

Outgoing (2):

- `APP-R-AUTH-G5-GLOBAL-COMPUTABILITY-LIFT` `GAP_NO_DERIVATION`: [AUTH-G5-GLOBAL-COMPUTABILITY-LIFT](AUTH-G5-GLOBAL-COMPUTABILITY-LIFT.md) (OPEN)
- `APP-R-AUTH-RICE-THEOREM-IMPORT` `CONDITIONAL_ON_IMPORT`: [AUTH-RICE-THEOREM-IMPORT](AUTH-RICE-THEOREM-IMPORT.md) (IMPORTED_ASSUMPTION)
