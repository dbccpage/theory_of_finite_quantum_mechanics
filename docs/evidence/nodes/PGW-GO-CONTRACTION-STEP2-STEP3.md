# PGW-GO-CONTRACTION-STEP2-STEP3

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The contraction family strikes changes from the base seed. The second derivation strikes removal and keeps identification, adding a term and adding an assertion (Lean Step3); every change comes with a carrying map q, the identity for an addition and a merge for an identification, sending terms to terms, each asserted xry to an asserted q(x) r q(y) and the names to the names, and carrying maps compose along every sequence (Step3.carries, Reach3.carries). The third derivation also strikes identification (Lean Step2, two kinds): Step2.toStep3 embeds each of its changes as a second-seed change and Reach2.toReach3 each sequence, so the earlier one-change and sequence theorems restrict to it, and its containment of a state in its outcome is a carrying map with the identity.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The Lean names run opposite to the derivation numbers (Step3 is the second seed's three-kind step, Step2 the third seed's two-kind step); the embedding is a restriction, and no carrying map exists under the base seed, where a removal un-asserts.

## Source status

genesis_ongoing paper/second/claim_ledger.md D5 and paper/third/claim_ledger.md D5; lean4/Second/Carry.lean, lean4/Third/Step.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisOngoing/Second/Carry.lean`

- file: [lean4/Imported/GenesisOngoing/Second/Carry.lean](../../../lean4/Imported/GenesisOngoing/Second/Carry.lean)
- sha256 (`bytes`): `e31778a48b6eb0b107c9d640fe3a7a8319034891bad0b33d20bfa47a1e524b3d`
- cited in: node.lean, record TFQ-0478
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.Second.Carry`): recorded sha256 `e31778a48b6eb0b107c9d640fe3a7a8319034891bad0b33d20bfa47a1e524b3d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/Second/Carry.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Reach3.carries` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Reach3.carries` |
| `Step3.carries` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Step3.carries` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoing/Third/Step.lean`

- file: [lean4/Imported/GenesisOngoing/Third/Step.lean](../../../lean4/Imported/GenesisOngoing/Third/Step.lean)
- sha256 (`bytes`): `aceb819fa92ee7c3bee3f2aa0d8f3de9ea04b6fc902706c067e50450412bb215`
- cited in: node.lean, record TFQ-0478
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoing.Third.Step`): recorded sha256 `aceb819fa92ee7c3bee3f2aa0d8f3de9ea04b6fc902706c067e50450412bb215` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoing/Third/Step.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Reach2.toReach3` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Reach2.toReach3` |
| `Step2.toStep3` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms Step2.toStep3` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/second/reach.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/second/reach.py](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/second/reach.py)
- sha256 (`bytes`): `961d2ad0323f9ed5939089a1d5653cab1ce6549d4001fb834581d7eae7e934db`
- cited in: record TFQ-0478

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `carrying_map` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/third/reach.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/third/reach.py](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/third/reach.py)
- sha256 (`bytes`): `1dda0ce25f95722cf7e212b063b3f25f985edb92fe99d537d10d200045103ae1`
- cited in: record TFQ-0478

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `embedding` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/second/claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/second/claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/second/claim_ledger.md)
- sha256 (`lf-normalised`): `4fe64144a7b8389c0720d6dd57974282e7112487608aea21e47b243eb62e5c8a`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/third/claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/third/claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/third/claim_ledger.md)
- sha256 (`lf-normalised`): `ba648ff3183dbc72eb805e09e3f1d3a96c977ba87f6e3133d72bb3afb5abd5da`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0478_go_contraction_step2_step3.md`

- file: [dag/derivations/02_genesis/tfq_0478_go_contraction_step2_step3.md](../../../dag/derivations/02_genesis/tfq_0478_go_contraction_step2_step3.md)
- sha256 (`lf-normalised`): `56d4704730b0ac7ea5010afb2a18458ecd80f0ab15ba44c7e6c9f4031099df72`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0478
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/005_oegenong/levels/level_06_stage_embeddings.md`

- file: `omega_engine_education/documentation/005_oegenong/levels/level_06_stage_embeddings.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0478 rust: the H3V7N5QF package holds no Rust

## Routes

Incoming (1):

- `PGW-R-GO-CONTRACTION-STEP2-STEP3` `DERIVED_LEAN`: [PGW-GO-REACH-CEILING](PGW-GO-REACH-CEILING.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-GO-MULTIPLICITY-MONOTONE` `DERIVED_LEAN`: [PGW-GO-MULTIPLICITY-MONOTONE](PGW-GO-MULTIPLICITY-MONOTONE.md) (PROVED_LEAN)
