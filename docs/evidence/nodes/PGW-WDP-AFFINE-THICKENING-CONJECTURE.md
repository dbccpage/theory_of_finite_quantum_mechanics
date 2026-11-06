# PGW-WDP-AFFINE-THICKENING-CONJECTURE

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Construct a finite observation and recovery cost reduction for rational affine supports thickened by bounded independent measurement error epsilon \> 0, replacing Appendix Y's discrete finite-fiber counting argument.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Open conjecture in affine_thickening_conjecture.md; Appendix Y's exact finite-fiber theorem applies only at zero thickening (epsilon = 0).

## Source status

Open derivation target in docs/02_requiring_derivation/affine_thickening_conjecture.md

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/exact_linear.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/exact_linear.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/exact_linear.py)
- sha256 (`bytes`): `fd7fd10731129a792e1bb12466fd57b7df9417f3b917a41b1c18a5219720d15d`
- cited in: record TFQ-0581

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ExactField` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/affine_thickening_conjecture.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/affine_thickening_conjecture.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/affine_thickening_conjecture.md)
- sha256 (`lf-normalised`): `92e3f6b93516c7ddf8f0a70fab5af5135d7020c117d3cbe53bf08a50096d9a29`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0581_wdp_affine_thickening_conjecture.md`

- file: [dag/derivations/06_wdp/tfq_0581_wdp_affine_thickening_conjecture.md](../../../dag/derivations/06_wdp/tfq_0581_wdp_affine_thickening_conjecture.md)
- sha256 (`lf-normalised`): `05fc184d4c5280eb22ba47c7495e4bd15d75d60a805c49cf306b6d89aeb9acda`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0581
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0581 lean4: finite reduction for epsilon-thickened affine supports is open
- TFQ-0581 rust: no Rust solver for epsilon-thickened affine supports yet

## Routes

Incoming (1):

- `PGW-R-WDP-AFFINE-THICKENING-CONJECTURE` `GAP_NO_DERIVATION`: [PGW-WDP-EXACT-SCALAR-HADAMARD-OBSTRUCTION](PGW-WDP-EXACT-SCALAR-HADAMARD-OBSTRUCTION.md) (PROVED_LEAN), [PGW-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION](PGW-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-MERON-M1-CORRELATION-ESTIMATES` `GAP_NO_DERIVATION`: [PGW-WDP-MERON-M1-CORRELATION-ESTIMATES](PGW-WDP-MERON-M1-CORRELATION-ESTIMATES.md) (OPEN)
