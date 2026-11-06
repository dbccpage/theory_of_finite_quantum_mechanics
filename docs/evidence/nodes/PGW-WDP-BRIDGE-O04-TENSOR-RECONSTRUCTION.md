# PGW-WDP-BRIDGE-O04-TENSOR-RECONSTRUCTION

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Enlarged Genesis bridge obligation GEN-WDP-O04: justify effect and probability axioms, scalar and Hilbert choices, and local tensor composition sufficient for operational quantum reconstruction.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
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

GEN-WDP-O04 remains open; classical models, non-trace readout families, and unrestricted real carriers remain live countermodels unless ruled out by explicit axioms.

## Source status

GEN-WDP-O04 open operational reconstruction obligation in genesis_bridge_register.md

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteStateEffectReadout.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteStateEffectReadout.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteStateEffectReadout.lean)
- sha256 (`bytes`): `8a1a2c2eab8ea57e8a691d01a1e32ce61be13ca9183ec26e4255f0c2e83c9d63`
- cited in: node.lean, record TFQ-0569
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteStateEffectReadout.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `born_numerator_identity` | yes | yes | yes | - | `#print axioms born_numerator_identity` |

- counts toward the grade: yes

### Python: `atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/quantum.py)
- sha256 (`bytes`): `ae67ba7c20d156bcc74833a16b7e751b27b246d039686693759d9b6065e9b128`
- cited in: record TFQ-0569

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `to_gaussian_rational` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md)
- sha256 (`lf-normalised`): `e411f9eace9de18c2583922d16d85be03fcbe4c35976ca3d7a33a0c3cfdea143`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0569_wdp_bridge_o04_tensor_reconstruction.md`

- file: [dag/derivations/06_wdp/tfq_0569_wdp_bridge_o04_tensor_reconstruction.md](../../../dag/derivations/06_wdp/tfq_0569_wdp_bridge_o04_tensor_reconstruction.md)
- sha256 (`lf-normalised`): `221ed78c1c52edd2fb235062d97b49693ea11ed523746e5dab42bde25e96fc5b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0569
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0569 rust: unconditional operational quantum selection is open

## Routes

Incoming (1):

- `PGW-R-WDP-BRIDGE-O04-TENSOR-RECONSTRUCTION` `GAP_NO_DERIVATION`: [PGW-WDP-BRIDGE-O03-GUARDED-HISTORY-COHERENCE](PGW-WDP-BRIDGE-O03-GUARDED-HISTORY-COHERENCE.md) (PROVED_LEAN), [PG-WDP-GENESIS-BRIDGE-OBLIGATIONS](PG-WDP-GENESIS-BRIDGE-OBLIGATIONS.md) (OPEN)

Outgoing (3):

- `PGW-R-WDP-ADDITIVE-TENSOR-COMPLETION` `DERIVED_LEAN`: [PGW-WDP-ADDITIVE-TENSOR-COMPLETION](PGW-WDP-ADDITIVE-TENSOR-COMPLETION.md) (PROVED_LEAN)
- `PGW-R-WDP-BRIDGE-O05-AUTHORIZATION-FIREWALL` `GAP_NO_DERIVATION`: [PGW-WDP-BRIDGE-O05-AUTHORIZATION-FIREWALL](PGW-WDP-BRIDGE-O05-AUTHORIZATION-FIREWALL.md) (OPEN)
- `PGW-R-WDP-MERON-M1-CORRELATION-ESTIMATES` `GAP_NO_DERIVATION`: [PGW-WDP-MERON-M1-CORRELATION-ESTIMATES](PGW-WDP-MERON-M1-CORRELATION-ESTIMATES.md) (OPEN)
