# PGW-WDP-OUT-1-SHARP-OBSERVER-COMPLETION

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Outstanding Derivation Target 1 (GEN-WDP-70): when realization image R and repair subspace B_1 differ, minimum observer row completion over Q requires dim(R intersect B_1) - dim(R intersect B_1 intersect ker O_0) added rows.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Mechanized in Lean 4 (sharp_observer_completion_formula_gen_wdp_70, equal_image_regime_reduction, and native_repair_realization_iff_preimage in WdpBatch2.lean) and checked in Python exact_linear.py.

## Source status

GEN-WDP-70 mechanized in Lean 4 (WdpBatch2.lean) and checked in Python exact_linear.py

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean)
- sha256 (`bytes`): `b40aa3e8417cf931d7fe83e997f927c00648d0bcdced7873735a60f8212c0413`
- cited in: node.lean, record TFQ-0571
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch2.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch2.equal_image_regime_reduction` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch2.equal_image_regime_reduction` |
| `WitnessedDifference.WdpBatch2.native_repair_realization_iff_preimage` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch2.native_repair_realization_iff_preimage` |
| `WitnessedDifference.WdpBatch2.sharp_observer_completion_formula_gen_wdp_70` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch2.sharp_observer_completion_formula_gen_wdp_70` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/exact_linear.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/exact_linear.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/exact_linear.py)
- sha256 (`bytes`): `fd7fd10731129a792e1bb12466fd57b7df9417f3b917a41b1c18a5219720d15d`
- cited in: record TFQ-0571

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ExactField` (python_symbol) | yes | yes | yes | - | - |

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

### Documents and data: `dag/derivations/06_wdp/tfq_0571_wdp_out_1_sharp_observer_completion.md`

- file: [dag/derivations/06_wdp/tfq_0571_wdp_out_1_sharp_observer_completion.md](../../../dag/derivations/06_wdp/tfq_0571_wdp_out_1_sharp_observer_completion.md)
- sha256 (`lf-normalised`): `1114f0eada157223e42141934a1708b590bab6093fd4057c50014d797c91a276`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0571
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0571 rust: checked in Python exact rational linear algebra

## Routes

Incoming (1):

- `PGW-R-WDP-OUT-1-SHARP-OBSERVER-COMPLETION` `DERIVED_LEAN`: [PGW-WDP-BRIDGE-O05-AUTHORIZATION-FIREWALL](PGW-WDP-BRIDGE-O05-AUTHORIZATION-FIREWALL.md) (OPEN), [PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR](PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR.md) (OPEN)

Outgoing (1):

- `PGW-R-WDP-OUT-2-GUARDED-SWAP-COHERENCE` `DERIVED_LEAN`: [PGW-WDP-OUT-2-GUARDED-SWAP-COHERENCE](PGW-WDP-OUT-2-GUARDED-SWAP-COHERENCE.md) (PROVED_LEAN)
