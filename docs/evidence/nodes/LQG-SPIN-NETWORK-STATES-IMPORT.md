# LQG-SPIN-NETWORK-STATES-IMPORT

Stage: [LOOP_QUANTUM_GRAVITY](../stages/LOOP_QUANTUM_GRAVITY.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Imported structure: states are graphs whose edges carry SU(2) irreducible representations (spins) and whose vertices carry intertwiners, in a Hilbert space built with the Haar measure on SU(2) (Peter-Weyl). The repository has no compact Lie group and no Haar measure: its circle-group nodes are open, and its spin-foam shadow uses q-deformed labels in cyclotomic fields.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- SU(2) Haar measure and Peter-Weyl decomposition (assumption)
- spin networks as a state basis (assumption)

## Bottleneck

The compact-group completion that the structure needs is the SU(2) analogue of the open U(1) circle gap FQ-GAP-U1-CIRCLE.

## Source status

Audited against arXiv:gr-qc/9505006 (Sections 4, 6 pp. 17-29) and arXiv:gr-qc/9602046 (Sections 2-3 pp. 4-15) on 2026-10-22; taken as an imported assumption of this branch.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/33_loop_quantum_gravity/tfq_2302_lqg_spin_network_states_import.md`

- file: [dag/derivations/33_loop_quantum_gravity/tfq_2302_lqg_spin_network_states_import.md](../../../dag/derivations/33_loop_quantum_gravity/tfq_2302_lqg_spin_network_states_import.md)
- sha256 (`lf-normalised`): `2322cb28e972b311396edbf2a1134fb96f149017cf43001e7b23267661e8e0f6`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2302
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:gr-qc/9505006`
- `external:arXiv:gr-qc/9602046`

## Routes

Incoming (2):

- `FRO-R-LQG-SPIN-NETWORK-STATES-IMPORT` `CONDITIONAL_ON_IMPORT`: [LQG-SPIN-NETWORK-KINEMATICS-SOURCE](LQG-SPIN-NETWORK-KINEMATICS-SOURCE.md) (SOURCE_RECORD)
- `FRO-R-LQG-SPIN-NETWORK-STATES-IMPORT-X1` `GAP_NO_DERIVATION`: [FQ-GAP-U1-CIRCLE](FQ-GAP-U1-CIRCLE.md) (CONDITIONAL)

Outgoing (1):

- `FRO-R-LQG-AREA-SPECTRUM-EXACT-TARGET` `DERIVED_LEAN`: [LQG-AREA-SPECTRUM-EXACT-TARGET](LQG-AREA-SPECTRUM-EXACT-TARGET.md) (PROVED_LEAN)
