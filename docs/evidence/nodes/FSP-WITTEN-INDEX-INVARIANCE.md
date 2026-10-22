# FSP-WITTEN-INDEX-INVARIANCE

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On a finite-dimensional graded Hilbert space with an exact supercharge Q and H = {Q, Q^dagger}, positive-energy levels pair bosons with fermions, so W = Tr\[(-1)^F exp(-beta H)\] = n_B(E=0) - n_F(E=0) for every beta, and unbroken supersymmetry has ground energy 0.

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

- exact supercharge with H = {Q, Q^dagger} on a finite graded space (assumption)

## Bottleneck

Standard result imported; it presupposes an exact lattice supercharge, which FSP-DERIV-040 leaves open, and gives no sign-free sampling of Z itself.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-042 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/fsp/lean4/regge_wdw_core.lean`

- file: [papers/core/fsp/lean4/regge_wdw_core.lean](../../../papers/core/fsp/lean4/regge_wdw_core.lean)
- sha256 (`bytes`): `8f20ead1eb7c40441e6ccee48c7b5c828d0d93319928ea2df7ec322226e164b9`
- cited in: node.source
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains papers/core/fsp/lean4/regge_wdw_core.lean`
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1206_fsp_witten_index_invariance.md`

- file: [dag/derivations/26_fsp/tfq_1206_fsp_witten_index_invariance.md](../../../dag/derivations/26_fsp/tfq_1206_fsp_witten_index_invariance.md)
- sha256 (`lf-normalised`): `54273d765a2628858ea35b8fc7b8e06622eb5c378adbd9fca4e2aace933bc243`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1206
- counts toward the grade: no

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-WITTEN-INDEX-INVARIANCE` `CONDITIONAL_ON_IMPORT`: [FSP-LATTICE-WESS-ZUMINO-SUSY](FSP-LATTICE-WESS-ZUMINO-SUSY.md) (OPEN)

Outgoing (2):

- `APP-R-FSP-KITAEV-HONEYCOMB-SOLUTION` `CONDITIONAL_ON_IMPORT`: [FSP-KITAEV-HONEYCOMB-SOLUTION](FSP-KITAEV-HONEYCOMB-SOLUTION.md) (IMPORTED_ASSUMPTION)
- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
