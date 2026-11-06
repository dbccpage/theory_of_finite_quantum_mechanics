# PGW-WD2-NO-ESCAPE-UPDATE-CONGRUENCE

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The initial observation kernel R_0 is an update congruence if and only if R_1 = R_0, R_infinity = R_0, and no pair in R_0 admits a separating input word (WD2-T3).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Establishes the four-way equivalence between update congruence of R_0, R_1 = R_0, R_n = R_0 for all n, and absence of separating words in Lean 4; pairs that escape R_0 are classified by shortest separating words in TFQ-0563.

## Source status

WD2-T3 proved in Lean 4 (FiniteDistinction.lean::Wd2.no_escape_equivalence)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean)
- sha256 (`bytes`): `5ad37f1db35cfbc13d56e204403f637565d877fb54979f3fc412565767969bc1`
- cited in: node.lean, record TFQ-0562
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Wd2.isUpdateCongruence_iff_r1_eq_r0` | yes | yes | yes | - | `#print axioms Wd2.isUpdateCongruence_iff_r1_eq_r0` |
| `Wd2.no_escape_equivalence` | yes | yes | yes | - | `#print axioms Wd2.no_escape_equivalence` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py)
- sha256 (`bytes`): `147de51ec0c53580db1f243c2ef3b8fcfa2bb001dcec753c8373ae41543bd63a`
- cited in: record TFQ-0562

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `no_escape_profile` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/01_substantiated/wd2_claim_ledger.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/01_substantiated/wd2_claim_ledger.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/01_substantiated/wd2_claim_ledger.md)
- sha256 (`lf-normalised`): `d4452e852d41814f4e6c92ecfbb006b488a9fb6330c570df2f2a1b1da81eacfd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0562_wd2_no_escape_update_congruence.md`

- file: [dag/derivations/06_wdp/tfq_0562_wd2_no_escape_update_congruence.md](../../../dag/derivations/06_wdp/tfq_0562_wd2_no_escape_update_congruence.md)
- sha256 (`lf-normalised`): `812b7e3a59c10acf77bdb9e4ff36285bdbfec071313890f60c682cf260a3d3f2`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0562
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0562 rust: verified directly in Lean 4 and Python

## Routes

Incoming (1):

- `PGW-R-WD2-NO-ESCAPE-UPDATE-CONGRUENCE` `DERIVED_LEAN`: [PGW-WD2-SHARP-STABILIZATION-BOUND](PGW-WD2-SHARP-STABILIZATION-BOUND.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WD2-SHORTEST-SEPARATING-WORD` `DERIVED_LEAN`: [PGW-WD2-SHORTEST-SEPARATING-WORD](PGW-WD2-SHORTEST-SEPARATING-WORD.md) (PROVED_LEAN)
