# FSP-DIRAC-KAHLER-SPINFOAM-CLAIM

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: Dirac-Kaehler fermions on simplicial lattices give 2^(D/2) flavors and EPRL-FK boundary contractions yield nonnegative spin-network weights; the only local content is the count 1+4+6+4+1 = 16 = 4 x 4 in D = 4, and no spinfoam amplitude is evaluated.

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

Evaluate EPRL-FK boundary contractions on a declared finite complex and determine their signs; the taste count is standard and carries no positivity.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-052 claims PROVED_LEAN; audited status OPEN

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

### Documents and data: `dag/derivations/26_fsp/tfq_1216_fsp_dirac_kahler_spinfoam_claim.md`

- file: [dag/derivations/26_fsp/tfq_1216_fsp_dirac_kahler_spinfoam_claim.md](../../../dag/derivations/26_fsp/tfq_1216_fsp_dirac_kahler_spinfoam_claim.md)
- sha256 (`lf-normalised`): `ebf02ff51d7deccec2ef9dcd68096b025816369989e6f85bb86d96bbd4a91753`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1216
- counts toward the grade: no

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `5a72c2f6006ea18c3362f0a63e8525b65d41898e8f1bd437b7e4c2e368c7e102`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-DIRAC-KAHLER-SPINFOAM-CLAIM` `GAP_NO_DERIVATION`: [FSP-CDT-FOLIATION-POSITIVITY](FSP-CDT-FOLIATION-POSITIVITY.md) (OPEN)

Outgoing (2):

- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
- `APP-R-FSP-XCUBE-FRACTON-MODEL` `CONDITIONAL_ON_IMPORT`: [FSP-XCUBE-FRACTON-MODEL](FSP-XCUBE-FRACTON-MODEL.md) (IMPORTED_ASSUMPTION)
