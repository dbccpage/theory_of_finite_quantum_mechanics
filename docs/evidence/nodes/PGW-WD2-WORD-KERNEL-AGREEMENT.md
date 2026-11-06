# PGW-WD2-WORD-KERNEL-AGREEMENT

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> At finite horizon n, the recursive indistinguishability relation R_n of a finite deterministic Moore machine coincides with the intersection of kernels of the observation map composed with update words of length at most n (WD2-L1).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
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

Establishes word-kernel agreement R_n = intersect_{|w|\<=n} ker(p o u_w) in Lean 4 for both concrete Nat machines and polymorphic state and alphabet types; does not bound stabilization horizon N (tracked in TFQ-0561).

## Source status

WD2-L1 proved in Lean 4 (FiniteDistinction.lean::Wd2.word_kernel_agreement, Wd2.poly_word_kernel_agreement) and checked in Python

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean)
- sha256 (`bytes`): `5ad37f1db35cfbc13d56e204403f637565d877fb54979f3fc412565767969bc1`
- cited in: node.lean, record TFQ-0559
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Wd2.poly_word_kernel_agreement` | yes | yes | yes | - | `#print axioms Wd2.poly_word_kernel_agreement` |
| `Wd2.word_kernel_agreement` | yes | yes | yes | - | `#print axioms Wd2.word_kernel_agreement` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py)
- sha256 (`bytes`): `147de51ec0c53580db1f243c2ef3b8fcfa2bb001dcec753c8373ae41543bd63a`
- cited in: record TFQ-0559

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `word_kernel_agrees` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/01_substantiated/wd2_claim_ledger.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/01_substantiated/wd2_claim_ledger.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/01_substantiated/wd2_claim_ledger.md)
- sha256 (`lf-normalised`): `d4452e852d41814f4e6c92ecfbb006b488a9fb6330c570df2f2a1b1da81eacfd`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/wd2_open_targets.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/wd2_open_targets.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/wd2_open_targets.md)
- sha256 (`lf-normalised`): `f5ddcb132fccb46c765a97473639476d70215c355eb6b6b8bb0c93fb67141f80`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0559_wd2_word_kernel_agreement.md`

- file: [dag/derivations/06_wdp/tfq_0559_wd2_word_kernel_agreement.md](../../../dag/derivations/06_wdp/tfq_0559_wd2_word_kernel_agreement.md)
- sha256 (`lf-normalised`): `a49bf4a2baa95313c02b90e229dc0f1288ed128783c8156a13c29c2f9484eb92`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0559
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0559 rust: verified directly in Lean 4 and Python

## Routes

Incoming (1):

- `PGW-R-WD2-WORD-KERNEL-AGREEMENT` `DERIVED_LEAN`: [PGW-WDP-HANDOFF-TO-L1](PGW-WDP-HANDOFF-TO-L1.md) (PROVED_LEAN), [PGW-WDP-FAILED-SAMENESS](PGW-WDP-FAILED-SAMENESS.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WD2-REFINEMENT-STABILIZATION` `DERIVED_LEAN`: [PGW-WD2-REFINEMENT-STABILIZATION](PGW-WD2-REFINEMENT-STABILIZATION.md) (PROVED_LEAN)
