# PGW-WD2-FACTORED-REPORT-PRESERVATION

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A step report that factors through the before-update and after-update state observations preserves every horizon relation R_n, whereas an unfactored report can split R_n classes (WD2-T5).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Establishes in Lean 4 that endpoint-factored step reports preserve R_n and exhibits the two-state unfactored report counterexample; endpoint factorization is sufficient but not necessary at infinite horizon.

## Source status

WD2-T5 proved in Lean 4 (FiniteDistinction.lean::Wd2.factored_report_preserves_related, Wd2.factored_report_preserves_polyRelated, Wd2.unfactored_report_splits_r0)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean)
- sha256 (`bytes`): `f9d24bffacd77ea20333c3c3f24bb0cf82e4c72d317b3582db08797c522ff692`
- cited in: node.lean, record TFQ-0564
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Wd2.factored_report_preserves_polyRelated` | yes | yes | yes | - | `#print axioms Wd2.factored_report_preserves_polyRelated` |
| `Wd2.factored_report_preserves_related` | yes | yes | yes | - | `#print axioms Wd2.factored_report_preserves_related` |
| `Wd2.unfactored_report_splits_r0` | yes | yes | yes | - | `#print axioms Wd2.unfactored_report_splits_r0` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py)
- sha256 (`bytes`): `147de51ec0c53580db1f243c2ef3b8fcfa2bb001dcec753c8373ae41543bd63a`
- cited in: record TFQ-0564

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `factored_report_profile` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/01_substantiated/wd2_claim_ledger.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/01_substantiated/wd2_claim_ledger.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/01_substantiated/wd2_claim_ledger.md)
- sha256 (`lf-normalised`): `d4452e852d41814f4e6c92ecfbb006b488a9fb6330c570df2f2a1b1da81eacfd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0564_wd2_factored_report_preservation.md`

- file: [dag/derivations/06_wdp/tfq_0564_wd2_factored_report_preservation.md](../../../dag/derivations/06_wdp/tfq_0564_wd2_factored_report_preservation.md)
- sha256 (`lf-normalised`): `73520aff7352f8203af03ab431b830c7a7aefa2f1452f47a56c100bea741aa5c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0564
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0564 rust: verified directly in Lean 4 and Python

## Routes

Incoming (1):

- `PGW-R-WD2-FACTORED-REPORT-PRESERVATION` `DERIVED_LEAN`: [PGW-WD2-SHORTEST-SEPARATING-WORD](PGW-WD2-SHORTEST-SEPARATING-WORD.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WD2-MINIMAL-DETERMINISTIC-QUOTIENT` `DERIVED_LEAN`: [PGW-WD2-MINIMAL-DETERMINISTIC-QUOTIENT](PGW-WD2-MINIMAL-DETERMINISTIC-QUOTIENT.md) (PROVED_LEAN)
