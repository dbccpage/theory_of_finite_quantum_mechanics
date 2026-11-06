# PGW-WDP-BRIDGE-O05-AUTHORIZATION-FIREWALL

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Enlarged Genesis bridge obligation GEN-WDP-O05: recover institutionally meaningful jurisdiction, appeal, facts, agreement, and execution from declared evidence, policy, and enforcement maps.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

GEN-WDP-O05 remains open by design as an external institutional boundary; WdpBatch6.lean::receipt_verification_independent_of_jurisdiction formalizes that software receipt verification does not confer external institutional standing or appeal rights.

## Source status

GEN-WDP-O05 non-implication firewall mechanized in WdpBatch6.lean; external institutional jurisdiction remains outside software

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FoundationalBridges.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FoundationalBridges.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FoundationalBridges.lean)
- sha256 (`bytes`): `8573a32551c075a0c995efc191a7c06e16f29ede9f03f13d3d0c6654a29c66a0`
- cited in: node.lean, record TFQ-0570
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FoundationalBridges.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `inscription_distinct_marks_apart` | yes | yes | yes | - | `#print axioms inscription_distinct_marks_apart` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)
- sha256 (`bytes`): `e1d9e23ed4bf94ba2f05b141cb8eecadcbd8e867ed8f2c1ca7ef86eedc82cfe1`
- cited in: node.lean, record TFQ-0570
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch6.receipt_verification_independent_of_jurisdiction` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch6.receipt_verification_independent_of_jurisdiction` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/foundational_bridges.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/foundational_bridges.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/foundational_bridges.py)
- sha256 (`bytes`): `8a955655b74671c6599df32e839bbaef8357e8d789869b009b63e063bc15bcbb`
- cited in: record TFQ-0570

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `apartness_witness` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md)
- sha256 (`lf-normalised`): `e411f9eace9de18c2583922d16d85be03fcbe4c35976ca3d7a33a0c3cfdea143`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0570_wdp_bridge_o05_authorization_firewall.md`

- file: [dag/derivations/06_wdp/tfq_0570_wdp_bridge_o05_authorization_firewall.md](../../../dag/derivations/06_wdp/tfq_0570_wdp_bridge_o05_authorization_firewall.md)
- sha256 (`lf-normalised`): `b7232f9ab0ea8116f1aad4fb9b1d83a587238b4845fd03b3b0f53fb1b767cb28`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0570
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0570 rust: external institutional jurisdiction cannot be discharged by software

## Routes

Incoming (1):

- `PGW-R-WDP-BRIDGE-O05-AUTHORIZATION-FIREWALL` `GAP_NO_DERIVATION`: [PGW-WDP-BRIDGE-O04-TENSOR-RECONSTRUCTION](PGW-WDP-BRIDGE-O04-TENSOR-RECONSTRUCTION.md) (OPEN), [PG-WDP-GENESIS-BRIDGE-OBLIGATIONS](PG-WDP-GENESIS-BRIDGE-OBLIGATIONS.md) (OPEN), [PGW-WDP-BRIDGE-REPORT-FIBER-OBSERVER](PGW-WDP-BRIDGE-REPORT-FIBER-OBSERVER.md) (PROVED_LEAN)

Outgoing (2):

- `PGW-R-WDP-OUT-1-SHARP-OBSERVER-COMPLETION` `DERIVED_LEAN`: [PGW-WDP-OUT-1-SHARP-OBSERVER-COMPLETION](PGW-WDP-OUT-1-SHARP-OBSERVER-COMPLETION.md) (PROVED_LEAN)
- `PGW-R-WDP-OUT-4-REJECTION-RULE-REUSE` `DERIVED_LEAN`: [PGW-WDP-OUT-4-REJECTION-RULE-REUSE](PGW-WDP-OUT-4-REJECTION-RULE-REUSE.md) (PROVED_LEAN)
