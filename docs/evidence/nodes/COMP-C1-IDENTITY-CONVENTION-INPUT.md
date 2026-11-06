# COMP-C1-IDENTITY-CONVENTION-INPUT

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Whether an admitted mark is a new state or one internal class with another depends on the identity convention, which is not derived; on a pairwise separated alphabet the opaque and exact-inscription conventions give the same marks, so blank, state and end marks must be admitted as separated marks or the convention declared.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Identity convention (opaque or exact-inscription), declared

## Bottleneck

Declare the identity convention before reading any mark of a machine alphabet as a new state; nothing in this chain derives it.

## Source status

dag/derivations/29_computation/genesis_to_universal_computation.md record COMP-C1c claims IMPORTED_ASSUMPTION; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisComputation.lean`

- file: [lean4/GenesisComputation.lean](../../../lean4/GenesisComputation.lean)
- sha256 (`bytes`): `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994`
- cited in: node.lean, record TFQ-1285
- replay: `verified`
  - receipt [evidence/lean_receipts/campaign_pgw-context-decision-procedure_lean_replay.json](../../../evidence/lean_receipts/campaign_pgw-context-decision-procedure_lean_replay.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [evidence/lean_receipts/lean_replay_campaign_computation.json](../../../evidence/lean_receipts/lean_replay_campaign_computation.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `IdentityConvention` | yes | yes | yes | module-level | `#print axioms IdentityConvention` |
| `separated_marks_not_collapsed` | yes | yes | yes | propext | `#print axioms separated_marks_not_collapsed` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/genesis_to_universal_computation.md`

- file: [dag/derivations/29_computation/genesis_to_universal_computation.md](../../../dag/derivations/29_computation/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `27c7822177fe483a605b87cb9927dd1909001331834df7ed9d0b60ec1ad3108d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1285_comp_c1_identity_convention_input.md`

- file: [dag/derivations/29_computation/tfq_1285_comp_c1_identity_convention_input.md](../../../dag/derivations/29_computation/tfq_1285_comp_c1_identity_convention_input.md)
- sha256 (`lf-normalised`): `fc59541e4bc96c56125637c1483193aa0ae901e4147499913c06915ea4350ba0`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1285
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-COMP-C1-IDENTITY-CONVENTION-INPUT` `CONDITIONAL_ON_IMPORT`: [COMP-C1-FIRST-SEPARATION-REPLAY](COMP-C1-FIRST-SEPARATION-REPLAY.md) (COMPUTATIONALLY_CHECKED), [PGW-IDENTITY-CONVENTION-UNDECIDABLE](PGW-IDENTITY-CONVENTION-UNDECIDABLE.md) (CONDITIONAL)

Outgoing (0):

