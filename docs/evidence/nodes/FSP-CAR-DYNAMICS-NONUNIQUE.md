# FSP-CAR-DYNAMICS-NONUNIQUE

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `PROVED_PROSE`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The CAR constrain the operators c_i, not the Hamiltonian: H = 0, free hopping -t sum c_i^dagger c_j and the Hubbard H(t, U) are distinct Hermitian number-conserving operators on the same CAR Fock space, so a physical Hamiltonian is an added admission (explicit 2-site Hubbard matrix computed by hand).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Hermitian Hamiltonian H = H^dagger (admitted)
- particle-number conservation \[H, N\] = 0 (admitted)
- locality graph and real hopping t (admitted)
- Hubbard on-site interaction U (admitted)

## Bottleneck

Hermiticity, number conservation, a locality graph, a one- and two-body truncation and the interaction U remain explicit admissions in every downstream sign record.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-021 claims PROVED_LEAN; audited status PROVED_PROSE

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/src/fsp/fermionic_hamiltonian.py`

- file: [code/python/src/fsp/fermionic_hamiltonian.py](../../../code/python/src/fsp/fermionic_hamiltonian.py)
- sha256 (`bytes`): `a4dc86f7f27c56cb8616761b11020be719336fef242972406f07dca87a8b744d`
- cited in: record TFQ-1187

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `DiscreteFermionicHamiltonian` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1187_fsp_car_dynamics_nonunique.md`

- file: [dag/derivations/26_fsp/tfq_1187_fsp_car_dynamics_nonunique.md](../../../dag/derivations/26_fsp/tfq_1187_fsp_car_dynamics_nonunique.md)
- sha256 (`lf-normalised`): `b4a44a3b7a2b76afe46488af6589560d25aecca1e194c9ff1820dc0e8ce71739`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1187
- counts toward the grade: no

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-CAR-DYNAMICS-NONUNIQUE` `DERIVED_PROSE`: [FSP-CAR-EXTERIOR-FOCK](FSP-CAR-EXTERIOR-FOCK.md) (PROVED_PROSE)

Outgoing (1):

- `APP-R-FSP-SIGNED-HOPPING-PATH-SERIES` `DERIVED_PROSE`: [FSP-SIGNED-HOPPING-PATH-SERIES](FSP-SIGNED-HOPPING-PATH-SERIES.md) (PROVED_PROSE)
