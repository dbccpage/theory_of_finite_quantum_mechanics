# PGW-WDP-BORN-RULE-NONSELECTION

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Positivity, normalization, phase invariance, and affinity admit a one-parameter family of state-effect readouts distinct from trace pairing, showing in this finite model that trace Born weights require an additional assumption (GEN-WDP-65).

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

Mechanized in Lean 4 (born_numerator_identity and probability_normalized in FiniteStateEffectReadout.lean plus deformed_probability_normalized, deformed_probability_nonnegative, and born_rule_nonselection_gen_wdp_65 in WdpBatch3.lean) and checked in Python quantum.py.

## Source status

GEN-WDP-65 mechanized in Lean 4 (FiniteStateEffectReadout.lean, WdpBatch3.lean) and checked in Python

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteStateEffectReadout.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteStateEffectReadout.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteStateEffectReadout.lean)
- sha256 (`bytes`): `8a1a2c2eab8ea57e8a691d01a1e32ce61be13ca9183ec26e4255f0c2e83c9d63`
- cited in: node.lean, record TFQ-0579
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteStateEffectReadout.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WDP.FiniteStateEffectReadout.born_numerator_identity` | yes | yes | yes | - | `#print axioms WDP.FiniteStateEffectReadout.born_numerator_identity` |
| `WDP.FiniteStateEffectReadout.probability_normalized` | yes | yes | yes | - | `#print axioms WDP.FiniteStateEffectReadout.probability_normalized` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean)
- sha256 (`bytes`): `8111f17913b6b991cace13c40f5762e8013e2362785e2e487229baf7d8c2d31f`
- cited in: node.lean, record TFQ-0579
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch3.born_rule_nonselection_gen_wdp_65` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch3.born_rule_nonselection_gen_wdp_65` |
| `WitnessedDifference.WdpBatch3.deformed_probability_nonnegative` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch3.deformed_probability_nonnegative` |
| `WitnessedDifference.WdpBatch3.deformed_probability_normalized` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch3.deformed_probability_normalized` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py)
- sha256 (`bytes`): `ae67ba7c20d156bcc74833a16b7e751b27b246d039686693759d9b6065e9b128`
- cited in: record TFQ-0579

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `to_gaussian_rational` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md)
- sha256 (`lf-normalised`): `e411f9eace9de18c2583922d16d85be03fcbe4c35976ca3d7a33a0c3cfdea143`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0579_wdp_born_rule_nonselection.md`

- file: [dag/derivations/06_wdp/tfq_0579_wdp_born_rule_nonselection.md](../../../dag/derivations/06_wdp/tfq_0579_wdp_born_rule_nonselection.md)
- sha256 (`lf-normalised`): `564413aabb22db4ae20b8733bddf76f42b8982cad0db7717aa832126a372bd2d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0579
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0579 rust: checked in Lean 4 and Python state-effect readout fixtures

## Routes

Incoming (1):

- `PGW-R-WDP-BORN-RULE-NONSELECTION` `DERIVED_LEAN`: [PGW-WDP-FINITE-HERMITIANIZATION](PGW-WDP-FINITE-HERMITIANIZATION.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-EXACT-SCALAR-HADAMARD-OBSTRUCTION` `DERIVED_LEAN`: [PGW-WDP-EXACT-SCALAR-HADAMARD-OBSTRUCTION](PGW-WDP-EXACT-SCALAR-HADAMARD-OBSTRUCTION.md) (PROVED_LEAN)
