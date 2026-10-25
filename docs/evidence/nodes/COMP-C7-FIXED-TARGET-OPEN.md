# COMP-C7-FIXED-TARGET-OPEN

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Adding erasing rules so that every halting word reduces to one fixed word should make Reach to that fixed word undecidable; this is not proved here.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Prove Reach R0 prime (startWord x) target iff (univFun x).Dom for the extended rule set R0 prime.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C7d claims OPEN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/29_computation/tfq_1311_comp_c7_fixed_target_open.md`

- file: [dag/derivations/29_computation/tfq_1311_comp_c7_fixed_target_open.md](../../../dag/derivations/29_computation/tfq_1311_comp_c7_fixed_target_open.md)
- sha256 (`lf-normalised`): `fc33c155c99849527d36c734ca3553fb02187c4c333a639f752db35dc2fc2bcb`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1311
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C7-FIXED-TARGET-OPEN` `GAP_NO_DERIVATION`: [COMP-C7-NF-REACH-UNDECIDABLE](COMP-C7-NF-REACH-UNDECIDABLE.md) (PROVED_LEAN)

Outgoing (0):

