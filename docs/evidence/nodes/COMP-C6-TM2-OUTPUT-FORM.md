# COMP-C6-TM2-OUTPUT-FORM

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The fixed TM2 machine PartrecToTM2.tr, started on init of the fixed code and the paired input, evaluates to halt applied to the value of Code.eval c n exactly when that value is defined.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Mathlib PartrecToTM2.tr_eval

## Bottleneck

TM2 level only; the corresponding output form at the TM0 level is open (COMP-C6e).

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C6b claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisCompUniv.lean`

- file: [lean4/GenesisCompUniv.lean](../../../lean4/GenesisCompUniv.lean)
- sha256 (`bytes`): `966d60cf259d7c22f275e13ab58dd6d027330f6ae146536eb68a97ddb97620f3`
- cited in: node.lean, node.source, record TFQ-1304
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisCompUniv`): recorded sha256 `966d60cf259d7c22f275e13ab58dd6d027330f6ae146536eb68a97ddb97620f3` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisCompUniv`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `tm2_computes_eval` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms tm2_computes_eval` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1304_comp_c6_tm2_output_form.md`

- file: [dag/derivations/29_computation/tfq_1304_comp_c6_tm2_output_form.md](../../../dag/derivations/29_computation/tfq_1304_comp_c6_tm2_output_form.md)
- sha256 (`lf-normalised`): `01f316d4c693f10ca308cd9d75a6c9033c0aab0a84cfe7ec1315434326bbe721`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1304
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `004aada51ca3ccf378160e4e84208bba2b409805f041a4ef7bbd8898576cd5c7`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C6-TM2-OUTPUT-FORM` `DERIVED_LEAN`: [COMP-C6-EVAL-HAS-A-CODE](COMP-C6-EVAL-HAS-A-CODE.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-COMP-C6-TM0-HALTING-EQUIVALENCE` `DERIVED_LEAN`: [COMP-C6-TM0-HALTING-EQUIVALENCE](COMP-C6-TM0-HALTING-EQUIVALENCE.md) (PROVED_LEAN)
