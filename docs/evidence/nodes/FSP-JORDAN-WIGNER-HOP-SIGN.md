# FSP-JORDAN-WIGNER-HOP-SIGN

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In the increasing occupation ordering on 6 modes, the sign of the hop c_target^dagger c_source on every occupation bitmask equals the product of the Jordan-Wigner parities of the annihilation and the creation step, checked exhaustively over all 2^6 states and ordered mode pairs.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Jordan-Wigner mapping between spin-1/2 Pauli operators and CAR operators (standard literature result)

## Bottleneck

The general Jordan-Wigner bijection c_j = (prod_{k\<j} -sigma^z_k) sigma^-_j between spin-1/2 chains and CAR operators is a standard result imported here, not derived or mechanized in this checkout.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-019 claims PROVED_LEAN; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/src/fsp/fermionic_hamiltonian.py`

- file: [code/python/src/fsp/fermionic_hamiltonian.py](../../../code/python/src/fsp/fermionic_hamiltonian.py)
- sha256 (`bytes`): `a4dc86f7f27c56cb8616761b11020be719336fef242972406f07dca87a8b744d`
- cited in: record TFQ-1185

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `_fermionic_sign` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `code/python/tests/fsp/sign_sql/test_exact_models.py`

- file: [code/python/tests/fsp/sign_sql/test_exact_models.py](../../../code/python/tests/fsp/sign_sql/test_exact_models.py)
- sha256 (`bytes`): `781feda50bb0aa8225ebfc1e7fb35b33f3792eb5a6075712eec7bbbd86c5b7f1`
- cited in: record TFQ-1185
- check: `python -m pytest code/python/tests/fsp/sign_sql/test_exact_models.py::test_hop_sign_replays_two_car_operations`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_hop_sign_replays_two_car_operations` (python_test) | yes | yes | yes | - | `python -m pytest code/python/tests/fsp/sign_sql/test_exact_models.py::test_hop_sign_replays_two_car_operations` |
- counts toward the grade: yes

### Python: `papers/core/fsp/code/sign_sql/exact_models.py`

- file: [papers/core/fsp/code/sign_sql/exact_models.py](../../../papers/core/fsp/code/sign_sql/exact_models.py)
- sha256 (`bytes`): `4ed949a915cf5e3a290017ab798d47d16af3912c343d809c320c2543ad5820c3`
- cited in: record TFQ-1185

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `hop_sign` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1185_fsp_jordan_wigner_hop_sign.md`

- file: [dag/derivations/26_fsp/tfq_1185_fsp_jordan_wigner_hop_sign.md](../../../dag/derivations/26_fsp/tfq_1185_fsp_jordan_wigner_hop_sign.md)
- sha256 (`lf-normalised`): `fb144ed45b395bc047804d579b56c6acb933ef914e6fcb74be01dbc0e8652ce6`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1185
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

- `APP-R-FSP-JORDAN-WIGNER-HOP-SIGN` `COMPUTED`: [FSP-CAR-EXTERIOR-FOCK](FSP-CAR-EXTERIOR-FOCK.md) (PROVED_PROSE)

Outgoing (1):

- `APP-R-FSP-SIGNED-HOPPING-PATH-SERIES` `DERIVED_PROSE`: [FSP-SIGNED-HOPPING-PATH-SERIES](FSP-SIGNED-HOPPING-PATH-SERIES.md) (PROVED_PROSE)
