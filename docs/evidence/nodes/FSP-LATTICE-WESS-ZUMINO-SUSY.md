# FSP-LATTICE-WESS-ZUMINO-SUSY

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: a finite-lattice 2D N=1 Wess-Zumino model with supercharges obeying {Q_a, Q_b} = 2 delta_ab H, H \>= 0 and exact boson-fermion pairing of nonzero levels; no such lattice construction exists in this checkout, and lattice discretizations generally keep at most a subalgebra exact.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
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

Specify the lattice model and which supercharge is exact; prove H = Q^2 or {Q, Q^dagger} on the finite Hilbert space before using pairing.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-040 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/26_fsp/tfq_1204_fsp_lattice_wess_zumino_susy.md`

- file: [dag/derivations/26_fsp/tfq_1204_fsp_lattice_wess_zumino_susy.md](../../../dag/derivations/26_fsp/tfq_1204_fsp_lattice_wess_zumino_susy.md)
- sha256 (`lf-normalised`): `26128185073ec74dd7ba16e105409150f4fd36fcafc71fa42894e92413f2adbd`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1204
- counts toward the grade: no

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-LATTICE-WESS-ZUMINO-SUSY` `GAP_NO_DERIVATION`: [FSP-CAR-EXTERIOR-FOCK](FSP-CAR-EXTERIOR-FOCK.md) (PROVED_PROSE), [FSP-IMAGINARY-MU-REAL-DET](FSP-IMAGINARY-MU-REAL-DET.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `APP-R-FSP-NICOLAI-MAP-CLAIM` `GAP_NO_DERIVATION`: [FSP-NICOLAI-MAP-CLAIM](FSP-NICOLAI-MAP-CLAIM.md) (OPEN)
- `APP-R-FSP-WITTEN-INDEX-INVARIANCE` `CONDITIONAL_ON_IMPORT`: [FSP-WITTEN-INDEX-INVARIANCE](FSP-WITTEN-INDEX-INVARIANCE.md) (IMPORTED_ASSUMPTION)
