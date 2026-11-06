# PGW-WDP-EXACT-SCALAR-HADAMARD-OBSTRUCTION

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No rational scalar squares to 1/2, so normalized Hadamard and T gates cannot be represented inside the exact Gaussian-rational matrix algebra without quadratic irrational extension or scaled-unitary tracking (GEN-WDP-68).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
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

FiniteProcessComposition.lean and WdpBatch4.lean formalize 2-adic parity descent (nat_two_mul_sq_ne_sq, int_two_mul_sq_ne_sq, exact_scalar_hadamard_and_t_obstruction) alongside unitary_mass_preserving.

## Source status

GEN-WDP-68 proved in §17.11 and mechanized in FiniteProcessComposition.lean and WdpBatch4.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteProcessComposition.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteProcessComposition.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteProcessComposition.lean)
- sha256 (`bytes`): `596b51d29039af39c0f5d68b06816d933d84cb50a7639faf407f19a92544a45b`
- cited in: node.lean, record TFQ-0580
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteProcessComposition.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WDP.FiniteProcessComposition.postFactor_compose` | yes | yes | yes | - | `#print axioms WDP.FiniteProcessComposition.postFactor_compose` |
| `WDP.FiniteProcessComposition.unitary_mass_preserving` | yes | yes | yes | - | `#print axioms WDP.FiniteProcessComposition.unitary_mass_preserving` |
| `WitnessedDifference.FiniteProcessComposition.int_two_mul_sq_ne_sq` | yes | yes | yes | - | `#print axioms WitnessedDifference.FiniteProcessComposition.int_two_mul_sq_ne_sq` |
| `WitnessedDifference.FiniteProcessComposition.nat_two_mul_sq_ne_sq` | yes | yes | yes | - | `#print axioms WitnessedDifference.FiniteProcessComposition.nat_two_mul_sq_ne_sq` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean)
- sha256 (`bytes`): `4f63ebe575318a31ee55f58fe2008082727873250bd2ddcfc0ee960086a56e19`
- cited in: node.lean, record TFQ-0580
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch4.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch4.exact_scalar_hadamard_and_t_obstruction` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch4.exact_scalar_hadamard_and_t_obstruction` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py)
- sha256 (`bytes`): `ae67ba7c20d156bcc74833a16b7e751b27b246d039686693759d9b6065e9b128`
- cited in: record TFQ-0580

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `to_gaussian_rational` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md)
- sha256 (`lf-normalised`): `e411f9eace9de18c2583922d16d85be03fcbe4c35976ca3d7a33a0c3cfdea143`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0580_wdp_exact_scalar_hadamard_obstruction.md`

- file: [dag/derivations/06_wdp/tfq_0580_wdp_exact_scalar_hadamard_obstruction.md](../../../dag/derivations/06_wdp/tfq_0580_wdp_exact_scalar_hadamard_obstruction.md)
- sha256 (`lf-normalised`): `1cdf1810ecd0a1573c0da37e50a93e2209a1b8212909e3fa94b6f3ef2c707b97`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0580
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0580 rust: checked in Lean 4 and Python process composition modules

## Routes

Incoming (1):

- `PGW-R-WDP-EXACT-SCALAR-HADAMARD-OBSTRUCTION` `DERIVED_LEAN`: [PGW-WDP-BORN-RULE-NONSELECTION](PGW-WDP-BORN-RULE-NONSELECTION.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-AFFINE-THICKENING-CONJECTURE` `DERIVED_LEAN`: [PGW-WDP-AFFINE-THICKENING-CONJECTURE](PGW-WDP-AFFINE-THICKENING-CONJECTURE.md) (PROVED_LEAN)
