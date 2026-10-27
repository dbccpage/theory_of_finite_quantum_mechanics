# COMP-C3-NO-FIXED-BOUND

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> If the map from an input to its start word were computable and one length bound witnessed every halting start word inside the bound, normal-form reachability would be decidable, contradicting nfReach_not_computable.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 14
- distinct cited Lean declarations covered by a current replay receipt: 14
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The checked slice is one letter, no rewrite step, and length bound 1: (0) reaches itself, misses the empty word, and (0, 0) has length 2. A computable map from an input to a start word, one bound containing every halting start word, and a clash with normal-form reachability stay open. The older citations reachB_iff and nfReach_not_computable do not discharge this slice.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C3e claims CONDITIONAL; audited status CONDITIONAL

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ComputationC3NoFixedBound.lean`

- file: [lean4/ComputationC3NoFixedBound.lean](../../../lean4/ComputationC3NoFixedBound.lean)
- sha256 (`bytes`): `3976a6960ee7650cdbb431214f8b8585dbdc9443bc924c7f2d6e4a2d6b78be12`
- cited in: node.lean, receipt dag/research/campaign_comp-c3-no-fixed-bound_lean_replay.json (ComputationC3NoFixedBound), receipt dag/research/pr_383_round2_replay.json (ComputationC3NoFixedBound), record TFQ-1295
- replay: `verified`
  - receipt [dag/research/campaign_comp-c3-no-fixed-bound_lean_replay.json](../../../dag/research/campaign_comp-c3-no-fixed-bound_lean_replay.json) (module `ComputationC3NoFixedBound`): recorded sha256 `3976a6960ee7650cdbb431214f8b8585dbdc9443bc924c7f2d6e4a2d6b78be12` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_383_round2_replay.json](../../../dag/research/pr_383_round2_replay.json) (module `ComputationC3NoFixedBound`): recorded sha256 `3976a6960ee7650cdbb431214f8b8585dbdc9443bc924c7f2d6e4a2d6b78be12` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ComputationC3NoFixedBound`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ComputationC3NoFixedBound.Word` | yes | yes | yes | none | `#print axioms ComputationC3NoFixedBound.Word` |
| `ComputationC3NoFixedBound.bound` | yes | yes | yes | none | `#print axioms ComputationC3NoFixedBound.bound` |
| `ComputationC3NoFixedBound.emptyW` | yes | yes | yes | none | `#print axioms ComputationC3NoFixedBound.emptyW` |
| `ComputationC3NoFixedBound.empty_in` | yes | yes | yes | propext | `#print axioms ComputationC3NoFixedBound.empty_in` |
| `ComputationC3NoFixedBound.inBound` | yes | yes | yes | none | `#print axioms ComputationC3NoFixedBound.inBound` |
| `ComputationC3NoFixedBound.long` | yes | yes | yes | propext | `#print axioms ComputationC3NoFixedBound.long` |
| `ComputationC3NoFixedBound.long_len` | yes | yes | yes | propext | `#print axioms ComputationC3NoFixedBound.long_len` |
| `ComputationC3NoFixedBound.long_out` | yes | yes | yes | propext | `#print axioms ComputationC3NoFixedBound.long_out` |
| `ComputationC3NoFixedBound.not_empty` | yes | yes | yes | propext | `#print axioms ComputationC3NoFixedBound.not_empty` |
| `ComputationC3NoFixedBound.not_long` | yes | yes | yes | propext | `#print axioms ComputationC3NoFixedBound.not_long` |
| `ComputationC3NoFixedBound.reach_eq` | yes | yes | yes | none | `#print axioms ComputationC3NoFixedBound.reach_eq` |
| `ComputationC3NoFixedBound.reaches_self` | yes | yes | yes | propext | `#print axioms ComputationC3NoFixedBound.reaches_self` |
| `ComputationC3NoFixedBound.start` | yes | yes | yes | propext | `#print axioms ComputationC3NoFixedBound.start` |
| `ComputationC3NoFixedBound.start_in` | yes | yes | yes | Quot.sound, propext | `#print axioms ComputationC3NoFixedBound.start_in` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1295_comp_c3_no_fixed_bound.md`

- file: [dag/derivations/29_computation/tfq_1295_comp_c3_no_fixed_bound.md](../../../dag/derivations/29_computation/tfq_1295_comp_c3_no_fixed_bound.md)
- sha256 (`lf-normalised`): `e9ef54e7ceea34e4649fb13e24629c49e11875201eae6445826573914e9a7169`
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

