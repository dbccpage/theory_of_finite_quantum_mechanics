# PGW-WDP-FINITE-HERMITIANIZATION

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A supplied rational-linear operator J satisfying J^2 = -I compatible with a symmetric positive-semidefinite bilinear form constructs a Q(i)-Hermitian positive-semidefinite form with the same radical, while leaving the sign of J unselected (GEN-WDP-62, GEN-WDP-63).

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

Requires a supplied compatible complex structure J; positive form alone does not select between J and -J.

## Source status

GEN-WDP-62/63 proved in Lean 4 (FiniteHermitianization.lean)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteHermitianization.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteHermitianization.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteHermitianization.lean)
- sha256 (`bytes`): `96a984deb110972836d9f41b597513fd58e62294dd5d3246806e9699ae59a504`
- cited in: node.lean, record TFQ-0578
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteHermitianization.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WDP.FiniteHermitianization.hermitian_radical_iff_form_radical` | yes | yes | yes | - | `#print axioms WDP.FiniteHermitianization.hermitian_radical_iff_form_radical` |
| `WDP.FiniteHermitianization.hermitian_self_nonnegative` | yes | yes | yes | - | `#print axioms WDP.FiniteHermitianization.hermitian_self_nonnegative` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py)
- sha256 (`bytes`): `ae67ba7c20d156bcc74833a16b7e751b27b246d039686693759d9b6065e9b128`
- cited in: record TFQ-0578

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `to_gaussian_rational` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md)
- sha256 (`lf-normalised`): `e411f9eace9de18c2583922d16d85be03fcbe4c35976ca3d7a33a0c3cfdea143`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0578_wdp_finite_hermitianization.md`

- file: [dag/derivations/06_wdp/tfq_0578_wdp_finite_hermitianization.md](../../../dag/derivations/06_wdp/tfq_0578_wdp_finite_hermitianization.md)
- sha256 (`lf-normalised`): `bce2514d3cdea93a84c29c9846d121651020763252ea1f91d2c918f89254e8ff`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0578
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0578 rust: verified in Lean 4 and Python

## Routes

Incoming (1):

- `PGW-R-WDP-FINITE-HERMITIANIZATION` `DERIVED_LEAN`: [PGW-WDP-DAGGER-OBSERVER-GRAM-RADICAL](PGW-WDP-DAGGER-OBSERVER-GRAM-RADICAL.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-BORN-RULE-NONSELECTION` `DERIVED_LEAN`: [PGW-WDP-BORN-RULE-NONSELECTION](PGW-WDP-BORN-RULE-NONSELECTION.md) (PROVED_LEAN)
