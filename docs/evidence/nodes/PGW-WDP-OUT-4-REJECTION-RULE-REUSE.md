# PGW-WDP-OUT-4-REJECTION-RULE-REUSE

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Outstanding Derivation Target 4 (GEN-WDP-72): a sound rejection rule pushed forward along a representation map remains sound on the target image only under fiber-constant target questions and explicit out-of-image abstention (NO_RULE).

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

Mechanized on the nine-element image carriers in Lean 4 (reuse_decode_encode2, reuse_encode_decode_image, reuse_soundness_iff, reuse_coverage_iff, and reuse_scan_thresholds_and_task2_trap in WdpBatch3.lean) and checked in Python authority.py.

## Source status

GEN-WDP-72 nine-element reuse theorem mechanized in Lean 4 (WdpBatch3.lean) and checked in Python

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean)
- sha256 (`bytes`): `8111f17913b6b991cace13c40f5762e8013e2362785e2e487229baf7d8c2d31f`
- cited in: node.lean, record TFQ-0574
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch3.reuse_coverage_iff` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch3.reuse_coverage_iff` |
| `WitnessedDifference.WdpBatch3.reuse_decode_encode2` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch3.reuse_decode_encode2` |
| `WitnessedDifference.WdpBatch3.reuse_encode_decode_image` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch3.reuse_encode_decode_image` |
| `WitnessedDifference.WdpBatch3.reuse_scan_thresholds_and_task2_trap` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch3.reuse_scan_thresholds_and_task2_trap` |
| `WitnessedDifference.WdpBatch3.reuse_soundness_iff` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch3.reuse_soundness_iff` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/foundational_bridges.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/foundational_bridges.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/foundational_bridges.py)
- sha256 (`bytes`): `8a955655b74671c6599df32e839bbaef8357e8d789869b009b63e063bc15bcbb`
- cited in: record TFQ-0574

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `apartness_witness` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/five_outstanding_derivations.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/five_outstanding_derivations.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/five_outstanding_derivations.md)
- sha256 (`lf-normalised`): `5159b5a0f8ccfd1f68042b29348fe45640ccac0a5e90852416e9cb987e867418`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md)
- sha256 (`lf-normalised`): `e411f9eace9de18c2583922d16d85be03fcbe4c35976ca3d7a33a0c3cfdea143`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0574_wdp_out_4_rejection_rule_reuse.md`

- file: [dag/derivations/06_wdp/tfq_0574_wdp_out_4_rejection_rule_reuse.md](../../../dag/derivations/06_wdp/tfq_0574_wdp_out_4_rejection_rule_reuse.md)
- sha256 (`lf-normalised`): `b69d607aa983b982ccc509225af77fe73ad673a0f4a792f40634eab0bd591d7f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0574
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0574 rust: checked by Python rejection-rule reuse witnesses

## Routes

Incoming (1):

- `PGW-R-WDP-OUT-4-REJECTION-RULE-REUSE` `DERIVED_LEAN`: [PGW-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION](PGW-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION.md) (PROVED_LEAN), [PGW-WDP-BRIDGE-O05-AUTHORIZATION-FIREWALL](PGW-WDP-BRIDGE-O05-AUTHORIZATION-FIREWALL.md) (OPEN)

Outgoing (1):

- `PGW-R-WDP-OUT-5-FUTURE-FAITHFUL-COMPRESSION` `DERIVED_LEAN`: [PGW-WDP-OUT-5-FUTURE-FAITHFUL-COMPRESSION](PGW-WDP-OUT-5-FUTURE-FAITHFUL-COMPRESSION.md) (PROVED_LEAN)
