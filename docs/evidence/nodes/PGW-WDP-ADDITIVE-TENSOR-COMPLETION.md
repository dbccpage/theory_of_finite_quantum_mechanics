# PGW-WDP-ADDITIVE-TENSOR-COMPLETION

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Finite alternatives on a declared generator carrier form a free commutative monoid, signed completion forms a free abelian group with its Grothendieck extension property, and biadditive composition factors uniquely through generator pairs (GEN-WDP-58, GEN-WDP-59).

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

Constructs the algebraic signed Z-module and biadditive tensor over integers; does not recover sequential order or select a complex Hilbert space.

## Source status

GEN-WDP-58/59 proved in Lean 4 (AdditiveTensorCompletion.lean)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/AdditiveTensorCompletion.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/AdditiveTensorCompletion.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/AdditiveTensorCompletion.lean)
- sha256 (`bytes`): `28db31ab24507cbdf72e331f18d6e27e014414a0ba771b02c1d1b9e822145165`
- cited in: node.lean, record TFQ-0576
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/AdditiveTensorCompletion.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WDP.AdditiveTensorCompletion.grothendieck_extension` | yes | yes | yes | - | `#print axioms WDP.AdditiveTensorCompletion.grothendieck_extension` |
| `WDP.AdditiveTensorCompletion.tensorFactor_unique` | yes | yes | yes | - | `#print axioms WDP.AdditiveTensorCompletion.tensorFactor_unique` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py)
- sha256 (`bytes`): `ae67ba7c20d156bcc74833a16b7e751b27b246d039686693759d9b6065e9b128`
- cited in: record TFQ-0576

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `to_gaussian_rational` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md)
- sha256 (`lf-normalised`): `e411f9eace9de18c2583922d16d85be03fcbe4c35976ca3d7a33a0c3cfdea143`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0576_wdp_additive_tensor_completion.md`

- file: [dag/derivations/06_wdp/tfq_0576_wdp_additive_tensor_completion.md](../../../dag/derivations/06_wdp/tfq_0576_wdp_additive_tensor_completion.md)
- sha256 (`lf-normalised`): `5236b3f4e03f1882ca007906bdee10fda58d85b77d1588500dd31ffacf2a5a2c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0576
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0576 rust: verified in Lean 4 and Python

## Routes

Incoming (1):

- `PGW-R-WDP-ADDITIVE-TENSOR-COMPLETION` `DERIVED_LEAN`: [PGW-WDP-OUT-5-FUTURE-FAITHFUL-COMPRESSION](PGW-WDP-OUT-5-FUTURE-FAITHFUL-COMPRESSION.md) (PROVED_LEAN), [PGW-WDP-BRIDGE-O04-TENSOR-RECONSTRUCTION](PGW-WDP-BRIDGE-O04-TENSOR-RECONSTRUCTION.md) (OPEN)

Outgoing (1):

- `PGW-R-WDP-DAGGER-OBSERVER-GRAM-RADICAL` `DERIVED_LEAN`: [PGW-WDP-DAGGER-OBSERVER-GRAM-RADICAL](PGW-WDP-DAGGER-OBSERVER-GRAM-RADICAL.md) (PROVED_LEAN)
