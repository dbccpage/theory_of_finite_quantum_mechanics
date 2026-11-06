# PGW-WDP-OUT-2-GUARDED-SWAP-COHERENCE

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Outstanding Derivation Target 2 (GEN-WDP-69): if the legal complete histories of a Source_25 causal ideal form a star-shaped guard with respect to one legal center schedule, every legal swap loop is contractible inside the guard.

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

Mechanized in Lean 4 (star_contraction_reaches_center, star_shaped_swap_complex_connected, star_shaped_loop_cochain_zero, and punctured_square_loop_not_contractible in WdpBatch3.lean alongside GuardedScheduleTopology.lean) and checked in Python obstruction.py.

## Source status

GEN-WDP-69 mechanized in Lean 4 (WdpBatch3.lean, GuardedScheduleTopology.lean) and checked in Python

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/GuardedScheduleTopology.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/GuardedScheduleTopology.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/GuardedScheduleTopology.lean)
- sha256 (`bytes`): `1c868acd20086e2a9825cde8ad0f7ce88613dc161197d79466385fdb5098f39d`
- cited in: node.lean, record TFQ-0572
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/GuardedScheduleTopology.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `replay_iff_prefixSafe` | yes | yes | yes | - | `#print axioms replay_iff_prefixSafe` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean)
- sha256 (`bytes`): `8111f17913b6b991cace13c40f5762e8013e2362785e2e487229baf7d8c2d31f`
- cited in: node.lean, record TFQ-0572
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch3.punctured_square_loop_not_contractible` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch3.punctured_square_loop_not_contractible` |
| `WitnessedDifference.WdpBatch3.star_contraction_reaches_center` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch3.star_contraction_reaches_center` |
| `WitnessedDifference.WdpBatch3.star_shaped_loop_cochain_zero` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch3.star_shaped_loop_cochain_zero` |
| `WitnessedDifference.WdpBatch3.star_shaped_swap_complex_connected` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch3.star_shaped_swap_complex_connected` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py)
- sha256 (`bytes`): `2c39d5d66e90bfe5675526a4018e66a8290aa1daef019fdaceb85c4326a356d1`
- cited in: record TFQ-0572

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `obstruction_signature` (python_symbol) | yes | yes | yes | - | - |

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

### Documents and data: `dag/derivations/06_wdp/tfq_0572_wdp_out_2_guarded_swap_coherence.md`

- file: [dag/derivations/06_wdp/tfq_0572_wdp_out_2_guarded_swap_coherence.md](../../../dag/derivations/06_wdp/tfq_0572_wdp_out_2_guarded_swap_coherence.md)
- sha256 (`lf-normalised`): `9c0dc61efebdc8dc0e85f29f1c4bad88826ee6c91918bac627fbedd4705e7a35`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0572
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0572 rust: checked by Python and Rust guarded schedule topology witnesses

## Routes

Incoming (1):

- `PGW-R-WDP-OUT-2-GUARDED-SWAP-COHERENCE` `DERIVED_LEAN`: [PGW-WDP-OUT-1-SHARP-OBSERVER-COMPLETION](PGW-WDP-OUT-1-SHARP-OBSERVER-COMPLETION.md) (PROVED_LEAN), [PGW-WDP-BRIDGE-O03-GUARDED-HISTORY-COHERENCE](PGW-WDP-BRIDGE-O03-GUARDED-HISTORY-COHERENCE.md) (OPEN)

Outgoing (1):

- `PGW-R-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION` `DERIVED_LEAN`: [PGW-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION](PGW-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION.md) (PROVED_LEAN)
