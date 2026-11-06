# PGW-WDP-AFFINE-THICKENING-CONJECTURE

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For rational affine support centers thickened by bounded measurement error epsilon \> 0, the three-valued cell classifier with explicit ABSTAIN_NO_RULE abstention classifies separated cells without error, abstains on ambiguous overlap intervals rather than issuing a false decision, and bounds dyadic cell covering cost.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Mechanized in Lean 4 (thickened_affine_cell_soundness, thickened_affine_boundary_abstains, thickened_affine_no_false_verdict, thickened_fiber_not_singleton, and thickened_affine_dyadic_covering_bound in WdpBatch6.lean); applies to bounded rational noise intervals and does not claim unbounded Gaussian tail recovery.

## Source status

Thickened affine cell classifier, sound NO_RULE abstention, and dyadic covering bound mechanized in WdpBatch6.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)
- sha256 (`bytes`): `1bf7c1e971d501d47ce848a7d7c8149dd75542ace9fa09b229da2b5cc67f580c`
- cited in: node.lean, record TFQ-0581
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch6.thickened_affine_boundary_abstains` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.thickened_affine_boundary_abstains` |
| `WitnessedDifference.WdpBatch6.thickened_affine_cell_soundness` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.thickened_affine_cell_soundness` |
| `WitnessedDifference.WdpBatch6.thickened_affine_dyadic_covering_bound` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.thickened_affine_dyadic_covering_bound` |
| `WitnessedDifference.WdpBatch6.thickened_affine_no_false_verdict` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.thickened_affine_no_false_verdict` |
| `WitnessedDifference.WdpBatch6.thickened_fiber_not_singleton` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.thickened_fiber_not_singleton` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/exact_linear.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/exact_linear.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/exact_linear.py)
- sha256 (`bytes`): `fd7fd10731129a792e1bb12466fd57b7df9417f3b917a41b1c18a5219720d15d`
- cited in: record TFQ-0581

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ExactField` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/affine_thickening_conjecture.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/affine_thickening_conjecture.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/affine_thickening_conjecture.md)
- sha256 (`lf-normalised`): `92e3f6b93516c7ddf8f0a70fab5af5135d7020c117d3cbe53bf08a50096d9a29`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0581_wdp_affine_thickening_conjecture.md`

- file: [dag/derivations/06_wdp/tfq_0581_wdp_affine_thickening_conjecture.md](../../../dag/derivations/06_wdp/tfq_0581_wdp_affine_thickening_conjecture.md)
- sha256 (`lf-normalised`): `971d151ef753756dd22952273f93c04a90e87db7bd99012d0de25c089ce8f53c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0581
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0581 rust: checked in Lean 4 rational arithmetic and Python ExactField

## Routes

Incoming (1):

- `PGW-R-WDP-AFFINE-THICKENING-CONJECTURE` `DERIVED_LEAN`: [PGW-WDP-EXACT-SCALAR-HADAMARD-OBSTRUCTION](PGW-WDP-EXACT-SCALAR-HADAMARD-OBSTRUCTION.md) (PROVED_LEAN), [PGW-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION](PGW-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-MERON-M1-CORRELATION-ESTIMATES` `GAP_NO_DERIVATION`: [PGW-WDP-MERON-M1-CORRELATION-ESTIMATES](PGW-WDP-MERON-M1-CORRELATION-ESTIMATES.md) (OPEN)
