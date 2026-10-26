# FSP-TROYER-WIESE-REDUCTION

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Troyer-Wiese (2005): the NP-complete decision whether a 3D +-J Ising spin glass has ground energy below a threshold reduces in polynomial time to estimating the thermal energy of the frustrated quantum model -sum J_ij sigma^x_i sigma^x_j at beta J \>= N ln 2 + ln(12N); a deterministic polynomial estimator for that family would give P = NP, a randomized one NP subset of BPP.

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

- Troyer and Wiese, PRL 94, 170201 (2005), cond-mat/0408370, equations (10)-(11) and footnote 9
- NP-completeness of the 3D Ising spin-glass ground-state decision problem (Barahona)

## Bottleneck

This is a worst-case statement about a model family under a precision promise; it is not formalized here, is not a reduction to the Hubbard model, and does not make any fixed finite system or every fermionic Hamiltonian intractable.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-026 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/26_fsp/tfq_1192_fsp_troyer_wiese_reduction.md`

- file: [dag/derivations/26_fsp/tfq_1192_fsp_troyer_wiese_reduction.md](../../../dag/derivations/26_fsp/tfq_1192_fsp_troyer_wiese_reduction.md)
- sha256 (`lf-normalised`): `78abcfafa81f1b17d6ab29ce4d824dfd4ceb97015fe077a5194c396deed9754e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1192
- counts toward the grade: no

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `5a72c2f6006ea18c3362f0a63e8525b65d41898e8f1bd437b7e4c2e368c7e102`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-TROYER-WIESE-REDUCTION` `CONDITIONAL_ON_IMPORT`: [FSP-SIGN-ESTIMATOR-VARIANCE](FSP-SIGN-ESTIMATOR-VARIANCE.md) (PROVED_PROSE), [FSP-FREE-TRIANGLE-REPRESENTATION](FSP-FREE-TRIANGLE-REPRESENTATION.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
