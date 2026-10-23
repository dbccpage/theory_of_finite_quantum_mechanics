# COMP-C3-NO-FIXED-BOUND

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> If the map from an input to its start word were computable and one length bound witnessed every halting start word inside the bound, normal-form reachability would be decidable, contradicting nfReach_not_computable.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- startWord_computable (open lemma)

## Bottleneck

Prove startWord_computable (COMP-C7c) and state the uniform version in Lean.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C3e claims CONDITIONAL; audited status CONDITIONAL

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisCompUniv.lean`

- file: [lean4/GenesisCompUniv.lean](../../../lean4/GenesisCompUniv.lean)
- sha256 (`bytes`): `966d60cf259d7c22f275e13ab58dd6d027330f6ae146536eb68a97ddb97620f3`
- cited in: node.lean, record TFQ-1295
- replay: `none`
- check: `cd lean4 && lake build GenesisCompUniv`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `nfReach_not_computable` | yes | yes | yes | - | `#print axioms nfReach_not_computable` |
- counts toward the grade: yes

### Lean: `lean4/GenesisComputation.lean`

- file: [lean4/GenesisComputation.lean](../../../lean4/GenesisComputation.lean)
- sha256 (`bytes`): `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994`
- cited in: node.lean, record TFQ-1295
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-decision-procedure_lean_replay.json](../../../dag/research/campaign_pgw-context-decision-procedure_lean_replay.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `reachB_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms reachB_iff` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1295_comp_c3_no_fixed_bound.md`

- file: [dag/derivations/29_computation/tfq_1295_comp_c3_no_fixed_bound.md](../../../dag/derivations/29_computation/tfq_1295_comp_c3_no_fixed_bound.md)
- sha256 (`lf-normalised`): `67b7f46be638410a35786030b0c4f5014cd4f5334e5923e38211e850fb8cb251`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1295
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C3-NO-FIXED-BOUND` `CONDITIONAL_ON_IMPORT`: [COMP-C3-RUNNER-NEEDS-BLANKS](COMP-C3-RUNNER-NEEDS-BLANKS.md) (PROVED_LEAN), [COMP-C7-NF-REACH-UNDECIDABLE](COMP-C7-NF-REACH-UNDECIDABLE.md) (PROVED_LEAN)

Outgoing (0):

