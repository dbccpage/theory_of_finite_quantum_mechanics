# AUTH-RICE-THEOREM-IMPORT

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No total computable procedure is sound and complete for a nontrivial extensional property of the programs of a Turing-complete language (Rice 1953); the source cites the theorem with its hypotheses and does not formalize it.

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

- Rice theorem (Rice 1953)
- Mathlib Nat.Partrec.Code with ComputablePred.rice and rice₂

## Bottleneck

State a local theorem that instantiates Mathlib ComputablePred.rice₂ for the chosen code language, with the semantic property and both nontriviality witnesses named, and bind it to the class-relative transport.

## Source status

papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md record AIT-5 claims cited; local formalization open; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/29_computation/tfq_1337_auth_rice_theorem_import.md`

- file: [dag/derivations/29_computation/tfq_1337_auth_rice_theorem_import.md](../../../dag/derivations/29_computation/tfq_1337_auth_rice_theorem_import.md)
- sha256 (`lf-normalised`): `c23b62a743f3429a04dbcc70d3c71947b2a131f6bc0fce80e64ae4e07c93ac51`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1337
- counts toward the grade: no

### Documents and data: `papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md`

- file: [papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md](../../../papers/foundations/authorization_incompleteness/authorization_incompleteness_theory.md)
- sha256 (`lf-normalised`): `4ca81b6ae8e724b54c7abf43ea951c119c2cff31a375e45cd7d79299adc7f70c`
- cited in: node.source
- counts toward the grade: yes

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

## Routes

Incoming (1):

- `APP-R-AUTH-RICE-THEOREM-IMPORT` `CONDITIONAL_ON_IMPORT`: [AUTH-G5B-CARRIER-ADMISSION-GATE](AUTH-G5B-CARRIER-ADMISSION-GATE.md) (DEFINITION)

Outgoing (1):

- `APP-R-AUTH-G5-GLOBAL-COMPUTABILITY-LIFT` `GAP_NO_DERIVATION`: [AUTH-G5-GLOBAL-COMPUTABILITY-LIFT](AUTH-G5-GLOBAL-COMPUTABILITY-LIFT.md) (OPEN)
