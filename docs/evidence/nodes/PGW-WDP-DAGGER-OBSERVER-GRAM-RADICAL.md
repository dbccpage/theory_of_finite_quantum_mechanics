# PGW-WDP-DAGGER-OBSERVER-GRAM-RADICAL

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A declared involution on typed generators extends uniquely to signed histories respecting componentwise tensor composition, and the coordinate Gram form of an additive observer is positive semidefinite with radical equal to its observation kernel (GEN-WDP-60, GEN-WDP-61).

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

Establishes in Lean 4 positive semidefiniteness and radical-kernel equality for the integer coordinate Gram form; executable reversal of native guarded edits remains separate.

## Source status

GEN-WDP-60/61 proved in Lean 4 (DaggerObserverPairing.lean)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/DaggerObserverPairing.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/DaggerObserverPairing.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/DaggerObserverPairing.lean)
- sha256 (`bytes`): `a5a4499f6f7e4443aef061f89ccad229ed1e64832f2d380f2bc53caaa8bf2c93`
- cited in: node.lean, record TFQ-0577
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/DaggerObserverPairing.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WDP.DaggerObserverPairing.observerPairing_self_nonnegative` | yes | yes | yes | - | `#print axioms WDP.DaggerObserverPairing.observerPairing_self_nonnegative` |
| `WDP.DaggerObserverPairing.observerPairing_self_zero_iff_kernel` | yes | yes | yes | - | `#print axioms WDP.DaggerObserverPairing.observerPairing_self_zero_iff_kernel` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py)
- sha256 (`bytes`): `ae67ba7c20d156bcc74833a16b7e751b27b246d039686693759d9b6065e9b128`
- cited in: record TFQ-0577

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `to_gaussian_rational` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md)
- sha256 (`lf-normalised`): `e411f9eace9de18c2583922d16d85be03fcbe4c35976ca3d7a33a0c3cfdea143`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0577_wdp_dagger_observer_gram_radical.md`

- file: [dag/derivations/06_wdp/tfq_0577_wdp_dagger_observer_gram_radical.md](../../../dag/derivations/06_wdp/tfq_0577_wdp_dagger_observer_gram_radical.md)
- sha256 (`lf-normalised`): `ab04b0c22a14d9f12d3fcbd0ed18c96ba5d0294c45454933e955e399fba7fc31`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0577
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0577 rust: verified in Lean 4 and Python

## Routes

Incoming (1):

- `PGW-R-WDP-DAGGER-OBSERVER-GRAM-RADICAL` `DERIVED_LEAN`: [PGW-WDP-ADDITIVE-TENSOR-COMPLETION](PGW-WDP-ADDITIVE-TENSOR-COMPLETION.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-FINITE-HERMITIANIZATION` `DERIVED_LEAN`: [PGW-WDP-FINITE-HERMITIANIZATION](PGW-WDP-FINITE-HERMITIANIZATION.md) (PROVED_LEAN)
