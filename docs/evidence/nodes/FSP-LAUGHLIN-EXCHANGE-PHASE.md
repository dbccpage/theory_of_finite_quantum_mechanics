# FSP-LAUGHLIN-EXCHANGE-PHASE

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Arovas-Schrieffer-Wilczek: adiabatic exchange of two quasiholes in the nu = 1/m Laughlin state gives statistical phase theta = pi/m.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Laughlin nu = 1/m state and quasihole Berry phase (literature)

## Bottleneck

No Berry-phase or torus computation is in this checkout; the local module fixes m = 3 and checks numeric constants only (ledger GIN-C16 withdraws its reading).

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-044 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/26_fsp/tfq_1208_fsp_laughlin_exchange_phase.md`

- file: [dag/derivations/26_fsp/tfq_1208_fsp_laughlin_exchange_phase.md](../../../dag/derivations/26_fsp/tfq_1208_fsp_laughlin_exchange_phase.md)
- sha256 (`lf-normalised`): `77205f624d406801e014b0306bbbb87add5543f5719395237a33aa258809dbbd`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1208
- counts toward the grade: no

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `3268ac1be0222f75b9b9238508325cab337a6f767114e2d25afff56163a42cf4`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-LAUGHLIN-EXCHANGE-PHASE` `CONDITIONAL_ON_IMPORT`: [FSP-KITAEV-HONEYCOMB-SOLUTION](FSP-KITAEV-HONEYCOMB-SOLUTION.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `APP-R-FSP-BF-2GROUP-SIGN-CLAIM` `GAP_NO_DERIVATION`: [FSP-BF-2GROUP-SIGN-CLAIM](FSP-BF-2GROUP-SIGN-CLAIM.md) (OPEN)
- `APP-R-FSP-FIBONACCI-ANYON-DATA` `CONDITIONAL_ON_IMPORT`: [FSP-FIBONACCI-ANYON-DATA](FSP-FIBONACCI-ANYON-DATA.md) (IMPORTED_ASSUMPTION)
