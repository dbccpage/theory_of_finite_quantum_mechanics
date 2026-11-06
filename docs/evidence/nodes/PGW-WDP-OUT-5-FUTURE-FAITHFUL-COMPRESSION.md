# PGW-WDP-OUT-5-FUTURE-FAITHFUL-COMPRESSION

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Outstanding Derivation Target 5 (GEN-WDP-73): on the bounded five-edit native carrier (at most 3 literal terms, count total at most 4, horizon h=2), clipped signed counts and a 13-coordinate integer report determine all horizon-2 future observations.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
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

Mechanized in Lean 4 for both h=2 (NativeFutureCompression.lean) and general horizon h with T \<= 2h reconstruction and T = 2h + 1 sharp collision (general_horizon_clipped_signed_counts_unique, general_horizon_sharp_collision, general_horizon_composition_bound in WdpBatch3.lean).

## Source status

GEN-WDP-73 mechanized in Lean 4 for h=2 (NativeFutureCompression.lean) and general horizon h (WdpBatch3.lean)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/NativeFutureCompression.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/NativeFutureCompression.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/NativeFutureCompression.lean)
- sha256 (`bytes`): `61e10d4c90cbebda03adf67598c8f62b2de8745627776be3efa4c856de4b986f`
- cited in: node.lean, record TFQ-0575
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/NativeFutureCompression.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `horizon_two_composition_bound` | yes | yes | yes | - | `#print axioms horizon_two_composition_bound` |
| `two_removal_answers_determine_clip` | yes | yes | yes | - | `#print axioms two_removal_answers_determine_clip` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean)
- sha256 (`bytes`): `8111f17913b6b991cace13c40f5762e8013e2362785e2e487229baf7d8c2d31f`
- cited in: node.lean, record TFQ-0575
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch3.general_horizon_clipped_signed_counts_unique` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch3.general_horizon_clipped_signed_counts_unique` |
| `WitnessedDifference.WdpBatch3.general_horizon_composition_bound` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch3.general_horizon_composition_bound` |
| `WitnessedDifference.WdpBatch3.general_horizon_sharp_collision` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch3.general_horizon_sharp_collision` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/retention_choices.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/retention_choices.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/retention_choices.py)
- sha256 (`bytes`): `391a7f3549fa1fbdfa050f7ad71b5f53cb902cafb73d1fbd39a7f4962d3c43a0`
- cited in: record TFQ-0575

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `RetentionSignature` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/five_outstanding_derivations.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/five_outstanding_derivations.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/five_outstanding_derivations.md)
- sha256 (`lf-normalised`): `a3d73b25967a6c6d44f0ef077d4ab708e52a42d9110e1591258c5d32e6e862d5`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md)
- sha256 (`lf-normalised`): `e411f9eace9de18c2583922d16d85be03fcbe4c35976ca3d7a33a0c3cfdea143`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0575_wdp_out_5_future_faithful_compression.md`

- file: [dag/derivations/06_wdp/tfq_0575_wdp_out_5_future_faithful_compression.md](../../../dag/derivations/06_wdp/tfq_0575_wdp_out_5_future_faithful_compression.md)
- sha256 (`lf-normalised`): `86b4d59adc8d3eb5c210c4d83762ffbffe6f787814e27ca36760eadae1ba8ce7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0575
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0575 rust: horizon-2 native compression verified in Lean 4 and Python

## Routes

Incoming (1):

- `PGW-R-WDP-OUT-5-FUTURE-FAITHFUL-COMPRESSION` `DERIVED_LEAN`: [PGW-WDP-OUT-4-REJECTION-RULE-REUSE](PGW-WDP-OUT-4-REJECTION-RULE-REUSE.md) (PROVED_LEAN), [PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR](PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR.md) (OPEN)

Outgoing (1):

- `PGW-R-WDP-ADDITIVE-TENSOR-COMPLETION` `DERIVED_LEAN`: [PGW-WDP-ADDITIVE-TENSOR-COMPLETION](PGW-WDP-ADDITIVE-TENSOR-COMPLETION.md) (PROVED_LEAN)
