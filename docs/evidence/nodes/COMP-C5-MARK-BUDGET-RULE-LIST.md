# COMP-C5-MARK-BUDGET-RULE-LIST

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A machine with tape alphabet G and state type L uses |G| + |L| + 2 marks, all of which must be admitted and separated; for finite G and L the rule set is the finite list ruleList M and the bounded decider of C3 applies to it.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The enumeration of marks by an equivalence with Fin is a declared choice.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C5c claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisCompTM.lean`

- file: [lean4/GenesisCompTM.lean](../../../lean4/GenesisCompTM.lean)
- sha256 (`bytes`): `5e02374ea98ced960a8d3deef1dd84f1b0d053ef00b268d66804af665e2dfe5c`
- cited in: node.lean, node.source, record TFQ-1301
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisCompTM`): recorded sha256 `5e02374ea98ced960a8d3deef1dd84f1b0d053ef00b268d66804af665e2dfe5c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisCompTM`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `card_sym` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms card_sym` |
| `mem_ruleList` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms mem_ruleList` |
| `reach_ruleList_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms reach_ruleList_iff` |
| `ruleList` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ruleList` |

- counts toward the grade: yes

### Lean: `lean4/GenesisComputation.lean`

- file: [lean4/GenesisComputation.lean](../../../lean4/GenesisComputation.lean)
- sha256 (`bytes`): `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994`
- cited in: node.lean, record TFQ-1301
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-decision-procedure_lean_replay.json](../../../dag/research/campaign_pgw-context-decision-procedure_lean_replay.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `canonicalRegime_pairwise` | yes | yes | yes | Quot.sound, propext | `#print axioms canonicalRegime_pairwise` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1301_comp_c5_mark_budget_rule_list.md`

- file: [dag/derivations/29_computation/tfq_1301_comp_c5_mark_budget_rule_list.md](../../../dag/derivations/29_computation/tfq_1301_comp_c5_mark_budget_rule_list.md)
- sha256 (`lf-normalised`): `b4c05b579156bbf428f8dd41dda91e50fd1eb57e0ea712cbfea582e08aab1b60`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1301
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `004aada51ca3ccf378160e4e84208bba2b409805f041a4ef7bbd8898576cd5c7`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C5-MARK-BUDGET-RULE-LIST` `DERIVED_LEAN`: [COMP-C5-TM0-STEP-SIMULATION](COMP-C5-TM0-STEP-SIMULATION.md) (PROVED_LEAN), [COMP-C1-CANONICAL-SEPARATED-ALPHABET](COMP-C1-CANONICAL-SEPARATED-ALPHABET.md) (PROVED_LEAN)

Outgoing (0):

