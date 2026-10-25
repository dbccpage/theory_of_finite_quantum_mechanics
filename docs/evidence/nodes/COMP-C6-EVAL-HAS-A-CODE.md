# COMP-C6-EVAL-HAS-A-CODE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> There is a fixed Nat.Partrec.Code u with eval u (pair (encode c) n) = eval c n for all codes c and inputs n, and a fixed ToPartrec code computing the same function on one natural number.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declaration references covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Mathlib Nat.Partrec.Code.eval_part and exists_code
- Mathlib Turing.ToPartrec.Code.exists_code

## Bottleneck

Imported infrastructure is cited, not re-derived; the codes are existence statements chosen by Classical.choose.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C6a claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisCompUniv.lean`

- file: [lean4/GenesisCompUniv.lean](../../../lean4/GenesisCompUniv.lean)
- sha256 (`bytes`): `966d60cf259d7c22f275e13ab58dd6d027330f6ae146536eb68a97ddb97620f3`
- cited in: node.lean, node.source, record TFQ-1303
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisCompUniv`): recorded sha256 `966d60cf259d7c22f275e13ab58dd6d027330f6ae146536eb68a97ddb97620f3` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisCompUniv`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `univCode_eval` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms univCode_eval` |
| `univCode_exists` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms univCode_exists` |
| `univFun_partrec` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms univFun_partrec` |
| `universal_code` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms universal_code` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1303_comp_c6_eval_has_a_code.md`

- file: [dag/derivations/29_computation/tfq_1303_comp_c6_eval_has_a_code.md](../../../dag/derivations/29_computation/tfq_1303_comp_c6_eval_has_a_code.md)
- sha256 (`lf-normalised`): `4fa478c19ba6ccff8d7c05d5d2abc1b62a8daaedfc4f2d146f28bd4a1ebb1bc1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1303
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C6-EVAL-HAS-A-CODE` `DERIVED_LEAN`: [COMP-C5-CLOSURES-HALTING](COMP-C5-CLOSURES-HALTING.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-COMP-C6-TM2-OUTPUT-FORM` `DERIVED_LEAN`: [COMP-C6-TM2-OUTPUT-FORM](COMP-C6-TM2-OUTPUT-FORM.md) (PROVED_LEAN)
