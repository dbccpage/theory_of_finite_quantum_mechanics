# COMP-C6-TM0-HALTING-EQUIVALENCE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For the fixed TM0 machine M0 = TM1to0.tr (TM2to1.tr PartrecToTM2.tr) and the explicit initial configurations initCfg0, M0 halts from initCfg0 (pair (encode c) n) iff Code.eval c n is defined.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Mathlib TM2to1.tr_respects
- Mathlib TM1to0.tr_respects
- Mathlib StateTransition.tr_eval_dom

## Bottleneck

Halting form only; the TM0 output form is open (COMP-C6e).

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C6c claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisCompUniv.lean`

- file: [lean4/GenesisCompUniv.lean](../../../lean4/GenesisCompUniv.lean)
- sha256 (`bytes`): `966d60cf259d7c22f275e13ab58dd6d027330f6ae146536eb68a97ddb97620f3`
- cited in: node.lean, node.source, record TFQ-1305
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisCompUniv`): recorded sha256 `966d60cf259d7c22f275e13ab58dd6d027330f6ae146536eb68a97ddb97620f3` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisCompUniv`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `dom_chain` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms dom_chain` |
| `halts_iff_dom` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms halts_iff_dom` |
| `halts_iff_eval_dom` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms halts_iff_eval_dom` |
| `initCfg0` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms initCfg0` |
| `trCfg_init_gen` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms trCfg_init_gen` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1305_comp_c6_tm0_halting_equivalence.md`

- file: [dag/derivations/29_computation/tfq_1305_comp_c6_tm0_halting_equivalence.md](../../../dag/derivations/29_computation/tfq_1305_comp_c6_tm0_halting_equivalence.md)
- sha256 (`lf-normalised`): `2271540a21ffb0fdd0a858004353e5d7b092979dc5833a167ff54181705a0ed4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1305
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C6-TM0-HALTING-EQUIVALENCE` `DERIVED_LEAN`: [COMP-C6-TM2-OUTPUT-FORM](COMP-C6-TM2-OUTPUT-FORM.md) (PROVED_LEAN), [COMP-C5-CLOSURES-HALTING](COMP-C5-CLOSURES-HALTING.md) (PROVED_LEAN)

Outgoing (3):

- `APP-R-COMP-C6-FINITE-MARKS` `DERIVED_LEAN`: [COMP-C6-FINITE-MARKS](COMP-C6-FINITE-MARKS.md) (PROVED_LEAN)
- `APP-R-COMP-C6-TM0-OUTPUT-FORM-OPEN` `GAP_NO_DERIVATION`: [COMP-C6-TM0-OUTPUT-FORM-OPEN](COMP-C6-TM0-OUTPUT-FORM-OPEN.md) (OPEN)
- `APP-R-COMP-C7-MACHINE-HALTING-UNDECIDABLE` `DERIVED_LEAN`: [COMP-C7-MACHINE-HALTING-UNDECIDABLE](COMP-C7-MACHINE-HALTING-UNDECIDABLE.md) (PROVED_LEAN)
