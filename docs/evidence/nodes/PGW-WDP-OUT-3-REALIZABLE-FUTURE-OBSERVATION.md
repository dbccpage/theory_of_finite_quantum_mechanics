# PGW-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Outstanding Derivation Target 3 (GEN-WDP-71): in the declared eight-state future-operation table model, realizable static observation costs strictly exceed unrestricted partition costs, and adaptive two-step policies reduce average cost without reducing worst-case depth.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
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

Mechanized on the declared eight-state table model in Lean 4 (obs_decoder_unique_on_nonempty and eight_state_realizable_observation_gen_wdp_71 in WdpBatch3.lean) and checked in Python observer.py.

## Source status

GEN-WDP-71 eight-state table model mechanized in Lean 4 (WdpBatch3.lean) and checked in Python

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean)
- sha256 (`bytes`): `8111f17913b6b991cace13c40f5762e8013e2362785e2e487229baf7d8c2d31f`
- cited in: node.lean, record TFQ-0573
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch3.eight_state_realizable_observation_gen_wdp_71` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch3.eight_state_realizable_observation_gen_wdp_71` |
| `WitnessedDifference.WdpBatch3.obs_decoder_unique_on_nonempty` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch3.obs_decoder_unique_on_nonempty` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/observer.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/observer.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/observer.py)
- sha256 (`bytes`): `8ca3528b4e8b891abc63a178d4a773b8b8b06da7665f418a7298f24baa261271`
- cited in: record TFQ-0573

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuotientObserver` (python_symbol) | yes | yes | yes | - | - |

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

### Documents and data: `dag/derivations/06_wdp/tfq_0573_wdp_out_3_realizable_future_observation.md`

- file: [dag/derivations/06_wdp/tfq_0573_wdp_out_3_realizable_future_observation.md](../../../dag/derivations/06_wdp/tfq_0573_wdp_out_3_realizable_future_observation.md)
- sha256 (`lf-normalised`): `83c5fcab4baaea6ce5c013641e2c4ed3b84b63c2af24a11e2ab364fb8eb6e53e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0573
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0573 rust: checked by Python table-model verifier

## Routes

Incoming (1):

- `PGW-R-WDP-OUT-3-REALIZABLE-FUTURE-OBSERVATION` `DERIVED_LEAN`: [PGW-WDP-OUT-2-GUARDED-SWAP-COHERENCE](PGW-WDP-OUT-2-GUARDED-SWAP-COHERENCE.md) (PROVED_LEAN), [PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR](PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR.md) (OPEN)

Outgoing (2):

- `PGW-R-WDP-AFFINE-THICKENING-CONJECTURE` `DERIVED_LEAN`: [PGW-WDP-AFFINE-THICKENING-CONJECTURE](PGW-WDP-AFFINE-THICKENING-CONJECTURE.md) (PROVED_LEAN)
- `PGW-R-WDP-OUT-4-REJECTION-RULE-REUSE` `DERIVED_LEAN`: [PGW-WDP-OUT-4-REJECTION-RULE-REUSE](PGW-WDP-OUT-4-REJECTION-RULE-REUSE.md) (PROVED_LEAN)
