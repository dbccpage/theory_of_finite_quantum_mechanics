# FSP-NICOLAI-MAP-CLAIM

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: on an off-shell supersymmetric lattice model the map xi = -partial^2 phi + W'(phi) has Jacobian equal to the fermion determinant and turns the partition function into a Gaussian with no sign problem; nothing in this checkout constructs the map or the Jacobian identity.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
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

Give the lattice model, prove det(d xi / d phi) = det D_F, and treat the sign of det D_F and the multiplicity of the map; Nicolai-map results are model specific in the literature.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-041 claims PROVED_LEAN; audited status OPEN

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

### Documents and data: `dag/derivations/26_fsp/tfq_1205_fsp_nicolai_map_claim.md`

- file: [dag/derivations/26_fsp/tfq_1205_fsp_nicolai_map_claim.md](../../../dag/derivations/26_fsp/tfq_1205_fsp_nicolai_map_claim.md)
- sha256 (`lf-normalised`): `641b2627c00d9cd715d24b6282521f1b4a637241434e6363ff6c7957770db009`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1205
- counts toward the grade: no

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `3e88f1a70b66b0b90cc915acb5c802c118775e65cc8970af6c5a423f27ddd755`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-NICOLAI-MAP-CLAIM` `GAP_NO_DERIVATION`: [FSP-LATTICE-WESS-ZUMINO-SUSY](FSP-LATTICE-WESS-ZUMINO-SUSY.md) (OPEN)

Outgoing (0):

