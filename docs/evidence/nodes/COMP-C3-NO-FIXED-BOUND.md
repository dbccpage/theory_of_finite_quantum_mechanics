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

### Lean: `lean4/CampaignCompC3NoFixedBound.lean`

- file: [lean4/CampaignCompC3NoFixedBound.lean](../../../lean4/CampaignCompC3NoFixedBound.lean)
- sha256 (`bytes`): `6bad30bdc8fa92b5b8f9aa946324f5c44438c77c6c3c5083628727aab22a7aae`
- cited in: node.lean, receipt dag/research/campaign_comp-c3-no-fixed-bound_lean_replay.json (CampaignCompC3NoFixedBound), receipt dag/research/pr_383_round2_replay.json (CampaignCompC3NoFixedBound), record TFQ-1295
- replay: `verified`
  - receipt [dag/research/campaign_comp-c3-no-fixed-bound_lean_replay.json](../../../dag/research/campaign_comp-c3-no-fixed-bound_lean_replay.json) (module `CampaignCompC3NoFixedBound`): recorded sha256 `6bad30bdc8fa92b5b8f9aa946324f5c44438c77c6c3c5083628727aab22a7aae` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_383_round2_replay.json](../../../dag/research/pr_383_round2_replay.json) (module `CampaignCompC3NoFixedBound`): recorded sha256 `6bad30bdc8fa92b5b8f9aa946324f5c44438c77c6c3c5083628727aab22a7aae` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignCompC3NoFixedBound`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignCompC3NoFixedBound.Word` | yes | yes | yes | none | `#print axioms CampaignCompC3NoFixedBound.Word` |
| `CampaignCompC3NoFixedBound.bound` | yes | yes | yes | none | `#print axioms CampaignCompC3NoFixedBound.bound` |
| `CampaignCompC3NoFixedBound.emptyW` | yes | yes | yes | none | `#print axioms CampaignCompC3NoFixedBound.emptyW` |
| `CampaignCompC3NoFixedBound.empty_in` | yes | yes | yes | propext | `#print axioms CampaignCompC3NoFixedBound.empty_in` |
| `CampaignCompC3NoFixedBound.inBound` | yes | yes | yes | none | `#print axioms CampaignCompC3NoFixedBound.inBound` |
| `CampaignCompC3NoFixedBound.long` | yes | yes | yes | propext | `#print axioms CampaignCompC3NoFixedBound.long` |
| `CampaignCompC3NoFixedBound.long_len` | yes | yes | yes | propext | `#print axioms CampaignCompC3NoFixedBound.long_len` |
| `CampaignCompC3NoFixedBound.long_out` | yes | yes | yes | propext | `#print axioms CampaignCompC3NoFixedBound.long_out` |
| `CampaignCompC3NoFixedBound.not_empty` | yes | yes | yes | propext | `#print axioms CampaignCompC3NoFixedBound.not_empty` |
| `CampaignCompC3NoFixedBound.not_long` | yes | yes | yes | propext | `#print axioms CampaignCompC3NoFixedBound.not_long` |
| `CampaignCompC3NoFixedBound.reach_eq` | yes | yes | yes | none | `#print axioms CampaignCompC3NoFixedBound.reach_eq` |
| `CampaignCompC3NoFixedBound.reaches_self` | yes | yes | yes | propext | `#print axioms CampaignCompC3NoFixedBound.reaches_self` |
| `CampaignCompC3NoFixedBound.start` | yes | yes | yes | propext | `#print axioms CampaignCompC3NoFixedBound.start` |
| `CampaignCompC3NoFixedBound.start_in` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignCompC3NoFixedBound.start_in` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1295_comp_c3_no_fixed_bound.md`

- file: [dag/derivations/29_computation/tfq_1295_comp_c3_no_fixed_bound.md](../../../dag/derivations/29_computation/tfq_1295_comp_c3_no_fixed_bound.md)
- sha256 (`lf-normalised`): `801fbd4fd5f2f3e24c58ed77f2a48c2b5051018751ce1276c9600db77be0fc85`
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

