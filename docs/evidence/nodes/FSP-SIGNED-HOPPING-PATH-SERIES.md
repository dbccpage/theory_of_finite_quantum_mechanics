# FSP-SIGNED-HOPPING-PATH-SERIES

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `PROVED_PROSE`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a finite self-adjoint H with H_xx = V_x, H_xy = -a_xy (-1)^{eps_xy} (a_xy \> 0, eps symmetric), beta \>= 0 and E* \>= max V_x, Z = e^{-beta E*} sum_m beta^m/m! sum over closed length-m configuration paths of prod K_{x_{j+1} x_j} with K = E* I - H, and each nonzero closed term has sign (-1)^{sum of eps along the path}.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 2
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- positive edge magnitudes a_xy, parities eps_xy and diagonal energies V_x on an orthonormal configuration basis (supplied; ledger ORIGIN-001)

## Bottleneck

The sign of a closed term is a property of the supplied magnitudes, parities and representation; vertex sign gauges remove all negative entries exactly when every configuration cycle is even (FSP-SWITCHING-NORMAL-FORM). Trotter slicing and its error are separate.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-022 claims PROVED_LEAN; audited status PROVED_PROSE

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/tests/fsp/sign_sql/test_exact_models.py`

- file: [code/python/tests/fsp/sign_sql/test_exact_models.py](../../../code/python/tests/fsp/sign_sql/test_exact_models.py)
- sha256 (`bytes`): `781feda50bb0aa8225ebfc1e7fb35b33f3792eb5a6075712eec7bbbd86c5b7f1`
- cited in: record TFQ-1188

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_hubbard_configuration_cycles_reconstruct_negative_gauge_holonomy` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/fsp/sign_sql/test_exact_models.py::test_hubbard_configuration_cycles_reconstruct_negative_gauge_holonomy` |
| `test_sql_hubbard_obstruction_agrees_with_independent_sign_normal_form` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/fsp/sign_sql/test_exact_models.py::test_sql_hubbard_obstruction_agrees_with_independent_sign_normal_form` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1188_fsp_signed_hopping_path_series.md`

- file: [dag/derivations/26_fsp/tfq_1188_fsp_signed_hopping_path_series.md](../../../dag/derivations/26_fsp/tfq_1188_fsp_signed_hopping_path_series.md)
- sha256 (`lf-normalised`): `a070b87b8f08aae21a6cc8c9486fe19afcc266319ee901e438bc1b80957bfb6a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1188
- counts toward the grade: no

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `5f5dfaa7a3794d1fee0299865df221b6db1c14ebf6f3925b1729e784a28e3194`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `3e88f1a70b66b0b90cc915acb5c802c118775e65cc8970af6c5a423f27ddd755`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-SIGNED-HOPPING-PATH-SERIES` `DERIVED_PROSE`: [FSP-CAR-DYNAMICS-NONUNIQUE](FSP-CAR-DYNAMICS-NONUNIQUE.md) (PROVED_PROSE), [FSP-JORDAN-WIGNER-HOP-SIGN](FSP-JORDAN-WIGNER-HOP-SIGN.md) (COMPUTATIONALLY_CHECKED)

Outgoing (3):

- `APP-R-FSP-AVERAGE-SIGN-DEFINITION` `DERIVED_PROSE`: [FSP-AVERAGE-SIGN-DEFINITION](FSP-AVERAGE-SIGN-DEFINITION.md) (DEFINITION)
- `APP-R-FSP-FREE-TRIANGLE-REPRESENTATION` `COMPUTED`: [FSP-FREE-TRIANGLE-REPRESENTATION](FSP-FREE-TRIANGLE-REPRESENTATION.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-FSP-INVOLUTION-PAIR-CANCELLATION` `DERIVED_LEAN`: [FSP-INVOLUTION-PAIR-CANCELLATION](FSP-INVOLUTION-PAIR-CANCELLATION.md) (PROVED_LEAN)
