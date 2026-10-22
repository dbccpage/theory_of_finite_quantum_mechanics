# COMP-C6-FINITE-MARKS

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Every word reachable from a start word of the fixed rewriting regime has its marks in the finite set markSet: two end markers, the 1250 tape marks of Bool x (K -\> Option G), and the state marks of the finite set S0 given by the Mathlib tr_supports chain.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 6 Lean reference(s) cited, 6 in this checkout (replay: none 6). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- Mathlib tr_supports for PartrecToTM2, TM2to1 and TM1to0

## Bottleneck

The size of S0 is not computed and the machine is not claimed small.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C6d claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisCompUniv.lean`

- file: [lean4/GenesisCompUniv.lean](../../../lean4/GenesisCompUniv.lean)
- sha256 (`bytes`): `966d60cf259d7c22f275e13ab58dd6d027330f6ae146536eb68a97ddb97620f3`
- cited in: node.lean, node.source, record TFQ-1306
- replay: `none`
- check: `cd lean4 && lake build GenesisCompUniv`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `card_G1` | yes | yes | yes | - | `#print axioms card_G1` |
| `init_mem` | yes | yes | yes | - | `#print axioms init_mem` |
| `markSet` | yes | yes | yes | - | `#print axioms markSet` |
| `step_closed` | yes | yes | yes | - | `#print axioms step_closed` |
| `used_marks_finite` | yes | yes | yes | - | `#print axioms used_marks_finite` |
| `used_state_marks_finite` | yes | yes | yes | - | `#print axioms used_state_marks_finite` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1306_comp_c6_finite_marks.md`

- file: [dag/derivations/29_computation/tfq_1306_comp_c6_finite_marks.md](../../../dag/derivations/29_computation/tfq_1306_comp_c6_finite_marks.md)
- sha256 (`lf-normalised`): `7dab3c108ab0db31a69bb05e4fbe2a370273138d716cb61e212367977f6b4c75`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1306
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C6-FINITE-MARKS` `DERIVED_LEAN`: [COMP-C6-TM0-HALTING-EQUIVALENCE](COMP-C6-TM0-HALTING-EQUIVALENCE.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-COMP-C8-MINIMALITY-FENCE` `GAP_NO_DERIVATION`: [COMP-C8-MINIMALITY-FENCE](COMP-C8-MINIMALITY-FENCE.md) (OPEN)
