# QCV-PHYSICAL-SATISFIABILITY-OPEN

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Whether any physical system has noise obeying the recurrence with level-bounded overhead, a fresh ancilla supply at rate r \>= lam/((1-g)*kappa) and fast classical control is not established here, in either direction; the rate comparison mu_repair \>= lambda_proj at scale stays open.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
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

A named packet (code family, noise hypothesis, repair capacity, residual quotient) and a locality bound would be needed before any verdict; no claim about physical viability is made.

## Source status

dag/research/quantum_computation_self_obstruction.md record QCV-Q5C claims OPEN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/29_computation/tfq_1326_qcv_physical_satisfiability_open.md`

- file: [dag/derivations/29_computation/tfq_1326_qcv_physical_satisfiability_open.md](../../../dag/derivations/29_computation/tfq_1326_qcv_physical_satisfiability_open.md)
- sha256 (`lf-normalised`): `8794ed69e8fcb70837974ee551b090147d17ff812ed446c645b3386390a25899`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1326
- counts toward the grade: no

### Documents and data: `dag/research/quantum_computation_self_obstruction.md`

- file: [dag/research/quantum_computation_self_obstruction.md](../../../dag/research/quantum_computation_self_obstruction.md)
- sha256 (`lf-normalised`): `8ae1b2ae291ee74f773da07740ebd0c1f98842bc01d7ec6a4d3c267e0077d178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-QCV-PHYSICAL-SATISFIABILITY-OPEN` `GAP_NO_DERIVATION`: [QCV-CONDITIONAL-VIABILITY-CERTIFICATE](QCV-CONDITIONAL-VIABILITY-CERTIFICATE.md) (PROVED_LEAN), [MAJ-OPEN-LIEB-ROBINSON-LOCALITY](MAJ-OPEN-LIEB-ROBINSON-LOCALITY.md) (OPEN), [DS-QM103-SHOW-THE-PACKET-PROTOCOL](DS-QM103-SHOW-THE-PACKET-PROTOCOL.md) (DEFINITION)

Outgoing (0):

