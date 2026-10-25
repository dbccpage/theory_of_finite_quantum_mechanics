# MUB-TOMOGRAPHY-INVERSION

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_PROSE`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Given d+1 MUB projector resolutions on a d-dimensional complex Hilbert carrier and trace-one rho, the probabilities p_bj=tr(rho P_bj) reconstruct rho as sum_bj p_bj P_bj minus I.

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

- complete d+1 MUB family
- complex Hilbert trace inner product

## Bottleneck

Mechanize the trace-inner-product dimension and reconstruction argument; constructing a complete MUB family is a separate existence obligation.

## Source status

Source record or explicit branch obligation; status scoped to the statement.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/tfq_0404_mub_tomography_inversion.md`

- file: [dag/derivations/25_mub/tfq_0404_mub_tomography_inversion.md](../../../dag/derivations/25_mub/tfq_0404_mub_tomography_inversion.md)
- sha256 (`lf-normalised`): `9590bd61c9dd6eb62ec4911c1b8425567464fbc8a1d4b755889bb4a9eaaf8b01`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0404
- counts toward the grade: no

### Documents and data: `papers/core/mub6/README.md`

- file: [papers/core/mub6/README.md](../../../papers/core/mub6/README.md)
- sha256 (`lf-normalised`): `df09e721db359b5d96928ae66ee18f6f67d8e805182e6ae7dd76d156496198f9`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB-TOMOGRAPHY-INVERSION` `DERIVED_PROSE`: [MUB-EXACT-PROJECTORS](MUB-EXACT-PROJECTORS.md) (DEFINITION)

Outgoing (0):

