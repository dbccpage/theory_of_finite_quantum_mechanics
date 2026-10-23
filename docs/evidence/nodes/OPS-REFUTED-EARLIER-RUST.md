# OPS-REFUTED-EARLIER-RUST

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `REFUTED`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> At head 0a0502646 of the source repository the following were wrong. (N4) Scenario::section_count multiplied arities without a check, and the limit was compared afterwards: 64 binary singletons (2^64 assignments) wrapped to 0 in a release build, so global_support returned an empty support and is_strongly_contextual returned true. (N5) ObserverDraft::declare accepted empty and whitespace strings, and the five strings were free text copied into the receipt: a norm "L2", a terminal "always OpenObstruction" and a layer "authoritative" each yielded the l1 value, ExactRepair and authority None. (N6) Proposition A2 claimed that no claim-to-receipt function exists, carried a layer row whose second completion was not an observer, and said the refusal test dropped five components when it dropped two; and verify_noncontextual_fraction read only lp.value from the embedded solution. (N7) delta0 checked only the number of entries, delta1 and flatten1 ignored extraneous keys and pairs outside every triple, and the only delta1 delta0 = 0 test ran on the Bell nerve, which has no triple. Recomputed here: 2^64 is 0 modulo 2^64.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Records superseded defects. The repaired behaviour is in nodes OPS-OBSERVER-DECLARATION-REFUSAL and OPS-RUST-RECEIPTS-AND-LIMITS, which are conditional (not run here).

## Source status

Ledger rows L035-N4 to L035-N7: refuted (the note's own earlier code and text), found in the review of PR 1080 of the source repository; repaired by rows A2, A3, A4, B9, B16 and B17. The earlier head is not in this repository, so the defects are not reproduced here.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `checks/independent/foc035_observer_presheaf.py`

- file: [checks/independent/foc035_observer_presheaf.py](../../../checks/independent/foc035_observer_presheaf.py)
- sha256 (`bytes`): `6c1962e9a7e6b987ed5ba1b47afca56f17065d81fbfd2522245711b3840967ef`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2531_ops_refuted_earlier_rust.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2531_ops_refuted_earlier_rust.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2531_ops_refuted_earlier_rust.md)
- sha256 (`lf-normalised`): `c7a6596014da8420e1169795d26c848315ef735fc25b38a0a8fbb4e14f0f4a93`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2531
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md)
- sha256 (`lf-normalised`): `da99779add73314574622d0db46ea4dfbc9b66c4938caf29ab98590033592ab4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md)
- sha256 (`lf-normalised`): `649532625cf9e8ec085a420fd1bad9227fcc4dae9f06ba02be1eb19f497e3ec7`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `OPS-R-REFUTED-EARLIER-RUST` `RECORD_PARENT`: [OPS-RUST-RECEIPTS-AND-LIMITS](OPS-RUST-RECEIPTS-AND-LIMITS.md) (CONDITIONAL), [OPS-OBSERVER-DECLARATION-REFUSAL](OPS-OBSERVER-DECLARATION-REFUSAL.md) (CONDITIONAL)

Outgoing (0):

