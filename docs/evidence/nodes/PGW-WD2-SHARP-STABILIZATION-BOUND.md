# PGW-WD2-SHARP-STABILIZATION-BOUND

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A finite deterministic Moore machine with state set S and b_0 initial observation classes stabilizes by horizon N \<= |S| - b_0, and the five-state chain reaches the sharp bound N = 3 = 5 - 2 (WD2-T2).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
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

Establishes the strict-refinement partition-cardinality bound N \<= |S| - b_0 and the general m-state sharp chain separation witness at horizon m - 2 in Lean 4; applies to finite deterministic Moore machines.

## Source status

WD2-T2 proved in Lean 4 (FiniteDistinction.lean::Wd2.stabilization_horizon_le_card_sub_b0, Wd2.sharp_chain_general_witness, Wd2.sharp_m5_bound)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean)
- sha256 (`bytes`): `f9d24bffacd77ea20333c3c3f24bb0cf82e4c72d317b3582db08797c522ff692`
- cited in: node.lean, record TFQ-0561
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Wd2.sharp_chain_general_witness` | yes | yes | yes | - | `#print axioms Wd2.sharp_chain_general_witness` |
| `Wd2.sharp_m5_bound` | yes | yes | yes | - | `#print axioms Wd2.sharp_m5_bound` |
| `Wd2.stabilization_horizon_le_card_sub_b0` | yes | yes | yes | - | `#print axioms Wd2.stabilization_horizon_le_card_sub_b0` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py)
- sha256 (`bytes`): `147de51ec0c53580db1f243c2ef3b8fcfa2bb001dcec753c8373ae41543bd63a`
- cited in: record TFQ-0561

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `sharp_profile` (python_symbol) | yes | yes | yes | - | - |

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

### Documents and data: `dag/derivations/06_wdp/tfq_0561_wd2_sharp_stabilization_bound.md`

- file: [dag/derivations/06_wdp/tfq_0561_wd2_sharp_stabilization_bound.md](../../../dag/derivations/06_wdp/tfq_0561_wd2_sharp_stabilization_bound.md)
- sha256 (`lf-normalised`): `277310750e4f026876487da218a341ce58149dde75279b2c13d822259270eefd`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0561
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0561 rust: verified directly in Lean 4 and Python

## Routes

Incoming (1):

- `PGW-R-WD2-SHARP-STABILIZATION-BOUND` `DERIVED_LEAN`: [PGW-WD2-REFINEMENT-STABILIZATION](PGW-WD2-REFINEMENT-STABILIZATION.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WD2-NO-ESCAPE-UPDATE-CONGRUENCE` `DERIVED_LEAN`: [PGW-WD2-NO-ESCAPE-UPDATE-CONGRUENCE](PGW-WD2-NO-ESCAPE-UPDATE-CONGRUENCE.md) (PROVED_LEAN)
