# PGW-WD2-MINIMAL-DETERMINISTIC-QUOTIENT

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The stabilized relation R_infinity is the coarsest observation-preserving update congruence, and every compatible deterministic quotient factors uniquely through S / R_infinity (WD2-T6).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Mechanized in Lean 4 (Wd2.rInfinity_coarsest_congruence and Wd2.minimal_deterministic_quotient_factorization in FiniteDistinction.lean) and checked in Python (minimal_quotient_profile in finite_distinction.py).

## Source status

WD2-T6 mechanized in Lean 4 (FiniteDistinction.lean) and checked in Python (finite_distinction.py)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean)
- sha256 (`bytes`): `5ad37f1db35cfbc13d56e204403f637565d877fb54979f3fc412565767969bc1`
- cited in: node.lean, record TFQ-0565
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Wd2.minimal_deterministic_quotient_factorization` | yes | yes | yes | - | `#print axioms Wd2.minimal_deterministic_quotient_factorization` |
| `Wd2.rInfinity_coarsest_congruence` | yes | yes | yes | - | `#print axioms Wd2.rInfinity_coarsest_congruence` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/tests/test_finite_distinction.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/tests/test_finite_distinction.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/tests/test_finite_distinction.py)
- sha256 (`bytes`): `22d8e18d720549eb3ad223935b763c508410272e0122c46e3fcc3293865bf43c`
- cited in: record TFQ-0565
- check: `python -m pytest atlas/finite_obstruction_calculus/witnessed_difference_programme/code/tests/test_finite_distinction.py::test_minimal_deterministic_quotient_factorization`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_minimal_deterministic_quotient_factorization` (python_test) | yes | yes | yes | - | `python -m pytest atlas/finite_obstruction_calculus/witnessed_difference_programme/code/tests/test_finite_distinction.py::test_minimal_deterministic_quotient_factorization` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py)
- sha256 (`bytes`): `147de51ec0c53580db1f243c2ef3b8fcfa2bb001dcec753c8373ae41543bd63a`
- cited in: record TFQ-0565

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `minimal_quotient_profile` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/01_substantiated/wd2_claim_ledger.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/01_substantiated/wd2_claim_ledger.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/01_substantiated/wd2_claim_ledger.md)
- sha256 (`lf-normalised`): `d4452e852d41814f4e6c92ecfbb006b488a9fb6330c570df2f2a1b1da81eacfd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0565_wd2_minimal_deterministic_quotient.md`

- file: [dag/derivations/06_wdp/tfq_0565_wd2_minimal_deterministic_quotient.md](../../../dag/derivations/06_wdp/tfq_0565_wd2_minimal_deterministic_quotient.md)
- sha256 (`lf-normalised`): `048f7523f0871f22cdda1711b5c76f655c7b862967431fc1cf0389712fee3d47`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0565
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0565 rust: no Rust certifier required for WD2-T6

## Routes

Incoming (1):

- `PGW-R-WD2-MINIMAL-DETERMINISTIC-QUOTIENT` `DERIVED_LEAN`: [PGW-WD2-FACTORED-REPORT-PRESERVATION](PGW-WD2-FACTORED-REPORT-PRESERVATION.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-BRIDGE-O01-CARRIER-CUT-GENESIS` `GAP_NO_DERIVATION`: [PGW-WDP-BRIDGE-O01-CARRIER-CUT-GENESIS](PGW-WDP-BRIDGE-O01-CARRIER-CUT-GENESIS.md) (OPEN)
