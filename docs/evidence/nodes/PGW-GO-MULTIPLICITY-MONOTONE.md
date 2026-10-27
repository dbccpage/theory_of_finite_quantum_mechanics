# PGW-GO-MULTIPLICITY-MONOTONE

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The fourth derivation counts assertions: a state has terms, a multiplicity per ordered pair and the names, arb is asserted once to begin with, and every change adds one term or raises one multiplicity by one, taking nothing away. Every change leaves its state contained in its outcome and containment composes, so along every sequence Reach4 s t n each multiplicity is the same or higher (Reach4.mult_le), at the pair writing arb as well (Reach4.arb_mult_le); terms, assertions and names persist and an obstruction is never cleared. A counted containment gives a containment of the supports, so the third derivation's conclusions survive on the supports.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Reading C1': asserted means multiplicity at least one, with support and indicator maps to the earlier model (assumption)

## Bottleneck

Monotone for the fourth seed's additions only; the fifth derivation restores the four kinds of change on counted assertions, so this monotonicity is not claimed there, and a multiplicity can rise above one (arb_twice).

## Source status

genesis_ongoing paper/fourth/claim_ledger.md D5 to D7; lean4/Fourth/Contain.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisOngoing/Fourth/Contain.lean`

- file: [lean4/Imported/GenesisOngoing/Fourth/Contain.lean](../../../lean4/Imported/GenesisOngoing/Fourth/Contain.lean)
- sha256 (`bytes`): `9111abbe1c0bf66978e0788d1060342a9f33be4fb9b8352d2e6fc265b6c3426a`
- cited in: node.lean, node.source, record TFQ-0479
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.Fourth.Contain`): recorded sha256 `9111abbe1c0bf66978e0788d1060342a9f33be4fb9b8352d2e6fc265b6c3426a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/Fourth/Contain.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Reach4.arb_mult_le` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Reach4.arb_mult_le` |
| `Reach4.contains` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Reach4.contains` |
| `Reach4.mult_le` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Reach4.mult_le` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/fourth/invariants.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/fourth/invariants.py](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/fourth/invariants.py)
- sha256 (`bytes`): `e35e13ad67c5204b3887a72e6d22850b2744ac965364a6c19f68bd52487cd2f8`
- cited in: record TFQ-0479

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `never_decreases` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/fourth/claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/fourth/claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/fourth/claim_ledger.md)
- sha256 (`lf-normalised`): `124372cb4904463699e4281c0c964d4b11842ca2bff5f6522d4adf595eb9a092`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0479_go_multiplicity_monotone.md`

- file: [dag/derivations/02_genesis/tfq_0479_go_multiplicity_monotone.md](../../../dag/derivations/02_genesis/tfq_0479_go_multiplicity_monotone.md)
- sha256 (`lf-normalised`): `ba3b6b9fc2b23edf34090bba70569eeaa209e9af65f708e57368b8c302e67d8f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0479
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:8b8d536217ef3d16457e9c7a2cdbc492da7bf00addbd2f6c83cfdae08870f395:37`

## Absences recorded by the TFQ records

- TFQ-0479 rust: the H3V7N5QF package holds no Rust

## Routes

Incoming (1):

- `PGW-R-GO-MULTIPLICITY-MONOTONE` `DERIVED_LEAN`: [PGW-GO-CONTRACTION-STEP2-STEP3](PGW-GO-CONTRACTION-STEP2-STEP3.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-GO-TWO-RELATIONS-SWAP` `DERIVED_LEAN`: [PGW-GO-TWO-RELATIONS-SWAP](PGW-GO-TWO-RELATIONS-SWAP.md) (PROVED_LEAN)
