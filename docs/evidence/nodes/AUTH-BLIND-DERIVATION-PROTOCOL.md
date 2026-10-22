# AUTH-BLIND-DERIVATION-PROTOCOL

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A derivation run toward computation is a proposal source: its prompt, model, tools, repository state, available context and outputs are frozen, every notion is labeled input, definition, theorem, example or open assumption, each lift carries a positive witness and a failed-descent control, and literature comparison happens only after sealing; isolation records provenance and does not show novelty or validity.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Apply the protocol to the Genesis to computability derivation and keep recovered material out of any run meant to be blind until that run is sealed.

## Source status

papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md record AIT-TC1 claims design; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/29_computation/tfq_1339_auth_blind_derivation_protocol.md`

- file: [dag/derivations/29_computation/tfq_1339_auth_blind_derivation_protocol.md](../../../dag/derivations/29_computation/tfq_1339_auth_blind_derivation_protocol.md)
- sha256 (`lf-normalised`): `424bcbf1a9a83177601079c1bf4ad9775918a2377895fff6dde23306fc1e01be`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1339
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md`

- file: [papers/foundations/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md](../../../papers/foundations/authorization_incompleteness/authorization_incompleteness_theory_claim_ledger.md)
- sha256 (`lf-normalised`): `28aa3a825d1b0296270b62f9a33a4a67b6c2a2d708028444a7f725ad46697feb`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/foundations/authorization_incompleteness/controlled_turing_derivation_series.md`

- file: [papers/foundations/authorization_incompleteness/controlled_turing_derivation_series.md](../../../papers/foundations/authorization_incompleteness/controlled_turing_derivation_series.md)
- sha256 (`lf-normalised`): `2573123162731ea63495b0ece777ae4b9e704e27b976fbc031df51c6f81c6f7b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/foundations/authorization_incompleteness/proof_program.md`

- file: [papers/foundations/authorization_incompleteness/proof_program.md](../../../papers/foundations/authorization_incompleteness/proof_program.md)
- sha256 (`lf-normalised`): `e624d01a2371d6d8856a17c535ad1916abd8b1353450755c7281fe22e87b720f`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-AUTH-BLIND-DERIVATION-PROTOCOL` `DERIVED_PROSE`: [PGW-GENESIS-FREEZE-ENDPOINT-LEDGER](PGW-GENESIS-FREEZE-ENDPOINT-LEDGER.md) (DEFINITION)

Outgoing (0):

