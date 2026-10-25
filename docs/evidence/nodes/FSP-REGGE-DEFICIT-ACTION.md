# FSP-REGGE-DEFICIT-ACTION

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On a 4D triangulation with squared edge lengths, the deficit angle at a hinge h is epsilon_h = 2 pi - sum of dihedral angles at h and the Regge action is S = sum_h A_h epsilon_h; its convergence to the Einstein-Hilbert action under refinement is a literature result imported here.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Regge calculus (Regge 1961; Cheeger-Mueller-Schrader convergence)

## Bottleneck

Regge calculus carries no fermion-sign content in this package; Lorentzian signature, convergence conditions and any sign consequence need separate evidence (ledger GIN-C13).

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-048 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/26_fsp/tfq_1212_fsp_regge_deficit_action.md`

- file: [dag/derivations/26_fsp/tfq_1212_fsp_regge_deficit_action.md](../../../dag/derivations/26_fsp/tfq_1212_fsp_regge_deficit_action.md)
- sha256 (`lf-normalised`): `41e4537320c8a4b8d479affc42288df4e4ac8a87c5f5d8333c9741aa47049554`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1212
- counts toward the grade: no

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-REGGE-DEFICIT-ACTION` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-DEGREE-K-TORSION-BALANCE](PGW-WDP-DEGREE-K-TORSION-BALANCE.md) (PROVED_PROSE), [FSP-COBORDISM-INTRINSIC-SIGN](FSP-COBORDISM-INTRINSIC-SIGN.md) (OPEN)

Outgoing (2):

- `APP-R-FSP-DISCRETE-WDW-CONSTRAINT` `GAP_NO_DERIVATION`: [FSP-DISCRETE-WDW-CONSTRAINT](FSP-DISCRETE-WDW-CONSTRAINT.md) (OPEN)
- `APP-R-FSP-PACHNER-INVARIANCE-CLAIM` `GAP_NO_DERIVATION`: [FSP-PACHNER-INVARIANCE-CLAIM](FSP-PACHNER-INVARIANCE-CLAIM.md) (OPEN)
