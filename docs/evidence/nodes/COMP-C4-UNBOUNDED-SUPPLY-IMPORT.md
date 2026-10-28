# COMP-C4-UNBOUNDED-SUPPLY-IMPORT

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A general-purpose rewriting regime needs words of unbounded length, which in Genesis terms is unbounded admission of fresh marks; stepE permits it but every admitDatum is a host event, closed Genesis saturates (TFQ-0451, TFQ-0487), TFQ-0482 gives unbounded sequence length over bounded state and not unbounded space, and no endogenous generator exists (TFQ-0504).

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

- Unbounded admission of fresh blank marks, supplied by host events (declared, not derived)

## Bottleneck

Derive an endogenous source of unboundedly many admitted data (TFQ-0504) or keep the supply as a recorded host input.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C4b claims IMPORTED_ASSUMPTION; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GenesisComputation.lean`

- file: [lean4/GenesisComputation.lean](../../../lean4/GenesisComputation.lean)
- sha256 (`bytes`): `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994`
- cited in: node.lean, record TFQ-1297
- replay: `verified`
  - receipt [dag/research/campaign_pgw-context-decision-procedure_lean_replay.json](../../../dag/research/campaign_pgw-context-decision-procedure_lean_replay.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/lean_replay_campaign_computation.json](../../../dag/research/lean_replay_campaign_computation.json) (module `GenesisComputation`): recorded sha256 `f7d47a38eba64f3ec82570efa952824487575f76305877a4acf0e15165657994` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `UnboundedSupply` | yes | yes | yes | module-level | `#print axioms UnboundedSupply` |
| `not_closed_of_unbounded` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms not_closed_of_unbounded` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0487_endogenous_demands_exogenous_payments.md`

- file: [dag/derivations/02_genesis/tfq_0487_endogenous_demands_exogenous_payments.md](../../../dag/derivations/02_genesis/tfq_0487_endogenous_demands_exogenous_payments.md)
- sha256 (`lf-normalised`): `d207bfef84719630ff2a9db1ace7bce4d77565614817cd5c51e4ad9683c53f4a`
- generated view: listed, not counted
- cited in: node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/29_computation/tfq_1297_comp_c4_unbounded_supply_import.md`

- file: [dag/derivations/29_computation/tfq_1297_comp_c4_unbounded_supply_import.md](../../../dag/derivations/29_computation/tfq_1297_comp_c4_unbounded_supply_import.md)
- sha256 (`lf-normalised`): `18044581259d4923269d63660936f4d79f03b5aa126ed00c89e13aabd077b414`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1297
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `004aada51ca3ccf378160e4e84208bba2b409805f041a4ef7bbd8898576cd5c7`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C4-UNBOUNDED-SUPPLY-IMPORT` `CONDITIONAL_ON_IMPORT`: [COMP-C4-STEPE-UNCAPPED](COMP-C4-STEPE-UNCAPPED.md) (PROVED_LEAN), [PGW-NO-ENDOGENOUS-DEMAND-GENERATOR](PGW-NO-ENDOGENOUS-DEMAND-GENERATOR.md) (PROVED_PROSE), [PGW-GO-LEFTOVER-UNBOUNDEDNESS](PGW-GO-LEFTOVER-UNBOUNDEDNESS.md) (PROVED_LEAN), [PGW-ENDOGENOUS-DEMAND-OB1](PGW-ENDOGENOUS-DEMAND-OB1.md) (OPEN)

Outgoing (1):

- `APP-R-COMP-C4-SUPPLY-GROWTH` `DERIVED_LEAN`: [COMP-C4-SUPPLY-GROWTH](COMP-C4-SUPPLY-GROWTH.md) (PROVED_LEAN)
