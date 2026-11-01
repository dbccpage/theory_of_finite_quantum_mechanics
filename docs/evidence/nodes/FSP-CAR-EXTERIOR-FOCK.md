# FSP-CAR-EXTERIOR-FOCK

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `PROVED_PROSE`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On an admitted N-dimensional complex inner-product space V with orthonormal basis e_i, creation c_i^dagger = e_i wedge - and interior annihilation c_i on the exterior algebra of V (dimension 2^N) satisfy {c_i, c_j} = 0 and {c_i, c_j^dagger} = delta_ij; in particular (c_i)^2 = 0.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- complex mode space V with inner product (admitted)
- exterior Fock space as the carrier for fermionic states (admitted)

## Bottleneck

Mechanize the CAR identities on the exterior algebra; the statistics choice (exterior versus symmetric algebra) is an admitted postulate, and identifying modes with spin-1/2 particles needs the relativistic spin-statistics theorem, outside this finite setting.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-018 claims PROVED_LEAN; audited status PROVED_PROSE

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/tests/fsp/sign_sql/test_exact_models.py`

- file: [code/python/tests/fsp/sign_sql/test_exact_models.py](../../../code/python/tests/fsp/sign_sql/test_exact_models.py)
- sha256 (`bytes`): `781feda50bb0aa8225ebfc1e7fb35b33f3792eb5a6075712eec7bbbd86c5b7f1`
- cited in: record TFQ-1184
- check: `python -m pytest code/python/tests/fsp/sign_sql/test_exact_models.py::test_hop_sign_replays_two_car_operations`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_hop_sign_replays_two_car_operations` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/fsp/sign_sql/test_exact_models.py::test_hop_sign_replays_two_car_operations` |

- counts toward the grade: yes

### Python: `papers/core/fsp/code/sign_sql/exact_models.py`

- file: [papers/core/fsp/code/sign_sql/exact_models.py](../../../papers/core/fsp/code/sign_sql/exact_models.py)
- sha256 (`bytes`): `4ed949a915cf5e3a290017ab798d47d16af3912c343d809c320c2543ad5820c3`
- cited in: record TFQ-1184

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `hop_sign` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1184_fsp_car_exterior_fock.md`

- file: [dag/derivations/26_fsp/tfq_1184_fsp_car_exterior_fock.md](../../../dag/derivations/26_fsp/tfq_1184_fsp_car_exterior_fock.md)
- sha256 (`lf-normalised`): `de56279c366cd00bf6a18a4c4c8de426a8275a9c21f1a20ad6634de1a15fa238`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1184
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

- `APP-R-FSP-CAR-EXTERIOR-FOCK` `DERIVED_PROSE`: [L1-IMP-HILBERT-INNER-PRODUCT](L1-IMP-HILBERT-INNER-PRODUCT.md) (CONDITIONAL), [L1-IMP-COMPLEX-FIELD](L1-IMP-COMPLEX-FIELD.md) (CONDITIONAL), [DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT](DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT.md) (IMPORTED_ASSUMPTION)

Outgoing (6):

- `APP-R-FSP-CAR-DYNAMICS-NONUNIQUE` `DERIVED_PROSE`: [FSP-CAR-DYNAMICS-NONUNIQUE](FSP-CAR-DYNAMICS-NONUNIQUE.md) (PROVED_PROSE)
- `APP-R-FSP-FREE-TRIANGLE-REPRESENTATION` `COMPUTED`: [FSP-FREE-TRIANGLE-REPRESENTATION](FSP-FREE-TRIANGLE-REPRESENTATION.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-FSP-JORDAN-WIGNER-HOP-SIGN` `COMPUTED`: [FSP-JORDAN-WIGNER-HOP-SIGN](FSP-JORDAN-WIGNER-HOP-SIGN.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-FSP-LATTICE-WESS-ZUMINO-SUSY` `GAP_NO_DERIVATION`: [FSP-LATTICE-WESS-ZUMINO-SUSY](FSP-LATTICE-WESS-ZUMINO-SUSY.md) (OPEN)
- `APP-R-FSP-MAJORANA-CLIFFORD-PARITY` `CONDITIONAL_ON_IMPORT`: [FSP-MAJORANA-CLIFFORD-PARITY](FSP-MAJORANA-CLIFFORD-PARITY.md) (IMPORTED_ASSUMPTION)
- `APP-R-FSP-WILSON-DIRAC-GAMMA5` `CONDITIONAL_ON_IMPORT`: [FSP-WILSON-DIRAC-GAMMA5](FSP-WILSON-DIRAC-GAMMA5.md) (IMPORTED_ASSUMPTION)
