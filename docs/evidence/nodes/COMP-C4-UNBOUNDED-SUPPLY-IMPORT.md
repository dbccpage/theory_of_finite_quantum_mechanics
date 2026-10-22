# COMP-C4-UNBOUNDED-SUPPLY-IMPORT

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A general-purpose rewriting regime needs words of unbounded length, which in Genesis terms is unbounded admission of fresh marks; stepE permits it but every admitDatum is a host event, closed Genesis saturates (TFQ-0451, TFQ-0487), TFQ-0482 gives unbounded sequence length over bounded state and not unbounded space, and no endogenous generator exists (TFQ-0504).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

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
- replay: `none`
- check: `cd lean4 && lake build GenesisComputation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `UnboundedSupply` | yes | yes | yes | - | `#print axioms UnboundedSupply` |
| `not_closed_of_unbounded` | yes | yes | yes | - | `#print axioms not_closed_of_unbounded` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0487_endogenous_demands_exogenous_payments.md`

- file: [dag/derivations/02_genesis/tfq_0487_endogenous_demands_exogenous_payments.md](../../../dag/derivations/02_genesis/tfq_0487_endogenous_demands_exogenous_payments.md)
- sha256 (`lf-normalised`): `f37b447dcb7db09b457f19ef4c715fe15cad95a4af7d8e828f90aa4741b4f052`
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
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C4-UNBOUNDED-SUPPLY-IMPORT` `CONDITIONAL_ON_IMPORT`: [COMP-C4-STEPE-UNCAPPED](COMP-C4-STEPE-UNCAPPED.md) (PROVED_LEAN), [PGW-NO-ENDOGENOUS-DEMAND-GENERATOR](PGW-NO-ENDOGENOUS-DEMAND-GENERATOR.md) (PROVED_PROSE), [PGW-GO-LEFTOVER-UNBOUNDEDNESS](PGW-GO-LEFTOVER-UNBOUNDEDNESS.md) (PROVED_LEAN), [PGW-ENDOGENOUS-DEMAND-OB1](PGW-ENDOGENOUS-DEMAND-OB1.md) (OPEN)

Outgoing (1):

- `APP-R-COMP-C4-SUPPLY-GROWTH` `DERIVED_LEAN`: [COMP-C4-SUPPLY-GROWTH](COMP-C4-SUPPLY-GROWTH.md) (PROVED_LEAN)
