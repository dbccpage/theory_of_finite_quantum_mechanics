# COMP-C7-ENCODED-INSTANCE-REDUCTION

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> If the mark type has a Primcodable structure and startWord is computable, the normal-form reachability problem on words of the fixed regime is not a computable predicate.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Primcodable structure on the mark type and Computable startWord (open lemma startWord_computable)

## Bottleneck

Prove startWord_computable: a Primcodable structure on a mark type containing the infinite state type and a computability proof for the paired-input encoding.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C7c claims CONDITIONAL; audited status CONDITIONAL

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisCompUniv.lean`

- file: [lean4/GenesisCompUniv.lean](../../../lean4/GenesisCompUniv.lean)
- sha256 (`bytes`): `966d60cf259d7c22f275e13ab58dd6d027330f6ae146536eb68a97ddb97620f3`
- cited in: node.lean, node.source, record TFQ-1310
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisCompUniv`): recorded sha256 `966d60cf259d7c22f275e13ab58dd6d027330f6ae146536eb68a97ddb97620f3` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisCompUniv`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `reach_problem_not_computable` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms reach_problem_not_computable` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1310_comp_c7_encoded_instance_reduction.md`

- file: [dag/derivations/29_computation/tfq_1310_comp_c7_encoded_instance_reduction.md](../../../dag/derivations/29_computation/tfq_1310_comp_c7_encoded_instance_reduction.md)
- sha256 (`lf-normalised`): `48015f9383eb0f57c090c0cbeb4efa4692453fe6e70d08f20cdf9a840dca5e4b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1310
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C7-ENCODED-INSTANCE-REDUCTION` `CONDITIONAL_ON_IMPORT`: [COMP-C7-NF-REACH-UNDECIDABLE](COMP-C7-NF-REACH-UNDECIDABLE.md) (PROVED_LEAN)

Outgoing (0):

